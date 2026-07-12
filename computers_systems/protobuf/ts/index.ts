//  function to change a number in base 10 to a number in base 2 (binary)

function unsignedBaseTenToBinary(n: number) {
  let res = "0";
  // check if n is >= 0 and safe for JS number (https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)
  if (n < 0 || n > Number.MAX_SAFE_INTEGER) {
    throw new Error("n must be >= 0 and <= 18446744073709551615");
  }
  // à la mano
  let remainder = 0;
  let leftover = n;
  while (leftover >= 1) {
    remainder = leftover % 2;
    leftover -= remainder; // make it pair
    leftover = leftover / 2;
    res = leftover === 0.5 ? 1 + res : remainder + res;
  }
  res = res.slice(0, res.length - 1);
  return res;
}

function unsignedBinaryToBaseTen(n: string): number {
  //check that n is a binary number
  if (!/^[01]+$/.test(`${n}`)) {
    throw new Error("n must be a binary number");
  }

  let res: number = 0;
  for (let i = 0; i <= `${n}`.length; i++) {
    if (`${n}`[i] === "1") {
      res += Math.pow(2, `${n}`.length - 1 - i);
    }
  }
  return res;
}

export { unsignedBaseTenToBinary, unsignedBinaryToBaseTen };
