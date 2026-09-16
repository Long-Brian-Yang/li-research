import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/structures'))

class MaterialTests(unittest.TestCase):
    def test_transport_summary_units_and_negative_slopes(self):
        import finish_materials_transport as m
        t=np.arange(0,101,.1)
        v=m.summarize_curve(t,2+6*.02*t,32,10000,330)
        self.assertAlmostEqual(v['D_cm2_s'],2e-6)
        expected=(32/1e-26)*(1.602176634e-19)**2*(2e-10)/(1.380649e-23*330)*10
        self.assertAlmostEqual(v['sigma_mS_cm'],expected)
        bad=m.summarize_curve(t,10-.02*t,32,10000,330)
        self.assertIsNone(bad['sigma_mS_cm'])

    def test_arrhenius_slope_convention(self):
        import finish_materials_transport as m
        t=np.array([320.,330,340,350]); d=1e-2*np.exp(-.33/(8.617333262145e-5*t))
        fit=m.arrhenius(t,d)
        self.assertAlmostEqual(fit['Ea_eV'],.33)
        self.assertAlmostEqual(fit['R2'],1)
        self.assertAlmostEqual(fit['value_303_15'],1e-2*np.exp(-.33/(8.617333262145e-5*303.15)))
        self.assertIsNone(m.arrhenius(t,[1,0,2,3]))

    def test_lzoc_primary_uses_scientific_labels(self):
        import curate_overview_figures as c
        captured=[]
        original=c.finish
        c.finish=lambda fig,name:captured.append(fig)
        try:
            c.lzoc()
            labels=[line.get_label() for ax in captured[0].axes for line in ax.lines]
            self.assertFalse(any('0.5' in label or 'MTTK' in label for label in labels))
            self.assertFalse(any('Job ' in label for label in labels))
            self.assertTrue(any('NEP89' in label for label in labels))
        finally:
            c.finish=original
            import matplotlib.pyplot as plt
            plt.close('all')

if __name__=='__main__': unittest.main()
