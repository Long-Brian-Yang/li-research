from pathlib import Path
import importlib.util
import unittest
import numpy as np

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/structures/lzoc_order_motion.py'

class Motion(unittest.TestCase):
    def test_affine_and_translation(self):
        self.assertTrue(SCRIPT.exists())
        sp=importlib.util.spec_from_file_location('motion',SCRIPT);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
        h=np.array([np.eye(3)*10,np.eye(3)*12])
        s=np.array([[.2,.3,.4],[.7,.6,.5]])
        x=np.array([s@c for c in h]);orig=np.zeros((2,3))
        self.assertTrue(np.allclose(m.displacements(x,h,orig,np.array([1.,2.])),0))
        h[:]=np.eye(3)*10;x=np.array([s@h[0],s@h[0]+[2,1,0]])
        self.assertTrue(np.allclose(m.displacements(x,h,orig,np.array([1.,2.])),0))

if __name__=='__main__':unittest.main()
