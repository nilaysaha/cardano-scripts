#!/bin/python3

"""
In this we thread together the different steps to setup the node pool
"""

import create_keys_addr as cka
import process_certs as pc
import register_stake_pool as rsp

FSM_STATES=['generate', 'regiseter', 'submit']
FSM_SVAL=[False,False,False]


class Setup:
    def __init__(self):
        pass

    def _step_1(self):
        try:
            cka.fetch_init_files()
        except Exception:
            print(Exception)


    def _step_2(self):
        try:
            t = cka.CreatKAddr()
            t.main()
        except Exception as e:
            print(e)

    def _step_3(self):
        try:
            pc.get_funds_via_faucet()
        except Exception as e:
            print(e)

    def _step_4(self):
        try:
            pc.main()
        except Exception as e:
            print(e)

    def _step_5(self):
        try:
            rsp.main({'generate':True, 'register':False, 'submit': False})
        except Exception as e:
            print(e)

    def _step_6(self):
        pass

    def _step_7(self):
        try:
            rsp.main({'generate':False, 'register':True, 'submit': False})
        except Exception as e:
            print(e)

    def _step_8(self):
        try:
            rsp.main({'generate':False, 'register':False, 'submit': True})
        except Exception as e:
            print(e)
            
    def main():
        """
        Here in this function the overall setup will be executed using different submodules
        
        Step 1: fetch the config files for this chain
        Step 2: Create the keys and addresses
        Step 3: Get funds 
        Step 4: Register stake address
        Step 5: Generate stake pool keys
        Step 6: Manually configure relay and producer node configs.
        Step 7: Register stake pool with metadata
        Step 8: Submit the stake pool with transaction
        """
        for i in range(1,9):
            sname = "_step_%s"%(i)
            self.sname()


if __name__=="__main__":
    s = Setup()
    s.main()
        
