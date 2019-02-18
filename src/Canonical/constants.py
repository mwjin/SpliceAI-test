CL_max=10000
# Maximum nucleotide context length (CL_max/2 on either side of the 
# position of interest)
# CL_max should be an even number

SL=5000
# Sequence length of SpliceAIs (SL+CL will be the input length and
# SL will be the output length)

# directory settings
PROJECT_DIR='/extdata4/baeklab/minwoo/projects/SpliceAI-test'
DATA_DIR='/extdata4/baeklab/minwoo/projects/SpliceAI-test/data'
RESULT_DIR='/extdata4/baeklab/minwoo/projects/SpliceAI-test/results'
MODEL_DIR='/extdata4/baeklab/minwoo/projects/SpliceAI-test/spliceai/models'

# data path settings
REF_GENOME='/extdata6/Minwoo/data/ref-genome/hg19/hg19.fa'
SPLICE_TABLE='/extdata4/baeklab/minwoo/projects/SpliceAI-test/data/gencode_merge_dataset.txt'
SEQUENCE='/extdata4/baeklab/minwoo/projects/SpliceAI-test/data/gencode_merge_sequence.txt'
