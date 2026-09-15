import unittest, sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/structures'))

class MechanismTest(unittest.TestCase):
    def test_conditioned_displacement_uses_origin_coordination(self):
        from paper_aligned_analysis import conditioned_mobility
        x=np.zeros((5,2,3));x[:,:,0]=np.arange(5)[:,None]*np.array([1,2])
        cn=np.tile([0,2],(5,1))
        result=conditioned_mobility(x,cn,2,1)
        np.testing.assert_allclose(result[:,0],[0,2])
        np.testing.assert_allclose(result[:,1],[3,3])
        np.testing.assert_allclose(result[:,2],[4,16])
    def test_empty_coordination_classes_are_not_zero_measurements(self):
        from paper_aligned_analysis import conditioned_mobility
        result=conditioned_mobility(np.zeros((3,1,3)),np.ones((3,1),int),1,1)
        self.assertEqual(result.shape,(1,4))
        self.assertEqual(result[0,0],1)
        self.assertEqual(result[0,1],2)

if __name__=='__main__':unittest.main()
