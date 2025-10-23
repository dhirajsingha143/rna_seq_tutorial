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

# Downloading SRA files
for sra_id in sra_numbers:

    print("Downloading SRA files")

    start = time.time()
    subprocess.run(["prefetch", sra_id])
    end = time.time()

    time_taken = (end - start) / 60

    print(f"Time taken to download a sra file {sra_id}", f"{time_taken:.2f}")

# Checking files directory
for sra_id in sra_numbers:
    
    if len(sra_id) > 0:
        print("List of files downloaded:")
        subprocess.run(["tree", "-rh"])
        break
    else:
        print("No fastq file downloaded")

# Converting to FASTQ files for both ends if available
for sra_id in sra_numbers:

    os.chdir(sra_id)
    print("SRA file directory:", os.getcwd())
    print("Generating FASTQ for:", sra_id)
    start = time.time()
    subprocess.run(["fasterq-dump", f"{sra_id}.sra", "-O", "fastq_files", "--split-files"])
    end = time.time()
    time_taken = (end - start) / 60
    print("Time taken to generate FASTQ:", f"{time_taken:.2f} minutes")
    subprocess.run(["ls", "-lh"])
    os.chdir("..")

# Zipping the fastq files and deleting it
for sra_id in sra_numbers:
    
    # Go to sra sub folder
    os.chdir(sra_id)
    print("Downloaded SRA files directory:", os.getcwd())

    # navigate to the folder containing fastq files
    os.chdir("fastq_files")
    print("FASTQ file directory:", os.getcwd())

    patterns = sra_id + "*.fastq"
    file = sorted(glob.glob(patterns))

    if not file:
            print("No file found:", patterns)
    else:
        for f in file:
            start = time.time()
            print("zipping", f)
            subprocess.run(["gzip", f], check=True)
            end = time.time()
            time_taken = (end - start) / 60
            print("Time taken to zip FASTQ files:", f"{time_taken:.2f} minutes")
            subprocess.run(["ls", "-lh"])

    os.chdir("../..")
    print(f"Finished {sra_id}")

for sra_id in sra_numbers:

    # Go to sra sub folder
    os.chdir(sra_id)
    print("Downloaded SRA files directory:", os.getcwd())

    patterns = sra_id + ".sra"
    file = sorted(glob.glob(patterns))

    if not file:
        print("No sra file exist!!", patterns)
    else:
        for f in file:
            subprocess.run(["rm", f])
            print("Deleted downloaded SRR files")
    os.chdir("..")

for sra_id in sra_numbers:

    os.chdir(sra_id)
    print("SRA file directory:", os.getcwd())

    os.chdir("fastq_files")
    print("FASTQ file directory:", os.getcwd())

    for f in glob.glob(f"{sra_id}*.fastq.gz"):
        print("Quality control for:", f)
        start = time.time()
        subprocess.run(["fastqc", f])
        end = time.time()
        time_taken = (end - start) / 60
        print("Time taken for quality control:", f"{time_taken:.2f} minutes")

        os.chdir("../..")

# Destination change of zipped fastq files
cwd = os.getcwd()
dest_dir = os.path.abspath(os.path.join(cwd, "../clean_fastq"))
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
    fastq_files = glob.glob(f"{sra_id}*fastq.gz")

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

