import glob
import os
import time


def run_experiment(experiment_name, exp_home=None,
                   out_dir=None, db_name=None,
                   do_run=True, do_plot=True, overwrite=True,
                   partition=None):
    # Make sure the output directory exists
    out_dir = os.path.abspath(os.path.join(out_dir, experiment_name))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Move to the experiment home directory
    try:
        old_dir = os.getcwd()
        os.chdir(exp_home)

        # Import the module
        try:
            experiment_module = __import__(experiment_name, globals(), locals(),
                                           ['run', 'plot'])
        except ImportError as e:
            print "Couldn't import module", experiment_name + ":", str(e)
            return

        # Run the experiment
        if do_run:
            partition_desc = 'all' if partition is None else str(partition)
            print
            print "Running experiment '%s' on partition '%s'..." % (
                experiment_name, partition_desc)
            exec_module_method(
                experiment_module, 'run', experiment_name, out_dir=out_dir,
                db_name=db_name, overwrite=overwrite, partition=partition)

        # Plot the output
        if do_plot:
            print
            print "Generating plots for experiment:", experiment_name
            exec_module_method(
                experiment_module, 'plot', experiment_name, out_dir=out_dir,
                db_name=db_name)
    finally:
        os.chdir(old_dir)


def time_exec(method, *args, **kwargs):
    pre = time.time()
    try:
        method(*args, **kwargs)
    except TypeError as e:
        print "Method's signature is incorrect:", e.message
    except Exception as e:
        print "Error running method:", str(e)
    post = time.time()
    print "Done in %.3f seconds." % (post - pre)


def exec_module_method(module, method_name, *args, **kwargs):
    method = getattr(module, method_name, None)
    def _method(*args, **kwargs):
        if not method:
            print "Experiment", module.__name__,
            print "doesn't define a '%s' method. Nothing to do." % method_name
        else:
            method(*args, **kwargs)
    time_exec(_method, *args, **kwargs)


def list_experiments(experiment_home):
    try:
        old_dir = os.getcwd()
        os.chdir(experiment_home)
        modules = [
            os.path.splitext(os.path.basename(filename))[0]
            for filename in glob.glob('./*.py')
            if '__init__' not in filename
        ]
        output = []
        for m in modules:
            description = m + ': '
            try:
                module = __import__(m, globals(), locals())
                if not hasattr(module, 'run'):
                    continue
                description += module.__doc__ or '(No Description)'
            except ImportError as e:
                description += 'Import Error: ' + str(e)
            output.append(description)
    finally:
        os.chdir(old_dir)
    return output
