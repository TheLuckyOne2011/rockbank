// Short forms of longer answers that are fair to accept on their own:
//  - "X (Y)": X, and Y if it is short          e.g. "deep ocean (abyssal plain)" -> deep ocean, abyssal plain
//  - "A to B" ranges on streak/color questions  e.g. "pale yellow to white"      -> pale yellow, white
const words = s => String(s).trim().split(/\s+/).filter(Boolean).length;

function shortForms(q) {
  const out = [];
  for (const a of [q.answer, ...(q.accept || [])]) {
    if (typeof a !== 'string') continue;
    const m = a.match(/^([^()]+?)\s*\(([^()]+)\)\s*$/);
    if (m) {
      if (words(m[1]) <= 3) out.push(m[1].trim());
      // the parenthetical counts only when it reads like an alternate name, not a description
      if (words(m[2]) <= 2 && !/\b(the|a|an|of|to|in|on|at|by|for|from|with|before|after|near|may|is|are|not|no|and|or)\b/i.test(m[2])
          && !/[=+,;:]/.test(m[2])) out.push(m[2].trim());
    }
    const tags = q.tags || [];
    if ((tags.includes('streak') || tags.includes('color')) && /\bto\b/.test(a) && words(a) <= 6) {
      for (const part of a.replace(/\([^)]*\)/g, '').split(/\s+to\s+/)) if (words(part) <= 3) out.push(part.trim());
    }
  }
  return [...new Set(out.filter(x => x.replace(/[^a-z]/gi, '').length >= 3))];
}

// a typed question stays in play only if some accepted answer is a short term (3 words or fewer)
function hasShortAnswer(q) {
  return [q.answer, ...(q.accept || [])].some(a => typeof a === 'string' && words(a) <= 3) || shortForms(q).length > 0;
}

module.exports = { shortForms, hasShortAnswer, words };
