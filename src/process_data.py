"""Validate the published measurements and calculate participant-level changes."""
import csv
import hashlib
import io
import json
import math
import re
from pathlib import Path


class DataError(ValueError):
    pass


def parse_csv(text, group):
    if group not in {'novice', 'expert'}:
        raise DataError('Unknown experience group')
    reader = csv.DictReader(io.StringIO(text.replace('\r\r\n', '\n')))
    required = {'User ID', 'Study group', 'Session', 'Completeness', 'PRODa'}
    if not required.issubset(reader.fieldnames or []):
        raise DataError('Missing source columns')
    time_column = next((x for x in ('Time (min)', 'Time(min)') if x in reader.fieldnames), None)
    if time_column is None:
        raise DataError('Missing time column')
    result = []
    for source in reader:
        def number(key):
            try:
                value = float(source[key].strip().replace(',', '.'))
            except (KeyError, AttributeError, ValueError) as exc:
                raise DataError(f'Invalid value for {key}') from exc
            if not math.isfinite(value):
                raise DataError(f'Non-finite value for {key}')
            return value
        session = re.fullmatch(r'SUGG (enabled|disabled) - Task ([AB])', source['Session'].strip())
        if not session:
            raise DataError('Unknown session label')
        sequence = source['Study group'].strip()
        if sequence not in {'A', 'B', 'C', 'D'}:
            raise DataError('Unknown assignment group')
        mode = 'automatic' if session[1] == 'enabled' else 'manual'
        task = session[2]
        automatic_task = 'A' if sequence in {'A', 'D'} else 'B'
        if (task == automatic_task) != (mode == 'automatic'):
            raise DataError('Task assignment disagrees with sequence')
        completion, minutes = number('Completeness'), number(time_column)
        if not 0 <= completion <= 100 or minutes <= 0:
            raise DataError('Completion or time outside valid range')
        productivity = (completion / 100) / (minutes / 60)
        if abs(productivity - number('PRODa')) > 1e-8:
            raise DataError('Published productivity disagrees with completion/time')
        participant = source['User ID'].strip()
        if not participant:
            raise DataError('Empty participant ID')
        result.append(dict(participant_id=participant, experience_group=group,
                           sequence=sequence, mode=mode, task=task,
                           completion_pct=completion, time_minutes=minutes,
                           productivity_per_hour=productivity))
    if not result:
        raise DataError('Empty input')
    return result


def validate_pairs(records):
    participants = {}
    for row in records:
        pair = participants.setdefault(row['participant_id'], {})
        if row['mode'] in pair:
            raise DataError('Duplicate participant/mode')
        pair[row['mode']] = row
    for pid, pair in participants.items():
        if set(pair) != {'manual', 'automatic'}:
            raise DataError(f'Incomplete pair: {pid}')
        a, m = pair['automatic'], pair['manual']
        if a['experience_group'] != m['experience_group'] or a['sequence'] != m['sequence']:
            raise DataError(f'Inconsistent participant metadata: {pid}')
        if a['task'] == m['task']:
            raise DataError(f'Repeated task: {pid}')
    if {r['experience_group'] for r in records} != {'novice', 'expert'}:
        raise DataError('Both experience groups are required')


def read_data(root, config):
    root = Path(root)
    provenance = json.loads((root / config['provenance_file']).read_text(encoding='utf-8'))
    expected = {f['file']: f['sha256'] for f in provenance['files']}
    records = []
    for group, filename in config['input_files'].items():
        path = root / filename
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected.get(path.name):
            raise DataError(f'Source checksum mismatch: {path.name}')
        records.extend(parse_csv(raw.decode('utf-8-sig'), group))
    validate_pairs(records)
    return records


def paired_changes(records):
    pairs = {}
    for row in records:
        pairs.setdefault(row['participant_id'], {})[row['mode']] = row
    result = []
    for pid, pair in sorted(pairs.items()):
        a, m = pair['automatic'], pair['manual']
        row = dict(participant_id=pid, experience_group=a['experience_group'], sequence=a['sequence'])
        for field in ('productivity_per_hour', 'completion_pct', 'time_minutes'):
            row[field + '_change'] = a[field] - m[field]
        result.append(row)
    return result


def write_csv(path, rows):
    with Path(path).open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
