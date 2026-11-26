// A player is locked out after 3 new wrong answers; if nobody can still answer, the question ends early.
const test = require('node:test');
const assert = require('node:assert');
const { io: connect } = require('socket.io-client');
const { server, rooms } = require('../server');

const once = (s, ev) => new Promise(res => s.once(ev, res));
const emit = (s, ev, data) => new Promise(res => s.emit(ev, data, res));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const send = async (s, text) => { s.emit('answer', { text }); return once(s, 'result'); };

test('three strikes locks you out; repeats do not count', async () => {
  await new Promise(r => server.listen(0, r));
  const host = connect(`http://localhost:${server.address().port}`);
  try {
    const made = await emit(host, 'host:create', { hostPlays: true, hostName: 'Ann' });
    const qP = once(host, 'question');
    await emit(host, 'host:start');
    const q = await qP;
    rooms.get(made.pin).cur.q = { format: 'short', answer: 'Halite', accept: ['halite'], prompt: 'x', explanation: '' };
    await sleep(q.lockMs + 50);

    assert.equal((await send(host, 'calcite')).wrong, 1);
    assert.equal((await send(host, 'calcite')).status, 'repeat');   // free
    assert.equal((await send(host, 'gypsum')).wrong, 2);
    const reveal = once(host, 'reveal');
    const third = await send(host, 'quartz');
    assert.equal(third.wrong, 3);
    assert.equal(third.lockedOut, true);
    const rev = await reveal;                                       // solo player is out -> ends now
    assert.equal(rev.reason, 'everyone done');
    assert.equal(rev.awards[0].points, 0);
  } finally {
    host.close();
    server.close();
  }
});
