from apps.common.display_address import show_address, show_qr
from apps.ethereum import networks


async def ethereum_get_address(ctx, msg):
    from trezor.messages.EthereumAddress import EthereumAddress
    from trezor.crypto.curve import secp256k1
    from trezor.crypto.hashlib import sha3_256
    from apps.common import seed

    address_n = msg.address_n or ()

    node = await seed.derive_node(ctx, address_n)

    seckey = node.private_key()
    public_key = secp256k1.publickey(seckey, False)  # uncompressed
    address = sha3_256(public_key[1:]).digest(True)[12:]  # Keccak

    if msg.show_display:
        network = networks.by_slip44(address_n[1] & 0x7fffffff)
        hex_addr = _ethereum_address_hex(address, network)

        while True:
            if await show_address(ctx, hex_addr):
                break
            if await show_qr(ctx, hex_addr):
                break

    return EthereumAddress(address=address)


def _ethereum_address_hex(address, network=None):
    from ubinascii import hexlify
    from trezor.crypto.hashlib import sha3_256

    rskip60 = network is not None and network.rskip60

    hx = hexlify(address).decode()

    prefix = str(network.chain_id) + '0x' if rskip60 else ''
    hs = sha3_256(prefix + hx).digest(True)
    h = ''

    for i in range(20):
        l = hx[i * 2]
        if hs[i] & 0x80 and l >= 'a' and l <= 'f':
            l = l.upper()
        h += l
        l = hx[i * 2 + 1]
        if hs[i] & 0x08 and l >= 'a' and l <= 'f':
            l = l.upper()
        h += l

    return '0x' + h
