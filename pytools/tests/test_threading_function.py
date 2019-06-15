'''
Created on 15 juin 2019

@author: Eric
'''

from pytools.info.logger.duck import Duck; logger = Duck(level=Duck.INFO)
from pytools.threading import threading_function

def lambda_function(param1="Value", param2="Message"):
    logger.info(param2, "Valeur : {}".format(param1,))
    

if __name__ == '__main__':
    threading_function(lambda_function, {'param1':"Test1", 'param2':"Message pour le test 1"})
    threading_function(lambda_function, {'param1':"Test2", 'param2':"Message pour le test 2"})
    