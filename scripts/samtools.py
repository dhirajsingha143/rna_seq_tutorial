import os
import subprocess
import time
import glob

# SRA files list
sra_numbers = ["SRR7179508", "SRR7179541"]

# Current working directory
print("Current Working directory:", os.getcwd())


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

# Indexing files alignment files by running samtools
for sra_id in sra_numbers:

    os.chdir(sra_id)
    print(os.getcwd())

    for f in glob.glob(f"{sra_id}_trimmed.sorted.bam"):
        print("Indexing using samtools for:", f)
        start = time.time()
        output_bai = f"{f}.bai"

        print(f"[INFO] Indexing {f} to {output_bai} ...")

        subprocess.run(["samtools", "index", f])

        end = time.time()
        time_taken = (end - start) / 60
        print(f"Time taken to index file {f}:", f"{time_taken:.2f} minutes")

    os.chdir("..")