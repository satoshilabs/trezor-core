from trezor.messages import EosAsset

from apps.common import HARDENED, paths


def eos_name_to_string(value) -> str:
    charmap = ".12345abcdefghijklmnopqrstuvwxyz"
    tmp = value
    string = ""
    actual_size = 13
    for i in range(0, 13):
        c = charmap[tmp & (0x0F if i == 0 else 0x1F)]
        string = c + string
        tmp >>= 4 if i == 0 else 5

    while actual_size != 0 and string[actual_size - 1] == ".":
        actual_size -= 1

    return string[:actual_size]


def eos_asset_to_string(asset: EosAsset) -> str:
    symbol_bytes = int.to_bytes(asset.symbol, 8, "big")
    precision = symbol_bytes[7]
    symbol = bytes(reversed(symbol_bytes[:7])).rstrip(b"\x00").decode("ascii")

    amount_digits = str(asset.amount)
    if precision > 0:
        integer, fraction = amount_digits[:-precision], amount_digits[-precision:]
    else:
        integer, fraction = amount_digits, ""

    return "%s.%s %s" % (integer, fraction, symbol)


def pack_variant32(value: int) -> str:
    out = bytearray()
    val = value
    while True:
        b = val & 0x7F
        val >>= 7
        b |= (val > 0) << 7
        out.append(b)

        if val == 0:
            break

    return bytes(out)


def validate_full_path(path: list) -> bool:
    """
    Validates derivation path to equal 44'/194'/a'/0/0,
    where `a` is an account index from 0 to 1 000 000.
    Similar to Ethereum this should be 44'/194'/a', but for
    compatibility with other HW vendors we use 44'/194'/a'/0/0.
    """
    if len(path) != 5:
        return False
    if path[0] != 44 | HARDENED:
        return False
    if path[1] != 194 | HARDENED:
        return False
    if path[2] < HARDENED or path[2] > 1000000 | HARDENED:
        return False
    if path[3] != 0:
        return False
    if path[4] != 0:
        return False
    return True
