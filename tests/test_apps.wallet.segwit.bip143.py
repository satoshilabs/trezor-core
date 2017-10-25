from common import *

from trezor.messages.TxAck import TxAck

from apps.wallet.sign_tx.segwit_bip143 import *
from trezor.crypto import bip32, bip39


class TestSegwitBip143(unittest.TestCase):
    # pylint: disable=C0301

    tx = SignTx(coin_name='Bitcoin', version=1, lock_time=0x00000492, inputs_count=1, outputs_count=2)
    inp1 = TxInputType(address_n=[0],
                       prev_hash=unhexlify('db6b1b20aa0fd7b23880be2ecbd4a98130974cf4748fb66092ac4d3ceb1a5477'),
                       prev_index=1,
                       amount=1000000000,  # 10 btc
                       script_type=None,
                       sequence=0xfffffffe)
    out1 = TxOutputType(address='1Fyxts6r24DpEieygQiNnWxUdb18ANa5p7',
                        amount=0x000000000bebb4b8,
                        script_type=OutputScriptType.PAYTOWITNESS,
                        address_n=None)
    out2 = TxOutputType(address='1Q5YjKVj5yQWHBBsyEBamkfph3cA6G9KK8',
                        amount=0x000000002faf0800,
                        script_type=OutputScriptType.PAYTOWITNESS,
                        address_n=None)

    def test_bip143_inputs(self):
        func = bip143_process_inputs(self.tx)

        func.send(None)
        try:
            func.send(TxAck(tx=TransactionType(inputs=[self.inp1])))
        except StopIteration as e:
            self.assertEqual(hexlify(e.value[0]), b'db6b1b20aa0fd7b23880be2ecbd4a98130974cf4748fb66092ac4d3ceb1a547701000000')
            self.assertEqual(hexlify(e.value[1]), b'b0287b4a252ac05af83d2dcef00ba313af78a3e9c329afa216eb3aa2a7b4613a')
            self.assertEqual(hexlify(e.value[2]), b'18606b350cd8bf565266bc352f0caddcf01e8fa789dd8a15386327cf8cabe198')
        else:
            raise AssertionError


    def test_bip143_outputs(self):

        seed = bip39.seed('alcohol woman abuse must during monitor noble actual mixed trade anger aisle', '')
        root = bip32.from_seed(seed, 'secp256k1')
        coin = coins.by_name(self.tx.coin_name)
        func = bip143_outputs(self.tx, coin, root)

        func.send(None)
        func.send(TxAck(tx=TransactionType(outputs=[self.out1])))
        try:
            func.send(TxAck(tx=TransactionType(outputs=[self.out2])))
        except StopIteration as e:
            self.assertEqual(hexlify(e.value), b'de984f44532e2173ca0d64314fcefe6d30da6f8cf27bafa706da61df8a226c83')  # todo better?
        else:
            raise AssertionError


    def test_bip143_preimage(self):

        seed = bip39.seed('alcohol woman abuse must during monitor noble actual mixed trade anger aisle', '')
        root = bip32.from_seed(seed, 'secp256k1')
        func = bip143_preimage(self.tx, root)

        func.send(None)
        func.send(TxAck(tx=TransactionType(inputs=[self.inp1])))  # for bip143_process_inputs
        func.send(TxAck(tx=TransactionType(inputs=[self.inp1])))  # for bip143_preimage main loop
        func.send(TxAck(tx=TransactionType(outputs=[self.out1])))  # for bip143_outputs
        try:
            func.send(TxAck(tx=TransactionType(outputs=[self.out2])))
        except StopIteration as e:
            # this hash does not correspond to the BIP 143 testing data
            # the pubKey can't be mocked and therefore the scriptCode is different
            self.assertEqual(hexlify(e.value), b'6e28aca7041720995d4acf59bbda64eef5d6f23723d23f2e994757546674bbd9')
        else:
            raise AssertionError




if __name__ == '__main__':
    unittest.main()
