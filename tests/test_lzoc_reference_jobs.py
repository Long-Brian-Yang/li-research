from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1] / 'hpc/tsubame_26icp/production'

class ReferenceJobs(unittest.TestCase):
    def test_third_source_is_explicit(self):
        text = (BASE / 'amorphous_lzoc_reference.sh').read_text()
        self.assertIn('3) SOURCE="$ROOT/materials/candidates/LZOC/kim2025_data18_seed"', text)

    def test_initial_relaxation_and_velocities(self):
        path = BASE / 'amorphous_lzoc_reference.lmp'
        self.assertTrue(path.exists(), 'Reference simulation input missing')
        text = path.read_text()
        self.assertLess(text.index('minimize'), text.index('velocity all create'))
        self.assertLess(text.index('velocity all create'), text.index('fix mix'))
        self.assertIn('pair_coeff * * Li Zr O Cl', text)
        self.assertIn('timestep 0.0005', text)
        self.assertEqual([int(x.split()[1]) for x in text.splitlines() if x.startswith('run ')], [20000,60000,10000,20000])
        self.assertIn('write_data candidate_final.data',text)

    def test_two_sources_and_isolated_outputs(self):
        path = BASE / 'amorphous_lzoc_reference.sh'
        self.assertTrue(path.exists(), 'Reference wrapper missing')
        text = path.read_text()
        self.assertIn('#$ -t 1-2',text)
        self.assertIn('kim2025_derived_seed',text)
        self.assertIn('kim2025_data19_seed',text)
        self.assertIn('reference_${JOB_ID',text)
        self.assertIn('source_${SGE_TASK_ID',text)
        self.assertIn('sha256sum',text)

if __name__ == '__main__':
    unittest.main()
