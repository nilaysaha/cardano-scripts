#!/usr/bin/env python3

import redis, json
from rq import Connection, Worker
from rq import Queue as Queue_RQ
import monitor_payment as mp

PLIST='QUEUE'
MAX_NUM_WORKERS=3
PROCESSING_LIST='PROCESS'

DEFAULT_RQ_QUEUE_NAME='NftMinting'
DEFAULT_NUM_WORKERS=1

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
        


class RQ:
    def __init__(self, queue_name=DEFAULT_RQ_QUEUE_NAME):
        self.q = Queue_RQ(queue_name, connection=rhost)
        self.qname = queue_name
        
    def queue(self, task_id):
        result = self.q.enqueue(mp.main_task, task_id)

    def queue_with_retry(self, task_id, num_retry):
        from rq import Retry
        self.q.enqueue(mp.main_task, retry=Retry(max=num_retry))

    def start_worker(self, num_workers=DEFAULT_NUM_WORKERS ):
        # Start a worker with a custom name
        for i in range(DEFAULT_NUM_WORKERS):
            print(f"Now starting a redis worker for connecting to redis queue for monitoring payment")
            worker = Worker([self.q], connection=rhost, name='rq_worker_'+str(i))
        
        
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
