'''
Created on 11 mai 2019

@author: Eric
'''
from datetime import datetime

from colorama import Fore, Back

import logging as log


class Level:
    '''
    Classe modélisant le niveau de log
    '''    
    def __init__(self, level):
        self.level=level
    
    def __repr__(self):
        return f"Level {str(self)}"
    
    def __int__(self):
        return self.level
    
    def __str__(self):
        if self.level == log.DEBUG:
            return "DEBUG"
        elif self.level == log.INFO:
            return "INFO"
        elif self.level == log.WARNING:
            return "WARNING"
        elif self.level == log.ERROR:
            return "ERROR"
        elif self.level == log.CRITICAL:
            return "CRITICAL"
        elif self.level == log.FATAL:
            return "FATAL"
        else:
            return str(self.level)

class Duck():
    '''
    The Duck class is an derivated class from standard class Logger.
    This class preformate several properties for simplify the common use.
    '''
    FORMAT = "%(message)s"
    DEFAUL_DUCK_FORMAT = "%LEVEL%:%DATE%:%MESSAGE%"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # LEVEL CONSTANTES 
    DEBUG = Level(log.DEBUG)
    INFO = Level(log.INFO)
    WARNING = Level(log.WARNING)
    ERROR = Level(log.ERROR)
    CRITICAL = Level(log.CRITICAL)
    FATAL = Level(log.FATAL)
    
    def __init__(self, **kwargs):
        '''
        Param�tres `kwargs` :
        - format_duck : False si utilisation du format logging. Si True utilisation du format Duck. Par defaut True.
        - format : format Duck si`format_duck` est actif. Sinon c'est le format logging.
        - les autres param�tres sont pass�es`logging.basicconfig(**kwargs)`
        '''
        self.logger = log.getLogger()
        
        # Format
        self.format_duck = kwargs.pop('format_duck',True)
        if self.format_duck:
            self.format = kwargs.pop('format', Duck.DEFAUL_DUCK_FORMAT)
            kwargs['format']=Duck.FORMAT
        
        # Level
        _level = kwargs.pop("level", self.logger.getEffectiveLevel())
        if isinstance(_level, Level):
            kwargs['level'] = int(_level)
        else:
            kwargs['level'] = _level
        
        log.basicConfig(**kwargs)
        self.set_level(kwargs['level'])
        
    def get_level(self):
        return Level(self.logger.getEffectiveLevel())    
    
    def set_level(self, level):
        if isinstance(level, Level):
            self.logger.setLevel(int(level))
        elif isinstance(level, int):
            self.logger.setLevel(level)
        else:
            log.error(f"{self.__class__}.set_level :'level' est de type {type(level)} et doit être de type 'Level' ou 'int'.")    
    
    def debug(self, *args, **kwargs):
        _list = list(args)
        msg = Fore.BLUE + self.format_message(Duck.DEBUG,_list) + Fore.RESET
        self.logger.debug(msg, **kwargs)
        
    def info(self, *args, **kwargs):
        _list = list(args)
        msg = Fore.GREEN + self.format_message(Duck.INFO, _list) + Fore.RESET
        self.logger.info( msg, **kwargs)
        
    def warning(self, *args, **kwargs):
        _list = list(args)
        msg = Fore.MAGENTA + self.format_message(Duck.WARNING,_list) + Fore.RESET
        self.logger.warning(msg, **kwargs)

    def error(self, *args, **kwargs):
        _list = list(args)
        msg = Fore.RED + self.format_message(Duck.ERROR,_list) + Fore.RESET
        self.logger.error(msg, **kwargs)
        
    def critical(self, *args, **kwargs):
        _list = list(args)
        msg = Back.MAGENTA + Fore.WHITE+ self.format_message(Duck.CRITICAL,_list) + Fore.RESET + Back.RESET
        self.logger.critical(msg, **kwargs)
        
    def fatal(self, *args, **kwargs):
        _list = list(args)
        msg = Back.RED + Fore.WHITE+ self.format_message(Duck.FATAL,_list) + Fore.RESET + Back.RESET
        self.logger.fatal(msg, **kwargs)

    def format_header(self, level):
        if isinstance(level, Level):
            str_level = str(level)
        elif isinstance(level, int):
            str_level = str(Level(level))
        else:
            str_level = str(level)
            
        header = self.format.upper().replace("%LEVEL%", str_level)
        header = header.replace("%DATE%", datetime.today().strftime(self.DATE_FORMAT))
        
        if not isinstance(header, str):
            log.error(f"{self.__class__}.format_header : Le type retourné est {type(header)}. Attendu 'str'")
            return "DEFAULT_HEADER:{}:%MESSAGE%".format(datetime.today())
        return header

    def format_message(self, level, list_messages):
        if len(list_messages) == 1:
            msg = str(list_messages.pop())
        elif len(list_messages) == 0:
            msg = "<No message>"
        else:
            msg =  "\n\t- ".join([str(item) for item in list_messages])
            
        return self.format_header(level).replace("%MESSAGE%",msg)
