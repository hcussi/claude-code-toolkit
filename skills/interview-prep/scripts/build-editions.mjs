#!/usr/bin/env node
// Build the two interview-prep HTML editions (tracker + reading) from a content
// model, by injecting it into the bundled templates. No dependencies.
//
// Usage:
//   node build-editions.mjs <content.json> [outDir]
//
// content.json shape:
//   {
//     "meta": { "role": "...", "tagline": "...", "heroTitle": "...", "heroLead": "..." },
//     "categories": [
//       { "id": "oop", "name": "OOP & SOLID", "sub": "one line",
//         "blocks": [ { "h": "Heading", "html": "<ul>...</ul>" } ],
//         "qa": [ ["Question?", "Answer."] ] }
//     ]
//   }
//
// Writes <outDir>/tracker.html and <outDir>/reading.html.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const refs = resolve(here, "..", "references");

function die(msg) {
  console.error("build-editions: " + msg);
  process.exit(1);
}

const [, , contentArg, outArg] = process.argv;
if (!contentArg) die("missing <content.json> argument.\nUsage: node build-editions.mjs <content.json> [outDir]");

const contentPath = resolve(process.cwd(), contentArg);
const outDir = resolve(process.cwd(), outArg || ".");
mkdirSync(outDir, { recursive: true });

let content;
try {
  content = JSON.parse(readFileSync(contentPath, "utf8"));
} catch (e) {
  die("could not read/parse " + contentPath + ": " + e.message);
}

// ---- validate shape (friendly errors) ----
const meta = content.meta || {};
const categories = content.categories;
if (!Array.isArray(categories) || categories.length === 0) {
  die('"categories" must be a non-empty array.');
}
categories.forEach((c, i) => {
  if (!c.id) die(`category[${i}] is missing "id".`);
  if (!c.name) die(`category[${i}] (${c.id}) is missing "name".`);
  if (!Array.isArray(c.blocks) || c.blocks.length === 0) die(`category "${c.id}" needs a non-empty "blocks" array.`);
  c.blocks.forEach((b, j) => {
    if (!b.h) die(`category "${c.id}" block[${j}] is missing "h" (heading).`);
    if (typeof b.html !== "string" || !b.html.trim()) die(`category "${c.id}" block[${j}] is missing "html".`);
  });
  if (c.qa && !Array.isArray(c.qa)) die(`category "${c.id}" "qa" must be an array of [question, answer] pairs.`);
});

// ---- safe JSON embedding inside <script> ----
function embed(value) {
  return JSON.stringify(value)
    .replace(/<\/(script)/gi, "<\\/$1") // do not close the host <script>
    .replace(/\u2028/g, "\\u2028") // line/paragraph separators are invalid raw in JS source
    .replace(/\u2029/g, "\\u2029");
}

const DATA_JSON = embed(categories);
const META_JSON = embed(meta);

function build(templateFile, outFile) {
  let tpl;
  try {
    tpl = readFileSync(join(refs, templateFile), "utf8");
  } catch (e) {
    die("could not read template " + templateFile + ": " + e.message);
  }
  let out = tpl
    .replace("/*INTERVIEW_PREP_DATA*/ null", DATA_JSON)
    .replace("/*INTERVIEW_PREP_META*/ null", META_JSON);
  if (out.indexOf("/*INTERVIEW_PREP_DATA*/") !== -1) {
    die("data placeholder not found/replaced in " + templateFile + " (template may be corrupted).");
  }
  const dest = join(outDir, outFile);
  writeFileSync(dest, out);
  return dest;
}

const tracker = build("tracker-edition.template.html", "tracker.html");
const reading = build("reading-edition.template.html", "reading.html");

const totalBlocks = categories.reduce((n, c) => n + c.blocks.length, 0);
const totalQa = categories.reduce((n, c) => n + (c.qa ? c.qa.length : 0), 0);

console.log("Built interview-prep editions:");
console.log("  tracker : " + tracker);
console.log("  reading : " + reading);
console.log(`  content : ${categories.length} topics, ${totalBlocks} read-blocks, ${totalQa} Q&A`);
