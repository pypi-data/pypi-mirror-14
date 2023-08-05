from subprocess import Popen, PIPE

# Not doable within python and a pipe properly
# https://stackoverflow.com/questions/8466926/using-python-subprocess-to-redirect-stdout-to-stdin
# https://www.biostars.org/p/15298

# Test if samtools is available

Popen("segemehl.x -d genome.fa -i index.idx -q read.fa "
            "| samtools view -Shb - > out.bam", shell=True, stderr=PIPE)

# if this is not the case generate as before a SAM file and covert it to 
