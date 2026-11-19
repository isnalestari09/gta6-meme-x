// GTA 6 meme on X — make.fun bounty entry gta6-meme-x-01 (Node 22, stdlib only).
//
// This program does exactly one thing: it copies POST.json from the
// repository root to /output/POST.json, where the gate reads the address of
// the X post that is the entry. The post itself is what gets judged: the
// house reads the post from X (its first picture and its text) and hands
// that to the judge. Nothing this program writes about the post is judged.
//
// Local preview, outside the grader's container:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

// Read the post address first so a malformed POST.json fails loudly
// instead of being copied through silently.
let postUrl: string;
try {
  const parsed = JSON.parse(readFileSync(source, "utf8")) as { url?: unknown };
  if (typeof parsed.url !== "string" || !/^https?:\/\//.test(parsed.url)) {
    throw new Error("POST.json has no url string");
  }
  postUrl = parsed.url;
} catch (err) {
  console.error(`POST.json could not be read from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}

try {
  copyFileSync(source, target);
  console.log(`copied ${source} -> ${target} (${postUrl})`);
} catch (err) {
  console.error(`could not copy POST.json from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}
