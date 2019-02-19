from common import *

from apps.onegram.get_public_key import _get_public_key, _public_key_to_wif
from trezor.crypto import bip32, bip39
from ubinascii import hexlify, unhexlify


class TestEosGetPublicKey(unittest.TestCase):
    def test_get_public_key_scheme(self):
        mnemonic = "one one one one one one one one one one one onegram"
        seed = bip39.seed(mnemonic, '')

        derivation_paths = [
            [0x80000000 | 44, 0x80000000 | 204, 0x80000000, 0, 0],
            [0x80000000 | 44, 0x80000000 | 204, 0x80000000, 0, 1],
            [0x80000000 | 44, 0x80000000 | 204],
            [0x80000000 | 44, 0x80000000 | 204, 0x80000000, 0, 0x80000000],
        ]

        public_keys = [
            b'0281c89a0ae5ec0b25426fac4739687202491ec67470cf45b50466794488dff356',
            b'031d3459058196b93c1a4816f09de7798043af0e42b64379d5d5b9fa2bd1c926b3',
            b'030307f8bd7a9bccb376087e3ecf332cce77ed27e82b2c6710b5c8494d205acc93',
            b'027e57796bc3f2af650d8f17366380eb72b4fcb2ba810105906851878768bb9364',
        ]

        wif_keys = [
            'OGC5seW3PZW6xkcYZWLT3ygRhet2eQq8JX9bXEeJGjQEaHjgv2U8y',
            'OGC746X5TRVyJGPG6J5kHx4G13VMKQAdoDfqbyfkjFRVoL2k8EvxV',
            'OGC6rZxRharERsdS11qNqwJZNMaFLmjLWAZNYJvLgiRsRHf3JQ8pi',
            'OGC5r8akV2oRfmfwCvhZMLsnGPqyL6gDAK6W24gKe6cghBk18s4d9',
        ]

        for index, path in enumerate(derivation_paths):
            node = bip32.from_seed(seed, 'secp256k1')
            node.derive_path(path)
            wif, public_key = _get_public_key(node)

            self.assertEqual(hexlify(public_key), public_keys[index])
            self.assertEqual(wif, wif_keys[index])
            self.assertEqual(_public_key_to_wif(public_key), wif_keys[index])


if __name__ == '__main__':
    unittest.main()