# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:35:54 2018

@author: Eric
"""

import pickle
import logging as log

class Writable:
    LIST_ATTR = []
    def __init__(self):
        pass

    def save(self, filename=None):
        """
        Save the object attributs in the list LIST_ATTR
        """
        obj_dict = {}
        for attr in self.LIST_ATTR:
            if hasattr(self, attr):
                obj_dict[attr] = getattr(self, attr)
        try:
            with open(filename, 'wb') as file:
                pickle.dump(obj_dict, file)
        except Exception as err:
            log.error('<{}.save> : {}'.format(self.__class__,err))
