#!/extdata6/Doyeon/anaconda3/envs/minu/bin/python3
"""
Make jobs to test SpliceAI
"""

from lab.job import Job, qsub_sge
from lab.utils import time_stamp
from constants import PROJECT_DIR, DATA_DIR, RESULT_DIR
from utils import chrom_list

import os
import sys


def main():
    """
    Bootstrap
    """
    # job scheduler settings
    queue = '24_730.q'
    is_test = True

    prev_job_prefix = 'Minu.SpliceAI.Preprocess.Data'
    job_name_prefix = 'Minu.SpliceAI.Test.Model'
    log_dir = '%s/log/%s/%s' % (PROJECT_DIR, job_name_prefix, time_stamp())

    # path settings
    dataset_path_format = '{0}/gencode_merge_dataset_%s.h5'.format(DATA_DIR)
    output_dir = RESULT_DIR
    os.makedirs(output_dir, exist_ok=True)
    output_path_format = '{0}/SpliceAI_10K_gencode_merge_%s.txt'.format(output_dir)

    jobs = []
    test_model_script = '%s/src/Canonical/test_model.py' % PROJECT_DIR

    chroms = chrom_list()

    for chrom in chroms:
        dataset_path = dataset_path_format % chrom
        output_path = output_path_format % chrom
        cmd = '%s 10000 %s > %s' % (test_model_script, dataset_path, output_path)

        if is_test:
            print(cmd)
        else:
            prev_job_name = '%s.%s' % (prev_job_prefix, chrom)
            one_job_name = '%s.%s' % (job_name_prefix, chrom)
            one_job = Job(one_job_name, cmd, hold_jid=prev_job_name)
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
