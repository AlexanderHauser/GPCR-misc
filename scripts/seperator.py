#!/mnt/cluster/home/ans/python2.7/python

import os
import time
import getopt
import sys
from Bio import SeqIO



def batch_iterator(iterator, batch_size) :
    """Returns lists of length batch_size.
 
    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.
 
    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True #Make sure we loop once
    while entry :
        batch = []
        while len(batch) < batch_size :
            try :
                entry = iterator.next()
            except StopIteration :
                entry = None
            if entry is None :
                #End of file
                break
            batch.append(entry)
        if batch :
            yield batch
def usage():
    print "\nSeperates a fasta file into:\nProteinGI:ProteinSequence"
    print "-h\t--help\t\tShow this message"
    print "-i\t--input\t\tFile to seperate"
    
def main (argv):
    try:
        opts, args = getopt.getopt(argv, "i:", ["input"])
    except getopt.GetoptError:
        usage()     
        sys.exit(2)

    # default values
    filename = False

    # arguments
    for opt,arg in opts:
        if opt in ("-h", "--help"):
            sys.exit()
        elif opt in ("-i", "--input"):
            filename = arg
    print filename
    record_iter = SeqIO.parse(open(filename),"fasta")
    for i, batch in enumerate(batch_iterator(record_iter, 1)) :
        #filename = "%i.fasta" % (i+1)
        
        # get the GI number
        gi = batch[0].id
        parts = gi.split("|")
        gi_code = parts[1]

        filename =  gi_code + ".fasta"
            
        handle = open(filename, "w")
        count = SeqIO.write(batch, handle, "fasta")
        handle.close()
        print "Wrote %i records to %s" % (count, filename)

if __name__ == "__main__":
    main(sys.argv[1:])
