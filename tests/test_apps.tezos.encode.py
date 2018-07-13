from common import *
from ubinascii import unhexlify
from apps.tezos.sign_tx import _encode_zarith, _encode_data_with_bool_prefix


class TestTezosEncoding(unittest.TestCase):

    def test_tezos_encode_zarith(self):
        inputs = [2000000, 159066, 200, 60000, 157000000, 0]
        outputs = ["80897a", "dada09", "c801", "e0d403", "c0c2ee4a", "00"]

        for i, o in zip(inputs, outputs):
            self.assertEqual(_encode_zarith(i), unhexlify(o))

    def test_tezos_encode_data_with_bool_prefix(self):
        self.assertEqual(_encode_data_with_bool_prefix(None), bytes([0]))

        data = "afffeb1dc3c0"
        self.assertEqual(_encode_data_with_bool_prefix(unhexlify(data)),
                         unhexlify("ff" + data))


if __name__ == '__main__':
    unittest.main()
