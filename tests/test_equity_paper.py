"""Check the published equity parameters and worked-example arithmetic.

Run with: python3 -m unittest discover -s tests -v
These checks validate the paper's tables; they are not a production margin engine.
"""

import math
from pathlib import Path
import re
import unittest


PAPER = Path(__file__).resolve().parents[1] / "08equities.tex"


def table_rows(label):
    text = PAPER.read_text()
    table = text.split(r"\label{" + label + "}", 1)[1]
    body = table.split(r"\midrule", 1)[1].split(r"\bottomrule", 1)[0]
    return [
        [cell.strip() for cell in row.split("&")]
        for row in body.split(r"\\")
        if row.strip()
    ]


class EquityPaperTests(unittest.TestCase):
    def test_parameters_match_simm_v26(self):
        # ISDA SIMM v2.6 paragraphs 56, 59 and 77, independently transcribed
        # from the published parameter tables. Threshold units are USD million
        # of sensitivity to a 1% relative price move, not USD million notional.
        weights = [30, 33, 36, 29, 26, 25, 34, 28, 36, 50, 50]
        correlations = [.18, .20, .28, .24, .25, .36, .35, .37, .23, .27, 0]
        thresholds = [3, 3, 3, 3, 12, 12, 12, 12, .64, .37, .37]
        buckets = [str(i) for i in range(1, 11)] + ["Residual"]
        expected = list(zip(buckets, weights, correlations, thresholds))
        actual = [
            (bucket, float(weight), float(correlation), float(threshold))
            for bucket, weight, correlation, threshold
            in table_rows("tab:equity-parameters")
        ]
        self.assertEqual(actual, expected)

    def test_worked_example(self):
        # Independently evaluate the documented inputs and equations before
        # comparing each displayed percentage at its published precision.
        rows = table_rows("tab:equity-example")
        self.assertEqual(len(rows), 4)
        for cap, sessions, horizon, haircut, lltv, ltv in rows:
            with self.subTest(cap=cap):
                exposure = float(cap) * 1000
                count = math.ceil(exposure / (0.10 * 200_000))
                lh = max(10, 1 + count + 1)
                self.assertEqual(int(sessions), count)
                self.assertEqual(int(horizon), lh)
                concentration = max(1, math.sqrt(0.01 * exposure / 370_000))
                h0 = 50 * 0.01 * concentration * math.sqrt(lh / 10) + .025
                if h0 >= 1:
                    self.assertEqual(haircut, "Ineligible")
                    self.assertEqual(float(lltv), 0)
                    self.assertEqual(float(ltv), 0)
                    continue
                cost = .20 * lh / 252
                theta = .75 * (1 - h0) / (1 + .75 * cost)
                h = h0 + theta * cost
                for displayed, calculated in zip(
                    [haircut, lltv, ltv], [h, theta, max(0, theta - .08)]
                ):
                    self.assertEqual(displayed, f"{100 * calculated:.2f}")
                self.assertAlmostEqual(theta, .75 * (1 - h))

    def test_concentration_threshold_exposure(self):
        # Guard against confusing the 1% sensitivity with the entire position.
        rows = table_rows("tab:equity-parameters")
        threshold = float(next(row[3] for row in rows if row[0] == "10")) * 1e6
        text = PAPER.read_text()
        onset = re.search(r"above USD (\d+) million of exposure", text)
        self.assertIsNotNone(onset)
        self.assertEqual(float(onset.group(1)) * 1e6, threshold / .01)


if __name__ == "__main__":
    unittest.main()
