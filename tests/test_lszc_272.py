import json
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np
from ase.io import read

ROOT = Path(__file__).resolve().parents[1]


class TestLSZC272(unittest.TestCase):
    def test_seed_supercell(self):
        script = ROOT / 'scripts/structures/prepare_lszc_272.py'
        self.assertTrue(script.exists(), '272-atom preparation not implemented')
        subprocess.run([sys.executable, str(script)], check=True)
        base = ROOT / 'materials/candidates/LSZC'
        parent = read(base / 'source/Supplementary Data 1.txt', format='cif')
        out = base / 'seed_272'
        a = read(out / 'model.xyz')
        c = read(out / 'initial_structure.cif')
        info = json.loads((out / 'validation.json').read_text())
        self.assertEqual(len(a), 272)
        self.assertEqual(info['counts'], {'Li':32, 'Zr':32, 'Cl':128, 'S':16, 'O':64})
        self.assertEqual(info['repeat'], [1,2,1])
        self.assertTrue(np.allclose(a.cell, parent.repeat((1,2,1)).cell))
        self.assertTrue(np.allclose(a.positions, parent.repeat((1,2,1)).positions))
        self.assertAlmostEqual(a.get_volume(), 2*parent.get_volume(), places=5)
        self.assertEqual(len(c), 272)
        self.assertTrue(np.allclose(a.cell, c.cell))
        self.assertGreater(info['minimum_distance_A'], 1.0)
        self.assertFalse(info['validated_amorphous'])


if __name__ == '__main__':
    unittest.main()
