"""Download daily price data for the India crypto-premium study.

Standard library only. Run from the repo root:
    python3 crypto-premium-india/scripts/fetch_data.py

Every source is optional: a failure is reported and the script moves on, so
partial downloads still land in data/raw/. Hosts needed (allow them in the
environment's network settings, or run this on your own laptop):
    public.coindcx.com, api.wazirx.com, data-api.binance.vision,
    raw.githubusercontent.com
"""

import csv
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
START = datetime(2021, 1, 1, tzinfo=timezone.utc)
END = datetime.now(timezone.utc)
DAY_MS = 86_400_000


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-script"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def write_rows(name, rows):
    rows = sorted({r["date"]: r for r in rows}.values(), key=lambda r: r["date"])
    path = os.path.join(RAW, name)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "open", "high", "low", "close", "volume"])
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {len(rows)} rows -> {path}")


def ms_to_date(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")


def coindcx(pair, outfile):
    """CoinDCX INR market (pair like I-USDT_INR). Pages back 1000 days at a time."""
    rows, end_ms = [], int(END.timestamp() * 1000)
    start_ms = int(START.timestamp() * 1000)
    while end_ms > start_ms:
        url = (f"https://public.coindcx.com/market_data/candles?pair={pair}"
               f"&interval=1d&startTime={max(start_ms, end_ms - 1000 * DAY_MS)}"
               f"&endTime={end_ms}&limit=1000")
        data = get_json(url)
        if not data:
            break
        for c in data:
            rows.append({"date": ms_to_date(c["time"]), "open": c["open"], "high": c["high"],
                         "low": c["low"], "close": c["close"], "volume": c["volume"]})
        end_ms = min(c["time"] for c in data) - 1
        time.sleep(0.5)
    write_rows(outfile, rows)


def wazirx(symbol, outfile):
    """WazirX INR market (symbol like usdtinr). Trading halted after the 18 Jul 2024 hack."""
    rows, start_s = [], int(START.timestamp())
    end_s = int(END.timestamp())
    while start_s < end_s:
        url = (f"https://api.wazirx.com/sapi/v1/klines?symbol={symbol}&interval=1d"
               f"&startTime={start_s}&endTime={end_s}&limit=2000")
        data = get_json(url)
        if not data:
            break
        for k in data:
            rows.append({"date": ms_to_date(k[0] * 1000), "open": k[1], "high": k[2],
                         "low": k[3], "close": k[4], "volume": k[5]})
        start_s = data[-1][0] + 86_400
        time.sleep(0.5)
    write_rows(outfile, rows)


def binance(symbol, outfile):
    """Binance global USDT market (symbol like BTCUSDT), daily candles in UTC."""
    rows, start_ms = [], int(START.timestamp() * 1000)
    end_ms = int(END.timestamp() * 1000)
    while start_ms < end_ms:
        url = (f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}"
               f"&interval=1d&startTime={start_ms}&limit=1000")
        data = get_json(url)
        if not data:
            break
        for k in data:
            rows.append({"date": ms_to_date(k[0]), "open": k[1], "high": k[2],
                         "low": k[3], "close": k[4], "volume": k[5]})
        start_ms = data[-1][0] + DAY_MS
        time.sleep(0.3)
    write_rows(outfile, rows)


def github_mirrors():
    """FRED DEXINUS mirror and Coin Metrics community data (global USD prices)."""
    fx = urllib.request.urlopen(
        "https://raw.githubusercontent.com/datasets/exchange-rates/main/data/daily.csv",
        timeout=120).read().decode().splitlines()
    with open(os.path.join(RAW, "usdinr_fred_daily.csv"), "w") as f:
        f.write("\n".join([fx[0]] + [l for l in fx[1:] if ",India," in l]) + "\n")
    for asset in ("btc", "usdt"):
        urllib.request.urlretrieve(
            f"https://raw.githubusercontent.com/coinmetrics/data/master/csv/{asset}.csv",
            os.path.join(RAW, f"{asset}_coinmetrics.csv"))
    print("  wrote FRED and Coin Metrics mirrors")


JOBS = [
    ("GitHub mirrors (FX, Coin Metrics)", github_mirrors),
    ("CoinDCX USDT/INR", lambda: coindcx("I-USDT_INR", "coindcx_usdtinr.csv")),
    ("CoinDCX BTC/INR", lambda: coindcx("I-BTC_INR", "coindcx_btcinr.csv")),
    ("WazirX USDT/INR", lambda: wazirx("usdtinr", "wazirx_usdtinr.csv")),
    ("WazirX BTC/INR", lambda: wazirx("btcinr", "wazirx_btcinr.csv")),
    ("Binance BTC/USDT", lambda: binance("BTCUSDT", "binance_btcusdt.csv")),
]

if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    failed = []
    for name, job in JOBS:
        print(name)
        try:
            job()
        except Exception as e:  # keep going; report at the end
            print(f"  FAILED: {e}")
            failed.append(name)
    if failed:
        print("\nFailed sources:", ", ".join(failed))
        sys.exit(1)
