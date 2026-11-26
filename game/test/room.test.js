// End-to-end: three clients play one question through the real server.
const test = require('node:test');
const assert = require('node:assert');
const { io: connect } = require('socket.io-client');
process.env.PORT = 0;
const { server, rooms } = require('../server');

const once = (s, ev) => new Promise(res => s.once(ev, res));
const emit = (s, ev, data) => new Promise(res => s.emit(ev, data, res));
const sleep = ms => new Promise(r => setTimeout(r, ms));

test('lock, penalties, place order and early end at half the room', async () => {
  await new Promise(r => server.listen(0, r));
  const url = `http://localhost:${server.address().port}`;
  const host = connect(url), b = connect(url), c = connect(url);
  try {
    const made = await emit(host, 'host:create', { hostPlays: true, hostName: 'Ann', settings: { count: 10 } });
    assert.ok(made.ok);
    assert.ok((await emit(b, 'player:join', { pin: made.pin, name: 'Bo' })).ok);
    assert.ok((await emit(c, 'player:join', { pin: made.pin, name: 'Cy' })).ok);

    const r = rooms.get(made.pin);
    const qP = once(b, 'question');
    assert.ok((await emit(host, 'host:start')).ok);
    const q = await qP;
    assert.equal(q.needed, 2); // 3 players -> 2 correct ends it
    assert.equal(q.roster.length, 3);

    // force a known question so answers are deterministic
    r.cur.q = { format: 'short', answer: 'Halite', accept: ['halite', 'rock salt'], prompt: 'x', explanation: '' };

    host.emit('answer', { text: 'halite' });
    assert.equal((await once(host, 'result')).status, 'locked');

    await sleep(q.lockMs + 50);
    const seenByCy = once(c, 'progress');
    host.emit('answer', { text: 'halite' });         // Ann: correct, 1st, within 0.5 s
    const ra = await once(host, 'result');
    assert.equal(ra.status, 'correct');
    assert.equal(ra.points, 1000);
    const pr = await seenByCy;                       // others see that Ann got it, not her answer
    assert.equal(pr.latest, 'Ann');
    assert.ok(!JSON.stringify(pr).toLowerCase().includes('halite'));

    b.emit('answer', { text: 'calcite' });           // Bo: wrong once
    assert.equal((await once(b, 'result')).status, 'wrong');
    b.emit('answer', { text: 'calcite' });           // same wrong answer: not charged again
    assert.equal((await once(b, 'result')).status, 'repeat');
    b.emit('answer', { text: 'rock salt' });         // Bo: correct, 2nd, 1 wrong
    const rb = await once(b, 'result');
    assert.equal(rb.status, 'correct');
    assert.equal(rb.points, 1000 - 200 - 100);       // still inside 0.5 s

    const rev = await once(c, 'reveal');             // half the room correct -> ends without Cy
    assert.equal(rev.reason, 'answered');
    const pts = Object.fromEntries(rev.awards.map(a => [a.name, a.points]));
    assert.deepEqual(pts, { Ann: 1000, Bo: 700, Cy: 0 });
  } finally {
    host.close(); b.close(); c.close();
    server.close();
  }
});
