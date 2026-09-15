import unittest
import sys
import importlib.util
from pathlib import Path
import numpy as np
from ase import Atoms

P=Path(__file__).resolve().parents[1]/'scripts/structures/review_release_trials.py'

class ReviewTests(unittest.TestCase):
    def test_analysis_contract(self):
        self.assertTrue(P.exists(), 'release review implementation missing')
        sys.path.insert(0,str(P.parent))
        spec=importlib.util.spec_from_file_location('review',P)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        a=Atoms('NN',positions=[[0,0,0],[9,0,0]],cell=[10,10,10],pbc=True)
        self.assertAlmostEqual(m.contacts(a,'N','N',1.5)[0],1.)
        self.assertEqual(m.contacts(a,'N','N',1.5)[1].tolist(),[1,1])
        t=np.zeros((400,18));t[:,0]=300;t[:,2]=4;t[:,3:6]=.1;t[:,9:]=np.diag([10.,10.,10.]).reshape(9)
        v=m.thermo_values(t,a)
        np.testing.assert_allclose(v[:,0],300)
        np.testing.assert_allclose(v[:,1],2)
        np.testing.assert_allclose(v[:,2],.1)
        np.testing.assert_allclose(v[:,3],sum(a.get_masses())*1.66053906660/1000)
        t[0,0]=np.nan
        with self.assertRaises(ValueError):m.thermo_values(t,a)

if __name__=='__main__':unittest.main()
