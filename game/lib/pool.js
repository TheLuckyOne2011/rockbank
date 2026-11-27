// Load questions.json and pick a round.
const fs = require('fs');
const path = require('path');

const DB = path.join(__dirname, '..', '..', 'questions.json');
// photos: an explicit folder, else the full rockid library next to this repo, else the small set bundled in game/images
const FULL_LIBRARY = path.join(__dirname, '..', '..', '..', 'rockid', 'images');
const BUNDLED = path.join(__dirname, '..', 'images');
const IMAGES = process.env.ROCKID_IMAGES || (fs.existsSync(FULL_LIBRARY) ? FULL_LIBRARY : BUNDLED);

const PLAYABLE = new Set(['mcq', 'tf', 'multi', 'order', 'numeric', 'short', 'frq']);
// Multiple-choice questions are played as typed answers, so drop the ones that only make sense with their options.
const NEEDS_OPTIONS = /\b(of these|of the following|the following|which pair|does not belong|odd one)\b/i;
const NEEDS_OPTIONS_CAPS = /\b(NOT|LEAST)\b/; // capitalized emphasis, as in "Which is NOT..."
const sentences = s => (String(s).match(/[.!?](\s|$)/g) || []).length;

const { shortForms, hasShortAnswer } = require('./parts');

function playable(q) {
  if (!PLAYABLE.has(q.format)) return false;
  if (q.format === 'frq') return false;                                     // no sentence answers
  if ((q.format === 'short' || q.format === 'mcq') && !hasShortAnswer(q)) return false; // must be answerable with a short term
  if (q.format === 'mcq' && (NEEDS_OPTIONS.test(q.prompt) || NEEDS_OPTIONS_CAPS.test(q.prompt))) return false;
  if (q.format === 'mcq' && /^(both|neither|all|none) /i.test(q.answer)) return false;
  if (q.format === 'frq' && sentences(q.answer) > 2) return false; // keep free-response to about a sentence
  if (q.image && !fs.existsSync(path.join(IMAGES, q.image.specimen))) return false;
  return true;
}

const { kind } = require('./kind');
const all = JSON.parse(fs.readFileSync(DB, 'utf8')).questions.filter(playable);
for (const q of all) q.kind = kind(q);
// share of each round drawn from reasoning questions (the rest are straight recall)
const REASONING_SHARE = 2 / 3;

const MIXES = {
  everything: () => true,
  identification: q => ['3h.ii', '3i.ii'].includes(q.topic) || !!q.image,
  properties: q => q.topic.startsWith('3h.') && !['3h.ii'].includes(q.topic),
  concepts: q => q.kind === 'reasoning',
};

function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function pickRound({ count, level, mix }) {
  let pool = shuffle(all.filter(q => (level === 'state' || q.level === 'regional') && (MIXES[mix] || MIXES.everything)(q)));
  if (mix === 'everything' || !MIXES[mix]) {
    // interleave so about two thirds are reasoning questions and one third recall
    const reason = pool.filter(q => q.kind === 'reasoning'), recall = pool.filter(q => q.kind !== 'reasoning');
    pool = [];
    let r = 0, f = 0;
    while (r < reason.length || f < recall.length) {
      const wantReason = f >= recall.length || (r < reason.length && (r + 1) / (r + f + 1) <= REASONING_SHARE + 1e-9);
      pool.push(wantReason ? reason[r++] : recall[f++]);
    }
  }
  const out = [], usedStations = new Set(), usedPrompts = new Set();
  for (const q of pool) {
    if (out.length >= count) break;
    if (q.station && usedStations.has(q.station.id)) continue; // at most one part per specimen chain
    const dup = q.image ? q.prompt + '|' + q.image.specimen : q.prompt;
    if (usedPrompts.has(dup)) continue;
    if (q.station) usedStations.add(q.station.id);
    usedPrompts.add(dup);
    out.push(prepare(q));
  }
  return out;
}

// Server-side copy of the question with display order fixed and an image chosen.
function prepare(q) {
  const p = { ...q, prompt: q.prompt.replace(/^\[Specimen \d+\]\s*/, '') };
  if (q.format === 'mcq') { // typed answer: no options shown
    p.format = 'short';
    p.accept = [q.answer, ...(q.accept || [])];
    delete p.options;
  }
  if (p.format === 'short') p.accept = [...new Set([...(p.accept || []), ...shortForms(q)])]; // short forms count too
  if (q.format === 'order') p.options = shuffle([...q.answer]);
  if (q.format === 'tf') delete p.options;
  if (q.image) {
    const dir = path.join(IMAGES, q.image.specimen);
    const files = fs.readdirSync(dir).filter(f => /\.(jpe?g|png|webp)$/i.test(f));
    p.imageUrl = files.length ? `/img/${q.image.specimen}/${files[Math.floor(Math.random() * files.length)]}` : null;
  }
  return p;
}

// What players are allowed to see before the question ends.
function publicView(p) {
  const v = { format: p.format, prompt: p.prompt, topicName: p.topicName, imageUrl: p.imageUrl || null, unit: p.unit || null };
  if (p.options) v.options = p.options;
  return v;
}

function answerText(p) {
  const letter = i => String.fromCharCode(65 + i);
  if (p.format === 'tf') return p.answer;
  if (p.format === 'multi') return p.answer.map(a => `${letter(p.options.indexOf(a))}. ${a}`).join(' · ');
  if (p.format === 'order') return p.answer.map(a => letter(p.options.indexOf(a))).join('') + ' — ' + p.answer.join(' → ');
  if (p.format === 'numeric') return `${p.answer}${p.unit ? ' ' + p.unit : ''}${p.tolerance ? ` (±${p.tolerance})` : ''}`;
  return String(p.answer);
}

module.exports = { pickRound, publicView, answerText, IMAGES, count: () => all.length, MIXES };
