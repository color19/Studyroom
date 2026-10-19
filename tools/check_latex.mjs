// Check that every LaTeX formula in a cards.json renders in KaTeX.
//   npm install katex@0.16.11   (once, anywhere)
//   node tools/check_latex.mjs my/cards.json
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const katex = require('katex');
const cards = JSON.parse(readFileSync(process.argv[2], 'utf8'));
let bad = 0, n = 0;
for (const [key, c] of Object.entries(cards)) {
  for (const s of (c.ftex || c.formulas_latex || c.f || [])) {
    n++;
    try { katex.renderToString(s, { displayMode: true, throwOnError: true, strict: 'ignore' }); }
    catch (e) { bad++; console.log(key, '|', s, '|', e.message.slice(0, 90)); }
  }
}
console.log(`${n} formulas, bad ${bad}`);
process.exit(bad ? 1 : 0);
