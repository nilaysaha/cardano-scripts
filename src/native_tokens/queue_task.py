#!/usr/bin/env python3

import redis, json
from rq import Connection, Worker
from rq import Queue as Queue_RQ
import monitor_payment as mp
import configparser

rhost = redis.Redis(host='localhost', port=6379, db=0)

config = configparser.ConfigParser()
config.read('./config.py')

class Queue:
    def __init__(self,queue_name=None):
        if queue_name == None:
            queue_name = config['COMMON']['DEFAULT_RQ_QUEUE_NAME']
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
    def __init__(self, queue_name=config['COMMON']['DEFAULT_RQ_QUEUE_NAME']):
        self.q = Queue_RQ(queue_name, connection=rhost)
        self.qname = queue_name
        
    def queue(self, task_id):
        result = self.q.enqueue(mp.main_task, task_id)

    def queue_with_retry(self, task_id, num_retry):
        from rq import Retry
        self.q.enqueue(mp.main_task, retry=Retry(max=num_retry))

    def start_worker(self, num_workers=config['COMMON']['DEFAULT_NUM_WORKERS']):
        # Start a worker with a custom name
        for i in range(DEFAULT_NUM_WORKERS):
            print(f"Now starting a redis worker for connecting to redis queue for monitoring payment")
            worker = Worker([self.q], connection=rhost, name='rq_worker_'+str(i))
        

class Daemon_RQ:
    def __init__(self, queue_name, num_workers):
        try:
            q = RQ(queue_name)
            q.start_worker(num_workers)
        except:
            logging.exception("Something wrong with Redis RQ WORKERS. ")
            sys.exit(1)


            
if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--uuid', dest='uuid', help="This customer uuid being assigned")
    parser.add_argument('--list', dest='list', action='store_true')
    parser.add_argument('--run', dest='run', action="store_true", help="Start monitoring the queue and take action if needed")
    parser.add_argument('--queuename', dest='queuename', help='Name of the queue that the RQ wrapper is using to push uuid into')
    parser.add_argument('--numWorker', dest='numWorker', help='Number of workers to pick up task on redis via RQ wrapper')    

    args = parser.parse_args()
    q = Queue()
    
    if args.uuid != None:
        q.queue(args.uuid)
    elif args.uuid == None and not args.list:
        print("Did not recieve any argument. See help. python3 queue_task.py --help")
    elif args.list:
        q.show()

    if args.run:
        if args.queuename == None:
            qname = config['COMMON']['DEFAULT_RQ_QUEUE_NAME']
        else:
            qname = args.queuename
            
        if args.numWorker == None:
            n = config['COMMON']['DEFAULT_NUM_WORKERS']
        else:
            n = args.numWorker
            
        #Now we are shifting to use Python RQ wrapper to queue/exec jobs
        q.Daemon_RQ(qname, n)
 
        
