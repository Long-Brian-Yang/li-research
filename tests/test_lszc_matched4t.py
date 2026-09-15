from pathlib import Path
import subprocess
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/structures/submit_lszc_matched4t.sh'

class MatchedTests(unittest.TestCase):
    def test_matched_four_temperatures(self):
        self.assertTrue(SCRIPT.is_file(),'matched four-temperature runner missing')
        plans=[]
        for task,T in enumerate([320,330,340,350],1):
            s=subprocess.check_output(['bash',str(SCRIPT),'--plan',str(task)],text=True)
            self.assertIn(f'T={T}',s)
            self.assertIn('equil50|100000',s)
            self.assertIn('production|600000',s)
            self.assertIn('time_step=0.5',s)
            plans.append(s.splitlines()[1])
        self.assertEqual(len(set(plans)),1,'all temperatures must use the same source cell')

    def test_reject_bad_task(self):
        self.assertTrue(SCRIPT.is_file(),'matched four-temperature runner missing')
        self.assertNotEqual(subprocess.run(['bash',str(SCRIPT),'--plan','0'],capture_output=True).returncode,0)

if __name__=='__main__':unittest.main()
