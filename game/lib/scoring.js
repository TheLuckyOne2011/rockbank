// Scoring rules for the base game mode. Pure functions so they can be unit-tested.

const RULES = {
  lockMs: 3000,          // answers can't be submitted for the first 3 s (typing is allowed)
  fullWindowMs: 500,     // a correct answer within 0.5 s of unlock earns the full 1000
  full: 1000,
  floorAtCap: 500,       // the time value slides one point at a time down to 500 at the time cap
  wrongPenalty: 200,     // each wrong submission costs 200 from the eventual correct score
  placePenalty: [0, 100, 300], // 1st / 2nd / 3rd correct answer
  minCorrect: 100,       // a correct answer never scores below 100
  maxWrong: 3,           // the 3rd wrong answer locks you out of the question
};

// Points still on the table at this moment, before wrong answers and place.
// capMs is measured from unlock: 1000 until 0.5 s, then a straight-line slide to 500 at the cap (whole numbers).
function timeValue(msSinceUnlock, capMs) {
  const { full, floorAtCap, fullWindowMs } = RULES;
  if (msSinceUnlock <= fullWindowMs) return full;
  const span = Math.max(1, capMs - fullWindowMs);
  const frac = Math.min(1, (msSinceUnlock - fullWindowMs) / span);
  return Math.max(floorAtCap, Math.ceil(full - (full - floorAtCap) * frac));
}

// place: 1 for the first player to answer correctly, 2 for the second, ...
function placePenalty(place) {
  const p = RULES.placePenalty;
  return p[Math.min(place, p.length) - 1] ?? p[p.length - 1];
}

function correctScore(msSinceUnlock, capMs, wrongCount, place) {
  const raw = timeValue(msSinceUnlock, capMs) - RULES.wrongPenalty * wrongCount - placePenalty(place);
  return Math.max(RULES.minCorrect, raw);
}

// The question ends once half the room (rounded up) has answered correctly.
const neededCorrect = playerCount => Math.ceil(playerCount / 2);

module.exports = { RULES, timeValue, placePenalty, correctScore, neededCorrect };
