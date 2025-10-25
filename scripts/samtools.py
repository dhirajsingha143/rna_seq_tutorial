import os
import subprocess
import time
import glob

# SRA files list
sra_numbers = ["SRR7179508", "SRR7179541"]

# Current working directory
print("Current Working directory:", os.getcwd())


# Defined paths
reference_dir = "reference"
gtf_file = os.path.join(reference_dir, "Homo_sapiens.GRCh38.114.gtf.gz")

download_url = "ftp://ftp.ensembl.org/pub/release-114/gtf/homo_sapiens/Homo_sapiens.GRCh38.114.gtf.gz"

# Create reference directory if it doesn't exist
os.makedirs(reference_dir, exist_ok=True)

# Check if GTF file exists, if not download it
if not os.path.exists(gtf_file):
    print(f"[INFO] GTF file not found. Downloading from:\n {download_url}")
    try:
        subprocess.run(["wget", download_url])
        print("[Success] Download completed.")
    except Exception as e:
        print(f"[Error] Download failed: {e}")
        exit(1)
else:
    print("[INFO] GTF file already exists. Skipping download.")

print("\n✅ Samtools GTF file setup is complete.\n")


# Sorting files alignment files by running samtools

# Change to new directory created
os.chdir("sra_files") 
print(os.getcwd())

os.chdir("hisat2_alignment") 
print(os.getcwd())


for sra_id in sra_numbers:

    os.chdir(sra_id)
    
    for f in glob.glob(f"{sra_id}_trimmed.sam"):
        print("Sorting using samtools for:", f)
        start = time.time()
        os.makedirs(f"../../hisat2_alignment/{sra_id}", exist_ok=True)
        output_sam = f"../../hisat2_alignment/{sra_id}/{sra_id}_trimmed.sorted.bam"

        print(f"[INFO] Sorting {f} to {output_sam} ...")

        subprocess.run(["samtools", "sort", "-@", "4", "-o", output_sam, f])

        end = time.time()
        time_taken = (end - start) / 60
        print(f"Time taken to align file {f}:", f"{time_taken:.2f} minutes")
        os.chdir("..")