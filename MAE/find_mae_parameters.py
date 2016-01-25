import sys
import gzip

try:
    i_file = gzip.open(sys.argv[1], 'r').readlines()
except:
    print "Error input file..."

# try:
#     o_file = open(sys.argv[2], 'w')
# except:
#     print "Error output file..."

try:
    param_name = sys.argv[2]
except:
    print "Error command line mae param..."

def param_value(i_file, param_name):
    open_key = 0
    i = 0
    idx = 0
    sep = 0
    res = []
    for line in i_file:
        line = line.strip()
        if '{' in line:
            i = 0
            sep = 0
            open_key = 1
        if '}' in line:
            i = 0
            sep = 0
            open_key = 0
        if line == ':::':
            sep = 1
        if open_key:
            i += 1
            if line == param_name:
                idx = i
            if sep:
                idx -= 1
                if idx == 0:
                    res.append(line)
    return res

if __name__ == '__main__':
    title = param_value(i_file, 's_m_title')
    values = param_value(i_file, param_name)
    for k, v in zip(title[1:], values):
        print k, v