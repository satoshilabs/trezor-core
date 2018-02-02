
def message_digest(message):
    from apps.wallet.sign_tx.signing import write_varint
    from trezor.crypto.hashlib import sha3_256
    from apps.common.hash_writer import HashWriter

    h = HashWriter(sha3_256)
    signed_message_header = 'Ethereum Signed Message:\n'
    write_varint(h, len(signed_message_header))
    h.extend(signed_message_header)
    write_varint(h, len(message))
    h.extend(message)

    return h.get_digest(True)


async def ethereum_sign_message(ctx, msg):
    from trezor.messages.EthereumMessageSignature import EthereumMessageSignature
    from trezor.crypto.curve import secp256k1
    from ..common import seed

    address_n = msg.address_n or ()
    node = await seed.get_root(ctx)
    node.derive_path(address_n)

    signature = secp256k1.sign(node.private_key(), message_digest(msg.message), False)

    sig = EthereumMessageSignature()
    sig.address = node.ethereum_pubkeyhash()
    sig.signature = signature[1:] + bytearray([signature[0]])
    return sig
