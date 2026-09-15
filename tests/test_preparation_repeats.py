"""Check actual dry-run schedules before scheduler submission."""
from pathlib import Path
import subprocess
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/structures/submit_preparation_repeats.sh'

class PreparationTests(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(SCRIPT.is_file(), 'bounded preparation runner missing')

    def test_schedules(self):
        self.assertTrue(SCRIPT.is_file(), 'bounded preparation runner missing')
        for task, material, total in [(1,'Li3PS4',611),(2,'Li3PS4',611),(3,'LiPON',63),(4,'LiPON',63)]:
            out=subprocess.check_output(['bash',str(SCRIPT),'--plan',str(task)],text=True)
            self.assertIn(material,out)
            rows=[line.split('|') for line in out.splitlines() if '|' in line]
            self.assertEqual(sum(int(row[1])*.5/1000 for row in rows),total)
            self.assertNotIn('production', ' '.join(row[0] for row in rows))
            self.assertTrue(all(int(row[1])%100==0 for row in rows))
        a=subprocess.check_output(['bash',str(SCRIPT),'--plan','1'],text=True)
        b=subprocess.check_output(['bash',str(SCRIPT),'--plan','2'],text=True)
        self.assertNotEqual(a.splitlines()[0],b.splitlines()[0])

    def test_invalid_task(self):
        self.assertTrue(SCRIPT.is_file(), 'bounded preparation runner missing')
        self.assertNotEqual(subprocess.run(['bash',str(SCRIPT),'--plan','5'],capture_output=True).returncode,0)

if __name__=='__main__': unittest.main()
