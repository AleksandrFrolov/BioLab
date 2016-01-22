import os
import sys
from rdkit import Chem
from collections import namedtuple

Template = namedtuple('Template', "smiles, name, idx")
MOL_HEAD = Template(Chem.MolFromSmiles('NC1=CC=C(I)C=C1F'), '', 0)
MOL_TAIL = Template(Chem.MolFromSmiles('CNC(=O)'), '', 2)

try:
    ROOT_DIR = sys.argv[1]
    INPUT_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]
except:
    print "Error command line..."

try:
    i_file = open(os.path.join(ROOT_DIR, INPUT_FILE), 'r').readlines()
except:
    print "Not exist input file..."

try:
    o_file = open(os.path.join(ROOT_DIR, OUTPUT_FILE), 'w')
except:
    print "Can't create output file"

def get_attachers(smiles):
    rings = smiles.GetRingInfo().AtomRings()
    res = []
    for ring in rings:
        for r in ring:
            if smiles.GetAtomWithIdx(r).GetTotalNumHs() > 0:
                res.append(r)
    return res

def attach_fragment(core, tacher):
    combo = Chem.CombineMols(core.smiles, tacher.smiles)
    edcombo = Chem.EditableMol(combo)
    edcombo.AddBond(core.idx, core.smiles.GetNumAtoms() + tacher.idx, order=Chem.rdchem.BondType.SINGLE)
    return edcombo.GetMol()


if __name__ == '__main__':
    e = 0
    unique_res = []
    try:
        for mol in i_file:
            smiles, name = mol.strip().split(' ')
            bonds = [i for i in get_attachers(Chem.MolFromSmiles(smiles)) if i < len(smiles)]
            for i in bonds:
                fragment = Template(Chem.MolFromSmiles(smiles), '%s_%s' % (name, i), i)
                head = attach_fragment(MOL_HEAD, fragment)
                for l in bonds:
                    if l != i:
                        molecule = attach_fragment(MOL_TAIL, Template(head, name, l + MOL_HEAD.smiles.GetNumAtoms()))
                        if Chem.MolToSmiles(molecule) not in unique_res:
                            o_file.write('%s %s_%s\n' % (Chem.MolToSmiles(molecule), fragment.name, l))
                            unique_res.append(Chem.MolToSmiles(molecule))
                            e += 1
    except:
        print 'Total: %s' % e