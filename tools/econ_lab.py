#!/usr/bin/env python3
"""Offline, date-precision vintage selection and guarded economic arithmetic."""
import argparse
import csv
import json
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {'series_id', 'period_start', 'period_end', 'frequency', 'measure', 'unit',
          'scope', 'method_version', 'comparability_group', 'release_date',
          'captured_date', 'value', 'kind', 'source_url'}


def read_rows(path):
    with Path(path).open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        if not FIELDS.issubset(reader.fieldnames or []):
            raise ValueError('Missing required observation fields')
        rows = list(reader)
    seen = set()
    for row in rows:
        if any(not row[k].strip() for k in FIELDS):
            raise ValueError('Empty required field')
        for k in ('period_start', 'period_end', 'release_date', 'captured_date'):
            date.fromisoformat(row[k])
        if row['period_end'] < row['period_start']:
            raise ValueError('Reversed observation period')
        value = Decimal(row['value'])
        if not value.is_finite():
            raise ValueError('Non-finite value')
        if row['kind'] not in {'official', 'teaching'}:
            raise ValueError('Unknown observation kind')
        if row['kind'] == 'official' and not row['source_url'].startswith('https://'):
            raise ValueError('Official observation needs source URL')
        key = tuple(row[k] for k in ('series_id', 'period_start', 'period_end', 'release_date'))
        if key in seen:
            raise ValueError('Duplicate date-precision vintage key')
        seen.add(key)
    return rows


def snapshot(rows, as_of):
    cutoff = date.fromisoformat(as_of)
    chosen = {}
    for row in rows:
        if date.fromisoformat(row['release_date']) > cutoff:
            continue
        key = tuple(row[k] for k in ('series_id', 'period_start', 'period_end'))
        if key not in chosen or row['release_date'] > chosen[key]['release_date']:
            chosen[key] = dict(row)
    return sorted(chosen.values(), key=lambda r: (r['series_id'], r['period_end']))


def single_month(current, previous):
    """Subtract consecutive YTD level/area observations only after explicit comparability checks."""
    for key in ('series_id', 'period_start', 'frequency', 'measure', 'unit', 'scope',
                'method_version', 'comparability_group', 'kind'):
        if current[key] != previous[key]:
            raise ValueError('Incompatible field: ' + key)
    if current['frequency'] != 'ytd' or current['measure'] not in {'nominal_level', 'area'}:
        raise ValueError('Only YTD levels/areas may be differenced')
    now, before = date.fromisoformat(current['period_end']), date.fromisoformat(previous['period_end'])
    start = date.fromisoformat(current['period_start'])
    if start != date(now.year, 1, 1) or now.year != before.year:
        raise ValueError('YTD observations must start in the same calendar year')
    if now.month != before.month + 1:
        raise ValueError('Cannot infer one month from non-consecutive periods')
    if before != date(now.year, now.month, 1) - timedelta(days=1) or (now + timedelta(days=1)).day != 1:
        raise ValueError('Month-end observations required')
    return Decimal(current['value']) - Decimal(previous['value'])


def monthly_payment(balance, annual_rate, months):
    balance, annual_rate = float(balance), float(annual_rate)
    if balance < 0 or annual_rate < 0 or months <= 0:
        raise ValueError('Invalid amortization parameters')
    if annual_rate == 0:
        return balance / months
    r = annual_rate / 12
    return balance * r / (1 - (1 + r) ** (-months))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'data/observations.csv')
    parser.add_argument('--as-of', required=True, help='YYYY-MM-DD, end-of-day information cutoff')
    args = parser.parse_args()
    try:
        rows = snapshot(read_rows(args.input), args.as_of)
    except (ValueError, OSError) as e:
        parser.error(str(e))
    print(json.dumps({'as_of': args.as_of, 'cutoff_precision': 'day_end',
                      'observations': rows}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
