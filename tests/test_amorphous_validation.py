import importlib.util
from pathlib import Path
import unittest

class ValidationTest(unittest.TestCase):
    def test_force_metrics(self):
        p=Path(__file__).resolve().parents[1]/'scripts/structures/check_nep_dft.py'
        self.assertTrue(p.exists(), 'force comparison module missing')
        spec=importlib.util.spec_from_file_location('fv',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        import numpy as np
        r=m.metrics(np.zeros((2,3)),np.ones((2,3)))
        self.assertAlmostEqual(r['component_MAE_eVA'],1.)
        self.assertAlmostEqual(r['component_RMSE_eVA'],1.)
    def test_pair_excludes_self(self):
        p=Path(__file__).resolve().parents[1]/'scripts/structures/validate_amorphous_trials.py'
        self.assertTrue(p.exists(), 'analysis module missing')
        spec=importlib.util.spec_from_file_location('av',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        from ase import Atoms
        import numpy as np
        a=Atoms('PP',positions=[[0,0,0],[1,0,0]],cell=[10,10,10],pbc=True)
        g,cn=m.pair(a,'P','P',np.array([0.,.5,1.5]),1.2)
        self.assertEqual(g[0],0)
        self.assertEqual(cn.tolist(),[1,1])
if __name__=='__main__': unittest.main()
