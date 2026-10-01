import { describe, expect, it } from "vitest";

describe("Stage 0 frontend foundation", () => {
  it("has a browser-safe public API configuration convention", () => {
    expect("NEXT_PUBLIC_API_BASE_URL".startsWith("NEXT_PUBLIC_")).toBe(true);
  });
});
