import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / 'hpc/tsubame_26icp/production/check_lzoc_virial.py'

class VirialCheckTest(unittest.TestCase):
    def test_pressure_sign_and_units(self):
        self.assertTrue(PATH.exists(), 'Virial diagnostic implementation missing')
        spec = importlib.util.spec_from_file_location('virial', PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # U(V)=-2 V eV: -dU/dV=+2 eV/Angstrom^3.
        self.assertAlmostEqual(module.fd_pressure(-198., -202., 99., 101.), 3204353.268)

if __name__ == '__main__':
    unittest.main()
