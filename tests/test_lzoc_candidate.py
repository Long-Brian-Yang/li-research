from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1] / 'hpc/tsubame_26icp/production'

class CandidateContract(unittest.TestCase):
    def test_candidate_stages(self):
        path = BASE / 'amorphous_lzoc_candidate.lmp'
        self.assertTrue(path.exists(), 'Candidate input missing')
        text = path.read_text()
        for command in ['timestep 0.0005', 'pair_coeff * * Li Zr O Cl',
                        'fix mix all nvt temp 1500 1500 0.1',
                        'fix cool all nvt temp 1500 300 0.1',
                        'fix release all npt temp 300 300 0.1 iso 1 1 1.0',
                        'write_data candidate_final.data']:
            self.assertIn(command, text)
        steps = [int(l.split()[1]) for l in text.splitlines() if l.startswith('run ')]
        self.assertEqual(steps, [20000, 60000, 10000, 20000])
        self.assertNotIn('velocity all create', text)

    def test_single_job(self):
        path = BASE / 'amorphous_lzoc_candidate.sh'
        self.assertTrue(path.exists(), 'Candidate wrapper missing')
        text = path.read_text()
        self.assertNotIn('#$ -t ', text)
        self.assertIn('rebuild_8628860/replica_1', text)
        self.assertIn('candidate_${JOB_ID', text)
        self.assertIn('sha256sum', text)

if __name__ == '__main__':
    unittest.main()
