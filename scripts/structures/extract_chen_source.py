"""Read-only extraction of published source workbook; run in bundled runtime."""
from pathlib import Path
import csv, json, hashlib
import openpyxl

root=Path(__file__).resolve().parents[2]
base=root/'results/amorphous_review_20260915'
out=base/'final_comparisons';out.mkdir(exist_ok=True,parents=True)
p=base/'source/literature/Chen2025_source.xlsx'
w=openpyxl.load_workbook(p,read_only=True,data_only=True)
for sheet in ['Fig. 1e','Fig. 1f','Fig. 1g','Fig. 3a','Fig. 3b']:
    with (out/('Chen2025_'+sheet.replace(' ','_')+'.csv')).open('w') as f:
        csv.writer(f,lineterminator='\n').writerows(w[sheet].values)
(out/'literature_source.json').write_text(json.dumps({
    'DOI':'10.1038/s41467-025-56322-x','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    'url':'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-56322-x/MediaObjects/41467_2025_56322_MOESM3_ESM.xlsx',
    'extracted_sheets':['Fig. 1e','Fig. 1f','Fig. 1g','Fig. 3a','Fig. 3b']},indent=2)+'\n')
