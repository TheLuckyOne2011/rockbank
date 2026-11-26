// Text hints, matched to how answers are graded (see check.js):
//  - names/terms: letter patterns; digits stay hidden until the last hint
//  - sentences: graded by key words, so hint 2 shows one key word fewer than needed and hint 3 shows just enough
const isLetter = ch => /[a-z]/i.test(ch);
const isChar = ch => /[a-z0-9]/i.test(ch);
const letterCount = s => [...s].filter(isChar).length;
const SMALL = new Set('a an the and or of in on at to by for from with as is are was were be it its this that than then into not no'.split(' '));

// keep(i, word) decides which characters stay visible; digits are hidden unless showDigits
function maskWord(w, keep, showDigits = false) {
  return [...w].map((ch, i) => {
    if (!isChar(ch)) return ch;
    if (/\d/.test(ch)) return showDigits ? ch : '_';
    return keep(i, w) ? ch : '_';
  }).join('');
}

function textHints(answer) {
  const s = String(answer).trim();
  const words = s.split(/\s+/);

  if (letterCount(s) <= 2 && words.length === 1) {
    return [`${s.length} character${s.length === 1 ? '' : 's'}`, /\d/.test(s) ? 'It contains a number' : 'Think of an element symbol or short formula', s];
  }

  if (/\d/.test(s) && s.length <= 12) {
    // short numeric answer like "5.5–6" or "2 directions"
    return [`A number or range (${s.length} characters)`, words.map(w => maskWord(w, () => true, false)).join(' '),
            [...s].map((ch, i) => (i < s.length - 1 || !isChar(ch) ? ch : '_')).join('')];
  }

  if (words.length > 5) {
    // sentence: key words are the longer, non-filler words
    const key = words.map((w, i) => ({ i, k: !SMALL.has(w.toLowerCase().replace(/[^a-z]/g, '')) && w.replace(/[^a-z0-9]/gi, '').length >= 3 }))
      .filter(x => x.k).map(x => x.i);
    const need = Math.max(2, Math.ceil(key.length / 3));
    const reveal = n => {
      const shown = new Set(key.slice(0, n));
      return words.map((w, i) => (shown.has(i) || !key.includes(i) ? w : maskWord(w, j => j === 0))).join(' ');
    };
    return [`${words.length} words: ${words.map(w => maskWord(w, j => j === 0)).join(' ')}`, reveal(Math.max(1, need - 1)), reveal(need)];
  }

  // name or short phrase: letter patterns
  const n = letterCount(s);
  return [
    `${words.map(w => maskWord(w, i => i === 0)).join(' ')}  (${n} character${n === 1 ? '' : 's'})`,
    words.map(w => maskWord(w, i => i === 0 || i % 2 === 0)).join(' '),
    words.map(w => maskWord(w, (i, word) => letterCount(word) <= 2 || i !== word.length - 1, true)).join(' '),
  ];
}

// For sentence answers: the pieces needed to reveal key words one at a time.
function sentenceParts(answer) {
  const words = String(answer).trim().split(/\s+/);
  if (words.length <= 5) return null;
  const key = words.map((w, i) => ({ i, k: !SMALL.has(w.toLowerCase().replace(/[^a-z]/g, '')) && w.replace(/[^a-z0-9]/gi, '').length >= 3 }))
    .filter(x => x.k).map(x => x.i);
  const reveal = n => {
    const shown = new Set(key.slice(0, n));
    return words.map((w, i) => (shown.has(i) || !key.includes(i) ? w : maskWord(w, j => j === 0))).join(' ');
  };
  return { key, reveal, shape: `${words.length} words: ${words.map(w => maskWord(w, j => j === 0)).join(' ')}` };
}

module.exports = { textHints, sentenceParts };
