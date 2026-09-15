import importlib.util
import sys
import unittest
from pathlib import Path
import numpy as np

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts/structures'
sys.path.insert(0,str(SCRIPTS))

class TransportTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('analyze_lips_transport'), 'New analysis module must exist')
        import analyze_lips_transport
        return analyze_lips_transport

    def test_msd_direct_and_units(self):
        m=self.module()
        x=np.random.default_rng(10).normal(size=(51,8,3)).cumsum(0)
        msd=m.window_msd(x)
        for lag in (1,7,20):
            self.assertAlmostEqual(msd[lag],np.mean(np.sum((x[lag:]-x[:-lag])**2,axis=2)),places=10)
        t=np.arange(100)*.1
        self.assertAlmostEqual(m.fit_msd(t,6*.12*t+.8,2,8)['D_cm2_s'],1.2e-5)
        expected=192/(10000e-24)*(1.602176634e-19)**2*1e-6/(1.380649e-23*300)*1000
        self.assertAlmostEqual(m.sigma_mscm(1e-6,192,10000,300),expected)

    def test_wrapped_motion(self):
        m=self.module();cell=np.eye(3)*10
        x=np.zeros((30,1,3));x[:,0,0]=np.arange(30)*.7+8
        np.testing.assert_allclose(m.unwrap(x%10,cell),x,atol=1e-12)

if __name__=='__main__':unittest.main()
