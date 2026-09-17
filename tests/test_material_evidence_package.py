import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import read

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/structures"))


class MaterialEvidencePackageTests(unittest.TestCase):
    def test_uniform_indices_include_first_and_last_frame(self):
        from build_material_evidence_package import uniform_indices

        indices = uniform_indices(total_frames=1001, target_frames=101)
        self.assertEqual(len(indices), 101)
        self.assertEqual(indices[0], 0)
        self.assertEqual(indices[-1], 1000)
        self.assertTrue(np.all(np.diff(indices) > 0))

    def test_write_xyz_chunks_preserves_metadata_and_frame_order(self):
        from build_material_evidence_package import write_xyz_chunks

        frames = []
        for index in range(7):
            atoms = Atoms("Li2", positions=[[index, 0, 0], [0, index, 0]],
                          cell=[10, 10, 10], pbc=True)
            frames.append(atoms)

        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary)
            records = write_xyz_chunks(
                frames=frames,
                selected_indices=[0, 2, 4, 6],
                output_dir=out,
                stem="trajectory_600K",
                frame_interval_ps=0.1,
                max_frames_per_chunk=2,
                common_metadata={"material": "test", "temperature_K": 600},
            )

            self.assertEqual(len(records), 2)
            self.assertEqual([r["source_frame_indices"] for r in records],
                             [[0, 2], [4, 6]])
            self.assertEqual(records[0]["time_ps"], [0.0, 0.2])
            self.assertEqual(records[1]["time_ps"], [0.4, 0.6])
            for record in records:
                path = out / record["file"]
                self.assertTrue(path.is_file())
                self.assertEqual(len(read(path, index=":")), 2)
                self.assertEqual(record["atom_count"], 2)
                self.assertEqual(len(record["sha256"]), 64)

    def test_readme_explains_sampled_trajectory_scope(self):
        from build_material_evidence_package import render_readme

        text = render_readme({"structures": [], "trajectories": []})
        self.assertIn("complete source trajectories", text.lower())
        self.assertIn("manifest.json", text)
        self.assertIn("uniformly sampled", text.lower())

    def test_readme_uses_manifest_directory_for_trajectory_links(self):
        from build_material_evidence_package import render_readme

        manifest = {
            "structures": [],
            "trajectories": [{
                "id": "example",
                "directory": "amorphous/example",
                "purpose": "NVT production",
                "metadata": {"material": "LiX", "model": "NEP89", "temperature_K": 600},
                "chunks": [{"file": "trajectory_part01.xyz"}],
            }],
        }
        text = render_readme(manifest)
        self.assertIn("(amorphous/example/trajectory_part01.xyz)", text)

    def test_lammps_type_numbers_can_be_restored_to_elements(self):
        from build_material_evidence_package import apply_type_symbols

        frame = Atoms(numbers=[1, 2, 3, 1], positions=np.zeros((4, 3)))
        fixed = apply_type_symbols(frame, {1: "Li", 2: "Y", 3: "Cl"})
        self.assertEqual(fixed.get_chemical_symbols(), ["Li", "Y", "Cl", "Li"])


if __name__ == "__main__":
    unittest.main()
