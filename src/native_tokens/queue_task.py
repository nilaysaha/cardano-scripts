#!/usr/bin/env python3

import redis, json

LIST='PAYMENT'

class Queue:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        
    def queue(self, uuid, qaddr):
        item = json.dumps({"uuid": uuid, "addr": qaddr}, separators=(',', ':'))
        self.r.lpush(LIST, item )
        
    def fetch(self):
        if self.r.llen(LIST) > 0:
            return self.r.lpop(LIST)
        else:
            print(f"No more items to return. Hence returning None")
            return None

    def show(self):
        for item in self.r.lrange(LIST, 0, -1):
            print(item)
        

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--uuid', dest='uuid', help="This customer uuid being assigned")
    parser.add_argument('--addr', dest='addr', help="Address to which the nft needs to be sent to")
    parser.add_argument('--list', dest='list', action='store_true')
    args = parser.parse_args()

    q = Queue()
    
    if args.uuid != None and args.addr != None:
        q.queue(args.uuid, args.addr)
    elif args.uuid == None and args.addr == None and not args.list:
        print("Did not recieve any argument. See help. python3 queue_task.py --help")
    elif args.list:
        q.show()
