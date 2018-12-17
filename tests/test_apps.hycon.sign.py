from common import *
from apps.hycon.base58_hycon import blake2b_hash
from apps.hycon.helpers import hycon_from_string, hycon_to_string, address_to_byte_array
from apps.hycon.sign_tx import sign
from trezor.messages.HyconSignTx import HyconSignTx
from apps.hycon.serialize import serialize

class TestHyconSign(unittest.TestCase):
    def test_hycon_from_string(self):
        amount1 = hycon_from_string("1000000000000.000001")
        self.assertEqual(amount1, 1000000000000000001000)
        self.assertEqual(hycon_to_string(1000000000000000001000), "1000000000000.000001")
        amount2 = hycon_from_string("7000000000000.123456789")
        self.assertEqual(amount2, 7000000000000123456789)
        result = amount1 + amount2
        self.assertEqual(result, 8000000000000123457789)
        self.assertEqual(hycon_to_string(result), "8000000000000.123457789")

    def test_sign(self):
        private_key = unhexlify("e09167abb9327bb3748e5dd1b9d3d40832b33eb0b041deeee8e44ff47030a61d")
        digest = unhexlify("c3f92350f0baf80f2fa41f9e6bb3287e1802808b9fa7464cf2beb463b9b05626")
        result = sign(digest, private_key)

        self.assertEqual(result[1], 1)
        self.assertEqual(result[0], unhexlify("fd67de0827ccf8bc957eeb185ba0ea78aa1cd5cad74aea40244361ee7df68e36025aebc4ae6b18628135ea3ef5a70ea3681a7082c44af0899f0f59b50f2707b9"))

    def test_encode_tx(self):
        tx = HyconSignTx("H3N2sCstx81NvvVy3hkrhGsNS43834YWw", "H497fHm8gbPZxaXySKpV17a7beYBF9Ut3", "0.000000001", "0.000000001", 1024)
        result = serialize(tx, "H3N2sCstx81NvvVy3hkrhGsNS43834YWw")

        self.assertEqual(result, unhexlify("0a14a9961e18748b1b76e3ebfaef491cef3ab2d5bb081214e161124d4aa41ca0df6bafecb0408971cff6c0961801200128800852056879636f6e"))


if __name__ == "__main__":
    unittest.main()
