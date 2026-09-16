from pathlib import Path
import unittest
import re

P=Path(__file__).resolve().parents[1]/'hpc/tsubame_26icp/production'
class FourTemperatureContract(unittest.TestCase):
    def test_duration_and_ensembles(self):
        p=P/'amorphous_lzoc_4t.lmp'
        self.assertTrue(p.exists())
        s=p.read_text()
        self.assertEqual(re.findall(r'^run (\d+)$',s,re.M),['20000','100000','400000'])
        self.assertIn('timestep 0.0005',s)
        self.assertIn('npt temp ${temperature} ${temperature} 0.1 iso 1 1 1.0',s)
        self.assertIn('nvt temp ${temperature} ${temperature} 0.1',s)
        self.assertIn('pair_coeff * * Li Zr O Cl',s)
    def test_production_is_separate(self):
        p=P/'amorphous_lzoc_4t.lmp'
        self.assertTrue(p.exists())
        s=p.read_text(); production=s.split('log production/log.lammps')[-1]
        self.assertIn('reset_timestep 0',production)
        self.assertIn('compute li_msd lithium msd com yes',production)
        self.assertIn('production/trajectory.lammpstrj',production)
        self.assertNotIn('npt ',production)
        self.assertIn('unfix equil',s)
    def test_unique_outputs_and_temperatures(self):
        p=P/'amorphous_lzoc_4t.sh'
        self.assertTrue(p.exists())
        s=p.read_text()
        self.assertIn('TEMPERATURES=(600 700 800 900)',s)
        self.assertIn('#$ -t 1-4',s)
        self.assertIn('equilibrate_8634186/equilibrated_300K.data',s)
        self.assertIn('mkdir "$OUT"',s)
        self.assertIn('7450a1a366025fa4094eba6ce414698b2bcc67a6c86cc53c6c9dd2046ce4c584',s)
