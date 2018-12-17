from common import *
from apps.common.paths import HARDENED
from trezor.crypto import base58
from apps.hycon.base58_hycon import blake2b_hash
from apps.hycon.helpers import address_from_public_key, validate_full_path, address_to_byte_array, address_to_string, hycon_from_string, hycon_to_string


class TestHyconAddress(unittest.TestCase):

    def test_base58_decode(self):
        arr = base58.decode('wTsQGpbicAZsXcmSHN8XmcNR9wX')
        self.assertEqual(arr, unhexlify('4366e2a531a891233fd59cfa5f062a0f1018af6a'))

    def test_base58_encode(self):
        result = base58.encode(unhexlify('4366e2a531a891233fd59cfa5f062a0f1018af6a'))
        self.assertEqual(result, 'wTsQGpbicAZsXcmSHN8XmcNR9wX')

    def test_base58_blake2b_byte(self):
        result = blake2b_hash(unhexlify('02c4199d83e47650b854e027188eade5378d19c94c13b226f43310fb144bc224af'))
        self.assertEqual(result, unhexlify('dafec57d0062e2317f6d0f294366e2a531a891233fd59cfa5f062a0f1018af6a'))

    def test_base58_blake2b_string(self):
        result = blake2b_hash('02c4199d83e47650b854e027188eade5378d19c94c13b226f43310fb144bc224af')
        self.assertEqual(result, unhexlify('dafec57d0062e2317f6d0f294366e2a531a891233fd59cfa5f062a0f1018af6a'))

    def test_address_to_byte_array(self):
        addr = address_to_byte_array('HwTsQGpbicAZsXcmSHN8XmcNR9wXHtw7')
        self.assertEqual(addr, unhexlify('4366e2a531a891233fd59cfa5f062a0f1018af6a'))

    def test_address_from_public_key(self):
        addr = address_from_public_key(unhexlify('02c4199d83e47650b854e027188eade5378d19c94c13b226f43310fb144bc224af'))
        self.assertEqual(addr, unhexlify('4366e2a531a891233fd59cfa5f062a0f1018af6a'))

    def test_address_to_string(self):
        address = address_to_string(unhexlify('4366e2a531a891233fd59cfa5f062a0f1018af6a'))
        self.assertEqual(address, 'HwTsQGpbicAZsXcmSHN8XmcNR9wXHtw7')

    def test_paths(self):
        # 44'/1397'/a'/0/0 is correct
        incorrect_paths = [
            [44 | HARDENED],
            [44 | HARDENED, 1397 | HARDENED],
            [44 | HARDENED, 1397 | HARDENED, 0],
            [44 | HARDENED, 1397 | HARDENED, 0 | HARDENED, 0 | HARDENED],
            [44 | HARDENED, 1397 | HARDENED, 0 | HARDENED, 0 | HARDENED, 0 | HARDENED],
            [44 | HARDENED, 1397 | HARDENED, 0 | HARDENED, 1, 0],
            [44 | HARDENED, 1397 | HARDENED, 0 | HARDENED, 0, 5],
            [44 | HARDENED, 1397 | HARDENED, 9999 | HARDENED],
            [44 | HARDENED, 1397 | HARDENED, 9999000 | HARDENED, 0, 0],
            [44 | HARDENED, 60 | HARDENED, 0 | HARDENED, 0, 0],
            [1 | HARDENED, 1 | HARDENED, 1 | HARDENED],
        ]
        correct_paths = [
            [44 | HARDENED, 1397 | HARDENED, 0 | HARDENED, 0, 0],
            [44 | HARDENED, 1397 | HARDENED, 3 | HARDENED, 0, 0],
            [44 | HARDENED, 1397 | HARDENED, 9 | HARDENED, 0, 0],
        ]

        for path in incorrect_paths:
            self.assertFalse(validate_full_path(path))

        for path in correct_paths:
            self.assertTrue(validate_full_path(path))




if __name__ == '__main__':
    unittest.main()
