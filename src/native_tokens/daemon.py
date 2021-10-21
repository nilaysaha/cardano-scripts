#!/usr/bin/env python3

import logging, sys
import queue_task as qt
import configparser

config = configparser.ConfigParser()
config.read('./config.py')



class Daemon:
    def __init__(self, task):
        self.num_worker = qt.MAX_NUM_WORKERS
        self.qin  = qt.Queue(qt.PLIST)
        self.qout = qt.Queue(qt.PROCESSING_LIST)
        self.qhost = qt.rhost
        self.task = task

    def _unschedule(self, uuid):
        #remove the items from the processing queue.
        self.qout.remove(uuid)

    def schedule(self):
        while True:
            job_id = self.qhost.brpoplpush(qt.PLIST, qt.PROCESSING_LIST).decode('utf-8')
            if not job_id:
                continue
            
            # process the job
            if job_id:
                self.task(job_id)
                self._unschedule(job_id)


class Daemon_RQ:
    def __init__(self, queue_name, num_workers):
        try:
            q = qt.RQ(queue_name)
            q.start_worker(num_workers)
        except:
            logging.exception("Something wrong with Redis RQ WORKERS. ")
            sys.exit(1)
