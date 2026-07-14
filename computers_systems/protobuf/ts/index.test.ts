import { unsignedBinaryToBaseTen, unsignedBaseTenToBinary } from "./index.ts";
import { describe, expect, test } from "@jest/globals";

describe("encode: unsignedBaseTenToBinary", () => {
  test("should throw if unsigned", () => {
    expect(() => unsignedBaseTenToBinary(-1)).toThrow(
      "n must be >= 0 and <= 18446744073709551615",
    );
  });
  test("should throw if too big", () => {
    expect(() => unsignedBaseTenToBinary(Number.MAX_SAFE_INTEGER + 1)).toThrow(
      "n must be >= 0 and <= 18446744073709551615",
    );
  });
});
