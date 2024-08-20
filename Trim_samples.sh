#!/bin/bash
path_in="./"
trim_galore="/pah/to/trim_galore"
genome_index="/path/to/mousegenome_index"
# Run FastQC on all FASTQ files
fastqc ${path_in}*.fastq

# Trim your files

	#	-q 20: Trims low-quality ends from reads (default is 20).
	#	--length 30: Discards reads that become shorter than 30 bp after trimming.
	#	--paired: Specifies that the input files are paired-end.
	#	--fastqc: Runs FastQC after trimming.
	#	-o ${path_in}: Specifies the output directory.

for forward_read in ${path_in}/*_1.fastq; do
    # Define the reverse read file by replacing _1.fastq with _2.fastq
    reverse_read="${forward_read/_1.fastq/_2.fastq}"
    
    # Run Trim Galore with the specified options
    $trim_galore -q 20 --length 30 --paired --fastqc "${forward_read}" "${reverse_read}" --output_dir "${path_in}"

done


$trim_galore   -q 20 --length 30  --paired --fastqc *.fastq --output_dir ${path_in}
# Map your files

# Loop through all files in the input directory with the suffix '_1_trimmed.fq'

for file in ${path_in}*_1_val_1.fq; do
    echo $file
    # Extract the prefix by removing the path and the '_val_1.fq' suffix
    prefix=$(basename "$file" "_1_val_1.fq" )
    echo $prefix
    # Define the corresponding reverse read file using the prefix
    reverse_file="${path_in}${prefix}_2_val_2.fq"
    
    # Debug: Print the full paths of the input files
   # echo "Forward read file: $file"
   # echo "Reverse read file: $reverse_file"
    
    # Check if the files exist
    if [[ ! -f "$file" ]]; then
        echo "Error: Forward read file not found: $file"
        continue
    fi
    if [[ ! -f "$reverse_file" ]]; then
        echo "Error: Reverse read file not found: $reverse_file"
        continue
    fi

    # Run STAR alignment with the specified options
    STAR --genomeDir "${genome_index}" \
         --runThreadN 12  \
         --readFilesIn "${file}" "${reverse_file}"  \
         --outFileNamePrefix "${path_in}${prefix}_tri" \
         --outSAMtype BAM SortedByCoordinate \
         --outSAMunmapped Within \
         --outSAMattributes Standard
    
    # Optionally, print a message to indicate that this iteration is complete
    echo "Alignment complete for prefix: ${prefix}"
    echo "Log saved to ${path_in}${prefix}_star.log"
done