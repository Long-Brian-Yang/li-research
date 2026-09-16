import json
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np
from ase.io import read

ROOT = Path(__file__).resolve().parents[1]


class TestLSZC(unittest.TestCase):
    def test_author_structure_conversion(self):
        script = ROOT / 'scripts/structures/prepare_lszc_nep.py'
        self.assertTrue(script.exists(), 'LSZC conversion is not implemented')
        subprocess.run([sys.executable, str(script)], check=True)
        base = ROOT / 'materials/candidates/LSZC'
        info = json.loads((base / 'validation.json').read_text())
        self.assertEqual(info['counts'], {'Li': 128, 'Zr': 128, 'Cl': 512, 'S': 64, 'O': 256})
        a = read(base / 'source/Supplementary Data 2.txt', format='cif')
        b = read(base / 'input/model.xyz')
        self.assertEqual(a.get_chemical_symbols(), b.get_chemical_symbols())
        self.assertTrue(np.allclose(a.cell, b.cell))
        self.assertTrue(np.allclose(a.positions, b.positions, atol=1e-7))
        self.assertTrue(b.pbc.all())
        self.assertGreater(info['minimum_distance_A'], 1.0)
        self.assertEqual(info['source_data'], 2)


if __name__ == '__main__':
    unittest.main()
