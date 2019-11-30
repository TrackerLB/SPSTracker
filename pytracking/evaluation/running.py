import numpy as np
import multiprocessing
import os
from itertools import product
from pytracking.evaluation import Sequence, Tracker
from os import makedirs
from os.path import join, isdir, isfile
from pytracking.evaluation.utils.pyvotkit.region import vot_float2str
from os.path import split

def run_sequence(seq: Sequence, tracker: Tracker, debug=False):
    """Runs a tracker on a sequence."""
    base_results_path = '{}/baseline/{}'.format(tracker.results_dir, seq.name)
    results_path = '{}.txt'.format(base_results_path)
    times_path = '{}_time.txt'.format(base_results_path)

    if os.path.isfile(results_path) and not debug:
        return

    print('Tracker: {} {} {} ,  Sequence: {}'.format(tracker.name, tracker.parameter_name, tracker.run_id, seq.name))

    if debug:
        tracked_bb, exec_times = tracker.run(seq, debug=debug)
    else:
        try:
            tracked_bb, exec_times = tracker.run(seq, debug=debug)
        except Exception as e:
            print(e)
            return
    path = base_results_path.split('/')
    path = path[-1]
    
    if not isdir(base_results_path): makedirs(base_results_path)
    results_path = join(base_results_path, '{:s}_001.txt').format(path)
    #'{}.txt'.format(base_results_path)
    with open(results_path, "w") as fin:
            for x in tracked_bb:
                fin.write("{:d}\n".format(x)) if isinstance(x, int) else \
                        fin.write(','.join([vot_float2str("%.4f", i) for i in x]) + '\n')
    # tracked_bb = np.array(tracked_bb).astype(int)
    exec_times = np.array(exec_times).astype(float)

    print('FPS: {}'.format(len(exec_times) / exec_times.sum()))
    # if not debug:
    #     np.savetxt(results_path, tracked_bb, delimiter='\t', fmt='%d')
    #     np.savetxt(times_path, exec_times, delimiter='\t', fmt='%f')


def run_dataset(dataset, trackers, debug=False, threads=0):
    """Runs a list of trackers on a dataset.
    args:
        dataset: List of Sequence instances, forming a dataset.
        trackers: List of Tracker instances.
        debug: Debug level.
        threads: Number of threads to use (default 0).
    """
    if threads == 0:
        mode = 'sequential'
    else:
        mode = 'parallel'

    if mode == 'sequential':
        for seq in dataset:
            for tracker_info in trackers:
                run_sequence(seq, tracker_info, debug=debug)
    elif mode == 'parallel':
        param_list = [(seq, tracker_info, debug) for seq, tracker_info in product(dataset, trackers)]
        with multiprocessing.Pool(processes=threads) as pool:
            pool.starmap(run_sequence, param_list)
    print('Done')
