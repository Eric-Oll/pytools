'''
Created on 15 juin 2019

@author: Eric
'''

from pytools.info.logger.duck import Duck; logger = Duck(level=Duck.DEBUG)
from pytools.prog.threading import threading_function
import time

def lambda_function(param1="Value", param2="Message", return_code=0):
    logger.info(param2, "Valeur : {}".format(param1,), "Time : {}".format(time.time()))
    time.sleep(3)
    logger.info(param2, "Valeur : {}".format(param1,), "Time : {}".format(time.time()))
    return return_code
    
def launch_test():
    result1 = threading_function(lambda_function, kwarg={'param1':"Test1", 'param2':"Message pour le test 1", 'return_code':1})
    result2 = threading_function(lambda_function, kwarg={'param1':"Test2", 'param2':"Message pour le test 2", 'return_code':2})
    
    print("Resultat 1 = {}".format(result1.get_return_value()))
    print("Resultat 2 = {}".format(result2.get_return_value()))
    


if __name__ == '__main__':
    launch_test()