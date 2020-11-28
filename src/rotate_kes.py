#!/usr/bin/python3

import sys, subprocess
import register_stake_pool as rsp

MINM_KES_PERIOD_REMAINING=3

class ChainProcess:
    """
    This presumes that we have a shelly-cardano.service file in /etc/systemd/system 
    so that systemctl is able to handle the commands below.
    """
    def __init__(self):
        pass

    def reload_chain(self):
        try:
            command = ["sudo", "systemctl", "reload", "shelly-cardano"]
            s = subprocess.check_output(command, stderr=True)
            print(f"reload chain first")
        except:
            print("Oops!", sys.exc_info(), "occurred in reload chain")

    def stop_chain(self):
        try:
            command = ["sudo", "systemctl", "stop", "shelly-cardano"]
            s = subprocess.check_output(command, stderr=True)
            print(f"stop chain first")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in stop chain")


    def start_chain(self):
        try:
            command = ["sudo", "systemctl", "start", "shelly-cardano"]
            s = subprocess.check_output(command, stderr=True)
            print(f"start chain ")
        except:
            print("Oops!", sys.exc_info()[0], "occurred in start chain")


def update_KES_params():
    try:
        p = rsp.PoolKeys()
        p.generate_kes_keys()
        p.generate_node_cert()
        #Now move the relevant files to kaddr_run directory
        rsp.setup_run_configs()
    except:
        print(f"Error occured in update kes params:{sys.exc_info()[0]}")
            

def main(min_KES):        
    remaining_kes_period = rsp.remaining_kes_period()
    print(f"remaining kes period:{remaining_kes_period}")
    if (remaining_kes_period < min_KES):
        #first generate new KES params
        update_KES_params()
        #next restart the chain
        # t = ChainProcess()
        # t.stop_chain()
        # t.start_chain()
        pass
    else:
        print(f"remaining KES {remaining_kes_period} is still greater than minimum {min_KES}")


        
if __name__=="__main__":
    import argparse
    descr = """
    We need to rotate after the kes expires.
    """
    parser = argparse.ArgumentParser(description=descr, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--minKES", type=int, help="When the remaining kes is less than this we will update the kes keys and node.cert and restart process.")
    
    args = parser.parse_args()
    print(args)
    
    if(args.minKES == None):
        min_KES = MINM_KES_PERIOD_REMAINING
    else:
        min_KES = args.minKES
        
    main(min_KES)
