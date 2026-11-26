// Picking the mode at room creation, a player leaving mid-game, and the host closing the room.
const test = require('node:test');
const assert = require('node:assert');
const { io: connect } = require('socket.io-client');
const { server, rooms } = require('../server');

const once = (s, ev) => new Promise(res => s.once(ev, res));
const emit = (s, ev, data) => new Promise(res => s.emit(ev, data, res));

test('mode chosen at creation; leaving and closing', async () => {
  await new Promise(r => server.listen(0, r));
  const url = `http://localhost:${server.address().port}`;
  const host = connect(url), bo = connect(url), cy = connect(url);
  try {
    const made = await emit(host, 'host:create', { hostPlays: true, hostName: 'Ann', settings: { mode: 'race' } });
    const r = rooms.get(made.pin);
    assert.equal(r.settings.mode, 'race');
    await emit(bo, 'player:join', { pin: made.pin, name: 'Bo' });
    await emit(cy, 'player:join', { pin: made.pin, name: 'Cy' });
    const started = once(bo, 'race:start');
    await emit(host, 'host:start');
    await started;
    assert.equal(r.race.state.size, 3);

    // Bo leaves mid-race: gone from the room and from the race
    assert.equal((await emit(bo, 'player:leave')).ok, true);
    assert.equal(r.players.size, 2);
    assert.equal(r.race.state.size, 2);
    assert.ok(![...r.players.values()].some(p => p.name === 'Bo'));

    // the host can't "leave" as a player; closing the room tells everyone and deletes it
    assert.equal((await emit(host, 'player:leave')).ok, false);
    const closed = once(cy, 'closed');
    await emit(host, 'host:close');
    await closed;
    assert.equal(rooms.has(made.pin), false);
  } finally {
    host.close(); bo.close(); cy.close();
    server.close();
  }
});
