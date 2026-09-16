import sys
import unittest
from pathlib import Path
import numpy as np
import json, re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/structures'))
from complete_amorphous_comparisons import sigma_mscm, angle_distribution
from analyze_lzoc_production import window_msd
from ase import Atoms

class Comparisons(unittest.TestCase):
    def test_fft_against_direct(self):
        x=np.random.default_rng(8).normal(size=(51,4,3)).cumsum(0)
        y=window_msd(x)
        for k in range(1,51):
            self.assertAlmostEqual(y[k],np.mean(np.sum((x[k:]-x[:-k])**2,axis=2)),places=9)
    def test_sigma_units(self):
        expected=(1e28*(1.602176634e-19)**2*1e-10/(1.380649e-23*300))*10
        self.assertAlmostEqual(sigma_mscm(1e-6,10,1000,300),expected)
    def test_tetrahedron(self):
        v=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)*2
        a=Atoms('PS4',positions=np.vstack([[0,0,0],v]),cell=[20]*3,pbc=True)
        z=angle_distribution(a,'P','S',2.6)
        np.testing.assert_allclose(z,109.4712206,atol=1e-6)
    def test_report_links_and_exports(self):
        root=Path(__file__).resolve().parents[1]
        out=root/'results/amorphous_review_20260915/final_comparisons'
        pngs=list(out.glob('*.png'))
        self.assertTrue(pngs)
        self.assertEqual({p.stem for p in pngs},{p.stem for p in out.glob('*.pdf')})
        self.assertEqual({p.stem for p in pngs},{p.stem for p in out.glob('*.svg')})
        for png in pngs:
            for ext in ['.pdf','.svg']:self.assertTrue(png.with_suffix(ext).is_file())
        for lang in ['en','ja']:
            p=out/f'report_{lang}.md'
            for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if '://' not in target:
                    self.assertTrue((p.parent/target.split('#')[0]).exists(),target)
    def test_saved_fit_consistency(self):
        out=Path(__file__).resolve().parents[1]/'results/amorphous_review_20260915/final_comparisons'
        d=json.loads((out/'results.json').read_text())
        for key,v in d.items():
            if not key.startswith('LZOC'):continue
            a=np.loadtxt(out/(key+'_MSD.csv'),delimiter=',',skiprows=1)
            from analyze_lzoc_production import fit_msd
            fit=fit_msd(a[:,0],a[:,1],10,40)
            self.assertAlmostEqual(fit['D_cm2_s'],v['fits'][-1]['D_cm2_s'],places=15)

if __name__=='__main__':unittest.main()
