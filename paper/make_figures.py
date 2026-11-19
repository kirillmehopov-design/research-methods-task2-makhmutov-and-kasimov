"""Render compact vector figures from the authoritative Task 3 results."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
r = json.loads((ROOT / 'data/processed/results.json').read_text())
out = ROOT / 'paper/figures'
out.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 8, 'pdf.fonttype': 42, 'axes.spines.top': False,
                     'axes.spines.right': False})
colors = ['#0072B2', '#D55E00', '#333333']
markers = ['o', 's', 'D']
fig, ax = plt.subplots(figsize=(3.5, 2.0), layout='constrained')
entries = [r['by_group'][g]['paired_changes']['productivity_per_hour_change']
           for g in ('novice', 'expert')] + [r['primary_contrast']]
for y, e, c, m in zip([2, 1, 0], entries, colors, markers):
    mean = e.get('mean', e.get('estimate'))
    lo, hi = e['ci95']
    ax.errorbar(mean, y, xerr=[[mean-lo], [hi-mean]], fmt=m, color=c, capsize=3)
ax.axvline(0, color='.5', ls='--', lw=.8)
ax.set(yticks=[2, 1, 0], yticklabels=['Novices', 'Experts', 'Experts minus\nnovices'],
       xlabel='Change (completed task fraction/hour)', ylim=(-.5, 2.5))
ax.grid(axis='x', alpha=.2)
fig.savefig(out / 'fig1_paired_changes.pdf')
plt.close(fig)
fig, axes = plt.subplots(1, 2, figsize=(3.5, 2.1), layout='constrained')
for ax, metric, unit, title in zip(axes, ['completion_pct', 'time_minutes'],
                                 ['Percentage points', 'Minutes'], ['Completion', 'Session time']):
    for x, g in enumerate(('novice', 'expert')):
        e = r['by_group'][g]['paired_changes'][metric+'_change']
        mean, (lo, hi) = e['mean'], e['ci95']
        ax.errorbar(x, mean, yerr=[[mean-lo], [hi-mean]], fmt=markers[x],
                    color=colors[x], capsize=3)
    ax.axhline(0, color='.5', ls='--', lw=.8)
    if metric == 'completion_pct':
        ax.axhline(-5, color='.3', ls=':', lw=1)
    ax.set(xticks=[0, 1], xticklabels=['Novice', 'Expert'], xlim=(-.5, 1.5),
           ylabel=unit, title=title)
    ax.grid(axis='y', alpha=.2)
fig.savefig(out / 'fig3_completion_time.pdf')
plt.close(fig)
