import glob
import os
import time

def run_experiment(experiment_name, out_dir=None, db_name=None,
                   do_run=True, do_plot=True, overwrite=True,
                   partition=None):
    # Make sure the output directory exists
    out_dir = os.path.abspath(os.path.join(out_dir, experiment_name))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Find a 'run' or a 'plot' method.
    if do_run:
        partition_desc = 'all' if partition is None else str(partition)
        print
        print "Running experiment:", experiment_name,
        print "on partition", partition_desc
        tmp = __import__('experiments.' + experiment_name, fromlist=['run'])
        pre = time.time()
        try:
            tmp.run(experiment_name, out_dir=out_dir, db_name=db_name,
                    overwrite=overwrite, partition=partition)
        except TypeError: # experiment doesn't support partitioning
            tmp.run(experiment_name, out_dir=out_dir, db_name=db_name,
                    overwrite=overwrite)
        post = time.time()
        print "Done in %.3f seconds." % (post - pre)

    if do_plot:
        print
        print "Generating plots for experiment:", experiment_name
        tmp = __import__('experiments.' + experiment_name, fromlist=['plot'])
        pre = time.time()
        tmp.plot(experiment_name, out_dir=out_dir, db_name=db_name)
        post = time.time()
        print "Done in %.3f seconds." % (post - pre)

def list_experiments():
    modules = [os.path.splitext(os.path.basename(filename))[0] for filename in
               glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))
               if '__init__' not in filename]
    return [m + ': ' + (getattr(__import__('experiments.'+ m), m).__doc__
                        or '(No Description)')
            for m in modules]
