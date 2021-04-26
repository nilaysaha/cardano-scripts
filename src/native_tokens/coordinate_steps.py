#!/usr/bin/env python3

import monitor_payment as mp
import create_nft_token as nft
import transfer_native_asset as ta

import logging
import colorama
from colorama import Fore, Back, Style


"""

This module will simulate the transition from people submitting data about their NFT and then paying for the minting of the token.

Phase 1: (Frontend)
  - Page loads with people being asked to submit details of their images and the Address to which they like to receive their minted token.
  - Submit that information.

Phase 2: (Backend)
   - In the backend we execute step to generate a unique pay.addr and return back this along with UUID generated.
   - People are shown the pay.addr and asked to submit a payment of 75 ADA for the same.

Phase 3: (Backend)
   - Monitor the payment of the ADA
   - Once payment comes do the post payment actions.
        - minting of tokens.
        - sending them to the recv.addr

"""
