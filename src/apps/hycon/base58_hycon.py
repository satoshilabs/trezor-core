from ubinascii import unhexlify
from trezor.crypto import hashlib

def blake2b_hash(ob):
    if type(ob) == str:
        ob = unhexlify(ob)
    blake2b_obj = hashlib.blake2b(outlen=32)
    blake2b_obj.update(ob)
    return blake2b_obj.digest()