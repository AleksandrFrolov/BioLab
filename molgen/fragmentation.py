from rdkit import Chem
from rdkit.Chem import BRICS
import re

def fragments_by_template(smiles, template):
    mol = Chem.MolFromSmiles(smiles)
    bis = mol.GetSubstructMatches(Chem.MolFromSmarts(template))
    bs = [mol.GetBondBetweenAtoms(x,y).GetIdx() for x,y in bis]
    nm = Chem.FragmentOnBonds(mol,bs)
    return Chem.MolToSmiles(nm, True) # return String. Fragments separate by dot.

def fragments_by_bonds(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return sorted(BRICS.BRICSDecompose(mol)) # return List


def treater(structure):
    return re.sub('\(*\[+\d*\*+\]+\)*', '', structure)

def only_cycles(mol):
    f = treater(mol)
    t = f
    for i in range(len(Chem.MolFromSmiles(f).GetAtoms())):
        if not Chem.MolFromSmiles(f).GetAtomWithIdx(i).IsInRing():
            t = Chem.MolToSmiles(Chem.DeleteSubstructs(Chem.MolFromSmiles(t), Chem.MolFromSmiles(Chem.MolFromSmiles(f).GetAtomWithIdx(i).GetSymbol())))
    return t

# ===========EXAMPLE===========
fbt = fragments_by_template('C1CCN[C@@H](C1)C2(CN(C2)C(=O)C3=C(C(=C(C=C3)F)F)NC4=C(C=C(C=C4)I)F)O', '[!R][R]')
fbb = fragments_by_bonds('C1CCN[C@@H](C1)C2(CN(C2)C(=O)C3=C(C(=C(C=C3)F)F)NC4=C(C=C(C=C4)I)F)O')

for f in fbb:
    print only_cycles(f)