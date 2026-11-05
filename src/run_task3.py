"""Rebuild all Task 3 deliverables and execute the notebook in a fresh kernel."""
import json
import asyncio
import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

from .report import write_report
from .runtime_benchmark import collect_runtime
from .task3_analysis import build_analysis, save_analysis
from .visualize import draw_figures


def execute_notebook(root):
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    kernel_root = root / 'outputs/jupyter'
    spec = kernel_root / 'kernels/task3'
    spec.mkdir(parents=True, exist_ok=True)
    (spec / 'kernel.json').write_text(json.dumps({
        'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'display_name': 'Task 3 Python', 'language': 'python',
    }))
    old_path = os.environ.get('JUPYTER_PATH')
    os.environ['JUPYTER_PATH'] = str(kernel_root) + (os.pathsep + old_path if old_path else '')
    os.environ['JUPYTER_PLATFORM_DIRS'] = '1'
    os.environ['IPYTHONDIR'] = str(root / 'outputs/ipython')
    os.environ['JUPYTER_RUNTIME_DIR'] = str(root / 'outputs/jupyter_runtime')
    notebook_path = root / 'notebooks/01_data_analysis.ipynb'
    try:
        notebook = nbformat.read(notebook_path, as_version=4)
        client = NotebookClient(notebook, timeout=180, kernel_name='task3',
                                resources={'metadata': {'path': str(root / 'notebooks')}})
        client.execute()
        notebook.metadata.kernelspec = {
            'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
        nbformat.write(notebook, notebook_path)
    finally:
        if old_path is None:
            os.environ.pop('JUPYTER_PATH', None)
        else:
            os.environ['JUPYTER_PATH'] = old_path


def main():
    root = Path(__file__).resolve().parents[1]
    save_analysis(root, build_analysis(root))
    print('Saved the 66 sessions, 33 pairs, and statistical results.', flush=True)
    collect_runtime(root)
    print('Collected separate runtime measurements.', flush=True)
    draw_figures(root)
    write_report(root)
    execute_notebook(root)
    from .check_submission import check
    check(root)
    print('Task 3 report, figures, and executed notebook are ready.', flush=True)


if __name__ == '__main__':
    main()
