const test = require('node:test');
const assert = require('node:assert');
const S = require('../lib/scoring');
const { check } = require('../lib/check');
const pool = require('../lib/pool');

const CAP = 45000;

test('time value: 1000 for 0.5 s, then slides by whole points to 500 at the cap', () => {
  assert.equal(S.timeValue(0, CAP), 1000);
  assert.equal(S.timeValue(500, CAP), 1000);
  assert.equal(S.timeValue(501, CAP), 1000);          // first point drops just after
  assert.equal(S.timeValue(590, CAP), 999);
  assert.equal(S.timeValue(22750, CAP), 750);         // halfway
  assert.equal(S.timeValue(CAP, CAP), 500);
  assert.equal(S.timeValue(CAP + 5000, CAP), 500);
  let prev = 1000;
  for (let ms = 0; ms <= CAP; ms += 37) {             // never jumps more than a couple of points per tick
    const v = S.timeValue(ms, CAP);
    assert.ok(Number.isInteger(v) && v <= prev && prev - v <= 2);
    prev = v;
  }
});

test('wrong answers cost 200 each, place penalties 0/100/300, floor 100', () => {
  assert.equal(S.correctScore(200, CAP, 0, 1), 1000);
  assert.equal(S.correctScore(200, CAP, 1, 1), 800);
  assert.equal(S.correctScore(200, CAP, 0, 2), 900);
  assert.equal(S.correctScore(200, CAP, 0, 3), 700);
  assert.equal(S.correctScore(CAP, CAP, 2, 3), 100);
  assert.equal(S.RULES.partial, undefined);
});

test('half the room rounded up must be correct', () => {
  assert.deepEqual([1, 2, 3, 4, 5, 6].map(S.neededCorrect), [1, 1, 2, 2, 3, 3]);
});

const short = (answer, accept = []) => ({ format: 'short', answer, accept });

test('names and terms: typos ok, wrong answers get a closeness score, no partial status', () => {
  const q = short('Amethyst', ['amethyst']);
  assert.equal(check(q, 'amethist').status, 'correct');
  assert.equal(check(q, 'it is amethyst').status, 'correct');
  const near = check(q, 'citrine');
  assert.equal(near.status, 'wrong');
  assert.ok(near.closeness >= 0.6, 'same family should look close');
  assert.ok(check(q, 'galena').closeness < 0.4);
  assert.equal(check(q, '').status, 'invalid');
});

test('typing every option does not count', () => {
  const q = short('felsic');
  assert.equal(check(q, 'felsic').status, 'correct');
  assert.equal(check(q, 'felsic intermediate mafic ultramafic').status, 'wrong');
});

test('alternate valid answers (converted multiple choice)', () => {
  const luster = short('adamantine', ['adamantine', 'submetallic']);
  assert.equal(check(luster, 'submetallic').status, 'correct');
  const sys = short('trigonal');
  assert.equal(check(sys, 'hexagonal').status, 'correct');
  const streak = short('white');
  assert.equal(check(streak, 'colorless').status, 'correct');
});

test('numbers and ranges in short answers', () => {
  assert.equal(check(short('5.5–6'), '6').status, 'correct');
  assert.equal(check(short('5.5–6'), '5.75').status, 'correct');
  assert.equal(check(short('5.5–6'), '7').status, 'wrong');
  assert.equal(check(short('15.5–19.3'), '19.3').status, 'correct');
  assert.equal(check(short('15.5–19.3'), '19,3').status, 'correct');      // decimal comma
  assert.equal(check(short('15.5–19.3'), '19').status, 'correct');
  assert.equal(check(short('15.5–19.3'), '20').status, 'wrong');
  assert.equal(check({ format: 'numeric', answer: 19.3, tolerance: 0.1 }, '19,3').status, 'correct');
  assert.equal(check({ format: 'numeric', answer: 1000, tolerance: 1 }, '1,000').status, 'correct');
  assert.equal(check(short('2 directions'), '2').status, 'correct');
  assert.equal(check(short('no cleavage'), 'none').status, 'correct');
});

test('sentence answers are graded laxly', () => {
  const q = short('high pressure and low temperature in a subduction zone');
  assert.equal(check(q, 'subduction zones').status, 'correct');
  assert.equal(check(q, 'high pressure').status, 'correct');
  assert.equal(check(q, 'a desert').status, 'wrong');
  const frq = { format: 'frq', answer: 'Basalt crystallizes from hot mafic magma; granite from cooler silica-rich melt.',
                keypoints: ['basalt = high-T minerals', 'granite = low-T minerals'] };
  assert.equal(check(frq, 'granite forms from cooler magma with more silica').status, 'correct');
  assert.equal(check(frq, 'because of erosion').status, 'wrong');
});

test('true/false, select-all, ordering, numeric', () => {
  assert.equal(check({ format: 'tf', answer: 'False' }, 'f').status, 'correct');
  assert.equal(check({ format: 'tf', answer: 'False' }, 'maybe').status, 'invalid');
  const m = { format: 'multi', options: ['A1', 'B1', 'C1', 'D1'], answer: ['A1', 'C1'] };
  assert.equal(check(m, 'CA').status, 'correct');
  assert.equal(check(m, 'A').status, 'wrong');
  assert.equal(check(m, 'A').closeness, 0.5);
  const o = { format: 'order', options: ['c', 'a', 'b'], answer: ['a', 'b', 'c'] };
  assert.equal(check(o, 'BCA').status, 'correct');
  assert.equal(check(o, 'AB').status, 'invalid');
  const n = { format: 'numeric', answer: 34.6, tolerance: 0.6 };
  assert.equal(check(n, '35').status, 'correct');
  assert.ok(check(n, '36.5').closeness > 0.8);
});

test('default rounds are about two thirds reasoning questions', () => {
  let reason = 0, total = 0;
  for (let i = 0; i < 40; i++) for (const q of pool.pickRound({ count: 30, level: 'regional', mix: 'everything' })) {
    total++; if (q.kind === 'reasoning') reason++;
  }
  assert.ok(reason / total > 0.6 && reason / total < 0.72, `reasoning share ${reason / total}`);
});

test('rounds contain no multiple-choice options and no option-dependent prompts', () => {
  const r = pool.pickRound({ count: 50, level: 'state', mix: 'everything' });
  for (const q of r) {
    assert.notEqual(q.format, 'mcq');
    if (q.format === 'short') assert.equal(q.options, undefined);
    assert.ok(!/\b(of these|of the following)\b/i.test(q.prompt) || ['multi', 'order', 'tf'].includes(q.format), q.prompt);
  }
});
