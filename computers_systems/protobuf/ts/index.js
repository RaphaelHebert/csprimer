//  function to change a number in base 10 to a number in base 2 (binary)
function baseTenToBinary(n) {
    var res = 0;
    // check if n is >= 0 and 64 bits max
    if (n < 0 || n > 18446744073709551615) {
        throw new Error("n must be >= 0 and <= 18446744073709551615");
    }
    res = parseInt(n.toString(2));
    return res;
}
function binaryToBaseTen(n) {
    // !!!! parseInt handle 32 bits integers maximum !!!!!
    return parseInt("".concat(n), 2);
}
var x = baseTenToBinary(16);
console.log(x);
