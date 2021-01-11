import logging
import sys
import time

class Logger(object):
    # Logger class
    # For further information please refer to https://docs.python.org/3/library/logging.html
    '''
    CRITICAL: 50
    ERROR: 40
    WARNING: 30
    INFO: 20
    DEBUG: 10
    NOTSET: 0
    '''
    
    instance = None
    def __init__(self,
                logger_name = 'Logger',
                address = '',
                level = logging.DEBUG,
                console_level = logging.ERROR,
                file_level = logging.DEBUG,
                mode = 'a'):

        super(Logger, self).__init__()
        if not Logger.instance:
            logging.basicConfig()
            
            Logger.instance = logging.getLogger(logger_name)
            Logger.instance.setLevel(level)
            Logger.instance.propagate = False
    
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(console_level)
            Logger.instance.addHandler(console_handler)
            
            file_handler = logging.FileHandler(address, mode = mode)
            file_handler.setLevel(file_level)
            formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s')
            file_handler.setFormatter(formatter)
            Logger.instance.addHandler(file_handler)
    
    def _correct_message(self, message):
        output = message + "\n"
        return output
        
    def debug(self, message):
        Logger.instance.debug(self._correct_message(message))

    def info(self, message):
        Logger.instance.info(self._correct_message(message))

    def warning(self, message):
        Logger.instance.warning(self._correct_message(message))

    def error(self, message):
        Logger.instance.error(self._correct_message(message))

    def critical(self, message):
        Logger.instance.critical(self._correct_message(message))

    def exception(self, message):
        Logger.instance.exception(self._correct_message(message))

if __name__ == "__main__":
    
    myLogger = Logger(address = "log.log")
    myLogger.info('Hi')
