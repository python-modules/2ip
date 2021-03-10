# -*- coding: utf-8 -*-

"""
Set up and handle logging
"""

# Import logging
import logging

# Import sys.exit and errno.EINTR for exception handling
from sys import exit
from errno import EINTR

class Logger(object):

    """
    Logging Module

    This logging handler will use the python "logging" module to output logs. If colorlog is available, the logs will be colored.

    For a slight performance boost, calls to log verbose, debug or trace level events will be skipped when running Python with the Optimize flag (-O).
    If running optimized, colorlog will also not be used.
    """

    ## Set trace and verbose log levels
    logging.TRACE = logging.DEBUG - 5
    logging.VERBOSE = logging.INFO - 5

    ## Set default log level
    def_verbosity = logging.INFO

    ## Set default error code for fatal errors
    def_code = EINTR

    def __init__(self, verbosity: int = def_verbosity) -> object:
        """Initialize logging

        Args:
            verbosity (int, optional): The verbosity level. Defaults to logging.INFO.

        Returns:
            object: logging object
        """
        ## Check if running in optimized mode; if not colorlog may be used
        if __debug__:
            colorlog = True
        else:
            colorlog = False

        ## Configure colorlog if possible, otherwise set up the logging module
        colorlog_setup = self.__setup(colorlog = colorlog)

        ## Add the fatal, trace and verbose log levels and set the handlers
        self.__add_handlers()

        ## Set the logging level
        self.__set_log_level(verbosity = verbosity)

        ## Logging setup completed
        logging.getLogger('twoip').verbose('Logging initialized')

        ## Output colorlog info if it would be enabled
        if colorlog == True and colorlog_setup == False:
            logging.info('Colorlog setup requested but the module could not be loaded; standard logging in use')

    def __add_handlers(self) -> None:
        """Create the levels and handlers for fatal, trace and verbose level logging
        """
        ## Add the trace and verbose levels
        logging.addLevelName(logging.TRACE, 'TRACE')
        logging.addLevelName(logging.VERBOSE, 'VERBOSE')

        ## Set the handlers that will be used to log events at the new levels
        setattr(logging.getLogger('twoip'), 'fatal', self.__log_fatal)
        setattr(logging.getLogger('twoip'), 'trace', self.__log_trace)
        setattr(logging.getLogger('twoip'), 'verbose', self.__log_verbose)

        ## Overwrite the handler for debug level events so that logging can be a noop if not needed
        setattr(logging.getLogger('twoip'), 'debug', self.__log_debug)

    @staticmethod
    def __setup(colorlog: bool) -> bool:
        """Initialize colorlog or perform basic config for logging module if not available

        Returns:
            bool: True if colorlog enabled otherwise False if not enabled
        """
        ## Set the output format for logs
        if __debug__:
            ## Use the CustomLogFactory function to fix up spacing of logged messages
            logging.setLogRecordFactory(CustomLogFactory)
            ## Create the output format with debugging info
            log_format = (
                '{asctime},{msecs:08.4f} - '
                '{levelname:10} - '
                '{func_origin:30} - '
                '{message:>5}'
            )
        else:
            ## Use basic output format
            log_format = (
                '{asctime} - '
                '{levelname:10} - '
                '{message}'
            )

        ## Set date format
        date_format = '%Y-%m-%d:%H:%M:%S'

        ## Check if colorlog should be used
        ## Only attempt to load if not running in optimized mode
        colorlog_imported = False
        if colorlog:
            try:
                from colorlog import ColoredFormatter
            except Exception:
                pass
            else:
                colorlog_imported = True

        ## Set up logging
        if colorlog_imported:
            formatter = ColoredFormatter(
                '{log_color}'
                f'{log_format}',
                datefmt = date_format,
                reset = True,
                style = '{',
                log_colors = {
                    'CRITICAL': 'black,bg_red',
                    'ERROR':    'red',
                    'WARNING':  'yellow',
                    'INFO':     'green',
                    'VERBOSE':  'cyan',
                    'DEBUG':    'purple',
                    'TRACE':    'thin_purple',
                },
            )
            ## Set logging formatter
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logging.getLogger().addHandler(handler)
        else:
            ## Initialize basic logging
            logging.basicConfig(
                format = f'{log_format}',
                datefmt = date_format,
                style = '{',
            )

        if colorlog_imported:
            return True
        else:
            return False

    @staticmethod
    def __set_log_level(verbosity: int) -> None:
        ## Set the available log levels
        levels = {
            0: logging.ERROR,
            1: logging.WARN,
            2: logging.INFO,
            3: logging.VERBOSE,
            4: logging.DEBUG,
            5: logging.TRACE,
        }

        ## Get the logger
        logger = logging.getLogger()

        ## Get the log level that should be used. If the log level is out of range (ie. above 6) the level will default to logging.TRACE
        level = levels.get(verbosity, logging.TRACE)

        ## Set the log level
        logger.setLevel(level)

    @staticmethod
    def __log_trace(message: str, stacklevel: int = 3, *args, **kwargs) -> None:
        """Log a message at the trace level

        Logging is only allowed if the code is not running in optimized mode.

        Args:
            message (str): The message to log
        """
        if __debug__: logging.log(logging.TRACE, message, stacklevel = stacklevel, *args, **kwargs)

    @staticmethod
    def __log_debug(message: str, stacklevel: int = 3, *args, **kwargs) -> None:
        """Log a message at the debug level

        Logging is only allowed if the code is not running in optimized mode.

        Args:
            message (str): The message to log
        """
        if __debug__: logging.log(logging.DEBUG, message, stacklevel = stacklevel, *args, **kwargs)

    @staticmethod
    def __log_verbose(message, stacklevel: int = 3, *args, **kwargs) -> None:
        """Log a message at the verbose level

        Logging is only allowed if the code is not running in optimized mode.

        Args:
            message (str): The message to log
        """
        if __debug__: logging.log(logging.VERBOSE, message, stacklevel = stacklevel, *args, **kwargs)

    @staticmethod
    def __log_fatal(message, stacklevel: int = 3, code: int = def_code, *args, **kwargs) -> None:
        """Log a message at the critical level and exit

        Args:
            message (str): The message to log
            code (int): The exit code to use. Defaults to errno.EINTR.
        """
        logging.critical(message, stacklevel = stacklevel, *args, **kwargs)
        ## Log stack info
        logging.log(logging.DEBUG, f'Exiting with error code {code} due to fatal error', stack_info = True, stacklevel = stacklevel)
        exit(code)

class CustomLogFactory(logging.LogRecord):
    """Custom logging format settings

    If the script is running in optimized mode this will not be used at all.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ## Provide the file name, function name and line number
        self.func_origin = f"{self.filename}.{self.funcName}():{self.lineno}"