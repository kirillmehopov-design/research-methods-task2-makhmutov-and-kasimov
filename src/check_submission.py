"""Validate saved notebook outputs, figure formats, and submission data."""
import json
from pathlib import Path

import nbformat
from PIL import Image


def check(root):
    root = Path(root)
    notebook = nbformat.read(root / 'notebooks/01_data_analysis.ipynb', as_version=4)
    nbformat.validate(notebook)
    cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
    assert cells, 'Notebook has no code cells'
    assert [cell.execution_count for cell in cells] == list(range(1, len(cells) + 1))
    assert all(cell.outputs for cell in cells), 'Missing visible output'
    assert not any(out.output_type == 'error' for cell in cells for out in cell.outputs)
    result = json.loads((root / 'data/processed/results.json').read_text())
    assert (result['participants'], result['observations']) == (33, 66)
    for name in ('fig1_paired_changes', 'fig2_productivity_distribution',
                 'fig3_completion_time', 'fig4_runtime'):
        pdf = root / 'reports/figures' / (name + '.pdf')
        assert pdf.read_bytes().startswith(b'%PDF'), f'Invalid PDF: {name}'
        with Image.open(root / 'reports/figures' / (name + '.png')) as image:
            assert min(image.info.get('dpi', (0, 0))) >= 299, f'Low DPI: {name}'
            image.verify()
    logs = [json.loads(line) for line in (root / 'data/raw/test_run.jsonl').read_text().splitlines()]
    config = json.loads((root / 'configs/runtime.json').read_text())
    for workload in ('sample', 'full'):
        for phase, key in [('warmup', 'warmup_runs'), ('benchmark', 'evaluation_runs')]:
            assert sum(r['workload'] == workload and r['phase'] == phase for r in logs) == config[key]
    assert (root / 'docs/domain_model.md').is_file()
    assert (root / 'reports/task3_report.md').is_file()
    print(f'Submission checks passed: {len(cells)} executed cells, 4 PDF/PNG pairs, 33 participant pairs.')


if __name__ == '__main__':
    check(Path(__file__).resolve().parents[1])
