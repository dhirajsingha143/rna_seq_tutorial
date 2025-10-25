import os
import subprocess
import time
import glob

# SRA files list
sra_numbers = ["SRR7179508", "SRR7179541"]

# Current working directory
print("Current Working directory:", os.getcwd())

# Download the reference genome index if not already present

# Defined paths
reference_dir = "reference"
tar_file = os.path.join(reference_dir, "grch38_genome.tar.gz")
extracted_dir = os.path.join(reference_dir, "grch38")
download_url = "https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz"

# Create reference directory if it doesn't exist
os.makedirs(reference_dir, exist_ok=True)

# Check if tar file exists, if not download it
if not os.path.exists(tar_file):
    print(f"[INFO] Reference tar file not found. Downloading from:\n {download_url}")
    try:
        subprocess.run(["wget", download_url])
        print("[Success] Download completed.")
    except Exception as e:
        print(f"[Error] Download failed: {e}")
        exit(1)
else:
    print("[INFO] Reference tar file already exists. Skipping download.")

# Check if extracted directory exists, if not — extract it
if not os.path.exists(extracted_dir):
    print(f"[INFO] Extracting {tar_file} to {extracted_dir} ...")
    try:
        subprocess.run(["tar", "-xvzf", tar_file, "-C", reference_dir], check=True)
        print(f"[SUCCESS] Extracted to: {extracted_dir}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Extraction failed: {e}")
        exit(1)
else:
    print(f"[OK] Found existing extracted index directory: {extracted_dir}")

print("\n✅ HISAT2 reference index setup is complete.\n")


# Alignment files download and running auto-alignment

reference_genome_path = os.path.abspath("reference/grch38/genome")

# Change to new directory created
os.chdir("sra_files") 
print(os.getcwd())

for sra_id in sra_numbers:

    os.chdir(sra_id)
    os.chdir("fastq_files")
    
    for f in glob.glob(f"{sra_id}_trimmed.fastq.gz"):
        print("Alignment using HISAT2 for:", f)
        start = time.time()
        os.makedirs(f"../../hisat2_alignment/{sra_id}", exist_ok=True)
        output_sam = f"../../hisat2_alignment/{sra_id}/{sra_id}_trimmed.sam"

        subprocess.run(["hisat2", "-p", "4", "-x", reference_genome_path, "-U", f, "-S", output_sam])

        end = time.time()
        time_taken = (end - start) / 60
        print(f"Time taken to align file {f}:", f"{time_taken:.2f} minutes")
        os.chdir("../..")