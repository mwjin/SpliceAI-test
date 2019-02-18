#!/usr/bin/env python2.7
"""
By parsing the splice table we made,
merge transcript start/end sites and splice sites of multiple isoforms with same gene name
"""

from __future__ import print_function
from constants import DATA_DIR

# path settings
in_file_path = '%s/gencode_dataset.txt' % DATA_DIR
out_file_path = in_file_path.replace('gencode', 'gencode_merge')


class Gene:
    def __init__(self):
        self.name = ''
        self.iso_cnt = 0
        self.chrom = ''
        self.strand = ''
        self.tx_start = 0
        self.tx_end = 0

        # for splice sites
        self.junc_starts = set()
        self.junc_ends = set()

    def __str__(self):
        junc_starts = list(self.junc_starts)
        junc_starts.sort()
        junc_start_str = ''

        for junc_start in junc_starts:
            junc_start_str += '%d,' % junc_start

        junc_ends = list(self.junc_ends)
        junc_ends.sort()
        junc_end_str = ''

        for junc_end in junc_ends:
            junc_end_str += '%d,' % junc_end

        return '%s\t%d\t%s\t%s\t%d\t%d\t%s\t%s' % \
               (self.name, self.iso_cnt, self.chrom, self.strand,
                self.tx_start, self.tx_end, junc_start_str, junc_end_str)

    def merge(self, iso_gene):
        assert self.name == iso_gene.name
        assert self.chrom == iso_gene.chrom
        assert self.strand == iso_gene.strand

        if iso_gene.tx_start < self.tx_start:
            self.tx_start = iso_gene.tx_start

        if self.tx_end < iso_gene.tx_end:
            self.tx_end = iso_gene.tx_end

        self.junc_starts = self.junc_starts.union(iso_gene.junc_starts)
        self.junc_ends = self.junc_ends.union(iso_gene.junc_ends)
        self.iso_cnt += 1

    def parse_dataset_entry(self, line_entry):
        assert self.name == ''

        fields = line_entry.strip().split('\t')
        self.name = fields[0]
        self.iso_cnt += 1
        self.chrom = fields[2]
        self.strand = fields[3]
        self.tx_start = int(fields[4])
        self.tx_end = int(fields[5])

        junc_starts = fields[6].strip(',').split(',')
        junc_ends = fields[7].strip(',').split(',')

        self.junc_starts.update(map(int, junc_starts))
        self.junc_ends.update(map(int, junc_ends))


gene_table = {}  # key: {gene_name}_{chrom}_{strand}, value: 'Gene' object

with open(in_file_path, 'r') as infile:
    for line in infile.readlines():
        gene = Gene()
        gene.parse_dataset_entry(line)
        gene_table_key = '%s_%s_%s' % (gene.name, gene.chrom, gene.strand)

        if gene_table_key in gene_table:
            gene_table[gene_table_key].merge(gene)
        else:
            gene_table[gene_table_key] = gene

with open(out_file_path, 'w') as outfile:
    for gene in gene_table.values():
        print(gene, file=outfile)
