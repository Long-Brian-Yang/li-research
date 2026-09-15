import unittest,sys,importlib.util
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/structures'))
class TestExtrapolation(unittest.TestCase):
 def test_known_arrhenius(self):
  self.assertIsNotNone(importlib.util.find_spec('portfolio_supplement'))
  from portfolio_supplement import extrapolate
  t=np.array([340.,360.,380.]);d=.01*np.exp(-.3/(8.617333262145e-5*t))
  ea,d300,r2=extrapolate(t,d)
  self.assertAlmostEqual(ea,.3)
  self.assertAlmostEqual(d300,.01*np.exp(-.3/(8.617333262145e-5*300)))
  self.assertAlmostEqual(r2,1)
