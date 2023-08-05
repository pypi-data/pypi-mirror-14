import copy
import random
import time
from itertools import product

import stat_logger
from stat_loader import to_postgres

class ParamGrid(object):
    def __init__(self, experiment_name, log_dir, overwrite=True, **params):
        """ A grid of parameters to run experiments on.

        `log_dir` is the directory to dump raw data to.

        `params` is a set of parameters of the form
        `param_name=[val1, val2, ...]`.
        """
        self.experiment_name = experiment_name
        grid_axes = [[(k, val) for val in params[k]] for k in params.iterkeys()]
        self.parameters = params.keys()
        self.grid_points = [dict(p) for p in product(*grid_axes)]
        random.shuffle(self.grid_points)
        self.n_points = len(self.grid_points)
        self.log_dir = log_dir
        self.overwrite = overwrite
        stat_logger.configure(settings={'log_dir': log_dir},
                              defaults={'exp_name': self.experiment_name})

    def run(self, func, n_runs=1, db_name=None):
        """ Run a function on a grid of parameter settings and log output.

        `func` is a function that takes a StatLogger and a value for each of
        `self.parameters`, and logs statistics generated during its execution
        to the logger.

        After executing this function, `self.logger` will have persisted stats
        to the filesystem.
        """

        for i, grid_point in enumerate(self.grid_points):
            grid_start = time.time()
            print "Running grid point %d of %d..." % (i+1, self.n_points)

            stat_logger.configure(defaults=grid_point)
            stat_logger.configure(defaults={'grid_point_id': i})
            for j in range(n_runs):
                run_start = time.time()
                print "Run %d of %d..." % (j+1, n_runs),
                stat_logger.configure(defaults={'run_id': j})
                func(**grid_point)
                run_end = time.time()
                print "finished in %3f seconds" % (run_end - run_start)
            grid_end = time.time()
            print ("Grid point %d finished in %3f seconds"
                   % (i+1, grid_end - grid_start))

        print "Finalizing logs..."
        stat_logger.finalize()
        print "Done!"
        if db_name:
            self.save_to_db(db_name)

    def save_to_db(self, db_name):
        print "Persisting logs to DB...",
        to_postgres(self.log_dir, db_name, self.experiment_name,
                    overwrite=self.overwrite)
        print "Done!"
