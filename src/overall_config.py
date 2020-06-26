#!/bin/python3

"""
In this we thread together the different steps to setup the node pool
"""

import sys
import create_keys_addr as cka
import process_certs as pc
# import register_stake_pool as rsp

class Setup:
    def __init__(self):
        pass

    def _step_1(self):
        print("_step_1")
        try:
            cka.fetch_init_files()
        except:
            e = sys.exc_info()[0]
            print(e)    

    def _step_2(self):
        import subprocess
        command = ["sudo", "systemctl", "start", "shelly-cardano"]
        print(f"please start the relay chain manually")
        print(f"Here ends the work for the cardano relay node. Next steps only relevant for the producer node")
            
    def _step_3(self):
        print('step 3')
        try:
            t = cka.CreateKAddr()
            t.main()
        except:
            e = sys.exc_info()[0]
            print(e)

        
    def _step_4(self):
        try:
            pc.get_funds_via_faucet()
        except Exception as e:
            print(e)

        
    def _step_5(self):
        # try:
        #     pc.main()
        # except Exception as e:
        #     print(e)
        pass
        
    def _step_6(self):
        # try:
        #     rsp.main({'generate':True, 'register':False, 'submit': False})
        # except Exception as e:
        #     print(e)
        pass
        
    def _step_7(self):
        pass

    def _step_8(self):
        # try:
        #     rsp.main({'generate':False, 'register':True, 'submit': False})
        # except Exception as e:
        #     print(e)
        pass
        
    def _step_9(self):
        # try:
        #     rsp.main({'generate':False, 'register':False, 'submit': True})
        # except Exception as e:
        #     print(e)
        pass
        
    def test_func(self):
        print('this is test function')
        return 0
        
    def exec_step(self,stepId):
        exec_map = {
            1: self._step_1,
            2: self._step_2,
            3: self._step_3,
            4: self._step_4,
            5: self._step_5,
            6: self._step_6,
            7: self._step_7,
            8: self._step_8,
            9: self._step_9,
            10: self.test_func
        }
        f = exec_map[stepId]
        f()
        print(f)

        
if __name__=="__main__":
    import argparse

    descr="""
    Step 1: fetch the config files for this chain
    Step 2: Now start the chain for relay using config file fetched.
    Step 3: Create the keys and addresses
    Step 4: Get funds  
    Step 5: Register stake address 
    Step 6: Generate stake pool keys 
    Step 7: Manually configure relay and producer node configs. 
    Step 8: Register stake pool with metadata
    Step 9: Submit the stake pool with transaction
    Step 10: test function
    """
    
    parser = argparse.ArgumentParser(description=descr, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                        help="Please input step to be executed")
    args = parser.parse_args()
    print(args.step)

    s = Setup()
    s.exec_step(args.step)
