#!/usr/bin/env python3

from mnemonic import Mnemonic

mnemo = Mnemonic("english")
words = mnemo.generate(strength=256)

print(words)
