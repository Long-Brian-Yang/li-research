import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class TestLiPON(unittest.TestCase):
    def test_input(self):
        script=ROOT/'scripts/structures/prepare_lipon_nep.py'
        self.assertTrue(script.exists(), 'missing converter')
        subprocess.run([sys.executable,str(script)],check=True)
        data=json.loads((ROOT/'materials/candidates/LiPON/validation.json').read_text())
        self.assertEqual(data['counts'],dict(Li=47,P=16,O=56,N=5))
        self.assertEqual(data['formal_charge'],0)
        self.assertGreater(data['minimum_distance_A'],1.0)
if __name__=='__main__': unittest.main()
