import subprocess
import time
import os
import glob

# SRA files list
sra_numbers = ["SRR7179508", "SRR7179541"]

# Current working directory
print("Current Working directory:", os.getcwd())

# Make Directory to save files
os.makedirs("sra_files", exist_ok=True)

# Change to new directory created
os.chdir("sra_files") 

# Downloading files in new directory
print("Downloading files in:", os.getcwd())

# Single End Reads Trimming automation

for sra_id in sra_numbers:

    os.chdir(sra_id)
    print("SRA file directory:", os.getcwd())

    os.chdir("fastq_files")
    print("FASTQ file directory:", os.getcwd())

    print("Trimming using Trimmomatic for:", sra_id)

    for f in glob.glob(f"{sra_id}*.fastq.gz"):
        print(f"File {f} Trimming started")
        start = time.time()
        subprocess.run([
            "trimmomatic", "SE", "-phred33",
            f,
            f"{sra_id}_trimmed.fastq.gz",
            "LEADING:3", "TRAILING:3", "SLIDINGWINDOW:4:15", "MINLEN:36"
        ])
        end = time.time()
        time_taken = (end - start) / 60
        print(f"Time taken to trim file {f}:", f"{time_taken:.2f} minutes")
        os.chdir("../..")