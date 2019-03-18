from ubinascii import hexlify

from common import *
from trezor.messages.OnegramAsset import OnegramAsset

from apps.onegram import writers


class TestOnegramWriters(unittest.TestCase):

    def test_onegram_write_varint(self):
        w = bytearray()
        writers.write_varint(w, 0)
        self.assertEqual(hexlify(w), b"00")

        w = bytearray()
        writers.write_varint(w, 1085)
        self.assertEqual(hexlify(w), b"bd08")

    def test_onegram_write_asset(self):
        w = bytearray()
        writers.write_asset(w, OnegramAsset(amount=10000, asset_id="1.3.0"))
        self.assertEqual(hexlify(w), b"102700000000000000")


if __name__ == "__main__":
    unittest.main()
