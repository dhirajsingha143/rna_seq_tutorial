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

for sra_id in sra_numbers:

    os.chdir(sra_id)
    print("SRA file directory:", os.getcwd())

    os.chdir("fastq_files")
    print("FASTQ file directory:", os.getcwd())

    for f in glob.glob(f"{sra_id}_trimmed.fastq.gz"):
        print("Quality control for:", f)
        start = time.time()
        subprocess.run(["fastqc", f])
        end = time.time()
        time_taken = (end - start) / 60
        print("Time taken for quality control:", f"{time_taken:.2f} minutes")

        os.chdir("../..")

# Destination change of zipped fastq files
cwd = os.getcwd()
dest_dir = os.path.abspath(os.path.join(cwd, "../QCT_zip"))
os.makedirs(dest_dir, exist_ok=True)
print("Destination directory:", dest_dir)

# Loop through each SRA ID
for sra_id in sra_numbers:
    # Go into SRA subfolder
    os.chdir(sra_id)
    print("\nSRA file directory:", os.getcwd())

    # Go into fastq_files subfolder
    os.chdir("fastq_files")
    print("FASTQ file directory:", os.getcwd())

    # Move all fastq.gz files to clean_fastq folder (2 levels up)
    fastq_files = glob.glob(f"{sra_id}*fastqc.zip")

    if not fastq_files:
        print(f"⚠️ No FASTQ files found for {sra_id}. Skipping...")
    else:
        for file in fastq_files:
            src = os.path.abspath(file)
            print(f"Moving {src} → {dest_dir}")
            subprocess.run(["mv", src, dest_dir], check=True)

    # Return two directories back for next loop
    os.chdir("../..")
    print(f"✅ Finished moving {sra_id} FASTQs\n{'-'*60}")

# MultiQC

# Move up one directory (from inside sra_files or fastq folder)
os.chdir("..")           
# Create folder if not exists                
os.makedirs("MultiQCT_report", exist_ok=True)  
# Print current working directory
print(os.getcwd())                      

subprocess.run(["multiqc", "QCT_zip/", "-o", "MultiQCT_report/"])
print("MultiQCT report generated in:", os.getcwd())

