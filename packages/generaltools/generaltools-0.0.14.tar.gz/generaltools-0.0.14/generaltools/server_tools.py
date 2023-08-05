import logging
import ConfigParser
import sys

from generaltools import log_tools

class GeneralServer(object):
    """ Server Functions that all Servers should contain.
    """
    def __init__(self, config_file=None, config_path="./"):
        if config_file:
            self.config = ConfigParser.ConfigParser()
            self.config.read("{}{}".format(config_path, config_file))

    def _handler(self, signum, frame):
        r'''A handler for Ctrl-c that exists the code. Allows to terminate the
        program by hand.'''
        self.log.error("The file detection server has been stopped")
        raise sys.exit()

    def _init_logger(self, log_directory, log_name):
        """ Set up a logging file """
        return log_tools.init_logger(log_name=log_name,
                                     log_directory=log_directory,
                                     log_level=logging.DEBUG)
