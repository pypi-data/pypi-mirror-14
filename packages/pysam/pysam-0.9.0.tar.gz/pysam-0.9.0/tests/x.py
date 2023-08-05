import os
import pysam
chrom_label="22"
start_pos=14464594 
final_pos=14464644
alignment_ftp_path = "ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/technical/" \
                                     "other_exome_alignments/HG00096/exome_alignment/"
alignment_filename = "HG00096.mapped.illumina.mosaik.GBR.exome.20111114.bam"
alignment_ftp_path = os.path.join(alignment_ftp_path, alignment_filename) 
# Watch out: as a side effect, SAMtools (and by extension, pysam) will 
#   save the bai file in the current working directory. 
bamfile = pysam.AlignmentFile(alignment_ftp_path)

for i in range(10000):
    read_depth = sum([1 for aligned_read in bamfile.fetch("22", start_pos, final_pos)])
    print i

bamfile.close()  
