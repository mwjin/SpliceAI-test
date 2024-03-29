#!/bin/bash

source constants.py

CLr=$((CL_max/2))
CLl=$(($CLr+1))
# First nucleotide not included by BEDtools

cat $SPLICE_TABLE | awk -v CLl=$CLl -v CLr=$CLr '{print $3"\t"($5-CLl)"\t"($6+CLr)}' > temp.bed

bedtools getfasta -bed temp.bed -fi $REF_GENOME -fo $SEQUENCE -tab

rm temp.bed
