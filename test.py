#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import binascii
import mnemonic
import bip32utils
from eth_account import Account
import itertools
from operator import itemgetter
import time
import random

def fact(n):
    res = 1
    for i in range (1, n + 1):
        res *= i
    return res
def nPr(n, r):
    return fact(n)/fact(n - r)
def nCr(n, r):
    return fact(n)/(fact(r)*fact(n - r))


start = time.time()
limit = 12.0
lim_ = 1.0
N = 10000
enlib = 'english.log'
mobj = mnemonic.Mnemonic("english")
enDict = open(enlib, "r").read().split('\n')
# load input and dict
print('🔎 Generating sorted mnemonic list ...')
susWords = [['bride', 1.00, 1],
['couple', 1.00, 1],
['reflect', 1.00, 1],
['portrait', 1.00, 1],
['soldier', 1.00, 1],
['cover', 1.00, 1],
['hold', 1.00, 1],
['mirror', 1.00, 1],
['stick', 0.75, 1],
['drum', 0.75, 1],
['hat', 0.75, 1],
['wedding', 0.75, 1],
['police', 0.75, 1],
['history', 0.50, 1],
['marriage', 0.50, 1],
['hand', 0.50, 1],
['uniform', 0.50, 1],
['ceremony', 0.50, 1],
['celebrate', 0.50, 1],
['groom', 0.50, 1],
['badge', 0.50, 1],
['memory', 0.25, 1],
['wife', 0.25, 1],
['husband', 0.25, 1],
['picture', 0.25, 1],
['man', 0.25, 1],
['woman', 0.25, 1],
['finger', 0.25, 1],
['gown', 0.25, 1],
['head', 0.00, 1],
['jewel', 0.00, 1],
['eye', 0.00, 1],
['proud', 0.00, 1],
['pride', 0.00, 1],
['vision', 0.00, 1],
['love', 0.00, 1],
['face', 0.00, 1],
['curtain', 0.25, 2],
['forest', 0.25, 2],
['old', 0.50, 2],
['glass', 0.75, 2],
['nature', 1.00, 2],
['window', 1.00, 2],
['bright', 1.00, 2],
['warm', 1.00, 2],
['title', 1.00, 2],
['view',1.00, 2]]

random.shuffle(susWords);
approved = [item for item in susWords if item[0] in enDict and item[1] >= lim_]
onlyWords = [i[0] for i in approved]
print('📜 Valid BIP39 words: ')
print(*onlyWords, sep=' ')

toTest = len(approved)
nCr = str(int(nCr(toTest, 12)))
# Generate ordered list of mnemonics to try
allC = []
for i in list(itertools.combinations(approved, 12)):
    sum = 0; string = []; unique = []
    for j in i:
        sum += j[1]
        string.append(j[0])
        unique.append(j[2])
    if sum >= limit and len(set(unique)) == 2 and len(set([unique.count(k) for k in set(unique)])) == 1:
        allC.append([' '.join(string), sum])

allC = sorted(allC, key=itemgetter(1))
toTrial = str(len(allC))
if 18 >= toTest >= 12:
    print('✅ 18>= len(list) >= 12' + ', Found: ' + str(toTest) + ', nCr = ' + toTrial)
elif len(approved) >= 18:
    print('❌ len(list) >= 18' + ', Found: ' + str(toTest) + ', nCr = ' + toTrial)
else:
    print('⚠️  Warning: len(list) < 12' + ', Found: ' + str(toTest) + ', nCr = ' + toTrial)

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

    addr = Account.from_key("0x" + binascii.hexlify(bip32_child_key_obj.PrivateKey()).decode()).address

    if (addr == "0xC399bd88A3471bfD277966Fef8e5110857e827Fc"):
        print('🔥🔥🔥')
        result = {
            'mnemonic_words': mnemonic_words,
            'entropy': entropy.hex(),
            'addr': addr,
            'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
            'privatekey': binascii.hexlify(bip32_child_key_obj.PrivateKey()).decode(),
            'coin': 'ETH'
        }
        pprint.pprint(result)

if __name__ == '__main__':
    print('⌛ Testing ...')
    for one in allC:
        print(one[0])
    i = 0
    for one in allC:
        try_this = one[0].split(' ')
        allPer = itertools.permutations(try_this)
        for each in allPer:
            i += 1
            if i == N:
                break
            try:
                bip39(' '.join(each))
            except Exception as error:
                ''
        break
    end = time.time()
    if i > 0:
        print('DONE')
        print(((end - start)/i)*fact(12), 'seconds')
        print((end - start)/i, 'seconds/trial')
    else:
        print('⚠️  Threshold too high')
