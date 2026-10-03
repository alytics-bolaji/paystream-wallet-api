#!/usr/bin/env python3
# healthcheck.py - is the wallet API up?
import sys
import json
import urllib.request
 
URL = "http://localhost:3000/health"
 
def is_healthy(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            body = json.load(response)
            return body.get("status") == "ok"
    except Exception:
        return False
 
if is_healthy(URL):
    print("OK - API healthy")
    sys.exit(0)
else:
    print("FAILED - API is down", file=sys.stderr)
    sys.exit(1)
