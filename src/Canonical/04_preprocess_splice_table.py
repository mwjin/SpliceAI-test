#!/extdata6/Doyeon/anaconda3/envs/minu/bin/python3
"""
Make jobs to make .h5 file for training and testing
For this script, a python3 interpreter with installed minwoooj/lab-modules is necessary.
"""

from lab.job import Job, qsub_sge
from lab.utils import time_stamp
from constants import PROJECT_DIR, DATA_DIR
from utils import chrom_list

import sys


def main():
    """
    Boostrap
    """
    # job scheduler settings
    queue = 'optiplex.q'
    is_test = False

    job_name_prefix = 'Minu.SpliceAI.Preprocess.Data'
    log_dir = '%s/log/%s/%s' % (PROJECT_DIR, job_name_prefix, time_stamp())

    jobs = []

    datafile_script = '%s/src/Canonical/create_datafile.py' % PROJECT_DIR
    dataset_script = '%s/src/Canonical/create_dataset.py' % PROJECT_DIR
    chroms = chrom_list()

    for chrom in chroms:
        datafile_path = '%s/gencode_merge_datafile_%s.h5' % (DATA_DIR, chrom)
        dataset_path = '%s/gencode_merge_dataset_%s.h5' % (DATA_DIR, chrom)

        cmd = '%s %s %s %s;' % (datafile_script, chrom, 'all', datafile_path)
        cmd += '%s %s %s;' % (dataset_script, datafile_path, dataset_path)

        if is_test:
            print(cmd)
        else:
            one_job_name = '%s.%s' % (job_name_prefix, chrom)
            one_job = Job(one_job_name, cmd)
            jobs.append(one_job)

    if not is_test:
        qsub_sge(jobs, queue, log_dir)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        function_name = sys.argv[1]
        function_parameters = sys.argv[2:]

        if function_name in locals().keys():
            locals()[function_name](*function_parameters)
        else:
            sys.exit('ERROR: function_name=%s, parameters=%s' % (function_name, function_parameters))
