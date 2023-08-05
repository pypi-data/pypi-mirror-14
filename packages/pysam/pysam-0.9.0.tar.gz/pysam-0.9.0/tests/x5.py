import pysam

f = pysam.AlignmentFile("A1b.bam")

for c in f.pileup():
    for x in c.pileups:
        print "#####################"
        print c.pos
        print x.indel, x.is_del

for c in f.pileup():
    for x in c.pileups:
        if x.indel == 0 and x.is_del != 0:
            print "#####################"
            print c.pos
            print x.indel, x.is_del
            print str(x.alignment)
