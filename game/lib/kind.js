// Sort questions into 'reasoning' (can be worked out from principles: processes, scenarios, calculations,
// diagrams, deducing an ID from clues) and 'recall' (a bare fact: a formula, a streak, a name origin, an example).

// tags whose questions can be reasoned out
const REASON_TAGS = new Set([
  'scenario', 'calculation', 'phase diagram', 'eutectic', 'lever rule', 'Al2SiO5', 'P-T', 'geothermal gradient',
  'Bowen', 'Goldich', 'index minerals', 'facies', 'classification', 'modes', 'grain size', 'Hjulström', 'stream velocity',
  'sorting', 'rounding', 'maturity', 'energy', 'cooling', 'igneous texture', 'magma', 'magma evolution', 'rock cycle',
  'weathering', 'depositional environment', 'sedimentary structure', 'metamorphism type', 'plate setting', 'volcano',
  'mineral formation', 'thin section texture', 'incompatible element', 'distinguish', 'properties', 'description',
  'protolith', 'grade', 'equivalents', 'radiometric dating', 'fractional crystallization', 'viscosity', 'temperature', 'silica',
]);
// rankings that are reasoning (Bowen, index minerals, coal rank...) vs. recall (hardness/SG lists)
const RECALL_RANKING = new Set(['hardness', 'specific gravity']);
// authored questions in these sections are about processes rather than single facts
const PROCESS_TOPIC = /^(3h\.vi\.2|3h\.xi|3h\.ix|3h\.x|3i\.iv\.[3-6]|3i\.iv\.6b|3i\.v\.[3-6]|3i\.vi\.[5-8]|3i\.vii|3i\.ix)$/;
// trivia that stays recall even inside a concept topic
const TRIVIA = /\b(example of|famous example|classic example|named (for|after)|name come|comes from|birthstone|Nickel-Strunz|state (mineral|gem|rock)|etymology)\b/i;

function kind(q) {
  if (TRIVIA.test(q.prompt)) return 'recall';
  if (q.image) return 'recall';
  const tags = q.tags || [];
  if (tags.includes('ranking') && tags.some(t => RECALL_RANKING.has(t))) return 'recall';
  if (tags.includes('vocabulary') || tags.includes('select all')) return 'recall';
  if (tags.some(t => REASON_TAGS.has(t))) return 'reasoning';
  if (q.format === 'numeric') return 'reasoning';
  if (q.source === 'authored' && PROCESS_TOPIC.test(q.topic)) return 'reasoning';
  return 'recall';
}

module.exports = { kind };
