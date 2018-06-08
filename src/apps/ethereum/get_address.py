from apps.wallet.get_address import _show_address, _show_qr


async def ethereum_get_address(ctx, msg):
    from trezor.messages.EthereumAddress import EthereumAddress
    from trezor.crypto.curve import secp256k1
    from trezor.crypto.hashlib import sha3_256
    from ..common import seed

    address_n = msg.address_n or ()

    node = await seed.derive_node(ctx, address_n)

    seckey = node.private_key()
    public_key = secp256k1.publickey(seckey, False)  # uncompressed
    address = sha3_256(public_key[1:]).digest(True)[12:]  # Keccak

    if msg.show_display:
        chain_id = decode_chain_id(address_n)

        hex_addr = _ethereum_address_hex(address, chain_id)
        while True:
            if await _show_address(ctx, hex_addr):
                break
            if await _show_qr(ctx, hex_addr):
                break

    return EthereumAddress(address=address)


''' <SLIP-44 coin ID, EIP-155 chain ID> '''
rksip60_applying_chains = {
    137: 30, # RSK MainNet
    37310: 31 # RSK TestNet
}


def decode_chain_id(dpath):
    slip44_network_id = dpath[1] - 2**31

    return rksip60_applying_chains.get(slip44_network_id, 0)


def _ethereum_address_hex(address, chain_id=None):
    from ubinascii import hexlify
    from trezor.crypto.hashlib import sha3_256

    applying_chain_ids = rksip60_applying_chains.values()

    hx = hexlify(address).decode()
    prefix = str(chain_id) + '0x' if (chain_id in applying_chain_ids) else ''
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
