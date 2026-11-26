// Race mode end to end: cooldowns, hints (+10 s wait, one at a time), the "first hint shown" mode, first to finish wins.
const test = require('node:test');
const assert = require('node:assert');
const { io: connect } = require('socket.io-client');
const { server, rooms } = require('../server');
const { RACE } = require('../lib/race');
const { hintsFor } = require('../lib/hints');

const once = (s, ev) => new Promise(res => s.once(ev, res));
const emit = (s, ev, data) => new Promise(res => s.emit(ev, data, res));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const send = async (s, text) => { s.emit('answer', { text }); return once(s, 'race:result'); };
const QS = ['alpha', 'bravo', 'charlie'].map(a => ({ format: 'short', answer: a, accept: [a], prompt: 'say ' + a, topicName: 't', explanation: '' }));

test('hints get stronger and the third nearly gives the answer', () => {
  const h = hintsFor({ format: 'short', answer: 'Amethyst' });
  assert.equal(h.length, 3);
  assert.match(h[0], /^A_{7}/);
  assert.equal(h[2], 'Amethys_');
});

let url;
test.before(async () => { await new Promise(r => server.listen(0, r)); url = `http://localhost:${server.address().port}`; });
test.after(() => server.close());

async function room(mode, names) {
  const sockets = names.map(() => connect(url));
  const made = await emit(sockets[0], 'host:create', { hostPlays: true, hostName: names[0], settings: { mode, count: 10 } });
  for (let i = 1; i < names.length; i++) await emit(sockets[i], 'player:join', { pin: made.pin, name: names[i] });
  const firsts = sockets.map(s => once(s, 'race:question'));
  await emit(sockets[0], 'host:start');
  const q0 = await Promise.all(firsts);
  const r = rooms.get(made.pin);
  r.questions = QS.map(q => ({ ...q }));
  r.race.total = QS.length;
  return { sockets, r, q0 };
}

test('race: hint adds 10 s wait, next hint locked until it runs out, first to finish wins', async () => {
  RACE.freeHintAfterMs = 60000;          // keep the free hint out of this test
  const { sockets: [ann, bo], r } = await room('race', ['Ann', 'Bo']);
  try {
    await sleep(RACE.cooldownMs + 50);
    ann.emit('race:hint');
    const h1 = await once(ann, 'race:hint');
    assert.equal(h1.n, 1);
    assert.equal(h1.hintsPaid, 1);
    assert.ok(h1.waitMs > RACE.hintPenaltyMs - 200, `wait ${h1.waitMs}`);       // the hint adds a 10 s wait
    assert.ok(h1.hintLockMs > RACE.hintPenaltyMs - 200);
    assert.equal((await send(ann, 'alpha')).status, 'cooldown');

    ann.emit('race:hint');                                                    // second hint too soon: refused
    const locked = await once(ann, 'race:result');
    assert.equal(locked.status, 'hintLocked');
    assert.equal(r.race.state.get(r.hostPlayerId).hintsUsed, 1);

    // fast-forward the hint timer, then a second hint is allowed
    const st = r.race.state.get(r.hostPlayerId);
    st.hintLockUntil = st.readyAt = Date.now();
    ann.emit('race:hint');
    assert.equal((await once(ann, 'race:hint')).n, 2);

    // finish the race: first to finish wins straight away
    st.readyAt = Date.now();
    assert.equal((await send(ann, 'alpha')).status, 'correct');
    st.readyAt = Date.now();
    assert.equal((await send(ann, 'bravo')).status, 'correct');
    st.readyAt = Date.now();
    const end = once(bo, 'race:end');
    assert.equal((await send(ann, 'charlie')).status, 'correct');
    const res = await end;
    assert.equal(res.standings[0].name, 'Ann');
    assert.equal(res.standings[0].finished, true);
    assert.equal(res.standings[0].hints, 2);
    assert.equal(res.standings[1].name, 'Bo');
    assert.equal(r.phase, 'final');
  } finally {
    ann.close(); bo.close();
  }
});

test('"first hint shown" mode: hint 1 is free on every question; the 30 s rule frees hint 2', async () => {
  RACE.freeHintAfterMs = 1200;           // shortened from 30 s for the test
  const { sockets: [ann], q0 } = await room('race_hint', ['Ann']);
  try {
    assert.equal(q0[0].hints.length, 1);
    assert.equal(q0[0].freeUpTo, 1);
    assert.equal(q0[0].hintsPaid, 0);
    assert.equal(q0[0].hintLockMs, 0);                               // a free hint doesn't lock the next one
    const free2 = await once(ann, 'race:hint');
    assert.equal(free2.n, 2);
    assert.equal(free2.free, true);
    assert.equal(free2.hintsPaid, 0);
    await sleep(Math.max(0, RACE.cooldownMs - 1200) + 50);
    const next = once(ann, 'race:question');
    assert.equal((await send(ann, 'alpha')).status, 'correct');
    const q1 = await next;
    assert.equal(q1.hints.length, 1);                                // hint 1 shown again on the next question
  } finally {
    ann.close();
    RACE.freeHintAfterMs = 30000;
  }
});
