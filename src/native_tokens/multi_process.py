#!/usr/bin/env python3

from multiprocessing import Process

import monitor_payment as mp


class TaskParallel:
    def __init__(self):
        self.workers = 10


    def task(self, uuid):
        p = Process(target=mp.Monitor, args=(uuid))
        p.start()

    
