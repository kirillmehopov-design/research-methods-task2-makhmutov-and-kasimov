# Bibliography verification

Checked on 19 November 2026. The Task 1 library is preserved byte-for-byte in
`library/Task1_References_Makhmutov_Kasimov.bib`. The compiled `.bib` selects ten
of those sources plus Guglielmi et al. and Ziegler et al.; all twelve are cited.

## Publication records

Crossref records matched titles and publication types for Imai, Moradi Dakhel,
Barke, Haindl, Kosar, Prather, Zare, Gambacorta, Hou, and Ziegler: journal articles
or scholarly proceedings papers. Crossref identifies publications rather than
documenting editorial review procedures. Guglielmi and Sergeyuk requests were
throttled; their publisher pages were checked instead.

- `imai2022substitute`: [IEEE proceedings](https://doi.org/10.1109/ICSE-Companion55297.2022.9793778).
- `dakhel2023asset`: [Journal of Systems and Software](https://doi.org/10.1016/j.jss.2023.111734).
- `barke2023grounded`: [PACMPL](https://doi.org/10.1145/3586030), [author-hosted version of record](https://shraddhabarke.github.io/raw/copilot.pdf).
- `haindl2024chatgpt`: [IEEE Access](https://doi.org/10.1109/ACCESS.2024.3445432).
- `kosar2024education`: [Mathematics](https://www.mdpi.com/2227-7390/12/5/629).
- `prather2024widening`: [ICER](https://doi.org/10.1145/3632620.3671116), [institutional record](https://research.aalto.fi/fi/publications/the-widening-gap-the-benefits-and-harms-of-generative-ai-for-novi/).
- `sergeyuk2025assistants`: [Information and Software Technology](https://www.sciencedirect.com/science/article/abs/pii/S0950584924002155).
- `zare2026security`: [HCII proceedings](https://doi.org/10.1007/978-3-032-29723-5_35).
- `gambacorta2026productivity`: [Journal of Financial Stability](https://www.sciencedirect.com/science/article/pii/S1572308926000458).
- `hou2024slr`: [ACM TOSEM](https://doi.org/10.1145/3695988), [author manuscript](https://arxiv.org/abs/2308.10620).
- `guglielmi2026copilot`: [Empirical Software Engineering](https://doi.org/10.1007/s10664-026-10965-6).
- `ziegler2022productivity`: [MAPS](https://doi.org/10.1145/3520312.3534864), [author manuscript](https://arxiv.org/abs/2205.06537).

Guglielmi appeared online on 3 November 2026; the publisher assigns volume 32,
article 42 to 2027. The citation uses 2027 and preserves the existing key.
Barke uses article-local pages 78:1--78:27 from the version of record; Crossref
also records continuous pages 85--111. Acronyms and product names are protected
in titles. DOI fields are retained without duplicate URLs.

## Selection and integration

Peng's Task 1 record is an arXiv preprint and is not counted toward the required
peer-reviewed total. Feng and Balasuriya remain in the preserved library; they
are omitted from the focused paper for scope and space. Related studies provide
context rather than pooled numerical baselines. Manual Copilot invocation in
the source dataset is the actual baseline.

The supplied `.bib` establishes the origin of the Task 1 references. A new Zotero
export or live Overleaf synchronization has not been performed in this contribution.
Complete the documented import/export workflow before claiming that integration.

## Final paper completion

The twelve existing keys and DOI fields are retained. Short linked Publisher
record notes make DOI destinations clickable in IEEEtran output, which otherwise
does not print the DOI field. No duplicate URL fields or local paths were added.
The original Task 1 library remains byte-identical to commit 0c62ac2.
Zotero import/export and live synchronization were unavailable and were not run.
