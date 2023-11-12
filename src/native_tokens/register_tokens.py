#!/bin/env python

import sys
sys.path.append('..')

import subprocess, json
import logging
import create_token as ct
import process_certs as pc
import colorama
from colorama import Fore, Back, Style

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
colorama.init(autoreset=True)

FILES={
    "policy": {
        "signature":"./kaddr_new/policy.skey",
        "script":"./kaddr_new/policy.json"        
    },
    "logo":{
        "img":"./kaddr_new/logo.png",
    }
}

METADATA = {
    "subject":"1a49530b152d1e090a0242ecfe79a5b6b7d28e57f0d9d1b64f42eba452454954",
    "name": "REIT",
    "description": "A protocol to unlock value and trade verified real estate assets",
    "policy":"12e4574d12610a77e01f3886d93e3d920105975965ed11341b5ba8f4",
    "ticker": "REIT",    
    "url":"https://reitcircles.com",
    "logo":"./kaddr_new/logo.png",
    "decimals":"6"
}


class RegisterToken:
    """
    based on the following page:https://github.com/cardano-foundation/cardano-token-registry/wiki/How-to-prepare-an-entry-for-the-registry
    """
    def __init__(self):
        self.name = METADATA['name']
        policy = METADATA['policy']
        b64name = "52454954"
        self.subject = policy+b64name

        
    def _prepare_draft(self):
        """
        token-metadata-creator entry --init baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65        
        """

        try:
            command = ["token-metadata-creator", "entry", "--init",self.subject]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")
        except:
            logging.exception("Prepare draft")


    def _add_required_fields(self,name=METADATA['name'], descr=METADATA['description'], policy=METADATA['policy']):
        """
        token-metadata-creator baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 \
        --name "My Gaming Token" \
        --description "A currency for the Metaverse." \
        --policy policy.json  (only for non script based policy)
        """

        try:
            #policy = pc.content(policy_file)
            command = [
                "token-metadata-creator", "entry", self.subject,
                "--name", name,
                "--description", descr
            ]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                        
        except:
            logging.exception("Failed to augment data with name, description and policy json data")


    def _add_optional_fields(self, ticker=METADATA['ticker'], url=METADATA['url'], decimals=METADATA['decimals'], logo=METADATA['logo']):
        """
        token-metadata-creator baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 \
        --ticker "TKN" \
        --url "https://finalfantasy.fandom.com/wiki/Gil" \
        --decimals 6 \
        --logo "icon.png"
        """

        try:
            command = ["token-metadata-creator", "entry", self.subject,
                       "--ticker", ticker,
                       "--url", url,
                       "--decimals",decimals,
                       "--logo", logo]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                        
        except:
            logging.exception("Failed to add optional field")


    def _sign_metadata(self):
        """
        token-metadata-creator baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 -a policy.skey
        """

        try:
            command = ["token-metadata-creator", "entry", self.subject, "-a", "./kaddr_new/owner.skey"]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                                    
        except:
            logging.exception("Failed to sign metadata")


    def _finalize_entry(self):
        """
        token-metadata-creator baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 --finalize
        """

        try:
            command = ["token-metadata-creator", "entry", self.subject, "--finalize"]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                                    
        except:
            logging.exception("Failed to sign metadata")


    def main(self):
        self._prepare_draft()
        self._add_required_fields()
        self._add_optional_fields()
        self._sign_metadata()
        self._finalize_entry()
        


if __name__ == "__main__":
    a = RegisterToken()
    a.main()
    
