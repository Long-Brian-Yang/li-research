from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
class ContinuationContract(unittest.TestCase):
    def test_equilibration_only(self):
        p=ROOT/'hpc/tsubame_26icp/production/amorphous_lzoc_equilibrate.lmp'
        self.assertTrue(p.exists(), 'continuation input missing')
        s=p.read_text()
        self.assertIn('timestep 0.0005',s)
        self.assertIn('run 100000',s)
        self.assertIn('npt temp 300 300 0.1 iso 1 1 1.0',s)
        self.assertNotIn('velocity all create',s)
        self.assertEqual(sum(line.startswith('run ') for line in s.splitlines()),1)
    def test_source_and_output(self):
        p=ROOT/'hpc/tsubame_26icp/production/amorphous_lzoc_equilibrate.sh'
        self.assertTrue(p.exists(), 'continuation wrapper missing')
        s=p.read_text()
        self.assertIn('reference_8631935/source_3/relaxed_300K.data',s)
        self.assertIn('equilibrate_${JOB_ID:?}',s)
        self.assertIn('mkdir "$OUT"',s)
        self.assertNotIn('#$ -t',s)
