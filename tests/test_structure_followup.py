import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/structures'))

class Motifs(unittest.TestCase):
    def test_isolated_tetrahedra(self):
        import structure_followup as m
        ps=np.zeros((2,8),bool);ps[0,:4]=True;ps[1,4:]=True
        self.assertEqual(m.motifs(ps,np.zeros((2,2),bool)),{'P1S4':2})
    def test_shared_s(self):
        import structure_followup as m
        ps=np.zeros((2,7),bool);ps[0,:4]=True;ps[1,3:]=True
        self.assertEqual(m.motifs(ps,np.zeros((2,2),bool)),{'P2S7':1})
    def test_pp_connected(self):
        import structure_followup as m
        ps=np.zeros((2,6),bool);ps[0,:3]=True;ps[1,3:]=True
        self.assertEqual(m.motifs(ps,np.array([[0,1],[1,0]],bool)),{'P2S6':1})
    def test_free_s_and_missing_neighbours(self):
        import structure_followup as m
        self.assertEqual(m.motifs(np.zeros((1,1),bool),np.zeros((1,1),bool)),{'P1S0':1,'P0S1':1})

if __name__=='__main__':unittest.main()
