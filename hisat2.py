
# Download the prebuilt HISAT2 Index for faster alignment
# wget https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz
# tar -xvzf grch38_genome.tar.gz

# Download annotation (GTF) file for downstream analysis (gene counting)
# wget ftp://ftp.ensembl.org/pub/release-114/gtf/homo_sapiens/Homo_sapiens.GRCh38.114.gtf.gz
# gunzip Homo_sapiens.GRCh38.114.gtf.gz

# Alignment run script (shell script)
````
hisat2 -p 4 -x reference/grch38_genome -U sra_files/SRR7179508/fastq_files/SRR7179508_trimmed.fastq.gz -S hisat2_alignment/SRR7179508_trimmed.samme
````

# Sorting using samtools (shell script)

````
samtools sort -@ 4 -o sample.sort.bam sample.sam
````

# Indexing using samtools (shell script)

````
samtools index sample.sort.bam
````
