#!/usr/bin/env python3

import sys, getopt
import re
from mnemonic import Mnemonic
from binascii import hexlify, unhexlify

def usage():
    print("Usage: bip39tool [-g] [-o words|seed|entropy] [-p PASSPHRASE] [INPUT]")

def help():
    usage()
    print("")
    print("Options:")
    print("  -g,--generate     Generate entropy instead of reading it from INPUT.")
    print("  -o,--output       Output format (words,seed,entropy). Default: seed")
    print("  -p,--passphrase   Passphrase. Only relevant with output format \"seed\". Default: (empty string)")
    print()
    print("INPUT format is detected automatically. Either mnemonic words or hex-encoded entropy are acceptable.")
    print()
    print("Examples:")
    print("  bip39tool -o words --generate")
    print("  bip39tool -o seed picnic scene hundred elite stairs modify hero apple popular stick weekend security")
    print()
    print("  (test vectors from https://github.com/trezor/python-mnemonic/blob/master/vectors.json)")
    print("  bip39tool -o words 7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f")
    print("  bip39tool -o entropy legal winner thank year wave sausage worth useful legal winner thank yellow")
    print("  bip39tool -o seed --passphrase TREZOR 7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f")
    print("  bip39tool -o seed --passphrase TREZOR legal winner thank year wave sausage worth useful legal winner thank yellow")
    print()
    print("Help:")
    print("  See the github project at https://github.com/jes/bip39tool")
    print("  Please email lkbhpools@gmail.com if you want to get in touch")

def main(argv):
    if len(argv) == 0:
        usage()
        print("See --help for more info")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "hgo:p:", ["help","generate","output=","passphrase="])
    except getopt.GetoptError:
        usage()
        print("See --help for more info")
        sys.exit(1)

    generate = False
    outputtype = 'seed'
    passphrase = ''

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit(0)
        elif opt in ("-g," "--generate"):
            generate = True
        elif opt in ("-o", "--output"):
            outputtype = arg
        elif opt in ("-p", "--passphrase"):
            passphrase = arg

    inputtxt = ' '.join(args)
    inputtype = 'words'
    if re.match("^[0-9a-fA-F]+$", inputtxt):
        inputtype = 'entropy'

    entropy = inputtxt

    mnemo = Mnemonic('english')

    if generate:
        # need to generate entropy: just generate some words and pretend we
        # received them as input
        inputtxt = mnemo.generate()
        inputtype = 'words'

    if inputtype == 'words':
        # the reason to convert words to entropy and then straight back again
        # is to sanity-check the words, e.g. in the case of words input and
        # words output
        try:
            entropy = hexlify(mnemo.to_entropy(inputtxt))
        except ValueError as e:
            sys.stderr.write("Sanity check of input words failed: " + e.message + "\n")
            sys.exit(1)

    words = mnemo.to_mnemonic(unhexlify(entropy))

    if outputtype == 'seed':
        print(hexlify(Mnemonic.to_seed(words, passphrase)))
    elif outputtype == 'words':
        print(words)
    elif outputtype == 'entropy':
        print(hexlify(mnemo.to_entropy(words)))
    else:
        sys.exit("Don't recognise output type " + outputtype)

if __name__ == "__main__":
    main(sys.argv[1:])
