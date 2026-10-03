#!/usr/bin/env python3
# healthcheck.py - wait for the wallet API to be healthy
import sys
import time
import json
import urllib.request
 
URL = "http://localhost:3000/health"
RETRIES = 10
 
def is_healthy(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return json.load(response).get("status") == "ok"
    except Exception:
        return False
 
for attempt in range(1, RETRIES + 1):
    if is_healthy(URL):
        print("OK - healthy after", attempt, "attempt(s)")
        sys.exit(0)
    print("  not ready yet ({}/{}); waiting 2s...".format(attempt, RETRIES))
    time.sleep(2)
 
print("FAILED - not healthy after", RETRIES, "attempts", file=sys.stderr)
sys.exit(1)
