import unittest,importlib.util
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[1]/'scripts/structures/pack_lszc.py'
class Tests(unittest.TestCase):
 def test_periodic_clearance(self):
  self.assertTrue(P.exists(),'packer missing')
  s=importlib.util.spec_from_file_location('pack',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
  self.assertAlmostEqual(m.clearance(np.array([[.2,0,0]]),np.array([[9.8,0,0]]),10),.4)
  self.assertEqual(m.clearance(np.array([[0,0,0]]),np.empty((0,3)),10),float('inf'))
if __name__=='__main__':unittest.main()
