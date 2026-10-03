import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('econ_lab', ROOT / 'tools/econ_lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

class EconomicDataTests(unittest.TestCase):
    def test_future_vintage_never_leaks(self):
        rows = lab.read_rows(ROOT / 'data/observations.csv')
        def gdp(cutoff):
            return [r['value'] for r in lab.snapshot(rows, cutoff) if r['series_id']=='cn_gdp_nominal']
        self.assertEqual(gdp('2025-01-16'), [])
        self.assertEqual(gdp('2025-06-30'), ['1349084'])
        self.assertEqual(gdp('2025-12-26'), ['1348066'])
        self.assertEqual(len(rows), 7)

    def test_cumulative_boundaries(self):
        a,b,c = lab.read_rows(ROOT / 'data/teaching_cumulative.csv')
        self.assertEqual(lab.single_month(b,a), 120)
        with self.assertRaises(ValueError): lab.single_month(c,b)
        with self.assertRaises(ValueError): lab.single_month(b,{**a,'unit':'million_CNY'})
        with self.assertRaises(ValueError): lab.single_month({**b,'measure':'real_yoy'},{**a,'measure':'real_yoy'})
        with self.assertRaises(ValueError): lab.single_month({**b,'period_end':'2025-05-31'},a)
        with self.assertRaises(ValueError): lab.single_month({**b,'period_end':'2025-03-30'},a)

    def test_duplicate_vintage_rejected(self):
        rows = lab.read_rows(ROOT / 'data/observations.csv')
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'duplicate.csv'
            with f.open('w',newline='') as out:
                writer=csv.DictWriter(out,fieldnames=rows[0].keys())
                writer.writeheader();writer.writerows([rows[0],rows[0]])
            with self.assertRaises(ValueError): lab.read_rows(f)

    def test_mortgage_accounting(self):
        b=1_000_000; rate=.033; payment=lab.monthly_payment(b,rate,300)
        self.assertAlmostEqual(payment,4899.615665856319,places=6)
        principal=0; interest=0
        for _ in range(12):
            charge=b*rate/12;paid=payment-charge;b-=paid;principal+=paid;interest+=charge
        self.assertAlmostEqual(principal+interest,12*payment,places=6)
        self.assertAlmostEqual(b,973810.858116508,places=5)
        self.assertEqual(lab.monthly_payment(1200,0,12),100)
        with self.assertRaises(ValueError):lab.monthly_payment(100,.03,0)

if __name__ == '__main__': unittest.main()
