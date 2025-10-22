import subprocess
import time
import os

# SRA files list
sra_numbers = ["SRR7179504","SRR7179541"]

# Current working directory
print("Current Working directory:", os.getcwd())

# Make Directory to save files
os.makedirs("sra_files", exist_ok=True)

# Change to new directory created
os.chdir("sra_files") 

# Downloading files in new directory
print("Downloading files in:", os.getcwd())

for sra_id in sra_numbers:

    print("Downloading SRA files")

    start = time.time()
    subprocess.run(["prefetch", sra_id])
    end = time.time()

    time_taken = (end - start) / 60

    print(f"Time taken to download a sra file {sra_id}", f"{time_taken:.2f}")
