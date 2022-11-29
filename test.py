#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import binascii
import mnemonic
import bip32utils

enlib = 'english.log'
mobj = mnemonic.Mnemonic("english")
enDict = open(enlib, "r").read().split('\n')
# load input and dict
arr = input('Enter space-separated words: ')
sus = list(map(str, arr.split(' ')))
approved = []
for item in sus:
    if item in enDict:
        approved.append(item)

print('Valid BIP39 words: ')
print(*approved, sep=' ')

def bip39(mnemonic_words):
    seed = mobj.to_seed(mnemonic_words)
    entropy = mobj.to_entropy(mnemonic_words)
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
        'entropy': entropy,
        'addr': bip32_child_key_obj.Address(),
        'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
        'privatekey': bip32_child_key_obj.WalletImportFormat(),
        'coin': 'ETH'
    }

if __name__ == '__main__':
    if len(approved) >= 12:
        print('len(list) >= 12')
    else:
        print('error: len(list) < 12')

    # TO DO
    #words = mobj.generate(strength=128)
    #pprint.pprint(bip39(words))
