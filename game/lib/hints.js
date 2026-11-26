// Three progressively stronger hints for a prepared question. Hint 3 nearly gives the answer away,
// so nobody can be stuck on a question forever.

const LETTER = i => String.fromCharCode(65 + i);
const isLetter = ch => /[a-z0-9]/i.test(ch);

const { textHints, sentenceParts } = require('./hints_text');
const { check } = require('./check');

function numberHints(answer, unit) {
  const a = Number(answer);
  const u = unit ? ` ${unit}` : '';
  const round = x => +x.toPrecision(3);
  const span = f => [round(a - Math.abs(a) * f), round(a + Math.abs(a) * f)].sort((x, y) => x - y);
  const [l1, h1] = span(0.5), [l2, h2] = span(0.2), [l3, h3] = span(0.05);
  if (a === 0) return ['It is a small number', 'It is less than 1', 'It is 0'];
  return [`Between ${l1} and ${h1}${u}`, `Between ${l2} and ${h2}${u}`, `Between ${l3} and ${h3}${u}`];
}

function hintsFor(p) {
  switch (p.format) {
    case 'numeric':
      return numberHints(p.answer, p.unit);
    case 'tf':
      return [`Topic: ${p.topicName}`, p.explanation ? `Think about: ${p.explanation}` : 'Think about whether every part of the statement is true',
              `The statement is ${p.answer === 'True' ? 'true' : 'false'}`];
    case 'multi': {
      const right = p.answer.map(a => LETTER(p.options.indexOf(a)));
      const wrong = p.options.map((o, i) => LETTER(i)).filter(L => !right.includes(L));
      const ruledOut = wrong.slice(0, Math.max(1, wrong.length - 1));
      return [`${right.length} option${right.length === 1 ? ' is' : 's are'} correct`, `${right[0]} is one of them`,
              `${right[0]} is correct; ${ruledOut.join(', ')} ${ruledOut.length === 1 ? 'is' : 'are'} wrong`];
    }
    case 'order': {
      const seq = p.answer.map(a => LETTER(p.options.indexOf(a)));
      return [`Starts with ${seq[0]}`, `Starts with ${seq.slice(0, 2).join('')}`, `Starts with ${seq.slice(0, Math.max(3, seq.length - 1)).join('')}`];
    }
    default: {
      const ans = String(p.answer);
      if (/^-?\d+(\.\d+)?$/.test(ans.trim())) return numberHints(ans, null);
      const sp = sentenceParts(ans);
      if (!sp) return textHints(ans);
      // sentence answers are graded by key words, so ask the grader: hint 2 stops one word short of an accepted
      // answer, hint 3 is the first version the grader accepts
      const ok = t => check(p, t).status === 'correct';
      let n = 0;
      while (n < sp.key.length && !ok(sp.reveal(n + 1))) n++;
      return [sp.shape, sp.reveal(n), sp.reveal(Math.min(sp.key.length, n + 1))];
    }
  }
}

module.exports = { hintsFor };
