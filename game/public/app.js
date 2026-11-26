/* Rockbank client: host screen and player screen in one page. */
const socket = io();
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const LETTER = i => String.fromCharCode(65 + i);

const me = { role: null, pin: null, playerId: null, name: null };
let lobby = null;          // last room state
let Q = null;              // current question state

function show(view) {
  document.querySelectorAll('.view').forEach(v => v.classList.toggle('on', v.id === 'v-' + view));
}
function topInfo() {
  $('topInfo').textContent = me.pin ? `Room ${me.pin}${me.name ? ', ' + me.name : ''}${me.role === 'host' ? ' (host)' : ''}` : '';
  $('exitBtn').hidden = !me.pin;
}

// ---------------------------------------------------------------- home
$('hostPlays').onchange = e => { $('hostName').hidden = !e.target.checked; if (e.target.checked) $('hostName').focus(); };
$('hostForm').onsubmit = e => {
  e.preventDefault();
  const hostPlays = $('hostPlays').checked;
  const hostName = $('hostName').value.trim() || 'Host';
  socket.emit('host:create', { hostPlays, hostName, settings: { mode: $('hostMode').value } }, res => {
    if (!res.ok) return;
    Object.assign(me, { role: 'host', pin: res.pin, playerId: res.playerId, name: hostPlays ? hostName : null });
    sessionStorage.setItem('rb-host', JSON.stringify({ pin: res.pin, hostToken: res.hostToken, name: me.name }));
    topInfo(); show('lobby');
  });
};
$('joinForm').onsubmit = e => {
  e.preventDefault();
  join($('joinPin').value.trim(), $('joinName').value.trim());
};
function join(pin, name, tok) {
  socket.emit('player:join', { pin, name, token: tok }, res => {
    if (!res.ok) {
      if (tok) { sessionStorage.removeItem('rb-player'); show('home'); $('joinErr').textContent = 'That room has closed.'; }
      else $('joinErr').textContent = res.error;
      return;
    }
    Object.assign(me, { role: 'player', pin: res.pin, playerId: res.playerId, name: res.name });
    sessionStorage.setItem('rb-player', JSON.stringify({ pin: res.pin, token: res.token }));
    topInfo();
    if (res.phase === 'lobby' || res.phase === 'final') show('lobby');
    else { show('question'); $('feedback').textContent = 'Rejoined - you will be back in on the next question.'; }
  });
}

// resume after refresh (per tab, so a host tab and a player tab in one browser stay separate)
(function resume() {
  const h = JSON.parse(sessionStorage.getItem('rb-host') || 'null');
  const p = JSON.parse(sessionStorage.getItem('rb-player') || 'null');
  if (h) socket.emit('host:resume', h, res => {
    if (!res.ok) { sessionStorage.removeItem('rb-host'); return show('home'); }
    Object.assign(me, { role: 'host', pin: res.pin, playerId: res.playerId, name: h.name });
    topInfo(); show(res.phase === 'final' ? 'final' : 'lobby');
  });
  else if (p) join(p.pin, '', p.token);
  else show('home');
  const qp = new URLSearchParams(location.search).get('room');
  if (qp) $('joinPin').value = qp;
})();

// ---------------------------------------------------------------- lobby
socket.on('room', st => {
  lobby = st;
  $('pin').textContent = st.pin;
  $('lanLine').textContent = st.lan.length ? `Join at ${st.lan[0]}` : '';
  $('pcount').textContent = `${st.players.length}/${st.max}`;
  $('players').innerHTML = st.players.map(p => `<li>${esc(p.name)}${p.isHost ? ' (host)' : ''}${p.id === me.playerId ? ' (you)' : ''}${p.connected ? '' : ' - disconnected'}${me.role === 'host' && !p.isHost ? ` <button data-kick="${p.id}">remove</button>` : ''}</li>`).join('')
    || '<li>No one yet</li>';
  const host = me.role === 'host';
  $('hostPanel').hidden = !host;
  $('waitMsg').hidden = host;
  if (host) {
    const s = st.settings;
    $('setCount').value = s.count; $('countOut').textContent = s.count;
    $('setLevel').value = s.level; $('setMix').value = s.mix; $('setCap').value = s.cap; $('setMode').value = s.mode;
    const isRace = s.mode.startsWith('race');
    $('capRow').hidden = isRace; $('raceRules').hidden = !isRace; $('classicRules').hidden = isRace;
    $('lobbyHostPlays').checked = st.hostPlays;
    $('lobbyHostName').hidden = !st.hostPlays || !!me.playerId;
    const n = st.players.filter(p => p.connected).length;
    $('startBtn').disabled = n < st.min;
    $('startBtn').textContent = n < st.min ? `Need ${st.min - n} more player${st.min - n > 1 ? 's' : ''}` : `Start game (${n} player${n === 1 ? "" : "s"})`;
  }
});
$('players').onclick = e => { const id = e.target.dataset.kick; if (id) socket.emit('host:kick', { id }); };
function pushSettings() {
  socket.emit('host:settings', { count: $('setCount').value, level: $('setLevel').value, mix: $('setMix').value, cap: $('setCap').value,
                                 mode: $('setMode').value });
}
$('setCount').oninput = () => { $('countOut').textContent = $('setCount').value; };
['setCount', 'setLevel', 'setMix', 'setCap', 'setMode'].forEach(id => $(id).addEventListener('change', pushSettings));
$('lobbyHostPlays').onchange = e => {
  const on = e.target.checked;
  const name = $('lobbyHostName').value.trim() || prompt('Your name?', 'Host') || 'Host';
  socket.emit('host:hostplays', { on, name }, res => {
    if (!res.ok) { e.target.checked = false; $('startErr').textContent = res.error; return; }
    me.playerId = res.playerId; me.name = on ? name : null; topInfo();
  });
};
$('startBtn').onclick = () => socket.emit('host:start', null, res => { $('startErr').textContent = res?.ok ? '' : res?.error || ''; });

// ---------------------------------------------------------------- question
socket.on('question', d => {
  const playing = !!me.name && d.roster.includes(me.name);
  const now = performance.now();
  Q = { ...d, playing, lockEnd: now + d.lockMs, capEnd: now + d.lockMs + d.capMs, wrong: 0, correct: [], done: false, rules: d.rules, sent: [] };
  show('question');
  $('qnum').textContent = `Question ${d.index + 1} / ${d.total}`;
  $('qtopic').textContent = d.view.topicName;
  $('qprompt').textContent = d.view.prompt;
  const img = d.view.imageUrl;
  $('qimgWrap').hidden = !img;
  if (img) $('qimg').src = img;
  const opts = d.view.options || [];
  $('qoptions').innerHTML = opts.map((o, i) => `<li data-i="${i}">${esc(o)}</li>`).join('');
  $('qhint').textContent = {
    tf: 'Type T or F.', multi: 'Select ALL that apply: type every correct letter, e.g. ACD.',
    order: `Type the letters in order, e.g. ${'ABCDEF'.slice(0, opts.length)}.`, numeric: `Type a number${d.view.unit ? ' (' + d.view.unit + ')' : ''}.`,
    short: 'Type your answer.', frq: 'Answer in a short sentence.',
  }[d.view.format] || '';
  $('answerArea').hidden = !playing;
  $('answerArea').classList.remove('done');
  const box = $('answerBox');
  box.value = ''; box.disabled = false; box.style.background = '';
  $('strikes').textContent = '';
  $('feedback').textContent = '';
  $('feed').innerHTML = '';
  $('hostControls').hidden = me.role !== 'host';
  progress({ correct: [], needed: d.needed });
  if (playing) setTimeout(() => box.focus(), 30);
  requestAnimationFrame(tick);
});

// 1000 until 0.5 s after unlock, then a straight slide (whole points) to 500 at the time cap
function timeValue(ms, R, capMs) {
  if (ms <= R.fullWindowMs) return R.full;
  const frac = Math.min(1, (ms - R.fullWindowMs) / Math.max(1, capMs - R.fullWindowMs));
  return Math.max(R.floorAtCap, Math.ceil(R.full - (R.full - R.floorAtCap) * frac));
}
function potential(ms) {
  const R = Q.rules;
  const place = Q.correct.length + 1;
  const pen = R.placePenalty[Math.min(place, R.placePenalty.length) - 1];
  return Math.max(R.minCorrect, timeValue(Math.max(0, ms), R, Q.capMs) - R.wrongPenalty * Q.wrong - pen);
}

function tick() {
  if (!Q || !$('v-question').classList.contains('on')) return;
  const now = performance.now();
  const locked = now < Q.lockEnd;
  const bar = $('timerBar');
  bar.parentElement.classList.toggle('locked', locked);
  if (locked) {
    bar.style.width = `${100 * (1 - (Q.lockEnd - now) / Q.lockMs)}%`;
    $('timerText').textContent = `Locked: ${((Q.lockEnd - now) / 1000).toFixed(1)} s`;
  } else {
    const left = Math.max(0, Q.capEnd - now);
    bar.style.width = `${100 * left / Q.capMs}%`;
    const f = 1 - left / Q.capMs;                       // dark green -> dark red over the answer phase
    bar.style.background = `hsl(${Math.round(120 * (1 - f))}, 70%, 25%)`;
    $('timerText').textContent = `${Math.ceil(left / 1000)} s left`;
  }
  $('answerArea').classList.toggle('locked', locked && !Q.done);
  $('answerBtn').disabled = locked || Q.done;
  if (!Q.done) $('potential').textContent = potential(now - Q.lockEnd);
  requestAnimationFrame(tick);
}

// ---- answer feed: your attempts (shaded by how close they were) and other players getting it right
function shade(closeness) {
  if (closeness >= 1) return 'hsl(120, 60%, 78%)';           // correct: green
  if (closeness < 0.2) return '';                              // not close: no highlight
  const hue = 55 + Math.round(45 * (closeness - 0.2) / 0.8);   // yellow (55) -> yellow-green (100)
  return `hsl(${hue}, 90%, ${82 - Math.round(8 * closeness)}%)`;
}
function feed(html, bg) {
  const li = document.createElement('li');
  li.innerHTML = html;
  if (bg) li.style.background = bg;
  $('feed').prepend(li);
}

function progress(p) {
  if (!Q) return;
  Q.correct = p.correct;
  $('qprogress').textContent = `${p.correct.length}/${p.needed} correct to end`;
  if (p.latest && p.latest !== me.name) feed(`${esc(p.latest)} got it right`, '');
}
socket.on('progress', progress);

// clicking an option types its letter (select-all and ordering questions)
$('qoptions').onclick = e => {
  const li = e.target.closest('li');
  if (!li || !Q?.playing || Q.done) return;
  const L = LETTER(+li.dataset.i);
  const box = $('answerBox');
  const letters = box.value.toUpperCase().replace(/[^A-Z]/g, '');
  if (Q.view.format === 'multi') {
    const set = new Set(letters.split('').filter(Boolean));
    set.has(L) ? set.delete(L) : set.add(L);
    box.value = [...set].sort().join('');
  } else box.value = letters.includes(L) ? letters.replace(L, '') : letters + L;
  box.focus();
};

$('answerForm').onsubmit = e => {
  e.preventDefault();
  if (!Q || Q.done) return;
  if (performance.now() < Q.lockEnd) { $('feedback').textContent = 'Still locked.'; return; }
  const text = $('answerBox').value.trim();
  if (!text) return;
  Q.sent.push(text);
  socket.emit('answer', { text });
};

socket.on('result', r => {
  if (!Q) return;
  const box = $('answerBox');
  const text = Q.sent.shift() ?? '';
  $('feedback').textContent = '';
  switch (r.status) {
    case 'correct':
      Q.done = true;
      $('potential').textContent = r.points;
      box.value = text; box.disabled = true;
      box.style.background = shade(1);
      $('answerArea').classList.add('done');
      feed(`${esc(text)} (+${r.points})`, shade(1));
      break;
    case 'wrong':
      Q.wrong = r.wrong;
      $('strikes').textContent = 'X '.repeat(r.wrong).trim();
      if (r.lockedOut) {
        Q.done = true; box.disabled = true;
        $('answerArea').classList.add('done');
        $('potential').textContent = 0;
        $('feedback').textContent = 'Locked out for this question (' + r.maxWrong + ' wrong).';
      }
      feed(esc(text), shade(r.closeness));
      box.select();
      break;
    case 'lockedOut': $('feedback').textContent = 'Locked out for this question.'; break;
    case 'repeat': feed(`${esc(text)} (already tried)`, shade(r.closeness)); box.select(); break;
    case 'invalid': $('feedback').textContent = r.note || 'Not a valid answer'; break;
    case 'locked': $('feedback').textContent = 'Still locked.'; break;
    case 'spectator': $('feedback').textContent = r.note; break;
    case 'closed': break;
  }
});

$('skipBtn').onclick = () => socket.emit('host:next');

// ---------------------------------------------------------------- reveal / final
socket.on('reveal', d => {
  show('reveal');
  $('rAnswer').textContent = d.answer;
  $('rExplain').textContent = d.explanation;
  $('rAwards').innerHTML = d.awards.map(a => {
    const res = a.correct ? `<span class="res-c">correct, ${['1st', '2nd', '3rd'][a.place - 1] || ''}, ${a.seconds}s${a.wrong ? `, ${a.wrong} wrong` : ''}</span>`
      : `<span class="res-w">${a.wrong ? a.wrong + ' wrong' : 'no answer'}</span>`;
    return `<tr><td>${esc(a.name)}</td><td>${res}</td><td class="num">+${a.points}</td></tr>`;
  }).join('');
  board($('rBoard'), d.standings);
  const host = me.role === 'host';
  $('nextBtn').hidden = !host;
  $('nextBtn').textContent = d.last ? 'See final results' : 'Next question';
  $('rWait').hidden = host;
  document.activeElement?.blur(); // Enter is handled globally; a focused button would fire twice
});
$('nextBtn').onclick = () => socket.emit('host:next');

function board(el, st) {
  el.innerHTML = st.map(p => `<li class="${p.id === me.playerId ? 'me' : ''}">${esc(p.name)}: ${p.score}</li>`).join('');
}

socket.on('final', d => {
  show('final');
  const top = d.standings[0];
  const tied = d.standings.filter(p => p.score === top.score);
  $('winner').textContent = tied.length > 1 ? `Tie: ${tied.map(p => p.name).join(' & ')}` : `${top.name} wins!`;
  board($('fBoard'), d.standings);
  $('againBtn').hidden = me.role !== 'host';
});
$('againBtn').onclick = () => socket.emit('host:lobby');
socket.on('lobby', () => show('lobby'));
socket.on('kicked', () => { sessionStorage.removeItem('rb-player'); Object.assign(me, { role: null, pin: null, name: null }); topInfo(); show('home'); $('joinErr').textContent = 'You were removed from the room.'; });

// host: Enter advances on the reveal screen
document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && me.role === 'host' && $('v-reveal').classList.contains('on')) socket.emit('host:next');
});

// ---------------------------------------------------------------- race mode
let RQ = null;          // current race question
let raceSent = [];      // texts awaiting a result, in order

function drawTrack(track) {
  $('rTrack').innerHTML = track.map(t => `<tr class="${t.name === me.name ? 'me' : ''}"><td>${esc(t.name)}</td>` +
    `<td class="lane"><div><span style="width:${100 * t.idx / t.total}%"></span></div></td><td>${t.idx}/${t.total}</td>` +
    `<td>${t.hints ? `${t.hints} hint${t.hints === 1 ? '' : 's'}` : ''}</td></tr>`).join('');
}
function raceFeed(html, bg) {
  const li = document.createElement('li');
  li.innerHTML = html;
  if (bg) li.style.background = bg;
  $('raceFeed').prepend(li);
}
function hintTally(paid) {
  if (!RQ) return;
  RQ.hintsPaid = paid;
  $('hintTally').textContent = `Hints used: ${paid}`;
}

socket.on('race:start', d => {
  show('race');
  RQ = null; raceSent = [];
  drawTrack(d.track);
  $('raceFeed').innerHTML = '';
  const playing = !!me.name && d.track.some(t => t.name === me.name);
  // a host who isn't playing just watches the track
  ['raceArea', 'rprompt', 'roptions', 'rhint', 'rTimer', 'rTimerText'].forEach(id => { $(id).hidden = !playing; });
  $('rqnum').parentElement.hidden = !playing;
  if (!playing) $('rimgWrap').hidden = true;
});

socket.on('race:question', d => {
  const now = performance.now();
  RQ = { ...d, readyAt: now + d.waitMs, waitTotal: Math.max(d.waitMs, 1), hintLockUntil: now + (d.hintLockMs || 0) };
  $('rqnum').textContent = `Question ${d.index + 1} / ${d.total}`;
  $('rtopic').textContent = d.view.topicName;
  $('rprompt').textContent = d.view.prompt;
  $('rimgWrap').hidden = !d.view.imageUrl;
  if (d.view.imageUrl) $('rimg').src = d.view.imageUrl;
  const opts = d.view.options || [];
  $('roptions').innerHTML = opts.map(o => `<li>${esc(o)}</li>`).join('');
  $('rhint').textContent = {
    tf: 'Type T or F.', multi: 'Select ALL that apply: type every correct letter, e.g. ACD.',
    order: `Type the letters in order, e.g. ${'ABCDEF'.slice(0, opts.length)}.`, numeric: `Type a number${d.view.unit ? ' (' + d.view.unit + ')' : ''}.`,
    short: 'Type your answer.', frq: 'Answer in a short sentence.',
  }[d.view.format] || '';
  const box = $('raceBox');
  box.value = ''; box.disabled = false;
  $('rFeedback').textContent = '';
  RQ.hintsShown = 0;
  $('rHints').innerHTML = '';
  resetHintBtn();
  (d.hints || []).forEach((h, i) => showHint(i + 1, h, i < d.freeUpTo));
  hintTally(d.hintsPaid);
  setTimeout(() => box.focus(), 20);
  requestAnimationFrame(raceTick);
});

function raceTick() {
  if (!RQ || !$('v-race').classList.contains('on')) return;
  const now = performance.now();
  const bar = $('rBar');
  if (now < RQ.readyAt) {
    bar.style.background = '#999';
    bar.style.width = `${100 * (1 - (RQ.readyAt - now) / RQ.waitTotal)}%`;
    $('rTimerText').textContent = `Cooldown: ${((RQ.readyAt - now) / 1000).toFixed(1)} s`;
    $('raceArea').classList.add('locked');
    $('raceBtn').disabled = true;
  } else {
    bar.style.background = 'hsl(120, 70%, 25%)';
    bar.style.width = '100%';
    $('rTimerText').textContent = 'Ready';
    $('raceArea').classList.remove('locked');
    $('raceBtn').disabled = false;
  }
  // the next hint unlocks only when the previous hint's timer has run out
  const left = RQ.maxHints - RQ.hintsShown;
  if (left <= 0) { $('hintBtn').disabled = true; $('hintBtn').textContent = 'No hints left'; }
  else if (now < RQ.hintLockUntil) {
    $('hintBtn').disabled = true;
    $('hintBtn').textContent = `Next hint in ${((RQ.hintLockUntil - now) / 1000).toFixed(1)} s`;
  } else {
    $('hintBtn').disabled = false; $('hintBtn').textContent = `Hint (+10 s wait), ${left} left`;
    if ($('rFeedback').textContent.startsWith('Next hint unlocks')) $('rFeedback').textContent = '';
  }
  requestAnimationFrame(raceTick);
}

$('raceForm').onsubmit = e => {
  e.preventDefault();
  if (!RQ) return;
  if (performance.now() < RQ.readyAt) { $('rFeedback').textContent = 'Cooling down.'; return; }
  const text = $('raceBox').value.trim();
  if (!text) return;
  raceSent.push(text);
  socket.emit('answer', { text });
};
$('hintBtn').onclick = () => { if (RQ && RQ.hintsShown < RQ.maxHints) socket.emit('race:hint'); };

function showHint(n, text, free) {
  const li = document.createElement('li');
  li.textContent = text + (free ? ' (free)' : '');
  $('rHints').appendChild(li);
  RQ.hintsShown = n;
}
function resetHintBtn() {
  $('hintBtn').disabled = false;
  $('hintBtn').textContent = `Hint (+10 s wait), ${RQ ? RQ.maxHints : 3} left`;
}

socket.on('race:hint', h => {
  if (!RQ) return;
  showHint(h.n, h.text, h.free);
  hintTally(h.hintsPaid);
  if (!h.free) {
    cooldown(h.waitMs);
    RQ.hintLockUntil = performance.now() + h.hintLockMs;
  }
});

function cooldown(ms) {
  if (!RQ) return;
  RQ.readyAt = performance.now() + ms;
  RQ.waitTotal = Math.max(ms, 1);
}

socket.on('race:result', r => {
  const text = ['correct', 'wrong', 'repeat', 'invalid', 'cooldown'].includes(r.status) ? (raceSent.shift() ?? '') : '';
  $('rFeedback').textContent = '';
  switch (r.status) {
    case 'correct': raceFeed(`Q${r.index + 1}: ${esc(text)}`, shade(1)); break;
    case 'wrong': raceFeed(esc(text), shade(r.closeness)); cooldown(r.waitMs); $('raceBox').select(); break;
    case 'repeat': raceFeed(`${esc(text)} (already tried)`, shade(r.closeness)); $('raceBox').select(); break;
    case 'cooldown': cooldown(r.waitMs); $('rFeedback').textContent = 'Cooling down.'; break;
    case 'invalid': $('rFeedback').textContent = r.note || 'Not a valid answer'; break;
    case 'spectator': $('rFeedback').textContent = r.note; break;
    case 'hintLocked': $('rFeedback').textContent = `Next hint unlocks in ${(r.waitMs / 1000).toFixed(1)} s.`; break;
  }
});

socket.on('race:progress', p => {
  drawTrack(p.track);
  const l = p.latest;
  if (l && l.name !== me.name) raceFeed(`${esc(l.name)} got question ${l.idx}`, '');
});

socket.on('race:end', d => {
  RQ = null;
  show('final');
  const w = d.standings[0];
  $('winner').textContent = `${w.name} wins the race!`;
  $('fBoard').innerHTML = d.standings.map(s => `<li class="${s.name === me.name ? 'me' : ''}">${esc(s.name)}: ${s.done}/${s.total}` +
    `${s.finished ? ` in ${s.seconds} s` : ''}${s.hints ? `, ${s.hints} hint${s.hints === 1 ? '' : 's'}` : ''}</li>`).join('');
  $('againBtn').hidden = me.role !== 'host';
});

// ---------------------------------------------------------------- exit
function goHome(msg) {
  sessionStorage.removeItem('rb-host'); sessionStorage.removeItem('rb-player');
  Object.assign(me, { role: null, pin: null, playerId: null, name: null });
  Q = null; RQ = null;
  topInfo(); show('home');
  $('joinErr').textContent = msg || '';
}
$('exitBtn').onclick = () => {
  if (me.role === 'host') {
    const inLobby = $('v-lobby').classList.contains('on');
    if (inLobby) {
      if (confirm('Close the room for everyone?')) socket.emit('host:close', null, () => goHome());
    } else if (confirm('End the game for everyone and go back to the lobby?')) socket.emit('host:lobby');
  } else if (me.role === 'player') {
    if (confirm('Leave the game?')) socket.emit('player:leave', null, () => goHome());
  }
};
socket.on('closed', () => { if (me.role !== 'host') goHome('The host closed the room.'); });
