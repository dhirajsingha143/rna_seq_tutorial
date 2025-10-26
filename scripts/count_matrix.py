import os
import glob
import time
import pandas as pd

# SRA files list
sra_numbers = ["SRR7179508", "SRR7179541"]

# Path where your featureCounts outputs are stored
path = "sra_files/bam_files"
files = glob.glob(os.path.join(path, "*.txt"))

if not files:
    print("No featureCounts output files found in the specified path.")
else:
    print("Files found:", files)

file = open(files[0],"rt")

# Reading the file

df = pd.read_csv(file, sep="\t", comment="#", dtype=str)
print(df.head())
print("Initial DataFrame shape:", df.shape)

# see all columns
print("\nColumns in DataFrame:", df.columns.tolist(),"\n")

# Detect sample columns
sample_cols = df.columns[6:].tolist()
print("\nDetected sample columns:", sample_cols,"\n")

# Dropping unnecessary columns
df = df.drop(columns = ['Chr', 'Start', 'End', 'Strand', 'Length'])

# check the shape after dropping columns
print(df.head())
print("DataFrame shape after dropping columns:", df.shape)

# Renaming the sample columns to SRA id list provided above
if len(sample_cols) != len(sra_numbers):
    print("Warning: Number of sample columns does not match number of SRA IDs provided.")
else:
    rename_dict = {old: new for old, new in zip(sample_cols, sra_numbers)}
    df = df.rename(columns=rename_dict)
    print("\nRenamed columns:\n", df.head(), "\n")

# set Geneid as index for easier downstream use
df.set_index("Geneid", inplace=True)

# write outputs
os.makedirs("counts_matrix", exist_ok=True)
csv_out = "counts_matrix/counts_matrix.csv"
df.to_csv(csv_out)

print(f"Wrote counts matrix: {csv_out}")
print("Shape:", df.shape)
