from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/structures/plot_lzoc_preparation.py'

class Preparation(unittest.TestCase):
    def test_md_only_excludes_final_minimization(self):
        self.assertTrue(SCRIPT.exists())
        spec = importlib.util.spec_from_file_location('prep', SCRIPT)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for i in (1,2,3):
            a = m.read_md(ROOT / f'materials/candidates/LZOC/archive/completed_reference_trials/source_{i}/candidate.log')
            self.assertEqual(a.shape, (1101,14))
            self.assertEqual(a[0,1], 0)
            self.assertEqual(a[-1,1],55)
            self.assertTrue((a[:,2]==192).all())
        self.assertAlmostEqual(a[-1,4],-912.769329166542,places=4)

if __name__=='__main__': unittest.main()
