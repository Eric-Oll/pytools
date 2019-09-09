# -*- coding: utf-8 -*-
"""
Created on Sat May 12 10:15:28 2018

@author: Eric
"""

from threading import Thread, RLock, Condition
from asyncio import Semaphore
import logging as log


class ThreadFlash(Thread):

    def __init__(self, func=None, func_argv=None, func_kwarg=None):
        Thread.__init__(self)
        self.return_is_set = False
        self.return_lock = Condition()
        self.return_lock.acquire()
        
        self.func = func
        self.argv = func_argv if func_argv is not None else ()
        self.kwarg = func_kwarg if func_kwarg is not None else {}
        self.return_value = None

    def run(self):
        log.debug("Run '{}' with parameters : \n argv={}\nkwarg={}"
                  .format(self.func, self.argv, self.kwarg))
        try:
            self.return_value = self.func(*self.argv, **self.kwarg)
            self.return_is_set = True
            self.return_lock.release()
            with self.return_lock:
                self.return_lock.notify()
            log.debug("Return value = {}".format(self.return_value))
        except Exception as err:
            log.error('Error', err)
        else:
            log.debug(f"End of function '{self.func}'.")

    def get_return_value(self):
        self.join()
        while not self.return_is_set:
            self.return_lock.wait_for(self.return_is_set, timeout=1)
        self.return_value
        
    # TODO : Faire une fonction de stop


def threading_function(func=None, argv=None, kwarg=None):
    th = ThreadFlash(func=func,
                     func_argv=argv,
                     func_kwarg=kwarg)
    th.start()
    return th
