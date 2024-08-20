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

To install the required tools and packages, you can follow the installation guides for each tool or use package managers like `conda` or `brew` (for macOS).

Example using `conda`:

```bash
conda create -n rnaseq-env python=3.8
conda activate rnaseq-env
conda install -c bioconda fastqc trim-galore star featurecounts multiqc sra-tools