from __future__ import print_function
import parmed as pmd
import unittest

try:
    from rdkit import Chem
    has_rdkit = True
except ImportError:
    has_rdkit = False


@unittest.skipUnless(has_rdkit, "Cannot test load_rdkit module without rdkit.")
class TestRDKit(unittest.TestCase):
    """ Tests loading of an rdkit Mol object """

    def test_load_rdkit_mol(self):
        m1 = Chem.MolFromSmiles('C1=CC=CN=C1')
        parm = pmd.load_rdkit(m1)
        self.assertEqual([atom.name for atom in parm.atoms], 
                         ['C1', 'C2', 'C3', 'C4', 'N1', 'C5']) 
        self.assertEqual(parm.residues[0].name, 'UNL')

    def test_load_smiles(self):
        smiles = 'C1=CC=CN=C1'
        parm = pmd.rdkit.from_smiles(smiles)
        self.assertEqual([atom.name for atom in parm.atoms], 
                         ['C1', 'C2', 'C3', 'C4', 'N1', 'C5']) 
        self.assertEqual(parm.residues[0].name, 'UNL')
