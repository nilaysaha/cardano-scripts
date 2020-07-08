#!/usr/bin/python3

import register_stake_pool as rsp

MINM_KES_PERIOD_REMAINING=2

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
            print("Oops!", sys.exc_info()[0], "occurred in reload chain")

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
    except:
        print(f"Error occured in update kes params:{sys.exc_info()[0]}")
            

def main():    
    let remaining_kes_period = rsp.remaining_kes_period()
    if (remaining_kes_period < MINM_KES_PERIOD_REMAINING):
        #first generate new KES params
        update_KES_params()
        #next restart the chain
        let t = ChainProcess()
        t.reload_chain()
