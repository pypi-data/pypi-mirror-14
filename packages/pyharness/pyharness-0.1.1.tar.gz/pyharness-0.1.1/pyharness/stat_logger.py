""" stat_logger: a logger for dumping data in JSON form to the filesystem.

    Example usage:
    # Set up the logger
    >>> configure(settings={'log_dir': 'logs'}, # directory to dump data
                  defaults={'g': 4}) # global params to log w/ each row
    >>> requireLoggers('run', 'iter') # avoid logging unnecessary tables
    >>> run_log = getLogger('run')
    >>> iter_log = getLogger('iter')

    # Run an experiment and log data
    >>> for run_id in range(3):
    >>>     configure(defaults={'run_id': run_id}) # add run_id to each row
    >>>     run_log.log(a=1, b=2) # log a row before the run
    >>>     for timestep in range(5):
    >>>         iter_log.log(timestep=timestep, val=20) # log to a different table
    >>>         iter_log.end_row() # done with this iteration
    >>>     run_log.log(c=10) # log a row after the run
    >>>     run_log.end_row() # done with this run
    >>> finalize() # finish logging

    # load the data we logged from the filesystem and print it.
    >>> logs = load()
    >>> import pprint
    >>> for table_name, table_data in logs.iteritems():
    >>>     pprint.pprint(table_name + ':')
    >>>     pprint.pprint(table_data)

"""
import copy
import json
import logging
import os

LOGGING_CONFIG = {
    'log_dir': None,
}

LOGGING_DEFAULTS = {
}

LOGGERS = {}

REQUIRED_LOGGERS = set()

def configure(settings={}, defaults={}):
    LOGGING_CONFIG.update(**settings)
    LOGGING_DEFAULTS.update(**defaults)

def getLogger(table_name):
    if table_name not in REQUIRED_LOGGERS:
        LOGGERS[table_name] = DummyStatLogger()

    # initialize the logger
    elif table_name not in LOGGERS:
        logger = logging.getLogger(table_name)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        log_dir = LOGGING_CONFIG.get('log_dir')
        if not log_dir:
            raise ValueError("Cannot use StatLogger without a log_dir! "
                             "Did you forget to call `configure()`?")
        log_file = os.path.join(log_dir, table_name + '.json')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logger.handlers = []
        logger.addHandler(logging.FileHandler(log_file))
        with open(log_file, 'w') as f:
            f.write('[')
        LOGGERS[table_name] = StatLogger(logger)

    return LOGGERS[table_name]

def requireLoggers(*table_names):
    REQUIRED_LOGGERS.update(set(table_names))

def finalize(table_names=None):
    if table_names is None:
        table_names = LOGGERS.iterkeys()
    for table_name in table_names:
        getLogger(table_name).finalize()

def load(table_names=None):
    if table_names is None:
        table_names = LOGGERS.iterkeys()
    tables = {}
    for table_name in table_names:
        tables[table_name] = getLogger(table_name).load()
    return tables

class StatLogger(object):
    def __init__(self, logger):
        self.logger = logger
        self.filename = logger.handlers[0].baseFilename
        self.cur_row = {}

    def log(self, **stats):
        self.cur_row.update(stats)

    def end_row(self):
        self.cur_row.update(LOGGING_DEFAULTS)
        message = json.dumps(self.to_json(self.cur_row)) + ','
        self.logger.info(message) # Persist the data
        self.cur_row = {}

    def finalize(self):
        with open(self.filename, 'rb+') as f:
            # remove the last comma in the file
            f.seek(-2, os.SEEK_END) # -2 for the last comma and a newline
            f.truncate()

            # close the json list
            f.write(']')

    def load(self):
        with open(self.filename, 'rb') as f:
            return json.load(f)

    def valid_json(self, value):
        # try coercing to json
        try:
            json.dumps(value)
            return value
        except TypeError:
            pass

        # is it a dictionary? recurse
        if isinstance(value, dict):
            return { k: self.valid_json(v) for k, v in value.iteritems() }

        # Otherwise it must be some unknown class. Just use the class name.
        return value.__name__

    def to_json(self, stats_dict):
        new_dict = {}
        for k, v in stats_dict.iteritems():
            new_dict[k] = self.valid_json(v)
        return new_dict

class DummyStatLogger(object):
    def __init__(self):
        pass

    def log(self, **stats):
        pass

    def end_row(self):
        pass

    def finalize(self):
        pass

    def load(self):
        return {}
