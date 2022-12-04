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
from functools import reduce
import sys

# load input and dict
enlib = 'english.log'
mobj = mnemonic.Mnemonic("english")
enDict = open(enlib, "r").read().split('\n')

id = int(sys.argv[1])
batch = int(sys.argv[2])

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

# variable -------------------------
susLists = [['police', 1, 1], ## FIXED
['pair',     1, 2],           ## !
['double',   1, 2],           ## !
['two',      1, 2],           ## !
['gossip',   1, 3],           ## ! FIXED
['drum',     2, 4],           ## ! FIXED
['marriage', 2, 4],           ## ! FIXED
['movie',    2, 5],           ## ! FIXED
['engage',   2, 5],           ## ! FIXED
['hope',     1, 6],           ## ! FIXED
['april',    1, 7],           ## ! FIXED
['window',   1, 9]]           ## ! FIXED
layer_ = [0, 8]               ## ! 0% : [0, 9], [1, 9], [1, 8]
# ----------------------------------

for layer in layer_:
    for i in enDict:
        if i != '':
            susLists.append([i, 1, layer])

print('🔎 Generating sorted mnemonic list ...')
susLists = sorted(susLists, key=itemgetter(2))
susGroup = []
for item in set([this[2] for this in susLists]):
    each_ = []
    for each in susLists:
        if each[2] == item:
            each_.append([each[0], each[1], each[2]])
    susGroup.append(each_)
all_ = []
nCount = []
valid = []
for susWords in susGroup:
    allIn = []; sum = 0
    if susWords[0][2] in layer_:
        nCount.append(len(susWords))
        for i in susWords:
            valid.append([i[0]])
            allIn.append([i[0], 1])
        all_.append(allIn)
        continue
    limit = susWords[0][1]
    random.shuffle(susWords);
    approved = [item for item in susWords if item[0] in enDict]
    valid.append([this_[0] for this_ in approved])
    onlyWords = [i[0] for i in approved]
    toTest = len(approved)
    nCount.append(nPr(toTest, int(len(susWords))))
    for i in list(itertools.permutations(approved, int(limit))):
        string = []
        for j in i:
            string.append(j[0])
        allIn.append([' '.join(string), 1])
    all_.append(allIn)

print('📜 Valid BIP39 words: ')
print(*[item for sublist in valid for item in sublist], sep=' ')
print('nPr =', int(reduce(lambda x, y: x*y, nCount)))
all = [];

# manual nesting; TO DO: replace with inverse do-while matrix
for i in all_[0]:
    for j in all_[1]:
        for k in all_[2]:
            for l in all_[3]:
                for m in all_[4]:
                    for n in all_[5]:
                        for o in all_[6]:
                            for p in all_[7]:
                                for q in all_[8]:
                                    for r in all_[9]:
                                        all.append([' '.join([i[0], j[0], k[0], l[0], m[0], n[0], o[0], p[0], q[0], r[0]]), (i[1] + j[1] + k[1] + l[1] + m[1] + n[1] + o[1] + p[1] + q[1] + r[1])])

all = sorted(all, key=itemgetter(1))
toTrial = str(len(all))
if 18 >= toTest >= 12:
    print('✅ 18>= len(list) >= 12' + ', Found: ' + str(toTest) + ', nPr = ' + toTrial)
elif len(approved) >= 18:
    print('❌ len(list) >= 18' + ', Found: ' + str(toTest) + ', nPr = ' + toTrial)
else:
    print('⚠️  Warning: len(list) < 12' + ', Found: ' + str(toTest) + ', nPr = ' + toTrial)

def bip39(mnemonic_words):
    seed = mobj.to_seed(mnemonic_words)
    entropy = mobj.to_entropy(mnemonic_words)
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        60 + bip32utils.BIP32_HARDEN
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
        with open('test.key', 'a') as file:
            file.write(str(result))
            return True
    else:
        return False

if __name__ == '__main__':
    print('⌛ Testing ...')
    i = 0
    for each in all:
        i += 1
        if (id + 1) * batch > i >= (id * batch) and len(each[0].split(' ')) == 12:
            try:
                success = bip39(each[0])
                if success:
                    break
                else:
                    continue
            except Exception as error:
                #print(i, error)
                ''
        elif i >= (id + 1) * batch and len(each[0].split(' ')) == 12:
            break
        elif len(each[0].split(' ')) != 12:
            print('error: len != 12')
            break


    end = time.time()
    if i > 0:
        print('DONE')
        print(((end - start)/i)*fact(12), 'seconds')
        print((end - start)/i, 'seconds/trial')
    else:
        print('⚠️  Threshold too high')
