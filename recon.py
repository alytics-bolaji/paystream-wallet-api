import sys
import csv
 
with open("transactions.csv", newline="") as f:
    rows = list(csv.DictReader(f))
 
print(len(rows), "transfers")
print("first:", rows[0]["transfer_id"], rows[0]["status"])

TAKE_RATE = 0.014
TOLERANCE = 1   # allow +/- 1 minor unit for rounding
 
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


total_sent = sum(int(r["sent_ngn_minor"]) for r in rows)
total_fees = sum(int(r["fee_ngn_minor"]) for r in rows)
mismatches = [(r["transfer_id"], problems_with(r)) for r in rows]
mismatches = [(tid, p) for tid, p in mismatches if p]
 
print("Total sent: NGN {:,.2f}".format(total_sent / 100))
print("Total fees: NGN {:,.2f}".format(total_fees / 100))
print("Mismatches:", len(mismatches))
for tid, probs in mismatches:
    print("  ", tid, "-", ", ".join(probs))
 
sys.exit(1 if mismatches else 0)

