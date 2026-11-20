// Entry point for news-image-20261119 (round 2).
// Copies the pre-rendered entry.png next to this file into /output/entry.png.
// Node 22, standard library only, no network, deterministic.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (${src})`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

const bytes = readFileSync(dst);
if (bytes.length === 0 || bytes.length > 1024 * 1024) {
  throw new Error(`entry.png size out of range: ${bytes.length} bytes`);
}
// PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (!PNG_MAGIC.every((b, i) => bytes[i] === b)) {
  throw new Error("entry.png does not start with the PNG signature");
}
console.log(`wrote ${dst} (${bytes.length} bytes)`);
