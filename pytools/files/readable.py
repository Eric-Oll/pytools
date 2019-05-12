# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:43:36 2018

@author: Eric
"""

import os
import pickle

import logging as log


class Readable:
    LIST_ATTR = []

    def __inti__(self):
        pass

    def load(self, filename=None):
        """
        Laod the object attributs in the list LIST_ATTR
        """
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as file:
                    obj_dict = pickle.load(file)
            except Exception as err:
                log.error("<{}.load>: {}".format(self.__class__, err))

            for attr in obj_dict:
                if hasattr(self, attr):
                    setattr(self, attr, obj_dict[attr])
        else:
            log.error('<{}.load> : File no found ''{}'''
                      .format(self.__class__, filename))
