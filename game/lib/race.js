// Race mode: everyone answers the same question list at their own pace; first to finish wins.
//  - after every graded answer (right or wrong) the player waits a 3 s cooldown before the next submission
//  - a correct answer brings up the next question immediately (the cooldown still applies to it)
//  - up to 3 hints per question, each adding 10 s to the wait; another hint can't be taken until that
//    hint's 10 s timer has run out
//  - after 30 s on a question, the next hint is revealed for free
//  - mode 'race_hint': hint 1 is shown (free) on every question
//  - no points; ranking is by questions completed, then by who got there first
const pool = require('./pool');
const { check } = require('./check');
const { hintsFor } = require('./hints');

const RACE = { cooldownMs: 3000, hintPenaltyMs: 10000, freeHintAfterMs: 30000, maxHints: 3 };

const hintList = q => (q._hints ||= hintsFor(q));
const freeAtStart = r => (r.settings.mode === 'race_hint' ? 1 : 0);

function track(r) {
  const R = r.race;
  return [...R.state.entries()].map(([id, st]) => ({ name: r.players.get(id)?.name, idx: st.idx, total: R.total, hints: st.hintsPaid }))
    .filter(t => t.name).sort((a, b) => b.idx - a.idx);
}

function standings(r) {
  const R = r.race;
  return [...R.state.entries()].map(([id, st]) => ({ id, name: r.players.get(id)?.name, done: st.idx, total: R.total, hints: st.hintsPaid,
    seconds: +(((st.doneAt || st.lastAt || R.startAt) - R.startAt) / 1000).toFixed(1), finished: st.idx >= R.total }))
    .filter(s => s.name).sort((a, b) => b.done - a.done || a.seconds - b.seconds);
}

function sendQuestion(io, r, id) {
  const R = r.race, st = R.state.get(id), p = r.players.get(id);
  if (!st || !p || st.idx >= R.total) return;
  const q = r.questions[st.idx];
  const now = Date.now();
  io.to(p.socketId).emit('race:question', { index: st.idx, total: R.total, view: pool.publicView(q),
    waitMs: Math.max(0, st.readyAt - now), cooldownMs: RACE.cooldownMs,
    hints: hintList(q).slice(0, st.hintsUsed), freeUpTo: st.freeUpTo, maxHints: RACE.maxHints, hintPenaltyMs: RACE.hintPenaltyMs,
    hintsPaid: st.hintsPaid, hintLockMs: Math.max(0, st.hintLockUntil - now) });
}

function emitHint(io, r, id, free) {
  const st = r.race.state.get(id), p = r.players.get(id);
  const now = Date.now();
  if (p) io.to(p.socketId).emit('race:hint', { n: st.hintsUsed, text: hintList(r.questions[st.idx])[st.hintsUsed - 1], free,
    hintsPaid: st.hintsPaid, waitMs: Math.max(0, st.readyAt - now), hintLockMs: Math.max(0, st.hintLockUntil - now) });
}

// new question for this player: reset hints (showing any free ones) and arm the 30 s free-hint timer
function beginQuestion(io, r, id) {
  const st = r.race.state.get(id);
  st.hintsUsed = freeAtStart(r);
  st.freeUpTo = st.hintsUsed;
  st.wrongKeys = new Set();
  clearTimeout(st.freeTimer);
  const idx = st.idx, before = st.hintsUsed;
  st.freeTimer = setTimeout(() => {
    if (r.race.ended || st.idx !== idx || st.hintsUsed !== before || st.hintsUsed >= RACE.maxHints) return;
    st.hintsUsed += 1;
    st.freeUpTo = st.hintsUsed;
    emitHint(io, r, id, true);
  }, RACE.freeHintAfterMs);
  sendQuestion(io, r, id);
}

function start(io, r) {
  const now = Date.now();
  const roster = [...r.players.values()].filter(p => p.connected);
  r.phase = 'race';
  r.race = { startAt: now, total: r.questions.length, state: new Map(), ended: false };
  for (const p of roster) r.race.state.set(p.id, { idx: 0, readyAt: now + RACE.cooldownMs, wrongKeys: new Set(), hintsUsed: 0, hintsPaid: 0,
                                                   freeUpTo: 0, hintLockUntil: 0, lastAt: now, doneAt: null, freeTimer: null });
  io.to(r.pin).emit('race:start', { total: r.race.total, cooldownMs: RACE.cooldownMs, track: track(r), firstHintShown: freeAtStart(r) > 0 });
  for (const p of roster) beginQuestion(io, r, p.id);
}

function submit(io, r, id, text, socket) {
  const R = r.race;
  if (!R || R.ended) return socket.emit('race:result', { status: 'closed' });
  const st = R.state.get(id);
  if (!st) return socket.emit('race:result', { status: 'spectator', note: 'You joined after the race started.' });
  const now = Date.now();
  if (now < st.readyAt) return socket.emit('race:result', { status: 'cooldown', waitMs: st.readyAt - now });
  const q = r.questions[st.idx];
  const g = check(q, text);
  if (g.status === 'invalid') return socket.emit('race:result', { status: 'invalid', note: g.note });
  if (g.status === 'correct') {
    st.readyAt = now + RACE.cooldownMs;
    st.hintLockUntil = 0;
    socket.emit('race:result', { status: 'correct', index: st.idx });
    st.idx += 1;
    st.lastAt = now;
    clearTimeout(st.freeTimer);
    io.to(r.pin).emit('race:progress', { track: track(r), latest: { name: r.players.get(id).name, idx: st.idx } });
    if (st.idx >= R.total) {
      st.doneAt = now;
      return finish(io, r);
    }
    return beginQuestion(io, r, id);
  }
  if (st.wrongKeys.has(g.key)) return socket.emit('race:result', { status: 'repeat', closeness: g.closeness });
  st.wrongKeys.add(g.key);
  st.readyAt = now + RACE.cooldownMs;
  socket.emit('race:result', { status: 'wrong', closeness: g.closeness, waitMs: RACE.cooldownMs });
}

// a paid hint adds 10 s to the wait; the next hint unlocks only once this hint's timer has run out
function hint(io, r, id, socket) {
  const R = r.race;
  if (!R || R.ended) return;
  const st = R.state.get(id);
  if (!st || st.hintsUsed >= RACE.maxHints) return;
  const now = Date.now();
  if (now < st.hintLockUntil) return socket?.emit('race:result', { status: 'hintLocked', waitMs: st.hintLockUntil - now });
  st.hintsUsed += 1;
  st.hintsPaid += 1;
  st.readyAt = Math.max(st.readyAt, now) + RACE.hintPenaltyMs;
  st.hintLockUntil = st.readyAt;
  emitHint(io, r, id, false);
  io.to(r.pin).emit('race:progress', { track: track(r) });
}

function finish(io, r) {
  const R = r.race;
  if (R.ended) return;
  R.ended = true;
  for (const st of R.state.values()) clearTimeout(st.freeTimer);
  r.phase = 'final';
  io.to(r.pin).emit('race:end', { standings: standings(r) });
}

// a player reconnecting mid-race gets their current question (and revealed hints) back
function resume(io, r, id) {
  if (r.phase === 'race' && r.race?.state.has(id)) {
    const p = r.players.get(id);
    io.to(p.socketId).emit('race:start', { total: r.race.total, cooldownMs: RACE.cooldownMs, track: track(r), firstHintShown: freeAtStart(r) > 0 });
    sendQuestion(io, r, id);
  }
}

// host sends everyone back to the lobby: stop timers
function stop(r) {
  if (r.race) { r.race.ended = true; for (const st of r.race.state.values()) clearTimeout(st.freeTimer); }
}

// kept for callers (a player leaving): with first-to-finish, leaving never ends the race by itself
function checkEnd() {}

module.exports = { RACE, start, submit, hint, resume, stop, standings, track, checkEnd };
