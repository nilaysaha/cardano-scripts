#!/bin/env python

import subprocess, json
import logging
import create_token as ct
import process_certs as pc

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')


FILES={
    "policy": {
        "signature":"./kaddr_token/policy.skey",
        "script":"./kaddr_token/policy.script"        
    },
    "logo":{
        "img":"./kaddr_token/logo.png",
    },
    "token":{
        "ticker": "REIT",
        "name": "REIT",
        "description": "Real estate investment trust",
        "url":"https://lkbh-pools.org",
        "logo":"https://lh4.googleusercontent.com/97d4TLg7x_Z4gDlEZZ-akJFBuY8sV8h_UotR6Vf502-YGrpfxBJc7lahWbU-q4hTDFMq4g=w16383",
        "unit":"2, cents"
    }
}


class RegisterToken:
    """
    based on the following page:https://github.com/cardano-foundation/cardano-token-registry/wiki/How-to-prepare-an-entry-for-the-registry
    """
    def __init__(self, name=FILES['token']['ticker']):
        self.name = name
        policy = ct.mint_new_asset(FILES['policy']['script'])
        b64name = "52454954"
        self.subject = policy+b64name

        
    def _prepare_draft(self):
        """
        cardano-metadata-submitter --init baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65        
        """

        try:
            command = ["cardano-metadata-submitter", "--init",self.subject]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")
        except:
            logging.exception("Prepare draft")


    def _augment_data(self,name=FILES['token']['name'], descr=FILES['token']['description'], policy_file=FILES['policy']['script']):
        """
        cardano-metadata-submitter baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 \
        --name "My Gaming Token" \
        --description "A currency for the Metaverse." \
        --policy policy.json
        """

        try:
            policy = pc.content[policy_file]
            command = ["cardano-metadata-submitter", self.subject,
                       "--name", name,
                       "--description", description,
                       "--policy", policy]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                        
        except:
            logging.exception("Failed to augment data with name, description and policy json data")


    def _add_optional_field(self, ticker=FILES['token']['ticker'], url=FILES['token']['url'], unit=FILES['token']['unit'], logo=FILES['token']['logo']):
        """
        cardano-metadata-submitter baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 \
        --ticker "TKN" \
        --url "https://finalfantasy.fandom.com/wiki/Gil" \
        --unit "2,cents" \
        --logo "icon.png"
        """

        try:
            command = ["cardano-metadata-submitter", self.subject,
                       "--ticker", ticker,
                       "--url", url, "--unit", unit, "--logo", logo]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                        
        except:
            logging.exception("Failed to add optional field")


    def _sign_metadata(self):
        """
        cardano-metadata-submitter baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 -a policy.skey
        """

        try:
            command = ["cardano-metadata-submitter", self.subject, "-a", FILES["policy"]["signature"]]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                                    
        except:
            logging.exception("Failed to sign metadata")


    def _finalize_entry(self):
        """
        cardano-metadata-submitter baa836fef09cb35e180fce4b55ded152907af1e2c840ed5218776f2f6d7961737365746e616d65 --finalize
        """

        try:
            command = ["cardano-metadata-submitter", self.subject, "--finalize"]
            s = subprocess.check_output(command, stderr=True, universal_newlines=True)
            print(Fore.GREEN + f"Successful:  Output of command {command} is:{s}")                                    
        except:
            logging.exception("Failed to sign metadata")


    def main(self):
        self._prepare_draft()
        self._augment_data()
        self._add_optional_field()
        self._sign_metadata()
        self._finalize_entry()
        


if __name__ == "__main__":
    a = RegisterToken()
    a.main()
    
