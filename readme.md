# RNA-seq Data Processing Automation Script

This automated script is designed to process RNA-seq data from the Gene Expression Omnibus (GEO) using a project ID. The script follows a standard RNA-seq analysis pipeline, allowing users to download, preprocess, and analyze sequencing data efficiently.

## Features

1. **Automated Download of SRA Files**:
    - The script automates the download of any number of SRS files using a GEO project ID.
    - It outputs a detailed list of SRS identifiers for all project samples along with their sizes in GB.

2. **Selective Download and Conversion**:
    - Users can choose specific SRS IDs (separated by space) to download in SRA format.
    - The downloaded SRA files are then converted to FASTQ format.

3. **Quality Control Analysis**:
    - The script performs quality control analysis on the raw FASTQ files for any number of samples.
    - It assesses the quality of the data using tools like FastQC.

4. **Trimming with Trim Galore**:
    - Raw data is trimmed using Trim Galore to maintain high-quality reads for downstream analysis.

5. **Alignment with STAR**:
    - The trimmed data is aligned using STAR in a paired-end design.
    - This step prepares the data for further analysis by aligning reads to the reference genome.

6. **Feature Counting**:
    - All aligned data is processed through the feature counting script to generate a count matrix.
    - The matrix file contains genes as rows and samples as columns.

7. **MultiQC Report Generation**:
    - A comprehensive report summarizing quality control metrics, trimming, and alignment steps is generated using MultiQC.

8. **Reformatting Gene Count Matrix**:
    - The gene count matrix file is reformatted to have two columns: `gene_id` and `gene_count`.

9. **Merging Gene Names**:
    - Due to an issue in feature counting, gene names are retrieved separately and merged into a final file named `merged_gene_count_matrix`.
    - This file includes `gene_id`, `Length`, and the SRA IDs as columns.

## Requirements

- Python 3.x
- FastQC
- Trim Galore
- STAR
- FeatureCounts
- MultiQC
- SRA Toolkit

## Installation
Step 1: Set Up the Environment

To install the required tools and packages, you can follow the installation guides for each tool or use package managers like `conda` or `brew` (for macOS).

Example using `conda`:


conda create -n rnaseq-env python=3.8
conda activate rnaseq-env
conda install -c bioconda fastqc trim-galore star featurecounts multiqc sra-tools

# Step 2: Install the Automation Scripts

This section provides instructions to install the required automation scripts: Greb_data.sh, Trim_samples.sh, Feature_Count.sh, and Data_formate.py.

1. Greb_data.sh Installation

	•	Purpose: This script automates the download of SRA files and their conversion to FASTQ format.
```bash

cp path/to/Greb_data.sh  <GEO_PROJECT_ID>  ~/rnaseq-scripts/ 
chmod +x ~/rnaseq-scripts/Greb_data.sh
```
2. Trim_samples.sh Installation

•	Purpose: This script handles trimming of raw data, alignment using STAR, and MultiQC report generation.

```bash
cp path/to/Trim_samples.sh ~/rnaseq-scripts/
chmod +x ~/rnaseq-scripts/Trim_samples.sh
```

3. Feature_Count.sh Installation

	•	Purpose: This script is used for feature counting and generating a count matrix.
```bash
cp path/to/Feature_Count.sh ~/rnaseq-scripts/
chmod +x ~/rnaseq-scripts/Feature_Count.sh
```

4. Data_formate.py Installation

	•	Purpose: This Python script reformats the gene count matrix and merges gene names with the count matrix.

```bash
cp path/to/Data_formate.py ~/rnaseq-scripts/
chmod +x ~/rnaseq-scripts/Data_formate.py
```

Usage

Once the scripts are installed, follow these steps to process your RNA-seq data:

	1.	Download SRA Files and Convert to FASTQ:
Greb_data.sh <GEO_PROJECT_ID>  <input_fastq_directory>
•	This will output SRA and FASTQ files.

	2.	Trim, Align, and Generate MultiQC Report:
Trim_samples.sh <input_fastq_directory>

	This script will produce .trim, .aligned, and MultiQC files.

	3.	Run Feature Counting:
Feature_Count.sh <aligned_bam_directory>

•	Outputs counts_gene_name.txt and gene_id_to_name.txt.

	4.	Reformat Gene Count Matrix:
Data_formate.py <input_count_matrix>
•	Produces reformatted_gene_data.csv and merged_gene_count_matrix.txt.




