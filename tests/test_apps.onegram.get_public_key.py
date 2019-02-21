from common import *

from apps.onegram.get_public_key import _get_public_key, _public_key_to_wif
from trezor.crypto import bip32, bip39
from ubinascii import hexlify, unhexlify


class TestEosGetPublicKey(unittest.TestCase):
    def test_get_public_key_scheme(self):
        mnemonic = "all all all all all all all all all all all all"
        seed = bip39.seed(mnemonic, '')

        derivation_paths = [
            [0x80000000 | 44, 0x80000000 | 204, 0x80000000, 0, 0],
            [0x80000000 | 44, 0x80000000 | 204, 0x80000000, 0, 1],
            [0x80000000 | 44, 0x80000000 | 204],
            [0x80000000 | 44, 0x80000000 | 204, 0x80000000, 0, 0x80000000],
        ]

        public_keys = [
            b'034313262d3882c7de129afa9ff1639c9ff9881e2d54b444d1ad8f6e6291b3e13f',
            b'0300bf07cdebdf37f25263697fab99070f5dc30bab13a830d243d37dab115a3427',
            b'03af47021b410f1bc96f4cc98f776bf5360171b916aeb464c857bd68d6fceabd78',
            b'02cd8354b2eb5b75f1c5d4f0f0da85f409701474b1aa93b7b5f1685d5be6b6b671',
        ]

        wif_keys = [
            'OGC7LmsAtnUHdXsXbpZ7NnYNAsHS8LUn5wGbosiG7FEt52991efr6',
            'OGC6qZbEZyRxQLkcZvZWwXh2ULirVWcxMtHro2mRpWShZCk5XLmcn',
            'OGC8ARkmKjvefMcVmGCgDpb1ux72DaJPEjuQVXuvixgkurodNkvZ1',
            'OGC6SzubhMkRakxS2TBX9Wrd13N9dSWf8VE1W7zS1WUii9DoLDwYr',
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