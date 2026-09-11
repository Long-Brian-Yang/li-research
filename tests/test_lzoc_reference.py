"""Composition and geometry checks for the literature-derived seed."""
import importlib.util
from pathlib import Path
import unittest
from collections import Counter
import numpy as np
from ase.io import read

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/structures/build_lzoc_reference.py'
REF = ROOT / 'materials/references/kim_2025_lzoc/extracted/Supplementary_Data_revised/Supplymentary_data_4 (hcp_O3).cif'

class ReferenceTests(unittest.TestCase):
    def load_module(self):
        self.assertTrue(SCRIPT.exists(), 'Reference builder is not implemented')
        spec = importlib.util.spec_from_file_location('builder', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_target_counts_and_neutrality(self):
        module = self.load_module()
        atoms, removed = module.build_target(read(REF), seed=20260911)
        counts = Counter(atoms.get_chemical_symbols())
        self.assertEqual(counts, dict(Li=42, Zr=24, Cl=114, O=12))
        self.assertEqual(counts['Li']+4*counts['Zr']-counts['Cl']-2*counts['O'], 0)
        self.assertEqual(len(removed), 36)

    def test_reproducible_and_preserves_framework(self):
        module = self.load_module()
        parent = read(REF)
        a, removed = module.build_target(parent, seed=20260911)
        b, removed_b = module.build_target(parent, seed=20260911)
        np.testing.assert_allclose(a.positions, b.positions)
        self.assertEqual(removed, removed_b)
        full = parent.repeat((2, 2, 1))
        mask = [s in ('Zr','O') for s in full.get_chemical_symbols()]
        amask = [s in ('Zr','O') for s in a.get_chemical_symbols()]
        np.testing.assert_allclose(full.positions[mask], a.positions[amask])
        np.testing.assert_allclose(full.cell, a.cell)

    def test_metrics_and_reject_wrong_parent(self):
        module = self.load_module()
        parent = read(REF)
        metrics = module.metrics(parent)
        self.assertEqual(metrics['counts'], dict(Li=15,Zr=6,Cl=33,O=3))
        self.assertGreater(metrics['minimum_pair_distance_A'], 1.0)
        self.assertGreater(metrics['density_g_cm3'], 1.0)
        parent[0].symbol = 'H'
        with self.assertRaises(ValueError):
            module.build_target(parent)

if __name__ == '__main__':
    unittest.main()
