#!/bin/bash
#project_id="PRJNA705172"
read -p "Enter the GEO project ID: " GEO_PROJECT_ID
# Prompt the user for the directory where the data should be saved
read -p "Enter the directory where you want to save the data: " path
# Create the directory if it doesn't exist
mkdir -p "$path"
# Change to the specified directory
cd "$path"
path="./"

esearch -db sra -query $GEO_PROJECT_ID | efetch -format xml | xtract -pattern EXPERIMENT_PACKAGE \
-element RUN@accession RUN@size | awk '{printf "%s\t%.2f GB\n", $1, $2/1024/1024/1024}' > Samples_SRS_Acc_numb.txt


# Read the SRA file information from the text file
mapfile -t sra_files < Samples_SRS_Acc_numb.txt

# Display the options to the user
echo "Select the corresponding numbers to download the SRA files (separated by spaces):"
index=1
for line in "${sra_files[@]}"; do
    echo "$index. $line"
    ((index++))
done

# Prompt user for selection
read -p "Enter the numbers: " choices

# Loop over each choice, download the corresponding file, and convert it in parallel
for choice in $choices; do
    if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt "${#sra_files[@]}" ]; then
        echo "Invalid selection: $choice"
    else
        selected_line=${sra_files[$((choice - 1))]}
        accession=$(echo $selected_line | awk '{print $1}')
        echo "Downloading and converting $accession..."
        
        # Download with prefetch and convert to FASTQ in parallel
        prefetch $accession
        
    fi
  done

for files in {$path}*; do fasterq-dump --split-files $files; done

fastqc ${path}*.fastq

# Wait for all background processes to complete
wait
echo "All downloads and conversions complete."
