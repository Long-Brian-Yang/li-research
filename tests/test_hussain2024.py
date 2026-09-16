import unittest
import subprocess
import sys
from pathlib import Path
from collections import Counter
import numpy as np
from ase.io import read

ROOT = Path(__file__).resolve().parents[1]

class TestReconstruction(unittest.TestCase):
    def test_192_atom_seed(self):
        script = ROOT / 'scripts/structures/prepare_hussain2024.py'
        self.assertTrue(script.exists(), 'reconstruction script missing')
        subprocess.run([sys.executable, str(script)], check=True)
        base = ROOT / 'materials/candidates/LZOC_Hussain2024/seed_192'
        a = read(base / 'model.xyz')
        b = read(base / 'initial_structure.cif')
        self.assertEqual(Counter(a.get_chemical_symbols()), dict(Li=42,Zr=24,Cl=114,O=12))
        self.assertEqual(len(b),192)
        self.assertTrue(np.allclose(a.cell,b.cell))
        self.assertTrue(a.pbc.all())
        d=a.get_all_distances(mic=True)
        np.fill_diagonal(d,np.inf)
        self.assertGreater(d.min(),1.6)
