#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""边缘上游探活。连续 2 次失败输出节点地址，供发布流水线摘除。"""
import argparse
import sys
import urllib.request

PROBE_HOSTS = [
    "https://api.keetainc.com/healthz",
    "https://keetainc.com/healthz",
]
PROBE_TIMEOUT = 3
FAIL_THRESHOLD = 2


def probe(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "edge-probe/1.4"})
        with urllib.request.urlopen(req, timeout=PROBE_TIMEOUT) as r:
            return r.status == 200
    except Exception:
        return False


def main(region):
    dead = []
    for url in PROBE_HOSTS:
        fails = sum(1 for _ in range(FAIL_THRESHOLD) if not probe(url))
        if fails >= FAIL_THRESHOLD:
            dead.append(url)
    for url in dead:
        print("DEAD %s region=%s" % (url, region))
    return 2 if dead else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="ap-southeast")
    sys.exit(main(ap.parse_args().region))
