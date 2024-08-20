import pandas as pd
import os

path="./NetResult/"
file_path = f"{path}/reformatted_gene_data.csv"

# Read the data into a DataFrame Genen name 
#data = []
#with open(path, 'r') as f:
#    for line in f:
        # Split the line into components
#        parts = line.strip().split()
#        # Extract gene_id and gene_name
#        gene_id = parts[1].replace('"', '')
#        gene_name = parts[3].replace('"', '')
#        # Append to the data list
#        data.append([gene_id, gene_name])

# Convert the data list to a DataFrame
#df = pd.DataFrame(data, columns=['gene_id', 'gene_name'])

# Save the DataFrame to a CSV file or display it
#df.to_csv('reformatted_gene_data.csv', index=False)
#df = pd.read_csv(f"{path}/reformatted_gene_data.csv")

# Load the gene_id to gene_name mapping file into a DataFrame
gene_names = pd.read_csv('reformatted_gene_data.csv')

print("Gene Names DataFrame columns:", gene_names.columns)


# Load the gene count matrix file into a DataFrame
gene_counts = pd.read_csv(f"{path}/gene_count_matrix copy.txt", sep='\t', comment='#', skiprows=1)
gene_counts = gene_counts.rename(columns={gene_counts.columns[0]: 'gene_id'}) #unify  name of first column 
print("Original columns:", gene_counts.columns)

# Function to trim the column names using basename
def trim_column_name(column_name):
    # Use basename to get the last part of the path
    base_name = os.path.basename(column_name)
    # Further split to get the first part before '_'
    return base_name.split('_')[0]

# Create a dictionary to rename only the columns from the third column onwards
columns_to_rename = {col: trim_column_name(col) for col in gene_counts.columns[2:]}

# Rename the columns in the DataFrame
gene_counts = gene_counts.rename(columns=columns_to_rename)

# Print columns after renaming to verify
print("Renamed columns:", gene_counts.columns)

# Merge the gene names into the gene count matrix based on gene_id
merged_data = pd.merge(gene_names, gene_counts, on='gene_id', how='right')

# Save the merged DataFrame to a new file
merged_data.to_csv('merged_gene_count_matrix.txt', sep='\t', index=False)

