import yaml
import requests
import time
import sys
import json
from urllib.parse import urlparse
from collections import defaultdict

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def extract_domain(url):
    parsed = urlparse(url)
    return parsed.hostname  # no port, just the domain

def check(endpoint):
    method = endpoint.get("method", "GET")
    headers = endpoint.get("headers")
    body_raw = endpoint.get("body")
    json_body = None

    if body_raw:
        try:
            json_body = json.loads(body_raw)
        except json.JSONDecodeError:
            pass  # not ideal, but if it's bad JSON, let the request fail

    try:
        start = time.perf_counter()
        res = requests.request(method, endpoint["url"], headers=headers, json=json_body, timeout=1)
        latency = time.perf_counter() - start

        if 200 <= res.status_code < 300 and latency <= 0.5:
            return "UP"
    except requests.RequestException:
        pass

    return "DOWN"

def monitor(config_path):
    endpoints = load_config(config_path)
    stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        cycle_start = time.perf_counter()

        for ep in endpoints:
            domain = extract_domain(ep["url"])
            status = check(ep)

            stats[domain]["total"] += 1
            if status == "UP":
                stats[domain]["up"] += 1

        for domain, data in stats.items():
            # Drop decimal, don't round — per spec
            availability = int((data["up"] / data["total"]) * 100)
            print(f"{domain} - {availability}% availability")

        print("------")

        # Adjust sleep to keep the 15-second interval on point
        elapsed = time.perf_counter() - cycle_start
        remaining = max(0, 15 - elapsed)
        time.sleep(remaining)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config.yaml>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        monitor(path)
    except KeyboardInterrupt:
        print("\nStopped by user.")
