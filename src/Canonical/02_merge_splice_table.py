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
        self.exon_starts = set()
        self.exon_ends = set()

    def __str__(self):
        exon_starts = list(self.exon_starts)
        exon_starts.sort()
        exon_start_str = ''

        for exon_start in exon_starts:
            exon_start_str += '%d,' % exon_start

        exon_ends = list(self.exon_ends)
        exon_ends.sort()
        exon_end_str = ''

        for exon_end in exon_ends:
            exon_end_str += '%d,' % exon_end

        return '%s\t%d\t%s\t%s\t%d\t%d\t%s\t%s' % \
               (self.name, self.iso_cnt, self.chrom, self.strand,
                self.tx_start, self.tx_end, exon_start_str, exon_end_str)

    def merge(self, iso_gene):
        assert self.name == iso_gene.name
        assert self.chrom == iso_gene.chrom
        assert self.strand == iso_gene.strand

        if iso_gene.tx_start < self.tx_start:
            self.tx_start = iso_gene.tx_start

        if self.tx_end < iso_gene.tx_end:
            self.tx_end = iso_gene.tx_end

        self.exon_starts.union(iso_gene.exon_starts)
        self.exon_ends.union(iso_gene.exon_ends)
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

        exon_starts = fields[6].strip(',').split(',')
        exon_ends = fields[6].strip(',').split(',')

        self.exon_starts.update(map(int, exon_starts))
        self.exon_ends.update(map(int, exon_ends))


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
