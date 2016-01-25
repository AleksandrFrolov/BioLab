from collections import namedtuple
from schrodinger import structure as st
from math import sqrt
from schrodinger.structutils import analyze as ssa


Receptor = namedtuple('Receptor', 'name, residue, atom')

def euclidean_distance(input, receptor, ligand):
    structures = []
    for structure in st.StructureReader(input):
        if structure.title == receptor.name:
            for atom in list(list(structure.residue)[receptor.residue].atom):
                if atom.index == receptor.atom:
                    raX = atom.x
                    raY = atom.y
                    raZ = atom.z
        else:
            atom_set = []
            for atom in list(structure.atom):
                if type(ligand[0]) == str:
                    tmp = atom.atom_type_name[0:len(ligand[0])]
                else:
                    tmp = int(atom.index)
                if tmp in ligand:
                    laX = atom.x
                    laY = atom.y
                    laZ = atom.z
                    atom_set.append(sqrt((raX - laX)*(raX - laX) + (raY - laY)*(raY - laY) + (raZ - laZ)*(raZ - laZ)))
            try:
                structures.append((structure.title, sorted(atom_set)[0]))
            except:
                print 'Error: structure %s.' % structure.title
    return sorted(set(structures), key=lambda x: x[1])


def RMSD(input, template):
    prototipe = []
    molecules_rmsd = []
    for structure in st.StructureReader(input):
        if structure.title == template[0]:
            core_atoms = ssa.evaluate_asl(structure, template[1])
            for atom in list(structure.atom):
                if atom.index in core_atoms:
                    raX = atom.x
                    raY = atom.y
                    raZ = atom.z
                    prototipe.append((raX, raY, raZ))
    for structure in st.StructureReader(input):
        if structure.title != template[0]:
            core_atoms = ssa.evaluate_asl(structure, template[1])
            rmsd = 0
            for atom in list(structure.atom):
                tmp_len = []
                if atom.index in core_atoms:
                    for pa in prototipe:
                        atoms_len = sqrt((pa[0] - atom.x)*(pa[0] - atom.x) + (pa[1] - atom.y)*(pa[1] - atom.y) + (pa[2] - atom.z)*(pa[2] - atom.z))
                        tmp_len.append(atoms_len)
                    rmsd += min(tmp_len)
        molecules_rmsd.append((structure.title, rmsd))
    return sorted(set(molecules_rmsd), key=lambda x: x[1])


# ===========EXAMPLE===========
path = '/home/frolov/schrodinger/MEK/2016/25_01_16/merge_rings_pv.mae'

len_RMSD = RMSD(path, ('cobimetinib', '"SMARTS. Nc1ccc(I)cc1"'))
for i in len_RMSD[0:70]:
    print i