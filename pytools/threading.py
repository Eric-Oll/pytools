# -*- coding: utf-8 -*-
"""
Created on Sat May 12 10:15:28 2018

@author: Eric
"""

from threading import Thread

import logging as log


class ThreadFlash(Thread):

    def __init__(self, func=None, func_argv=None, func_kwarg=None):
        Thread.__init__(self)

        self.func = func
        self.argv = func_argv if func_argv is not None else ()
        self.kwarg = func_kwarg if func_kwarg is not None else {}
        self.return_value = None

    def run(self):
        log.debug("Run '{}' with parameters : \n argv={}\nkwarg={}"
                  .format(self.func, self.argv, self.kwarg))
        try:
            self.return_value = self.func(*self.argv, **self.kwarg)
        except Exception as err:
            log.error('Error', err)
        else:
            log.debug(f"End of function '{self.func}'.")

    # TODO : Faire une fonction de stop


def threading_function(func=None, argv=None, kwarg=None):
    th = ThreadFlash(func=func,
                     func_argv=argv,
                     func_kwarg=kwarg)
    th.start()
    th.join()
    return th.return_value
