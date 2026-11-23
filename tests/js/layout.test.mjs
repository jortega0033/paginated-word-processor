import test from "node:test";
import assert from "node:assert/strict";

test("layout planner module loads", async () => {
  const mod = await import("../../word_processor/static/layout.mjs");
  assert.equal(typeof mod, "object");
});
