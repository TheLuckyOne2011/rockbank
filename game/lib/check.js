// Grade a typed answer.
// Returns { status: 'correct' | 'wrong' | 'invalid', key, closeness (0..1), note }
//   invalid   = unreadable input (empty, wrong letters) - not penalized
//   key       = normalized answer, so repeating the same wrong answer isn't charged twice
//   closeness = how near a wrong answer was, for the answer feed's highlight
//
// Names and terms use typo-tolerant exact matching. Sentence answers (3+ content words) are graded
// laxly by keyword overlap: covering about a third of the key words, or any one key point, is correct.
const path = require('path');
const SPEC = require(path.join(__dirname, '..', 'data', 'specimens.json'));

const norm = s => String(s ?? '').toLowerCase().normalize('NFKD').replace(/['’]/g, '').replace(/[^a-z0-9.]/g, '');

function lev(a, b) {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
  for (let j = 0; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
    }
  }
  return d[a.length][b.length];
}
const typoAllowance = len => Math.max(len >= 9 ? 2 : len >= 5 ? 1 : 0, Math.floor(len * 0.15));

// ---------------------------------------------------------------- words
const STOP = new Set(('a an the and or of in on at to by for from with as is are was were be been it its this that these those ' +
  'into onto over under than then which what when where how why who whom whose not no very more most less such can may ' +
  'also only about mainly mostly typically usually often generally commonly some any each both all other rock rocks mineral ' +
  'minerals specimen form forms formed forming made make makes one two thin section possible evidence').split(' '));
const SYN = { colourless: 'colorless', colorless: 'white', isometric: 'cubic', hexagonal: 'trigonal', grey: 'gray', sulphur: 'sulfur',
              aluminium: 'aluminum', fizz: 'effervesce', fizzes: 'effervesce', bubbles: 'effervesce', effervesces: 'effervesce',
              plutonic: 'intrusive', volcanic: 'extrusive', none: '0', zero: '0', no: '0' };
function stem(w) {
  w = SYN[w] || w;
  if (w.length > 5 && w.endsWith('ing')) w = w.slice(0, -3);
  else if (w.length > 4 && w.endsWith('ed')) w = w.slice(0, -2);
  else if (w.length > 4 && w.endsWith('ies')) w = w.slice(0, -3) + 'y';
  else if (w.length > 4 && /(ss|x|z|ch|sh)es$/.test(w)) w = w.slice(0, -2);
  else if (w.length > 3 && w.endsWith('s') && !w.endsWith('ss')) w = w.slice(0, -1);
  return SYN[w] || w;
}
const words = s => (String(s).toLowerCase().match(/[a-z0-9]+(?:\.[0-9]+)?/g) || []);
const content = s => [...new Set(words(s).filter(w => !STOP.has(w) && (w.length > 2 || /\d/.test(w))).map(stem))];
const numbers = s => (String(s).match(/-?\d+(?:\.\d+)?/g) || []).map(Number);

function wordHit(w, pool) {
  return pool.some(p => p === w || (w.length >= 5 && p.length >= 5 && lev(w, p) <= 1) ||
    (w.length >= 6 && p.length >= 6 && (w.startsWith(p.slice(0, 6)) || p.startsWith(w.slice(0, 6)))));
}

const OPPOSITES = [['slow', 'rapid'], ['slow', 'fast'], ['slow', 'quick'], ['high', 'low'], ['intrusive', 'extrusive'], ['felsic', 'mafic'],
  ['coarse', 'fine'], ['increase', 'decrease'], ['deep', 'shallow'], ['hot', 'cold'], ['wet', 'dry'], ['calcium', 'sodium'],
  ['foliated', 'nonfoliated'], ['mechanical', 'chemical'], ['continuous', 'discontinuous'], ['contact', 'regional'],
  ['clastic', 'chemical'], ['angular', 'rounded'], ['well', 'poorly'], ['concordant', 'discordant'], ['older', 'younger'],
  ['first', 'last'], ['top', 'bottom'], ['upper', 'lower']].map(p => p.map(stem));
// the input uses a word whose opposite is in the answer, and the answer doesn't use that word itself
function contradicts(tw, iw) {
  return OPPOSITES.some(([a, b]) => (tw.includes(a) && !tw.includes(b) && iw.includes(b) && !iw.includes(a)) ||
                                    (tw.includes(b) && !tw.includes(a) && iw.includes(a) && !iw.includes(b)) ||
                                    (tw.includes(a) && !tw.includes(b) && iw.includes(b)) || (tw.includes(b) && !tw.includes(a) && iw.includes(a)));
}

// ---------------------------------------------------------------- one target
function gradeAgainst(input, target) {
  const a = norm(input), b = norm(target);
  if (!a) return { correct: false, closeness: 0 };
  const digits = x => x.replace(/[^0-9.]/g, '');
  // typos are forgiven in letters, never in numbers ('35% An' is not '42% An')
  if (a === b || (lev(a, b) <= typoAllowance(b.length) && digits(a) === digits(b))) return { correct: true, closeness: 1 };
  // chemical formulas: exact (with a small typo allowance) only
  if (/^[A-Z(][A-Za-z0-9()·,.+\-\s]*$/.test(String(target).trim()) && /\d/.test(target) && !/[a-z]{4,}/.test(target))
    return { correct: false, closeness: Math.max(0, 1 - lev(a, b) / Math.max(a.length, b.length)) };

  const tw = content(target), iw = content(input);
  // "none" / "no cleavage" / "0"
  const isNone = t => /^\s*(no|none|0|zero)\b/i.test(t);
  if (isNone(target) && isNone(input) && words(target).length <= 3) return { correct: true, closeness: 1 };

  // numbers and ranges in short answers ("5.5-6", "2 directions", "about 650-800 °C")
  const tn = numbers(target), inum = numbers(input);
  if (tn.length && inum.length && tw.filter(w => !/\d/.test(w)).length <= 3) {
    const range = String(target).match(/(-?\d+(?:\.\d+)?)\s*(?:–|-|to)\s*(-?\d+(?:\.\d+)?)/);
    const ok = inum.every(x => tn.includes(x) || (range && x >= Math.min(+range[1], +range[2]) && x <= Math.max(+range[1], +range[2])));
    const extra = iw.filter(w => !/\d/.test(w) && !wordHit(w, tw));
    if (ok && extra.length === 0) return { correct: true, closeness: 1 };
  }

  // a different number than the answer's is wrong ("35% An" vs "42% An")
  if (tn.length && inum.length && !inum.every(x => tn.includes(x))) {
    const range = String(target).match(/(-?\d+(?:\.\d+)?)\s*(?:–|-|to)\s*(-?\d+(?:\.\d+)?)/);
    if (!range || !inum.every(x => x >= Math.min(+range[1], +range[2]) && x <= Math.max(+range[1], +range[2])))
      return { correct: false, closeness: 0.3 };
  }
  // saying the opposite is wrong ("slow cooling" for "rapid cooling")
  if (contradicts(tw, iw)) return { correct: false, closeness: 0.2 };

  // sentence-like answers: lax keyword coverage
  if (tw.length >= 3) {
    const hits = tw.filter(w => wordHit(w, iw)).length;
    const need = Math.max(2, Math.ceil(tw.length / 3));
    const tooLong = iw.length > 2 * tw.length + 6; // keyword dumps don't count
    if (hits >= need && !tooLong) return { correct: true, closeness: 1 };
    return { correct: false, closeness: Math.min(0.9, (hits / need) * 0.85) };
  }

  // short terms: one-word answers inside a longer reply ("it is calcite") still count
  if (tw.length && tw.every(w => wordHit(w, iw)) && iw.length <= tw.length) return { correct: true, closeness: 1 };
  const sim = 1 - lev(a, b) / Math.max(a.length, b.length);
  const overlap = tw.length ? tw.filter(w => wordHit(w, iw)).length / tw.length : 0;
  return { correct: false, closeness: Math.max(0, Math.max(sim, overlap * 0.8)) };
}

// ---------------------------------------------------------------- specimens (closeness only)
const nameIndex = [];
for (const s of SPEC.specimens) for (const n of [s.name, ...s.accept]) nameIndex.push({ key: norm(n), s });
function resolveSpecimen(text) {
  const n = norm(text);
  if (!n) return null;
  const exact = nameIndex.find(e => e.key === n);
  if (exact) return exact.s;
  let best = Infinity, hit = null, tie = false;
  for (const e of nameIndex) {
    const d = lev(n, e.key);
    if (d > typoAllowance(e.key.length)) continue;
    if (d < best) { best = d; hit = e.s; tie = false; } else if (d === best && e.s !== hit) tie = true;
  }
  return tie ? null : hit;
}
function sameFamily(a, b) {
  return a && b && a.slug !== b.slug && ((a.parent && a.parent === b.parent) || (a.subgroup && a.subgroup === b.subgroup));
}

// ---------------------------------------------------------------- formats
function checkText(q, input) {
  if (!norm(input)) return { status: 'invalid', note: 'Type an answer' };
  const targets = [q.answer, ...(q.accept || []), ...(q.keypoints || [])].filter(t => typeof t === 'string' && t.trim());
  let best = 0;
  for (const t of targets) {
    const g = gradeAgainst(input, t);
    if (g.correct) return { status: 'correct', key: 'txt' + norm(input), closeness: 1 };
    best = Math.max(best, g.closeness);
  }
  if (sameFamily(resolveSpecimen(q.answer), resolveSpecimen(input))) best = Math.max(best, 0.7);
  return { status: 'wrong', key: 'txt' + norm(input), closeness: +best.toFixed(2) };
}

function checkTF(q, input) {
  const t = String(input).trim().toLowerCase();
  const v = /^(t|true|yes|y)$/.test(t) ? 'True' : /^(f|false|no|n)$/.test(t) ? 'False' : null;
  if (!v) return { status: 'invalid', note: 'Type T or F' };
  return { status: v === q.answer ? 'correct' : 'wrong', key: 'tf' + v, closeness: 0 };
}

function letterIndex(ch, n) {
  const i = ch.toUpperCase().charCodeAt(0) - 65;
  return i >= 0 && i < n ? i : -1;
}
function parseLetters(input, n) {
  const letters = String(input).toUpperCase().replace(/[^A-Z]/g, '').split('');
  if (!letters.length) return null;
  const idx = letters.map(c => letterIndex(c, n));
  return idx.includes(-1) ? null : idx;
}

function checkMulti(q, input) {
  const idx = parseLetters(input, q.options.length);
  if (!idx) return { status: 'invalid', note: 'Type the letters of every correct option, e.g. ACD' };
  const picked = new Set(idx.map(i => q.options[i]));
  const right = new Set(q.answer);
  const key = 'set' + [...new Set(idx)].sort().join(',');
  const inter = [...picked].filter(x => right.has(x)).length;
  const union = new Set([...picked, ...right]).size;
  if (inter === union) return { status: 'correct', key, closeness: 1 };
  return { status: 'wrong', key, closeness: +(inter / union).toFixed(2) };
}

function checkOrder(q, input) {
  const idx = parseLetters(input, q.options.length);
  if (!idx || idx.length !== q.options.length || new Set(idx).size !== idx.length)
    return { status: 'invalid', note: `Type all ${q.options.length} letters in order` };
  const seq = idx.map(i => q.options[i]);
  const hits = seq.filter((x, i) => x === q.answer[i]).length;
  const key = 'ord' + idx.join('');
  if (hits === seq.length) return { status: 'correct', key, closeness: 1 };
  return { status: 'wrong', key, closeness: +(hits / seq.length).toFixed(2) };
}

function checkNumeric(q, input) {
  const m = String(input).replace(/,/g, '').match(/-?\d*\.?\d+(e-?\d+)?/i);
  if (!m) return { status: 'invalid', note: 'Type a number' };
  const x = parseFloat(m[0]), a = Number(q.answer), tol = Number(q.tolerance || 0);
  const key = 'num' + x;
  if (Math.abs(x - a) <= tol + 1e-9) return { status: 'correct', key, closeness: 1 };
  const rel = Math.abs(x - a) / Math.max(Math.abs(a), 1e-9);
  return { status: 'wrong', key, closeness: +Math.max(0, 1 - rel * 2).toFixed(2) };
}

// "19,3" is a decimal comma -> 19.3; "1,000" is a thousands separator -> 1000
const decimalComma = s => String(s ?? '').replace(/(\d),(\d{3})(?!\d)/g, '$1$2').replace(/(\d),(\d{1,2})(?!\d)/g, '$1.$2');

function check(q, input) {
  input = decimalComma(input);
  switch (q.format) {
    case 'short': case 'frq': return checkText(q, input);
    case 'tf': return checkTF(q, input);
    case 'multi': return checkMulti(q, input);
    case 'order': return checkOrder(q, input);
    case 'numeric': return checkNumeric(q, input);
    default: return { status: 'invalid', note: 'Unsupported question' };
  }
}

module.exports = { check, norm, lev, gradeAgainst, resolveSpecimen };
