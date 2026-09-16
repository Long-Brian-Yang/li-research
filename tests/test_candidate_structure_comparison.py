from pathlib import Path
import importlib.util
import unittest
import numpy as np
from ase import Atoms

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/structures/compare_lzoc_candidates.py'

class StructureComparison(unittest.TestCase):
    def test_pbc_and_normalization(self):
        self.assertTrue(SCRIPT.exists())
        spec=importlib.util.spec_from_file_location('compare',SCRIPT)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        a=Atoms('LiCl',positions=[[.1,0,0],[9.9,0,0]],cell=[10,10,10],pbc=True)
        edges=np.array([0.,.5,1.])
        rdf,cn=mod.pair_stats(a,'Li','Cl',edges,.3)
        self.assertEqual(cn.tolist(),[1])
        self.assertAlmostEqual(rdf[0]*(4*np.pi/3*.5**3)/1000,1)
        rdf,cn=mod.pair_stats(a,'Li','Li',edges,.3)
        self.assertEqual(cn.tolist(),[0])
        self.assertTrue(np.isnan(rdf).all())

if __name__=='__main__': unittest.main()
