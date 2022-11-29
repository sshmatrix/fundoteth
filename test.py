#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import binascii
import mnemonic
import bip32utils

mobj = mnemonic.Mnemonic("english")

def bip39(mnemonic_words):
    seed = mobj.to_seed(mnemonic_words)

    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)

    return {
        'mnemonic_words': mnemonic_words,
        'addr': bip32_child_key_obj.Address(),
        'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
        'privatekey': bip32_child_key_obj.WalletImportFormat(),
        'coin': 'ETH'
    }

if __name__ == '__main__':
    mobj = mnemonic.Mnemonic("english")
    mnemonic_words = mobj.generate(strength=128)
    pprint.pprint(bip39(mnemonic_words))
