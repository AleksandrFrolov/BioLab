import sys
import os
import gzip
from pymongo import MongoClient
from collections import OrderedDict

"PDB name structure must be uppercase symbol: 5DZL.pdb.gz"

def gz_reader(file):
    with gzip.open(file, 'rb') as f:
        return f.readlines()

PDB_SCHEME = OrderedDict([('PDB_ID', ''),
                          ('Title', ['HEADER', 'OBSLTE', 'TITLE', 'SPLIT', 'CAVEAT', 'COMPND', 'SOURCE', 'KEYWDS', 'EXPDTA', 'NUMMDL', 'MDLTYP', 'AUTHOR', 'REVDAT', 'SPRSDE', 'JRNL']),
                          ('Remark', ['REMARK', 'FTNOTE']),
                          ('Primary structure', ['DBREF', 'DBREF1', 'DBREF2', 'SEQADV', 'SEQRES', 'MODRES']),
                          ('Heterogen', ['HET', 'HETNAM', 'HETSYN', 'FORMUL']),
                          ('Secondary structure', ['HELIX', 'SHEET', 'TURN']),
                          ('Connectivity annotation', ['SSBOND', 'LINK', 'CISPEP', 'HYDBND', 'SLTBRG', 'TVECT']),
                          ('Miscellaneous features ', ['SITE']),
                          ('Crystallographic', ['CRYST1']),
                          ('Coordinate transformation', ['ORIGX1', 'ORIGX2', 'ORIGX3', 'SCALE1', 'SCALE2', 'SCALE3', 'MTRIX1', 'MTRIX2', 'MTRIX3']),
                          ('Coordinate', ['MODEL', 'ATOM', 'ANISOU', 'TER', 'HETATM', 'SIGATM', 'SIGUIJ',  'ENDMDL']),
                          ('Connectivity', ['CONECT']),
                          ('Bookkeeping', ['MASTER', 'END'])])

descr_list = []

for s in PDB_SCHEME.values():
    descr_list += s


def json_create(file):
    descr_dict = dict([(k, []) for k in descr_list])
    for s in gz_reader(file):
        pdb_key = s[0:6].strip()
        pdb_value = s[6:].strip()
        if pdb_value:
            descr_dict[pdb_key].append(pdb_value)

    result_dict = dict([(k, dict()) for k in PDB_SCHEME])
    for s in PDB_SCHEME:
        if s == 'PDB_ID':
            result_dict['PDB_ID'] = os.path.basename(file).split('.')[0]
        else:
            for i in PDB_SCHEME[s]:
                result_dict[s].update({i: descr_dict[i]})
    return result_dict

def db_writer(file):
    try:
        client = MongoClient('mongodb://...')
        db = client['pdb']
        p = db.pdb
        p_id = p.insert(json_create(file))
        client.close()
    except:
        pass

if __name__ == '__main__':
    try:
        ROOT_DIR = sys.argv[1]
    except:
        print "Error command line..."
        print "PDBParser.py path/pdb_structure.pdb.gz"
    i = 0
    for f in sorted(os.listdir(ROOT_DIR))[i:]:
        i += 1
        db_writer(os.path.join(ROOT_DIR, f))
        print '%s\t%s' % (i, f)