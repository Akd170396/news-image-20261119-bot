import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Copy the pre-rendered infographic into the harness output directory.
// The image is produced by render.py and lives next to this file.
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (${here})`);
}
mkdirSync("/output", { recursive: true });
copyFileSync(src, "/output/entry.png");
console.log(`copied entry.png (${statSync(src).size} bytes) to /output/entry.png`);
