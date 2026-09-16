import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TestLiPS(unittest.TestCase):
    def test_preparation(self):
        script = ROOT / 'scripts/structures/prepare_lips_nep.py'
        self.assertTrue(script.exists(), 'conversion script not implemented')
        subprocess.run([sys.executable, str(script)], check=True)
        base = ROOT / 'materials/candidates/Li3PS4_glass'
        info = json.loads((base/'validation.json').read_text())
        self.assertEqual(info['counts'], {'Li':192, 'P':64, 'S':256})
        self.assertGreater(info['minimum_distance_A'], 1.0)
        self.assertAlmostEqual(info['cell_A'][0], 25.63800048828125)
        self.assertEqual(int((base/'input/model.xyz').read_text().splitlines()[0]),512)

if __name__ == '__main__':
    unittest.main()
