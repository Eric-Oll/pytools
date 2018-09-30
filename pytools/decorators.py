# -*- coding: utf-8 -*-
"""
Created on Sun May 13 13:55:16 2018

@author: Eric
"""
import time

def timemark(label=''):
    def deco(exec_function):
        def marked_function(*args, **kwargs):
            print(f"Begin '{exec_function.__name__}' at {time.ctime()}: {label}")
            return_value = exec_function(*args, **kwargs)
            print(f"End '{exec_function.__name__} - at {time.ctime()}: {label}")
            return return_value
        return marked_function
    return deco
            