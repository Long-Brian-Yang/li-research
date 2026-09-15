import unittest
import sys
from pathlib import Path
import numpy as np
from ase import Atoms
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/structures'))
from finish_amorphous_analysis import frame_metrics, block_slopes

class Checks(unittest.TestCase):
    def test_periodic_coordination(self):
        a=Atoms('SOOOO',positions=[[0,0,0],[9,0,0],[0,1,0],[0,0,1],[0,0,9]],cell=[10,10,10],pbc=True)
        g,cn,minimum=frame_metrics(a,[('S','O',1.9)],np.arange(0,4,.1))
        self.assertEqual(cn[0],4)
        self.assertAlmostEqual(minimum,1)
        self.assertTrue(np.isfinite(g).all())
    def test_stationary_blocks(self):
        x=np.zeros((401,3,3)); result=block_slopes(x,.1,4,(1,5))
        np.testing.assert_allclose(result,0,atol=1e-12)

if __name__=='__main__':unittest.main()
