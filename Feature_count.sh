#!/bin/bash

path="./"
path2="./NetResult"
gft_file="/path/to/Mus_musculus.GRCm39.112.gtf"

gffread -T -o- ${gft_file} | awk '{if($9 ~ /gene_id/ && $9 ~ /gene_name/) print $0}' > modified.gtf

# Generate a count matrix for all samples combined
featureCounts -T 12 -p -s 2 -a ${gft_file} \
              -o ${path}/counts_gene_name.txt -g gene_id \
              ${path}*.bam

cut -f1,6- ${path}/counts_gene_name.txt >  ${path}/gene_count_matrix.txt

# Run MultiQC
multiqc ${path}. -o ${path}

gffread -T -o- "/Users/mostafa/Desktop/elham/Mus_musculus.GRCm39.112.gtf" | \
awk -F '\t' '$3 == "gene" {print $9}' | \
awk -F '; ' '{gene_id=""; gene_name=""; for(i=1;i<=NF;i++) {if ($i ~ /gene_id/) {gene_id=$i}; if ($i ~ /gene_name/) {gene_name=$i}} if (gene_id && gene_name) print gene_id, gene_name}' | \
sort | uniq > gene_id_to_name.txt

python3 ${path2}/Data_fromat.py  

