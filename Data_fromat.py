import pandas as pd
import os

#file_path = f"{path}/reformatted_gene_data.csv"

# Ask for the directory to save the data
path_in = input("Enter the directory where you want to save the data: ").strip()

# Validate the directory path
if os.path.isdir(path_in):
    print(f"The directory '{path_in}' is valid.")
else:
    print(f"The directory '{path_in}' does not exist. Please check the path and try again.")
    exit(1)  # Exiting with status 1 to indicate an error

# Ask for the genome index GTF file directory
geneome_index_GTF_path = input("Enter the directory where the genome index GTF file (unzipped form/decompressed form) is located: ").strip()

# Validate the file path
if os.path.isfile(geneome_index_GTF_path):
    print(f"The file '{geneome_index_GTF_path}' is valid.")
    
else:
    print(f"The file '{geneome_index_GTF_path}' does not exist. Please check the path and try again.")
    exit(1)  # Exiting with status 1 to indicate an error

data = []

with open(geneome_index_GTF_path, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        
        # Split the line into columns based on tab character
        parts = line.strip().split('\t')
        
        # Check if the feature type is 'gene' (3rd column in GTF format)
        if len(parts) > 2 and parts[2] == 'gene':
            # Extract the attributes column (the last column in the GTF format)
            attributes = parts[8]
            
            # Initialize gene_id and gene_name
            gene_id = ""
            gene_name = ""
            
            # Split the attributes by '; ' and extract gene_id and gene_name
            for attribute in attributes.split('; '):
                if attribute.startswith('gene_id'):
                    gene_id = attribute.split(' ')[1].replace('"', '')
                elif attribute.startswith('gene_name'):
                    gene_name = attribute.split(' ')[1].replace('"', '')

            # Append the extracted information to the data list if both gene_id and gene_name are found
            if gene_id and gene_name:
                data.append([gene_id, gene_name])

# Convert the data list to a DataFrame
df = pd.DataFrame(data, columns=['gene_id', 'gene_name'])

# Remove duplicates to ensure unique gene_id and gene_name pairs
df = df.drop_duplicates()

# Display the DataFrame to verify
print(df)
# Save the DataFrame to a CSV file or display it
df.to_csv(f"{path_in}/reformatted_gene_data.csv", index=False)
df = pd.read_csv(f"{path_in}/reformatted_gene_data.csv")

# Load the gene_id to gene_name mapping file into a DataFrame
gene_names = pd.read_csv('reformatted_gene_data.csv')

print("Gene Names DataFrame columns:", gene_names.columns)

# Ask for the genome index GTF file directory
gene_count_matrix_path = input("Enter the directory where the  gene_count_matrix file is located: ").strip()

# Validate the file path
if os.path.isfile(gene_count_matrix_path):
    print(f"The file '{gene_count_matrix_path}' is valid.")
   
else:
    print(f"The file '{gene_count_matrix_path}' does not exist. Please check the path and try again.")
    exit(1)  # Exiting with status 1 to indicate an error


# Load the gene count matrix file into a DataFrame
print(gene_count_matrix_path)
gene_counts = pd.read_csv(gene_count_matrix_path, sep='\t', comment='#', skiprows=1)
gene_counts = gene_counts.rename(columns={gene_counts.columns[0]: 'gene_id'}) #unify  name of first column 


# Remove duplicates based on 'gene_id'
gene_names = gene_names.drop_duplicates(subset='gene_id')
gene_counts = gene_counts.drop_duplicates(subset='gene_id')

# Verify the uniqueness
print("Unique gene_ids in gene_names:", gene_names['gene_id'].nunique())
print("Unique gene_ids in gene_counts:", gene_counts['gene_id'].nunique())

# Merge the gene names into the gene count matrix based on gene_id
merged_data = pd.merge(gene_names, gene_counts, on='gene_id', how='right')


# Save the merged DataFrame to a new file
merged_data.to_csv(f"{path_in}/merged_gene_count_matrix.csv", sep='\t', index=False)

