from micropython import const

from trezor.crypto import base58
from .base58_hycon import blake2b_hash
from ubinascii import hexlify

from apps.common import HARDENED

MIN_FEE = const(1)

def address_from_public_key(pubkey: bytes) -> bytes:
    hash_val = blake2b_hash(pubkey)
    address = bytearray(20)
    for i in range(12, 32):
        address[i - 12] = hash_val[i]

    return bytes(address)


def address_to_byte_array(address: str):
    if address[0] != 'H':
        raise Exception("Address is invalid. Expected address to start with \'H\'")
    check = address[-4:]
    address = address[1:-4]
    out = base58.decode(address)
    if len(out) != 20:
        raise Exception("Address must be 20 bytes long")
    expected_check_sum = address_checksum(out)
    if expected_check_sum != check:
        raise Exception("Address hash invalid checksum "+str(check)+" expected \'"+str(expected_check_sum)+"\'")
    return out

def address_checksum(arr):
    hash_val = blake2b_hash(arr)
    str_val = base58.encode(hash_val)
    str_val = str_val[:4]
    return str_val

def address_to_string(address: bytes) -> str:
    return 'H' + base58.encode(address) + address_checksum(address)


def validate_full_path(path: list) -> bool:
    if len(path) != 5:
        return False
    if path[0] != 44 | HARDENED:
        return False
    if path[1] != 1397 | HARDENED:
        return False
    if path[2] < HARDENED or path[2] > 1000000 | HARDENED:
        return False
    if path[3] != 0:
        return False
    if path[4] != 0:
        return False
    return True

def hycon_to_string(val: int):
    natural = int(val / 1000000000)
    sub_num = val % 1000000000
    if sub_num == 0:
        return str(natural)
    decimals = str(sub_num)
    while len(decimals) < 9:
        decimals = "0" + decimals

    while decimals[-1] == '0':
        decimals = decimals[:-1]

    return str(natural) + "." + decimals

def hycon_from_string(val):
    if val == "" or val is None:
        return 0
    if val[-1] == ".":
        val += "0"
    arr = val.split(".")
    hycon = int(arr[0])*pow(10, 9)
    if len(arr) > 1:
        if len(arr[1]) > 9:
            arr[1] = arr[1][:9]
        sub_hycon = int(arr[1]) * pow(10, 9 - len(arr[1]))
        hycon += sub_hycon
    return hycon

def bytes_to_hex_string(val: bytes) -> str:
    return hexlify(val).decode("utf-8")