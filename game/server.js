const express = require('express');
const http = require('http');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { Server } = require('socket.io');
const pool = require('./lib/pool');
const { check } = require('./lib/check');
const S = require('./lib/scoring');
const race = require('./lib/race');

const PORT = process.env.PORT || 3100;
const MIN_PLAYERS = 1, MAX_PLAYERS = 6; // 1 so the host can test solo
const REVEAL_GRACE_MS = 400; // let in-flight answers land before closing a question

const app = express();
const server = http.createServer(app);
const io = new Server(server);
app.use(express.static(path.join(__dirname, 'public')));
app.use('/img', express.static(pool.IMAGES, { maxAge: '1d' }));
app.get('/api/info', (req, res) => res.json({ lan: joinUrls(), questions: pool.count(), rules: S.RULES }));

// where players should go: the public address when hosted (Render sets RENDER_EXTERNAL_URL, or set PUBLIC_URL),
// otherwise this computer's addresses on the local network
function joinUrls() {
  const pub = process.env.PUBLIC_URL || process.env.RENDER_EXTERNAL_URL;
  return pub ? [pub] : lan().map(ip => `http://${ip}:${PORT}`);
}

function lan() {
  const out = [];
  for (const list of Object.values(os.networkInterfaces())) for (const i of list || []) if (i.family === 'IPv4' && !i.internal) out.push(i.address);
  return out;
}

const rooms = new Map();
const token = () => crypto.randomBytes(12).toString('hex');
function newPin() {
  let pin;
  do pin = String(Math.floor(1000 + Math.random() * 9000)); while (rooms.has(pin));
  return pin;
}

function cleanSettings(s = {}) {
  return {
    count: Math.min(50, Math.max(10, parseInt(s.count, 10) || 20)),
    level: s.level === 'state' ? 'state' : 'regional',
    mix: Object.keys(pool.MIXES).includes(s.mix) ? s.mix : 'everything',
    cap: [30, 45, 60, 90].includes(Number(s.cap)) ? Number(s.cap) : 45,
    mode: ['race', 'race_hint'].includes(s.mode) ? s.mode : 'classic',
  };
}

// ---------------------------------------------------------------- views
const playersOf = r => [...r.players.values()];
const standings = r => playersOf(r).sort((a, b) => b.score - a.score || a.joinedAt - b.joinedAt)
  .map(p => ({ id: p.id, name: p.name, score: p.score, connected: p.connected, isHost: p.isHost }));

function lobbyState(r) {
  return { pin: r.pin, phase: r.phase, settings: r.settings, hostPlays: !!r.hostPlayerId, players: standings(r),
           min: MIN_PLAYERS, max: MAX_PLAYERS, lan: joinUrls() };
}
const broadcastLobby = r => io.to(r.pin).emit('room', lobbyState(r));

// ---------------------------------------------------------------- game flow
function startGame(r) {
  r.questions = pool.pickRound(r.settings);
  r.qi = -1;
  for (const p of r.players.values()) p.score = 0;
  if (r.settings.mode.startsWith('race')) return race.start(io, r);
  nextQuestion(r);
}

function nextQuestion(r) {
  clearTimeout(r.timer);
  r.qi += 1;
  if (r.qi >= r.questions.length) return finish(r);
  const q = r.questions[r.qi];
  const now = Date.now();
  const roster = playersOf(r).filter(p => p.connected).map(p => p.id);
  r.phase = 'question';
  r.cur = {
    q, startAt: now, unlockAt: now + S.RULES.lockMs, endsAt: now + S.RULES.lockMs + r.settings.cap * 1000,
    roster: new Set(roster), needed: S.neededCorrect(roster.length), correct: [], subs: new Map(), ended: false,
  };
  for (const id of roster) r.cur.subs.set(id, { wrong: 0, wrongKeys: new Set(), correct: false, out: false, points: 0, place: 0, ms: null });
  io.to(r.pin).emit('question', {
    index: r.qi, total: r.questions.length, view: pool.publicView(q), lockMs: S.RULES.lockMs, capMs: r.settings.cap * 1000,
    needed: r.cur.needed, roster: roster.map(id => r.players.get(id).name), rules: S.RULES,
  });
  r.timer = setTimeout(() => endQuestion(r, 'time'), r.cur.endsAt - now);
}

function submit(r, playerId, text, socket) {
  const c = r.cur;
  if (r.phase !== 'question' || !c || c.ended) return socket.emit('result', { status: 'closed' });
  const sub = c.subs.get(playerId);
  if (!sub) return socket.emit('result', { status: 'spectator', note: 'You joined mid-question - you will play from the next one.' });
  if (sub.correct) return socket.emit('result', { status: 'done' });
  if (sub.out) return socket.emit('result', { status: 'lockedOut' });
  const now = Date.now();
  if (now < c.unlockAt) return socket.emit('result', { status: 'locked' });
  const g = check(c.q, text);
  if (g.status === 'invalid') return socket.emit('result', { status: 'invalid', note: g.note });
  if (g.status === 'correct') {
    sub.correct = true;
    sub.ms = now - c.unlockAt;
    sub.place = c.correct.length + 1;
    sub.points = S.correctScore(sub.ms, c.endsAt - c.unlockAt, sub.wrong, sub.place);
    c.correct.push(playerId);
    socket.emit('result', { status: 'correct', points: sub.points, place: sub.place, ms: sub.ms });
    io.to(r.pin).emit('progress', { correct: c.correct.map(id => r.players.get(id).name), needed: c.needed, latest: r.players.get(playerId).name });
    if (c.correct.length >= c.needed) {
      c.ended = true; // no more submissions count; brief grace so the last screens update
      clearTimeout(r.timer);
      r.timer = setTimeout(() => endQuestion(r, 'answered'), REVEAL_GRACE_MS);
    }
    return;
  }
  // wrong: only a new answer costs points
  if (sub.wrongKeys.has(g.key)) return socket.emit('result', { status: 'repeat', wrong: sub.wrong, closeness: g.closeness });
  sub.wrongKeys.add(g.key);
  sub.wrong += 1;
  sub.out = sub.wrong >= S.RULES.maxWrong;
  socket.emit('result', { status: 'wrong', wrong: sub.wrong, closeness: g.closeness, lockedOut: sub.out, maxWrong: S.RULES.maxWrong });
  // nobody left who can still answer -> end now instead of waiting for the time cap
  if ([...c.subs.values()].every(s => s.correct || s.out)) {
    c.ended = true;
    clearTimeout(r.timer);
    r.timer = setTimeout(() => endQuestion(r, 'everyone done'), REVEAL_GRACE_MS);
  }
}

function endQuestion(r, reason) {
  const c = r.cur;
  if (!c || r.phase !== 'question') return;
  clearTimeout(r.timer);
  c.ended = true;
  r.phase = 'reveal';
  const awards = [];
  for (const [id, sub] of c.subs) {
    const p = r.players.get(id);
    if (!p) continue;
    const pts = sub.correct ? sub.points : 0;
    p.score += pts;
    awards.push({ name: p.name, points: pts, correct: sub.correct, wrong: sub.wrong,
                  place: sub.place || null, seconds: sub.ms == null ? null : +(sub.ms / 1000).toFixed(2) });
  }
  awards.sort((a, b) => b.points - a.points);
  io.to(r.pin).emit('reveal', {
    reason, answer: pool.answerText(c.q), explanation: c.q.explanation || '', awards, standings: standings(r),
    index: r.qi, total: r.questions.length, last: r.qi === r.questions.length - 1,
  });
}

function finish(r) {
  r.phase = 'final';
  io.to(r.pin).emit('final', { standings: standings(r) });
  broadcastLobby(r);
}

// ---------------------------------------------------------------- sockets
io.on('connection', socket => {
  let room = null, playerId = null, isHost = false;

  function addPlayer(r, name, opts = {}) {
    const p = { id: token(), token: token(), name, socketId: socket.id, connected: true, score: 0, joinedAt: Date.now(), isHost: !!opts.isHost };
    r.players.set(p.id, p);
    return p;
  }

  socket.on('host:create', ({ hostPlays, hostName, settings } = {}, ack) => {
    const r = { pin: newPin(), phase: 'lobby', settings: cleanSettings(settings), players: new Map(), hostToken: token(), hostSocket: socket.id };
    rooms.set(r.pin, r);
    room = r; isHost = true;
    socket.join(r.pin);
    if (hostPlays) {
      const p = addPlayer(r, String(hostName || 'Host').trim().slice(0, 16) || 'Host', { isHost: true });
      r.hostPlayerId = p.id; playerId = p.id;
    }
    ack?.({ ok: true, pin: r.pin, hostToken: r.hostToken, playerId });
    broadcastLobby(r);
  });

  socket.on('host:resume', ({ pin, hostToken } = {}, ack) => {
    const r = rooms.get(pin);
    if (!r || r.hostToken !== hostToken) return ack?.({ ok: false });
    room = r; isHost = true; r.hostSocket = socket.id; socket.join(r.pin);
    if (r.hostPlayerId) { playerId = r.hostPlayerId; const p = r.players.get(playerId); p.socketId = socket.id; p.connected = true; }
    ack?.({ ok: true, pin: r.pin, playerId, phase: r.phase });
    broadcastLobby(r);
    if (playerId) race.resume(io, r, playerId);
  });

  socket.on('host:settings', (settings, ack) => {
    if (!isHost || room.phase !== 'lobby' && room.phase !== 'final') return;
    room.settings = cleanSettings(settings);
    broadcastLobby(room);
    ack?.({ ok: true });
  });

  socket.on('host:hostplays', ({ on, name } = {}, ack) => {
    if (!isHost || (room.phase !== 'lobby' && room.phase !== 'final')) return;
    if (on && !room.hostPlayerId) {
      if (room.players.size >= MAX_PLAYERS) return ack?.({ ok: false, error: 'Room is full' });
      const p = addPlayer(room, String(name || 'Host').trim().slice(0, 16) || 'Host', { isHost: true });
      room.hostPlayerId = playerId = p.id;
    } else if (!on && room.hostPlayerId) {
      room.players.delete(room.hostPlayerId);
      room.hostPlayerId = playerId = null;
    }
    ack?.({ ok: true, playerId });
    broadcastLobby(room);
  });

  socket.on('host:start', (_, ack) => {
    if (!isHost) return;
    const n = playersOf(room).filter(p => p.connected).length;
    if (n < MIN_PLAYERS) return ack?.({ ok: false, error: `Need at least ${MIN_PLAYERS} players` });
    startGame(room);
    ack?.({ ok: true });
  });

  socket.on('host:next', () => {
    if (!isHost) return;
    if (room.phase === 'reveal') nextQuestion(room);
    else if (room.phase === 'question') endQuestion(room, 'skipped');
  });

  socket.on('host:lobby', () => {
    if (!isHost) return;
    clearTimeout(room.timer);
    race.stop(room);
    room.phase = 'lobby';
    for (const p of room.players.values()) p.score = 0;
    io.to(room.pin).emit('lobby');
    broadcastLobby(room);
  });

  socket.on('host:kick', ({ id } = {}) => {
    if (!isHost || id === room.hostPlayerId) return;
    const p = room.players.get(id);
    if (!p) return;
    room.players.delete(id);
    io.to(p.socketId).emit('kicked');
    broadcastLobby(room);
  });

  socket.on('player:join', ({ pin, name, token: tok } = {}, ack) => {
    const r = rooms.get(String(pin || '').trim());
    if (!r) return ack?.({ ok: false, error: 'No room with that code' });
    let p = tok && [...r.players.values()].find(x => x.token === tok);
    if (p) {
      p.socketId = socket.id; p.connected = true;
    } else {
      name = String(name || '').trim().slice(0, 16);
      if (!name) return ack?.({ ok: false, error: 'Enter a name' });
      if (r.players.size >= MAX_PLAYERS) return ack?.({ ok: false, error: `Room is full (${MAX_PLAYERS} max)` });
      if ([...r.players.values()].some(x => x.name.toLowerCase() === name.toLowerCase())) return ack?.({ ok: false, error: 'That name is taken' });
      p = addPlayer(r, name);
    }
    room = r; playerId = p.id;
    socket.join(r.pin);
    ack?.({ ok: true, pin: r.pin, token: p.token, playerId: p.id, name: p.name, phase: r.phase });
    broadcastLobby(r);
    race.resume(io, r, p.id);
  });

  socket.on('answer', ({ text } = {}) => {
    if (!room || !playerId) return;
    const t = String(text ?? '').slice(0, 200);
    if (room.phase === 'race') return race.submit(io, room, playerId, t, socket);
    submit(room, playerId, t, socket);
  });

  // a player leaves the room (and any game in progress)
  socket.on('player:leave', (_, ack) => {
    if (!room || !playerId || playerId === room.hostPlayerId) return ack?.({ ok: false });
    const r = room;
    r.players.delete(playerId);
    if (r.cur) r.cur.subs.delete(playerId);
    if (r.race) { r.race.state.delete(playerId); race.checkEnd(io, r); }
    socket.leave(r.pin);
    room = null; playerId = null;
    ack?.({ ok: true });
    broadcastLobby(r);
    if (r.phase === 'race' && r.race && !r.race.ended) io.to(r.pin).emit('race:progress', { track: race.track(r) });
    // classic: if everyone still in the question is done, end it now
    if (r.phase === 'question' && r.cur && !r.cur.ended && [...r.cur.subs.values()].every(s => s.correct || s.out)) {
      r.cur.ended = true;
      clearTimeout(r.timer);
      r.timer = setTimeout(() => endQuestion(r, 'everyone done'), REVEAL_GRACE_MS);
    }
  });

  // host closes the room entirely
  socket.on('host:close', (_, ack) => {
    if (!isHost || !room) return;
    clearTimeout(room.timer);
    race.stop(room);
    io.to(room.pin).emit('closed');
    io.in(room.pin).socketsLeave(room.pin);
    rooms.delete(room.pin);
    room = null; playerId = null; isHost = false;
    ack?.({ ok: true });
  });

  socket.on('race:hint', () => {
    if (room && playerId && room.phase === 'race') race.hint(io, room, playerId, socket);
  });

  socket.on('disconnect', () => {
    if (!room) return;
    for (const p of room.players.values()) if (p.socketId === socket.id) p.connected = false;
    broadcastLobby(room);
  });
});

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`Rockbank game on http://localhost:${PORT}  (${pool.count()} playable questions)`);
    for (const ip of lan()) console.log(`  LAN: http://${ip}:${PORT}`);
  });
}

module.exports = { server, rooms };
