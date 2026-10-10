#!/usr/bin/env python3
"""paystream-ops -- one Python tool for Kenya's ops jobs.

The Python answer to Week 6's deploy.sh: instead of separate scripts, one
command with sub-commands.

  paystream-ops health
  paystream-ops reconcile --file transactions.csv
"""
import sys
import time
import json
import csv
import argparse
import urllib.request
import urllib.error

TAKE_RATE = 0.014
TOLERANCE = 1


# ---- health ----
def is_healthy(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return json.load(response).get("status") == "ok"
    except (urllib.error.URLError, ValueError, OSError):
        return False


def cmd_health(args):
    print("Health check:", args.url)
    for attempt in range(1, args.retries + 1):
        if is_healthy(args.url):
            print("OK - healthy after {} attempt(s)".format(attempt))
            return 0
        print("  not ready yet ({}/{}); waiting 2s...".format(attempt, args.retries))
        time.sleep(2)
    print("FAILED - API not healthy", file=sys.stderr)
    return 1


# ---- reconcile ----
def problems_with(row):
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


def cmd_reconcile(args):
    with open(args.file, newline="") as f:
        rows = list(csv.DictReader(f))
    total_sent = sum(int(r["sent_ngn_minor"]) for r in rows)
    total_fees = sum(int(r["fee_ngn_minor"]) for r in rows)
    mismatches = [(r["transfer_id"], problems_with(r)) for r in rows]
    mismatches = [(tid, p) for tid, p in mismatches if p]
    print("Transfers:  {}".format(len(rows)))
    print("Total sent: NGN {:,.2f}".format(total_sent / 100))
    print("Total fees: NGN {:,.2f}".format(total_fees / 100))
    print("Mismatches: {}".format(len(mismatches)))
    for tid, probs in mismatches:
        print("  {}: {}".format(tid, ", ".join(probs)))
    return 1 if mismatches else 0


def build_parser():
    p = argparse.ArgumentParser(prog="paystream-ops",
                                description="Kenya ops helper (Python)")
    sub = p.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("health", help="check the wallet API, with retries")
    h.add_argument("--url", default="http://localhost:3000/health")
    h.add_argument("--retries", type=int, default=10)
    h.set_defaults(func=cmd_health)

    r = sub.add_parser("reconcile", help="reconcile a transactions CSV")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_reconcile)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
