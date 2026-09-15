import unittest
import importlib.util
from pathlib import Path
import numpy as np

P=Path(__file__).resolve().parents[1]/'scripts/structures/analyze_lzoc_production.py'

class AnalysisTests(unittest.TestCase):
    def load(self):
        self.assertTrue(P.exists(), 'analysis implementation not yet present')
        s=importlib.util.spec_from_file_location('analysis',P)
        m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
        return m
    def test_windowed_msd_matches_direct(self):
        m=self.load();x=np.random.default_rng(91).normal(size=(100,4,3)).cumsum(0)
        expected=np.array([np.mean(np.sum((x[k:]-x[:-k])**2,axis=2)) for k in range(1,100)])
        np.testing.assert_allclose(m.window_msd(x)[1:],expected,atol=1e-10)
    def test_fit_units(self):
        m=self.load();t=np.arange(101.)
        r=m.fit_msd(t,6*0.2*t+2,10,80)
        self.assertAlmostEqual(r['D_cm2_s'],2e-5)
        self.assertAlmostEqual(r['R2'],1)
    def test_unwrap_triclinic(self):
        m=self.load();cell=np.array([[10.,0,0],[2,10,0],[0,3,10]])
        x=np.array([[[8.,2,2]],[[9,2,2]],[[10,2,2]],[[11,2,2]]])
        wrapped=(x@np.linalg.inv(cell)%1)@cell
        recovered=m.unwrap(wrapped,cell)
        np.testing.assert_allclose(recovered-recovered[0],x-x[0],atol=1e-12)

if __name__=='__main__': unittest.main()
