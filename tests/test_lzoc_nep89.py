from pathlib import Path
import unittest

class Protocol(unittest.TestCase):
    def test_parameterized_temperatures_and_no_shared_build(self):
        s=(Path(__file__).resolve().parents[1]/'hpc/tsubame_26icp/production/lzoc_nep89.sh').read_text()
        self.assertIn('TARGET_TEMP=${TARGET_TEMP:-600}',s)
        self.assertIn('600|700|800|900)',s)
        self.assertIn('${TARGET_TEMP}K_R1_${JOB_ID:?}',s)
        self.assertIn('nvt_mttk temp 300 ${TARGET_TEMP}',s)
        self.assertIn('npt_mttk temp ${TARGET_TEMP} ${TARGET_TEMP} iso 0.0001 0.0001',s)
        self.assertIn('nvt_mttk temp ${TARGET_TEMP} ${TARGET_TEMP}',s)
        self.assertNotIn('make -j',s)
        for n in ('STEPS=100000','STEPS=400000','time_step 0.5'):
            self.assertIn(n,s)

if __name__=='__main__': unittest.main()
