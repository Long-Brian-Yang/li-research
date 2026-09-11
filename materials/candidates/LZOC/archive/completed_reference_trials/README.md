# LZOC structure preparation archive

Three 192-atom Li42Zr24O12Cl114 candidates were prepared with MACE-MPA-0
on TSUBAME on 2026-09-11. Candidate 3 is provisionally selected for subsequent
work; see [selection and limitations](SELECTION.md). Numerical completion
does not establish full amorphization or validate the potential.

| Directory | Job/task | Kim 2025 source | Wall time | Final density (g/cm³) |
|---|---|---|---|---|
| [source_1](source_1/) | 8631903.1 | Supplementary Data 4 | 00:48:28 | 1.898929 |
| [source_2](source_2/) | 8631903.2 | Supplementary Data 19 | 00:47:20 | 1.911125 |
| [source_3](source_3/) | 8631935.3 | Supplementary Data 18 | 00:48:28 | 1.983256 |

These are related starting configurations, not independent amorphous replicas.
Each workflow comprises initial minimization, 10 ps mixing at 1500 K,
30 ps cooling to 300 K, 5 ps NVT and 10 ps NPT at 300 K, then final
fixed-cell minimization. All initial/final minimizations reached force tolerance.
The formal 50 ps equilibration + 200 ps production has not been submitted.

## Archive completeness

All three candidates now have the complete 15-file textual/structure-endpoint
set listed below. The interrupted transfer was resumed successfully, including
the actual job snapshots for sources 2 and 3. Archived input, input script and
job-wrapper hashes were checked against each run's `input_sha256.txt`.
Trajectory, restart and model/environment files remain excluded as described
below; completeness here refers to the textual/structure-endpoint archive.

## Run file definitions

- `input.data`: actual initial atomic structure.
- `initial_minimized.data`, `mixed.data`, `quenched.data`,
  `before_release.data`, `relaxed_300K.data`: preparation endpoints.
- `candidate_final.data`: final minimized structure, types 1/2/3/4 = Li/Zr/O/Cl.
- `candidate.log`, `stdout.txt`, `stderr.txt`: unmodified calculation logs.
- `in.lmp`, `submitted_job.sh`: actual submitted input and wrapper snapshots.
- `initial_structure_metadata.json`, `provenance.txt`, `input_sha256.txt`:
  source, construction procedure and original input/model fingerprints.

`input_sha256.txt` includes the remote model path; the model itself is not
bundled. Source paths in metadata preserve the original run provenance.
Git stores the structures and textual records, not trajectories, binary restart
files, model weights or software environments. These remain in the TSUBAME
run directories documented in `provenance.txt` and [SELECTION.md](SELECTION.md).

Literature source: Kim et al. (2025),
[DOI: 10.1038/s41467-025-65702-2](https://doi.org/10.1038/s41467-025-65702-2).
Published supplementary structures are CC BY 4.0. The archived inputs are
composition-adjusted derivatives, not the original published compositions.
