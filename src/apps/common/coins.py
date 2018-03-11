from trezor.messages.CoinType import CoinType

# the following list is generated using tools/codegen/gen_coins.py
# do not edit manually!
COINS = [
    CoinType(
        coin_name='Bitcoin',
        coin_shortcut='BTC',
        coin_label='Bitcoin',
        address_type=0,
        address_type_p2sh=5,
        maxfee_kb=2000000,
        minfee_kb=1000,
        signed_message_header='Bitcoin Signed Message:\n',
        hash_genesis_block='000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix='bc',
        bip44=0,
        segwit=True,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Low': 10, 'Economy': 70, 'Normal': 140, 'High': 200},
        dust_limit=546,
        blocktime_minutes=10,
        firmware='stable',
        address_prefix='bitcoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://btc-bitcore3.trezor.io', 'https://btc-bitcore1.trezor.io'],
    ),
    CoinType(
        coin_name='Testnet',
        coin_shortcut='TEST',
        coin_label='Testnet',
        address_type=111,
        address_type_p2sh=196,
        maxfee_kb=10000000,
        minfee_kb=1000,
        signed_message_header='Bitcoin Signed Message:\n',
        hash_genesis_block='000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943',
        xprv_magic=0x04358394,
        xpub_magic=0x043587cf,
        bech32_prefix='tb',
        bip44=1,
        segwit=True,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=546,
        blocktime_minutes=10,
        firmware='stable',
        address_prefix='bitcoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://testnet-bitcore1.trezor.io', 'https://testnet-bitcore2.trezor.io'],
    ),
    CoinType(
        coin_name='Bcash',
        coin_shortcut='BCH',
        coin_label='Bitcoin Cash',
        address_type=0,
        address_type_p2sh=5,
        maxfee_kb=500000,
        minfee_kb=1000,
        signed_message_header='Bitcoin Signed Message:\n',
        hash_genesis_block='000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix=None,
        bip44=145,
        segwit=False,
        forkid=0,
        force_bip143=True,
        default_fee_b={'Low': 10, 'Economy': 70, 'Normal': 140, 'High': 200},
        dust_limit=546,
        blocktime_minutes=10,
        firmware='stable',
        address_prefix='bitcoincash:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://bch-bitcore2.trezor.io'],
    ),
    CoinType(
        coin_name='Bcash Testnet',
        coin_shortcut='TBCH',
        coin_label='Bitcoin Cash Testnet',
        address_type=111,
        address_type_p2sh=196,
        maxfee_kb=10000000,
        minfee_kb=1000,
        signed_message_header='Bitcoin Signed Message:\n',
        hash_genesis_block='000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943',
        xprv_magic=0x04358394,
        xpub_magic=0x043587cf,
        bech32_prefix=None,
        bip44=1,
        segwit=False,
        forkid=0,
        force_bip143=True,
        default_fee_b={'Normal': 10},
        dust_limit=546,
        blocktime_minutes=10,
        firmware='debug',
        address_prefix='bitcoincash:',
        min_address_length=27,
        max_address_length=34,
        bitcore=[],
    ),
    CoinType(
        coin_name='Namecoin',
        coin_shortcut='NMC',
        coin_label='Namecoin',
        address_type=52,
        address_type_p2sh=5,
        maxfee_kb=10000000,
        minfee_kb=1000,
        signed_message_header='Namecoin Signed Message:\n',
        hash_genesis_block='000000000062b72c5e2ceb45fbc8587e807c155b0da735e6483dfba2f0a9c770',
        xprv_magic=0x019d9cfe,
        xpub_magic=0x019da462,
        bech32_prefix=None,
        bip44=7,
        segwit=False,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=2940,
        blocktime_minutes=10,
        firmware='stable',
        address_prefix='namecoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=[],
    ),
    CoinType(
        coin_name='Litecoin',
        coin_shortcut='LTC',
        coin_label='Litecoin',
        address_type=48,
        address_type_p2sh=50,
        maxfee_kb=40000000,
        minfee_kb=100000,
        signed_message_header='Litecoin Signed Message:\n',
        hash_genesis_block='12a765e31ffd4059bada1e25190f6e98c99d9714d334efa41a195a7e7e04bfe2',
        xprv_magic=0x019d9cfe,
        xpub_magic=0x019da462,
        bech32_prefix='ltc',
        bip44=2,
        segwit=True,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 1000},
        dust_limit=54600,
        blocktime_minutes=2.5,
        firmware='stable',
        address_prefix='litecoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://ltc-bitcore3.trezor.io'],
    ),
    CoinType(
        coin_name='Viacoin',
        coin_shortcut='VIA',
        coin_label='Viacoin',
        address_type=71,
        address_type_p2sh=22,
        maxfee_kb=400000,
        minfee_kb=1000,
        signed_message_header='Viacoin Signed Message:\n',
        hash_genesis_block='4e9b54001f9976049830128ec0331515eaabe35a70970d79971da1539a400ba1',
        xprv_magic=0X0488ADE4,
        xpub_magic=0X0488B21E,
        bech32_prefix='via',
        bip44=14,
        segwit=True,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=546,
        blocktime_minutes=0.4,
        firmware='stable',
        address_prefix='viacoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://explorer.viacoin.org'],
    ),
    CoinType(
        coin_name='Dogecoin',
        coin_shortcut='DOGE',
        coin_label='Dogecoin',
        address_type=30,
        address_type_p2sh=22,
        maxfee_kb=1000000000,
        minfee_kb=1000,
        signed_message_header='Dogecoin Signed Message:\n',
        hash_genesis_block='1a91e3dace36e2be3bf030a65679fe821aa1d6ef92e7c9902eb318182c355691',
        xprv_magic=0x02fac398,
        xpub_magic=0x02facafd,
        bech32_prefix=None,
        bip44=3,
        segwit=False,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=10000000,
        blocktime_minutes=1,
        firmware='stable',
        address_prefix='dogecoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=[],
    ),
    CoinType(
        coin_name='Dash',
        coin_shortcut='DASH',
        coin_label='Dash',
        address_type=76,
        address_type_p2sh=16,
        maxfee_kb=100000,
        minfee_kb=10000,
        signed_message_header='DarkCoin Signed Message:\n',
        hash_genesis_block='00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6',
        xprv_magic=0x02fe52f8,
        xpub_magic=0x02fe52cc,
        bech32_prefix=None,
        bip44=5,
        segwit=False,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=5460,
        blocktime_minutes=2.5,
        firmware='stable',
        address_prefix='dash:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://dash-bitcore1.trezor.io', 'https://dash-bitcore3.trezor.io'],
    ),
    CoinType(
        coin_name='Zcash',
        coin_shortcut='ZEC',
        coin_label='Zcash',
        address_type=7352,
        address_type_p2sh=7357,
        maxfee_kb=1000000,
        minfee_kb=1000,
        signed_message_header='Zcash Signed Message:\n',
        hash_genesis_block='00040fe8ec8471911baa1db1266ea15dd06b4a8a5c453883c000b031973dce08',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix=None,
        bip44=133,
        segwit=False,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=546,
        blocktime_minutes=2.5,
        firmware='stable',
        address_prefix='zcash:',
        min_address_length=35,
        max_address_length=95,
        bitcore=['https://zec-bitcore1.trezor.io/'],
    ),
    CoinType(
        coin_name='Zcash Testnet',
        coin_shortcut='TAZ',
        coin_label='Zcash Testnet',
        address_type=7461,
        address_type_p2sh=7354,
        maxfee_kb=10000000,
        minfee_kb=1000,
        signed_message_header='Zcash Signed Message:\n',
        hash_genesis_block='05a60a92d99d85997cce3b87616c089f6124d7342af37106edc76126334a2c38',
        xprv_magic=0x04358394,
        xpub_magic=0x043587cf,
        bech32_prefix=None,
        bip44=1,
        segwit=False,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=546,
        blocktime_minutes=2.5,
        firmware='debug',
        address_prefix='zcash:',
        min_address_length=35,
        max_address_length=95,
        bitcore=[],
    ),
    CoinType(
        coin_name='Bitcoin Gold',
        coin_shortcut='BTG',
        coin_label='Bitcoin Gold',
        address_type=38,
        address_type_p2sh=23,
        maxfee_kb=500000,
        minfee_kb=1000,
        signed_message_header='Bitcoin Gold Signed Message:\n',
        hash_genesis_block='000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix='btg',
        bip44=156,
        segwit=True,
        forkid=79,
        force_bip143=True,
        default_fee_b={'Low': 10, 'Economy': 70, 'Normal': 140, 'High': 200},
        dust_limit=546,
        blocktime_minutes=10,
        firmware='stable',
        address_prefix='bitcoingold:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://btg-bitcore2.trezor.io'],
    ),
    CoinType(
        coin_name='DigiByte',
        coin_shortcut='DGB',
        coin_label='DigiByte',
        address_type=30,
        address_type_p2sh=5,
        maxfee_kb=500000,
        minfee_kb=1000,
        signed_message_header='DigiByte Signed Message:\n',
        hash_genesis_block='7497ea1b465eb39f1c8f507bc877078fe016d6fcb6dfad3a64c98dcc6e1e8496',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix='dgb',
        bip44=20,
        segwit=True,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Low': 10, 'Economy': 70, 'Normal': 140, 'High': 200},
        dust_limit=546,
        blocktime_minutes=0.25,
        firmware='stable',
        address_prefix='digibyte:',
        min_address_length=27,
        max_address_length=34,
        bitcore=[],
    ),
    CoinType(
        coin_name='Monacoin',
        coin_shortcut='MONA',
        coin_label='Monacoin',
        address_type=50,
        address_type_p2sh=55,
        maxfee_kb=5000000,
        minfee_kb=100000,
        signed_message_header='Monacoin Signed Message:\n',
        hash_genesis_block='ff9f1c0116d19de7c9963845e129f9ed1bfc0b376eb54fd7afa42e0d418c8bb6',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix='mona',
        bip44=22,
        segwit=True,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 100000},
        dust_limit=54600,
        blocktime_minutes=1.5,
        firmware='stable',
        address_prefix='monacoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['https://mona.chainsight.info'],
    ),
    CoinType(
        coin_name='Fujicoin',
        coin_shortcut='FJC',
        coin_label='Fujicoin',
        address_type=36,
        address_type_p2sh=16,
        maxfee_kb=1000000,
        minfee_kb=100000,
        signed_message_header='FujiCoin Signed Message:\n',
        hash_genesis_block='adb6d9cfd74075e7f91608add4bd2a2ea636f70856183086842667a1597714a0',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix=None,
        bip44=75,
        segwit=False,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 100000},
        dust_limit=100000,
        blocktime_minutes=1.0,
        firmware='stable',
        address_prefix='fujicoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=['http://explorer.fujicoin.org/'],
    ),
    CoinType(
        coin_name='Vertcoin',
        coin_shortcut='VTC',
        coin_label='Vertcoin',
        address_type=71,
        address_type_p2sh=5,
        maxfee_kb=40000000,
        minfee_kb=100000,
        signed_message_header='Vertcoin Signed Message:\n',
        hash_genesis_block='4d96a915f49d40b1e5c2844d1ee2dccb90013a990ccea12c492d22110489f0c4',
        xprv_magic=0x0488ade4,
        xpub_magic=0x0488b21e,
        bech32_prefix='vtc',
        bip44=28,
        segwit=True,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 1000},
        dust_limit=54600,
        blocktime_minutes=2.5,
        firmware='stable',
        address_prefix='vertcoin:',
        min_address_length=27,
        max_address_length=34,
        bitcore=[],
    ),
    CoinType(
        coin_name='Decred Testnet',
        coin_shortcut='TDCR',
        coin_label='Testnet',
        address_type=3873,
        address_type_p2sh=3836,
        maxfee_kb=10000000,
        minfee_kb=1000,
        signed_message_header='Decred Signed Message:\n',
        hash_genesis_block='4261602a9d07d80ad47621a64ba6a07754902e496777edc4ff581946bd7bc29c',
        xprv_magic=0x04358397,
        xpub_magic=0x043587d1,
        bech32_prefix=None,
        bip44=1,
        segwit=False,
        forkid=None,
        force_bip143=False,
        default_fee_b={'Normal': 10},
        dust_limit=546,
        blocktime_minutes=10,
        firmware='debug',
        address_prefix='bitcoin:',
        min_address_length=35,
        max_address_length=35,
        bitcore=[],
    ),
]


def by_shortcut(shortcut):
    for c in COINS:
        if c.coin_shortcut == shortcut:
            return c
    raise ValueError('Unknown coin shortcut "%s"' % shortcut)


def by_name(name):
    for c in COINS:
        if c.coin_name == name:
            return c
    raise ValueError('Unknown coin name "%s"' % name)


def by_address_type(version):
    for c in COINS:
        if c.address_type == version:
            return c
    raise ValueError('Unknown coin address type %d' % version)
