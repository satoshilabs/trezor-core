from common import *
from apps.ethereum.get_address import _ethereum_address_hex


class TestEthereumGetAddress(unittest.TestCase):

    def test_ethereum_address_hex_eip55(self):
        # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md
        eip55 = [
            '0x52908400098527886E0F7030069857D2E4169EE7',
            '0x8617E340B3D01FA5F11F306F4090FD50E238070D',
            '0xde709f2102306220921060314715629080e2fb77',
            '0x27b1fdb04752bbc536007a920d24acb045561c26',
            '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed',
            '0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359',
            '0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB',
            '0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb',
        ]
        for s in eip55:
            s = s[2:]
            b = bytes([int(s[i:i + 2], 16) for i in range(0, len(s), 2)])
            h = _ethereum_address_hex(b)
            self.assertEqual(h, '0x' + s)


    def test_ethereum_address_hex_rskip60(self):
        # https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP60.md
        rskip60_chain_30 = [
            '0x5AaEb6053f3e94C9B9A09f33669435e7Ef1BeaeD',
            '0xFb6916095ca1dF60BB79Ce92cE3EA74C37C5D359',
            '0xdbf03b407C01e7cd3CbEA99509D93F8Dddc8c6fB',
            '0xD1220A0cF47C7B9bE7a2E6ba89F429762e7b9aDB'
        ]
        eip55 = [
            '0x52908400098527886E0F7030069857D2E4169EE7',
            '0x8617E340B3D01FA5F11F306F4090FD50E238070D',
            '0xde709f2102306220921060314715629080e2fb77',
            '0x27b1fdb04752bbc536007a920d24acb045561c26',
            '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed',
            '0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359',
            '0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB',
            '0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb',
        ]
        for s in rskip60_chain_30:
            s = s[2:]
            b = bytes([int(s[i:i + 2], 16) for i in range(0, len(s), 2)])
            h = _ethereum_address_hex(b, 30)
            self.assertEqual(h, '0x' + s)
        for s in rskip60_chain_30:
            s = s[2:]
            b = bytes([int(s[i:i + 2], 16) for i in range(0, len(s), 2)])
            h = _ethereum_address_hex(b, 30, True)
            self.assertEqual(h, '0x' + s)
        for s in eip55:
            s = s[2:]
            b = bytes([int(s[i:i + 2], 16) for i in range(0, len(s), 2)])
            h = _ethereum_address_hex(b, 1)
            self.assertEqual(h, '0x' + s)


if __name__ == '__main__':
    unittest.main()
