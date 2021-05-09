#!/usr/bin/env python3

import redis, json

PLIST='QUEUE'
MAX_NUM_WORKERS=3
PROCESSING_LIST='PROCESS'

rhost = redis.Redis(host='localhost', port=6379, db=0)

class Queue:
    def __init__(self,queue_name):
        self.name = queue_name
        
    def queue(self, uuid):
        rhost.lpush(self.name, uuid)
        
    def fetch(self):
        if rhost.llen(self.name) > 0:
            return rhost.lpop(self.name).decode('utf-8')
        else:
            print(f"No more items to return. Hence returning None")
            return None

    def show(self):
        for item in rhost.lrange(self.name, 0, -1):
            print(item)

    def len(self):
        return rhost.llen(self.name)

    def remove(self,uuid):
        """
        remove the first instance of uuid from the queue
        """
        
        rhost.lrem(self.name, 1, uuid)
        
        
            
if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--uuid', dest='uuid', help="This customer uuid being assigned")
    parser.add_argument('--list', dest='list', action='store_true')
    args = parser.parse_args()

    q = Queue()
    
    if args.uuid != None:
        q.queue(args.uuid)
    elif args.uuid == None and not args.list:
        print("Did not recieve any argument. See help. python3 queue_task.py --help")
    elif args.list:
        q.show()
