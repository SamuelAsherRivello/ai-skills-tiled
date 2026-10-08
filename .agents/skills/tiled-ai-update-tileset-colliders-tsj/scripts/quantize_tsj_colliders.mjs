import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const args = process.argv.slice(2);
const write = args.includes("--write");
const pathArg = args.find((arg) => arg !== "--write");

if (!pathArg) {
  throw new Error("Usage: node quantize_tsj_colliders.mjs <tileset.tsj> [--write]");
}

const path = resolve(pathArg);
const source = await readFile(path, "utf8");
const tileset = JSON.parse(source);
const width = tileset.tilewidth;
const height = tileset.tileheight;

if (width !== 64 || height !== 64) {
  throw new Error(`Unsupported ${width}x${height} grid: confirm an edge thickness before continuing`);
}

const edge = 4;
const changed = new Set();
const removed = [];
const canonical = new Set();

function geometry(object) {
  return JSON.stringify({
    height: object.height,
    polygon: object.polygon,
    width: object.width,
    x: object.x,
    y: object.y,
  });
}

function snap(value, maximum, tileId, objectId) {
  const target = Math.abs(value) <= Math.abs(value - maximum) ? 0 : maximum;
  if (Math.abs(value - target) > 4) {
    throw new Error(`Ambiguous polygon vertex on tile ${tileId}, object ${objectId}: ${value}`);
  }
  return target;
}

for (const tile of tileset.tiles ?? []) {
  const objects = tile.objectgroup?.objects;
  if (!objects?.length) continue;

  const retained = [];
  for (const object of objects) {
    const before = geometry(object);

    if (object.polygon) {
      const vertices = object.polygon.map((point) => ({
        x: snap(object.x + point.x, width, tile.id, object.id),
        y: snap(object.y + point.y, height, tile.id, object.id),
      }));
      if (vertices.length !== 3 || new Set(vertices.map(({ x, y }) => `${x},${y}`)).size !== 3) {
        throw new Error(`Ambiguous polygon on tile ${tile.id}, object ${object.id}`);
      }
      object.x = 0;
      object.y = 0;
      object.polygon = vertices;
    } else if (object.width === 0 || object.height === 0) {
      removed.push(`${tile.id}:${object.id}`);
      changed.add(tile.id);
      continue;
    } else if (object.width > width / 2 && object.height > height / 2) {
      Object.assign(object, { x: 0, y: 0, width, height });
    } else if (object.width > width / 2 && object.height <= height / 2) {
      const top = object.y + object.height / 2 < height / 2;
      Object.assign(object, { x: 0, y: top ? 0 : height - edge, width, height: edge });
    } else if (object.height > height / 2 && object.width <= width / 2) {
      const left = object.x + object.width / 2 < width / 2;
      Object.assign(object, { x: left ? 0 : width - edge, y: 0, width: edge, height });
    } else {
      throw new Error(`Ambiguous rectangle on tile ${tile.id}, object ${object.id}`);
    }

    retained.push(object);
    if (geometry(object) === before) canonical.add(tile.id);
    else changed.add(tile.id);
  }
  tile.objectgroup.objects = retained;
}

const report = {
  grid: `${width}x${height}`,
  edgeThickness: edge,
  changedTileIds: [...changed].sort((a, b) => a - b),
  removedObjects: removed,
  alreadyCanonicalTileIds: [...canonical].filter((id) => !changed.has(id)).sort((a, b) => a - b),
};

if (write) {
  await writeFile(path, `${JSON.stringify(tileset, null, 2)}\n`, "utf8");
}

console.log(JSON.stringify(report, null, 2));
