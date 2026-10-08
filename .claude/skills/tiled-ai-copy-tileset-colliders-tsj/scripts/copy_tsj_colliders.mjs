import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";

function argument(name) {
  const index = process.argv.indexOf(`--${name}`);
  if (index === -1 || !process.argv[index + 1] || process.argv[index + 1].startsWith("--")) {
    throw new Error(`Missing required --${name} <tileset.tsj> argument`);
  }
  return resolve(process.argv[index + 1]);
}

function pngDimensions(buffer, path) {
  const signature = "89504e470d0a1a0a";
  if (buffer.subarray(0, 8).toString("hex") !== signature || buffer.subarray(12, 16).toString("ascii") !== "IHDR") {
    throw new Error(`Referenced image is not a supported PNG: ${path}`);
  }
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}

function tileMap(tileset) {
  return new Map((tileset.tiles ?? []).map((tile) => [tile.id, tile]));
}

const fromPath = argument("from");
const toPath = argument("to");
const write = process.argv.includes("--write");

if (fromPath === toPath) throw new Error("--from and --to must identify different tilesets");

const [fromSource, toSource] = await Promise.all([
  readFile(fromPath, "utf8"),
  readFile(toPath, "utf8"),
]);
const from = JSON.parse(fromSource);
const to = JSON.parse(toSource);

for (const field of ["tilewidth", "tileheight", "tilecount", "columns", "margin", "spacing", "imagewidth", "imageheight"]) {
  if (from[field] !== to[field]) {
    throw new Error(`Tilesets are not 1:1: ${field} differs (${from[field]} versus ${to[field]})`);
  }
}

for (const [tileset, tsjPath] of [[from, fromPath], [to, toPath]]) {
  if (!tileset.image) throw new Error(`Tileset has no image reference: ${tsjPath}`);
  const imagePath = resolve(dirname(tsjPath), tileset.image);
  const actual = pngDimensions(await readFile(imagePath), imagePath);
  if (actual.width !== tileset.imagewidth || actual.height !== tileset.imageheight) {
    throw new Error(`Declared and actual PNG dimensions differ for ${imagePath}`);
  }
}

const sourceTiles = tileMap(from);
const destinationTiles = tileMap(to);
const sourceColliderIds = [];
const replacedColliderIds = [];
const removedColliderIds = [];

for (let id = 0; id < from.tilecount; id += 1) {
  const sourceGroup = sourceTiles.get(id)?.objectgroup;
  const destinationGroup = destinationTiles.get(id)?.objectgroup;

  if (sourceGroup) {
    sourceColliderIds.push(id);
    if (destinationGroup) replacedColliderIds.push(id);
    const tile = destinationTiles.get(id) ?? { id };
    tile.objectgroup = structuredClone(sourceGroup);
    destinationTiles.set(id, tile);
  } else if (destinationGroup) {
    removedColliderIds.push(id);
    delete destinationTiles.get(id).objectgroup;
  }
}

to.tiles = [...destinationTiles.values()].sort((a, b) => a.id - b.id);
if (to.tiles.length === 0) delete to.tiles;

const report = {
  from: fromPath,
  to: toPath,
  grid: `${from.columns} columns, ${from.tilecount} tiles, ${from.tilewidth}x${from.tileheight}`,
  sourceColliderIds,
  replacedColliderIds,
  removedColliderIds,
  write,
};

if (write) {
  await writeFile(toPath, `${JSON.stringify(to, null, 2)}\n`, "utf8");
  const saved = JSON.parse(await readFile(toPath, "utf8"));
  const savedTiles = tileMap(saved);
  for (let id = 0; id < from.tilecount; id += 1) {
    const expected = sourceTiles.get(id)?.objectgroup;
    const actual = savedTiles.get(id)?.objectgroup;
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      throw new Error(`Saved collider mismatch at local tile ID ${id}`);
    }
  }
}

console.log(JSON.stringify(report, null, 2));
