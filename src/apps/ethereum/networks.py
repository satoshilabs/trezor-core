suffixes = {
    1: 'ETH',    # Ethereum Mainnet
    2: 'EXP',    # Expanse
    3: 'tETH',   # Ethereum Testnet: Ropsten
    4: 'tETH',   # Ethereum Testnet: Rinkeby
    8: 'UBQ',    # UBIQ
    30: 'RSK',   # Rootstock Mainnet
    31: 'tRSK',  # Rootstock Testnet
    42: 'tETH',  # Ethereum Testnet: Kovan
    61: 'ETC',   # Ethereum Classic Mainnet
    62: 'tETC',  # Ethereum Classic Testnet
}


def suffix_by_chain_id(chain_id, tx_type=None):
    if tx_type==bytearray(b'\x01') and chain_id==1:
        return"WAN"
    else:
        return suffixes.get(chain_id, 'UNKN')
