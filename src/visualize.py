"""Create scientific figures from verified analysis outputs."""
import csv
import json
import random
import statistics
from pathlib import Path

from .benchmark import interval

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'novice': '#0072B2', 'expert': '#D55E00'}
GROUPS = ('novice', 'expert')


def export(figure, folder, name):
    figure.savefig(folder / (name + '.pdf'), bbox_inches='tight')
    figure.savefig(folder / (name + '.png'), dpi=300, bbox_inches='tight')
    plt.close(figure)


def draw_figures(root):
    root = Path(root)
    folder = root / 'reports/figures'
    folder.mkdir(parents=True, exist_ok=True)
    result = json.loads((root / 'data/processed/results.json').read_text())
    with (root / 'data/processed/observations.csv').open(newline='') as handle:
        records = list(csv.DictReader(handle))
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'pdf.fonttype': 42,
                         'axes.axisbelow': True})

    fig, ax = plt.subplots(figsize=(7.2, 3.8), layout='constrained')
    labels = ['Novices', 'Experts', 'Experts minus novices']
    estimates = [result['by_group'][g]['paired_changes']['productivity_per_hour_change']
                 for g in GROUPS] + [result['primary_contrast']]
    for i, (entry, color, marker) in enumerate(zip(estimates,
                [COLORS[g] for g in GROUPS] + ['#333333'], ['o', 's', 'D'])):
        mean = entry.get('mean', entry.get('estimate'))
        low, high = entry['ci95']
        ax.errorbar(mean, 2 - i, xerr=[[mean - low], [high - mean]],
                    fmt=marker, color=color, capsize=5, markersize=7)
    ax.axvline(0, color='0.5', linestyle='--', linewidth=1)
    ax.set(yticks=[2, 1, 0], yticklabels=labels, ylim=(-.5, 2.5),
           xlabel='Productivity change (completed task fraction/hour)',
           ylabel='Comparison', title='Automatic minus manual: paired changes and group contrast')
    ax.grid(axis='x', alpha=.25)
    export(fig, folder, 'fig1_paired_changes')

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.8), sharey=True, layout='constrained')
    rng = random.Random(42)
    for ax, group in zip(axes, GROUPS):
        data = []
        for mode in ('manual', 'automatic'):
            data.append([float(r['productivity_per_hour']) for r in records
                         if r['experience_group'] == group and r['mode'] == mode])
        ax.boxplot(data, positions=[1, 2], widths=.45, showfliers=False,
                   medianprops={'color': 'black'}, patch_artist=False)
        people = {}
        for row in records:
            if row['experience_group'] == group:
                people.setdefault(row['participant_id'], {})[row['mode']] = float(row['productivity_per_hour'])
        for pair in people.values():
            jitter = rng.uniform(-.06, .06)
            ax.plot([1 + jitter, 2 + jitter], [pair['manual'], pair['automatic']],
                    color=COLORS[group], marker='o' if group == 'novice' else 's',
                    alpha=.45, linewidth=.65, markersize=3)
        for position, values in enumerate(data, 1):
            mean = statistics.mean(values)
            low, high = interval([statistics.mean(rng.choices(values, k=len(values)))
                                  for _ in range(10000)])
            ax.errorbar(position + .23, mean, yerr=[[mean - low], [high - mean]],
                        fmt='D', color='black', capsize=3, markersize=4)
        ax.set(xticks=[1, 2], xticklabels=['Manual', 'Automatic'], xlabel='Copilot mode',
               title=f'{group.title()}s (n = {len(people)})')
        ax.grid(axis='y', alpha=.25)
    axes[0].set_ylim(0, max(float(r['productivity_per_hour']) for r in records) * 1.08)
    axes[0].set_ylabel('Productivity (completed task fraction/hour)')
    fig.suptitle('Observed distributions and participant pairs')
    export(fig, folder, 'fig2_productivity_distribution')

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6), layout='constrained')
    for ax, metric, title, unit in zip(axes, ['completion_pct', 'time_minutes'],
                                     ['Completion change', 'Session time change'],
                                     ['percentage points', 'minutes']):
        for i, group in enumerate(GROUPS):
            entry = result['by_group'][group]['paired_changes'][metric + '_change']
            mean, (low, high) = entry['mean'], entry['ci95']
            ax.errorbar(i, mean, yerr=[[mean - low], [high - mean]], color=COLORS[group],
                        fmt='o' if i == 0 else 's', capsize=5)
        ax.axhline(0, color='0.5', linestyle='--', linewidth=1)
        if metric == 'completion_pct':
            ax.axhline(-5, color='0.25', linestyle=':', label='Reporting threshold (-5 pp)')
            ax.legend(fontsize=8)
        ax.set(xticks=[0, 1], xticklabels=['Novices', 'Experts'], xlim=(-.5, 1.5),
               xlabel='Experience group', ylabel=f'Automatic minus manual ({unit})', title=title)
        ax.grid(axis='y', alpha=.25)
    export(fig, folder, 'fig3_completion_time')

    with (root / 'data/processed/runtime_summary.csv').open(newline='') as handle:
        runtime = list(csv.DictReader(handle))
    fig, ax = plt.subplots(figsize=(6.4, 3.5), layout='constrained')
    xs = [int(r['input_rows']) for r in runtime]
    means = [float(r['mean_ms']) for r in runtime]
    ax.errorbar(xs, means,
                yerr=[[m - float(r['ci95_low_ms']) for m, r in zip(means, runtime)],
                      [float(r['ci95_high_ms']) - m for m, r in zip(means, runtime)]],
                color=COLORS['novice'], fmt='o--', capsize=5)
    ax.set(xlabel='Input size (session rows)', ylabel='Parsing and pair-validation time (ms)',
           title='Supplementary local code benchmark', xticks=xs, ylim=(0, None))
    ax.grid(alpha=.25)
    export(fig, folder, 'fig4_runtime')
    return sorted(folder.glob('*.png'))


if __name__ == '__main__':
    draw_figures(Path(__file__).resolve().parents[1])
