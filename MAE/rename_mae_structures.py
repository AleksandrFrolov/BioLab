import sys
import gzip

"""
Script for rename mae structures. Add order number
"""

if __name__ == '__main__':
    try:
        mae_file = gzip.open(sys.argv[1], 'r').readlines()
    except:
        print "Error input mae file..."

    try:
        smi_file = open(sys.argv[2], 'r').readlines()
    except:
        print "Error input smiles file..."

    try:
        o_file = open(sys.argv[3], 'w')
    except:
        print "Error output file..."

    molecules = [l.split(' ')[1].strip() for l in smi_file if l]
    i = 0

    for line in mae_file:
        if line.strip() in molecules:
            i += 1
            line = "  %s-%s\n" % (line.strip(), i)
        o_file.write(line)