# LiNbCl6 amorphous: supplement retrieved, coordinates still missing

Requested together with LSZC on 2026-09-14. Intended exploratory engine: existing NEP89/GPUMD, not AIMD reproduction.

Paper: Li et al., *First-principles determination of ionic conductivity in crystalline and amorphous LiNbCl6 solid-state electrolytes for lithium batteries*, Journal of Physics: Condensed Matter 38, 245701 (2026), https://doi.org/10.1088/1361-648X/ae778d.

Publisher supplement DOI: https://doi.org/10.1088/1361-648X/ae778d/data1.

Initial retrieval 2026-09-14: publisher /pdf returned HTML, supplement redirect returned CAPTCHA. On retry, normal browser navigation successfully opened the public supplement page and exposed the publisher DOCX link without solving/bypassing a CAPTCHA. Downloaded actual 6.5 MB file to source/cmae778dsupp1.docx. Main article browser page explicitly requires subscription/institutional access; no full text acquired.

## Verified supplement content

- Finite-size test: 3x3x3 crystalline supercell, Li27 Nb27 Cl162 = 216 atoms; 30 ps at 1200 K. This is not the amorphous model size.
- Another amorphous configuration: 400, 500, 600, 700 K; 180 ps production at each temperature divided into six 30 ps segments. Reported conductivity 16.99 mS/cm and barrier 0.20 eV, distinct from main-paper structure results.
- DOCX contains descriptive text and five figures. No machine-readable coordinate tables or embedded CIF/POSCAR files found. No explicit melt temperature, melt duration, cooling rate or quench duration in extracted supplementary text.
- Initial /data1 command-line retry still returned HTML CAPTCHA, but browser-based public download succeeded. Do not retain the old statement that the supplement remains inaccessible.

Verified figure caption describes amorphous AIMD at 400/500/600/700 K, but this does not establish the initial cell, coordinates or exact melt-quench schedule. NEP89 includes Li/Nb/Cl, which establishes element coverage only.

No structure generated, no job submitted. Still need full Methods and author coordinates (or user-provided files) before building the sourced model. No arbitrary reuse of LZOC/LiPS cooling conditions.
