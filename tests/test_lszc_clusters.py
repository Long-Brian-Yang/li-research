import unittest
import importlib.util
from pathlib import Path
from ase import Atoms

P=Path(__file__).resolve().parents[1]/'scripts/structures/extract_lszc_clusters.py'
class Tests(unittest.TestCase):
    def test_periodic_cluster(self):
        self.assertTrue(P.exists(),'cluster extractor missing')
        spec=importlib.util.spec_from_file_location('clusters',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        a=Atoms('SO',positions=[[.2,0,0],[9,0,0]],cell=[10,10,10],pbc=True)
        clusters=m.extract(a)
        self.assertEqual(len(clusters),1)
        self.assertAlmostEqual(clusters[0][1].get_distance(0,1),1.2)
        a=Atoms('Li',positions=[[0,0,0]],cell=[10,10,10],pbc=True)
        self.assertEqual(m.extract(a),[])
if __name__=='__main__':unittest.main()
