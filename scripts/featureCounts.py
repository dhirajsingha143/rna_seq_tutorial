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
os.makedirs("sra_files/bam_files", exist_ok=True)

bam_folder = "../../bam_files"

# Change to new directory created
os.chdir("sra_files/hisat2_alignment") 
print(os.getcwd())

for sra_id in sra_numbers:

    os.chdir(sra_id)
    print(os.getcwd())

    for f in glob.glob(f"{sra_id}_trimmed.sorted.bam"):
        subprocess.run(["cp", f, bam_folder])
        print("Moved all bam files to:", bam_folder)
        os.chdir("..")
        print(os.getcwd())

print("\n✅ BAM files have been moved successfully.\n")


# Running featureCounts to get gene counts from BAM files
os.chdir("../bam_files")
print(os.getcwd())

# Expand all bam files in the folder
bam_files = glob.glob("*.sorted.bam")

if not bam_files:
    print("[Error] No BAM files found for featureCounts.")
    exit(1)

print(f"[INFO] Found {len(bam_files)} BAM files for featureCounts.")
for f in bam_files:
    print(f" - {f}")

command = [
    "featureCounts",
    "-T", "4",
    "-a", os.path.abspath(f"../../{gtf_file}"),
    "-o", "gene_counts.txt",
] + bam_files

subprocess.run(command, check=True)

print("\n✅ featureCounts has completed successfully. Gene counts are saved in 'gene_counts.txt'.\n")