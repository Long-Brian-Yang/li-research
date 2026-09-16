"""Static finite-volume pressure check; no relaxation, MD, or source edits."""
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

EV_A3_TO_BAR = 1602176.634


def fd_pressure(e_minus, e_plus, v_minus, v_plus):
    return -(e_plus - e_minus) / (v_plus - v_minus) * EV_A3_TO_BAR


def main():
    root = Path(os.environ['PROJECT_ROOT'])
    source = root / 'runs/amorphous/LZOC/mace_mpa0/high_temperature_8631254/replica_1'
    model = Path(os.environ['MODELS_ROOT']) / 'mace/mace-mpa-0-medium.model-mliap_lammps.pt'
    binary = os.environ['MACE_LMP_MLIAP']
    results = []
    metadata = {'model': str(model), 'model_sha256': hashlib.sha256(model.read_bytes()).hexdigest(),
                'epsilon_definition': 'fractional volume perturbation', 'kinetic_term': 'excluded',
                'snapshots': {}}
    for name, filename in [('start', 'input.data'), ('end', 'high_temperature_final.data')]:
        folder = Path(name)
        folder.mkdir()
        shutil.copy2(source / filename, folder / 'input.data')
        metadata['snapshots'][name] = {'source': str(source / filename),
            'sha256': hashlib.sha256((folder / 'input.data').read_bytes()).hexdigest()}
        lines = ['units metal', 'atom_style atomic', 'boundary p p p', 'atom_modify map yes',
                 'read_data input.data', f'pair_style mliap unified {model} 0',
                 'pair_coeff * * Li Zr O Cl', 'neighbor 2.0 bin',
                 'neigh_modify delay 0 every 1 check yes',
                 'compute pv all pressure NULL virial',
                 'thermo_style custom step pe vol c_pv', 'thermo_modify format float %.16g',
                 'run 0', 'print "CHECK base $(pe:%.16g) $(vol:%.16g) $(c_pv:%.16g)"']
        previous = 1.0
        for eps in [0.01, 0.003, 0.001]:
            for sign in [-1, 1]:
                scale = (1 + sign * eps) ** (1/3)
                ratio = scale / previous
                lines += [f'change_box all x scale {ratio:.17g} y scale {ratio:.17g} z scale {ratio:.17g} remap units box',
                          'run 0', f'print "CHECK {sign*eps:g} $(pe:%.16g) $(vol:%.16g) $(c_pv:%.16g)"']
                previous = scale
        (folder / 'in.lmp').write_text('\n'.join(lines) + '\n')
        with (folder / 'stdout.txt').open('w') as out, (folder / 'stderr.txt').open('w') as err:
            subprocess.run([binary, '-k', 'on', 'g', '1', '-sf', 'kk', '-pk', 'kokkos',
                            'newton', 'on', 'neigh', 'half', '-in', 'in.lmp', '-log', 'check.log'],
                           cwd=folder, stdout=out, stderr=err, check=True)
        measured = {}
        for line in (folder / 'stdout.txt').read_text().splitlines():
            if line.startswith('CHECK '):
                _, label, energy, volume, pressure = line.split()
                measured[label] = tuple(map(float, (energy, volume, pressure)))
        p_ref = measured['base'][2]
        for eps in [0.01, 0.003, 0.001]:
            minus = measured[f'{-eps:g}']; plus = measured[f'{eps:g}']
            p_fd = fd_pressure(minus[0], plus[0], minus[1], plus[1])
            results.append(dict(snapshot=name,volume_epsilon=eps,pressure_virial_bar=p_ref,
                pressure_finite_difference_bar=p_fd,difference_bar=p_fd-p_ref))
    Path('provenance.json').write_text(json.dumps(metadata, indent=2) + '\n')
    with Path('pressure_check.csv').open('w', newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0])); writer.writeheader(); writer.writerows(results)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
