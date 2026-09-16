"""Submission contract checks; actual LAMMPS execution remains a GPU check."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'hpc/tsubame_26icp/production'


class HighTemperatureContract(unittest.TestCase):
    def test_lammps_stage(self):
        path = BASE / 'amorphous_lzoc_high_temperature.lmp'
        self.assertTrue(path.is_file(), 'High-temperature input missing')
        text = path.read_text()
        for command in ['read_data input.data', 'pair_coeff * * Li Zr O Cl',
                        'timestep 0.0005', 'run 40000',
                        'fix bath all npt temp 1500 1500 0.1 iso 1.0 1.0 1.0',
                        'restart 2000 restart.*.bin',
                        'write_data high_temperature_final.data']:
            self.assertIn(command, text)
        self.assertNotIn('velocity all create', text)

    def test_job_provenance_and_scope(self):
        path = BASE / 'amorphous_lzoc_high_temperature.sh'
        self.assertTrue(path.is_file(), 'High-temperature job missing')
        text = path.read_text()
        for value in ['#$ -t 1-3', '#$ -tc 1', '#$ -l h_rt=0:45:00',
                      'rebuild_8628860/replica_${SGE_TASK_ID}',
                      'high_temperature_${JOB_ID}/replica_${SGE_TASK_ID}',
                      'sha256sum', 'pilot_final.data', 'test -s high_temperature_final.data']:
            self.assertIn(value, text)
        self.assertNotIn('qsub', text)


if __name__ == '__main__':
    unittest.main()
