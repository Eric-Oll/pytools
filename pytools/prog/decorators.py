# -*- coding: utf-8 -*-
"""
Created on Sun May 13 13:55:16 2018

@author: Eric
"""
import time
import warnings
import functools

def deprecated(message=''):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            warnings.warn("Call to deprecated function {}.\n{}".format(func.__name__, message),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return func(*args, **kwargs)
        return new_func
    return decorator

def timemark(label=''):

    def deco(exec_function):

        def marked_function(*args, **kwargs):
            print(f"Begin '{exec_function.__name__}' at {time.ctime()}: {label}")
            return_value = exec_function(*args, **kwargs)
            print(f"End '{exec_function.__name__} - at {time.ctime()}: {label}")
            return return_value

        return marked_function

    return deco
            
