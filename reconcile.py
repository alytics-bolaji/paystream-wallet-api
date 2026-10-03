#!/usr/bin/env python3
"""reconcile.py -- total the day's transfers and flag any that don't add up.

This is the kind of job Bash fights you on: parsing a CSV, doing exact money
maths, and reporting. Python does it in a few readable lines.
"""
import sys
import csv

TAKE_RATE = 0.014   # Paystream takes 1.4% of every transfer
TOLERANCE = 1       # allow +/- 1 minor unit for rounding


def problems_with(row):
    """Return a list of problems with one transfer (empty list = clean)."""
    problems = []
    sent = int(row["sent_ngn_minor"])
    fee = int(row["fee_ngn_minor"])
    fx = float(row["fx_rate_ngn_to_kes"])
    credited = int(row["credited_kes_minor"])

    if abs(fee - round(sent * TAKE_RATE)) > TOLERANCE:
        problems.append("fee is not 1.4%")
    if abs(credited - round((sent - fee) * fx)) > TOLERANCE:
        problems.append("credited amount doesn't match")
    if row["status"] != "settled":
        problems.append("status is " + row["status"])
    return problems


def main(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))

    total_sent = sum(int(r["sent_ngn_minor"]) for r in rows)
    total_fees = sum(int(r["fee_ngn_minor"]) for r in rows)
    mismatches = [(r["transfer_id"], problems_with(r)) for r in rows]
    mismatches = [(tid, probs) for tid, probs in mismatches if probs]

    print("Transfers:  {}".format(len(rows)))
    print("Total sent: NGN {:,.2f}".format(total_sent / 100))
    print("Total fees: NGN {:,.2f}".format(total_fees / 100))
    print("Mismatches: {}".format(len(mismatches)))
    for tid, probs in mismatches:
        print("  {}: {}".format(tid, ", ".join(probs)))

    return 1 if mismatches else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: reconcile.py <transactions.csv>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
