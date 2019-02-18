#!/usr/bin/env python2.7
"""
Make the splice table for this SpliceAI by parsing gff3 gene annotation file
"""

from __future__ import print_function
from constants import *

import os
import re

# path settings
gencode_path = '/extdata6/Minwoo/data/annotation/gencode_v19/gencode.v19.annotation.gff3'
out_dir = DATA_DIR
out_file_path = SPLICE_TABLE
os.makedirs(out_dir, exist_ok=True)

regex_chr = re.compile('^chr([0-9]{1,2}|[XY])$')

gene_table = {}  # mapping route: chrom -> strand -> gene_name -> transcript_name -> [exon_start_list, exon_end_list]
tx_to_position = {}  # key: transcript name, value: (chrom, strand, start, end)

with open(gencode_path, 'r') as infile:
    for line in infile:
        if line.startswith('#'):  # skip headers
            continue

        fields = line.strip().split('\t')
        chrom = fields[0]
        start = fields[3]
        end = fields[4]
        strand = fields[6]
        info_str = fields[8]
        info_table = {}

        # parse the INFO string
        info_list = info_str.split(';')

        for info in info_list:
            info_key, info_value = info.split('=')
            info_table[info_key] = info_value

        if not regex_chr.match(chrom) or info_table['gene_type'] != 'protein_coding':
            continue

        entry_type = fields[2]

        if entry_type == 'gene':
            gene_name = info_table['gene_name']

            if chrom not in gene_table:
                gene_table[chrom] = {}

            if strand not in gene_table[chrom]:
                gene_table[chrom][strand] = {}

            gene_table[chrom][strand][gene_name] = {}

        elif entry_type == 'transcript':
            gene_name = info_table['gene_name']
            tx_name = info_table['transcript_name']
            gene_table[chrom][strand][gene_name][tx_name] = [[], []]
            tx_to_position[tx_name] = (chrom, strand, start, end)

        elif entry_type == 'exon':
            gene_name = info_table['gene_name']
            tx_name = info_table['transcript_name']
            gene_table[chrom][strand][gene_name][tx_name][0].append(start)
            gene_table[chrom][strand][gene_name][tx_name][1].append(end)

with open(out_file_path, 'w') as outfile:
    for chrom in gene_table:
        for strand in gene_table[chrom]:
            for gene_name in gene_table[chrom][strand]:
                tx_num = 0

                for tx_name in gene_table[chrom][strand][gene_name]:
                    _, _, tx_start, tx_end = tx_to_position[tx_name]
                    exon_starts, exon_ends = gene_table[chrom][strand][gene_name][tx_name]

                    if len(exon_starts) == 1:
                        continue

                    junc_start_str = ''
                    junc_end_str = ''

                    for i in range(1, len(exon_starts)):
                        junc_start_str += '%s,' % exon_ends[i - 1]
                        junc_end_str += '%s,' % exon_starts[i]

                    print(gene_name, tx_num, chrom, strand, tx_start, tx_end, junc_start_str, junc_end_str,
                          sep='\t', end='\n', file=outfile)
                    tx_num += 1
