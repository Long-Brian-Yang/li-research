from pathlib import Path
import os
import subprocess
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'hpc/tsubame_26icp/production/nep89_npt_extension.sh'

class Extension(unittest.TestCase):
    def test_three_inputs_and_duration(self):
        self.assertTrue(SCRIPT.exists(), 'NPT extension script must exist')
        for temp, job in ((700,8653328),(800,8653329),(900,8653330)):
            r = subprocess.run(['bash',str(SCRIPT),'--print-input'], env={**os.environ,'TARGET_TEMP':str(temp)}, text=True,capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn(f'{temp}K_R1_{job}/equilibration/restart.xyz',r.stdout)
            self.assertIn(f'npt_mttk temp {temp} {temp} iso 0.0001 0.0001',r.stdout)
            self.assertIn('time_step 0.5',r.stdout)
            self.assertIn('run 100000',r.stdout)
            self.assertNotIn('nvt_mttk',r.stdout)
            self.assertNotIn('velocity ',r.stdout)
            self.assertNotIn('minimize ',r.stdout)
    def test_reject_600(self):
        self.assertTrue(SCRIPT.exists())
        r = subprocess.run(['bash',str(SCRIPT),'--print-input'],env={**os.environ,'TARGET_TEMP':'600'},capture_output=True)
        self.assertNotEqual(r.returncode,0)

if __name__ == '__main__': unittest.main()
