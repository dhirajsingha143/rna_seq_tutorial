import subprocess
import time
import os
from glob import glob

# List of SRA IDs to download
sra_numbers = [
    "SRR7179504", "SRR7179541"
]

# Make output directory folder for FASTQ files
output_dir = "fastq_files"
os.makedirs(output_dir, exist_ok=True)

# Function to download FASTQ files using fasterq-dump
for sra_id in sra_numbers:
    print(f"\n=== Downloading: {sra_id} ===")
    prefetch_cmd = f"prefetch {sra_id}"
    print("Command:", prefetch_cmd)

    start_time = time.time()
    subprocess.call(prefetch_cmd, shell=True)
    end_time = time.time()

    elapsed_min = (end_time - start_time) / 60
    print(f"⏱ Download time for {sra_id}: {elapsed_min:.2f} minutes")

# Step 2: Convert SRA to FASTQ
for sra_id in sra_numbers:
    sra_path = os.path.expanduser(f"~/ncbi/public/sra/{sra_id}.sra")
    print(f"\n=== Generating FASTQ for: {sra_id} ===")

    # Build the fasterq-dump command
    fasterq_cmd = (
        f"fasterq-dump {sra_path} --outdir fastq --split-files --threads 4"
    )
    print("Command:", fasterq_cmd)

    # Run fasterq-dump
    start_time = time.time()
    subprocess.call(fasterq_cmd, shell=True)
    end_time = time.time()
    elapsed_min = (end_time - start_time) / 60
    print(f"⏱ FASTQ generation time for {sra_id}: {elapsed_min:.2f} minutes")

    # Compress all generated FASTQ files for this SRA ID
    print(f"\n=== Compressing FASTQ files for: {sra_id} ===")
    fastq_files = glob(f"fastq/{sra_id}*.fastq")

    if not fastq_files:
        print(f"⚠️ No FASTQ files found for {sra_id}. Skipping compression.")
        continue

    for fq in fastq_files:
        print(f"📦 Compressing {fq} ...")
        start_zip = time.time()
        gzip_cmd = f"gzip -f --fast {fq}"  # use --fast for quicker compression
        subprocess.call(gzip_cmd, shell=True)
        end_zip = time.time()
        print(f"✅ Compressed {fq} in {(end_zip - start_zip):.2f} sec")

print("\n🎉 All downloads, FASTQ conversions, and compressions complete!")