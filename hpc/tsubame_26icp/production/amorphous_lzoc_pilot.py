"""Prepare a seeded, neutral-composition random LZOC cell and LAMMPS pilot.

The initial density is a numerical starting assumption, not experimental data.
This pilot does not certify amorphization or authorize production automatically.
"""
import json
import random
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=20260911)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    length = 19.0
    types = [1]*56 + [2]*32 + [3]*16 + [4]*152
    rng.shuffle(types)
    points = []
    # Initialization-only constraints; no distance restraints in MACE MD.
    cutoffs = {(1,1):2.0,(1,2):2.4,(1,3):1.9,(1,4):2.2,
               (2,2):3.0,(2,3):1.9,(2,4):2.3,
               (3,3):2.8,(3,4):2.5,(4,4):2.5}
    for kind in types:
        for attempt in range(100000):
            xyz = [rng.random()*length for _ in range(3)]
            if all(sum(min(abs(a-b), length-abs(a-b))**2 for a,b in zip(xyz,p)) >= cutoffs[tuple(sorted((kind,oldkind)))]**2 for p,oldkind in zip(points,types)):
                points.append(xyz)
                break
        else:
            raise RuntimeError('Packing failed')
    lines = ['LZOC random starting cell; not yet amorphous','', '256 atoms', '4 atom types','']
    lines += [f'0 {length} {axis}lo {axis}hi' for axis in 'xyz']
    lines += ['', 'Masses','', '1 6.94','2 91.224','3 15.999','4 35.45','','Atoms # atomic','']
    lines += [f'{i} {k} '+ ' '.join(f'{a:.10f}' for a in p) for i,(k,p) in enumerate(zip(types,points),1)]
    Path('input.data').write_text('\n'.join(lines)+'\n')
    Path('metadata.json').write_text(json.dumps(dict(composition='Li1.75ZrO0.5Cl4.75', counts=dict(Li=56,Zr=32,O=16,Cl=152),seed=args.seed,initial_box_A=length,pair_min_distance_A={f'{i}-{j}':v for (i,j),v in cutoffs.items()},type_map={'1':'Li','2':'Zr','3':'O','4':'Cl'},stage='rebuild pilot v2; not validated amorphous'),indent=2)+'\n')

if __name__ == '__main__':
    main()
