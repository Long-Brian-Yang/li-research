from pathlib import Path
import subprocess
import unittest

BASE=Path(__file__).resolve().parents[1]/'hpc/shared/nep89_gpumd'
class SharedGPUMD(unittest.TestCase):
    def test_shared_interface_and_output_isolation(self):
        self.assertTrue((BASE/'paths.sh').exists())
        s=(BASE/'run_gpumd.sh').read_text()
        self.assertIn('SGE_O_WORKDIR',s)
        self.assertIn('JOB_ID',s)
        self.assertIn('mkdir "$OUT"',s)
        self.assertIn('cp "$WORK/model.xyz" "$WORK/run.in" "$OUT/"',s)
        self.assertNotIn('make ',s)
        for f in ('paths.sh','run_gpumd.sh'):
            self.assertEqual(subprocess.run(['bash','-n',str(BASE/f)]).returncode,0)

if __name__=='__main__': unittest.main()
