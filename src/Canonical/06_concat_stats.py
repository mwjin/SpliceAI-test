#!/usr/bin/env python3
"""
Temporary code
"""

from utils import chrom_list
from constants import RESULT_DIR

import re

stats_path_format = '{0}/SpliceAI_10K_gencode_merge_%s.txt'.format(RESULT_DIR)
chroms = chrom_list()

# key: chrom, value: [acceptor_top_k_accuracy, acceptor_AUC, donor_top_k_accuracy, donor_AUC]
float_regex = re.compile('0[.]\d{4}')

for chrom in chroms:
    chrom_stats_path = stats_path_format % chrom
    acceptor_topk = ''
    acceptor_auc = ''
    donor_topk = ''
    donor_auc = ''
    avg_topk = ''
    avg_auc = ''

    with open(chrom_stats_path, 'r') as infile:
        lines = infile.readlines()
        if len(lines) > 0:
            acceptor_topk = float_regex.findall(lines[2])[1]
            acceptor_auc = float_regex.findall(lines[3])[0]
            donor_topk = float_regex.findall(lines[6])[1]
            donor_auc = float_regex.findall(lines[7])[0]
            avg_topk = '%.4f' % ((float(acceptor_topk) + float(donor_topk)) / 2)
            avg_auc = '%.4f' % ((float(acceptor_auc) + float(donor_auc)) / 2)

    print(chrom, acceptor_topk, acceptor_auc, donor_topk, donor_auc, avg_topk, avg_auc, sep='\t')
