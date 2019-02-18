CL_max=10000
# Maximum nucleotide context length (CL_max/2 on either side of the 
# position of interest)
# CL_max should be an even number

SL=5000
# Sequence length of SpliceAIs (SL+CL will be the input length and
# SL will be the output length)

# directory settings
project_dir='/extdata4/baeklab/minwoo/project/SpliceAI-test'
data_dir='/extdata4/baeklab/minwoo/project/SpliceAI-test/data'
result_dir='/extdata4/baeklab/minwoo/project/SpliceAI-test/results'

# data path settings
ref_genome='/extdata6/Minwoo/data/ref-genome/hg19/hg19.fa'
splice_table='/extdata4/baeklab/minwoo/projects/SpliceAI-test/data/canonical_dataset.txt'
sequence='/extdata4/baeklab/minwoo/projects/SpliceAI-test/data/canonical_sequence.txt'
