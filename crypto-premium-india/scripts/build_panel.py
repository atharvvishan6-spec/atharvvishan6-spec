"""Merge raw files into one daily panel and compute the crypto premium.

    python3 crypto-premium-india/scripts/build_panel.py

Output: data/processed/panel_daily.csv (open it in Excel).
Rows are days with an official USD/INR quote (FRED DEXINUS, New York noon
buying rate); crypto prices are UTC daily closes. INR exchange files that are
missing are skipped, and their premium columns stay blank.

Premium (log points x 100, roughly %):
    prem_usdt = 100 * [ln(USDT/INR) - ln(USD/INR) - ln(USDT/USD)]
    prem_btc  = 100 * [ln(BTC/INR)  - ln(USD/INR) - ln(BTC/USD)]
"""

import csv
import math
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "data")
RAW, OUT = os.path.join(BASE, "raw"), os.path.join(BASE, "processed")
START = "2021-01-01"

EVENTS = {  # policy dummies: 1 on and after the date
    "post_budget_2022": "2022-02-01",
    "post_tax30_2022": "2022-04-01",
    "post_tds1_2022": "2022-07-01",
    "post_tcs20_2023": "2023-10-01",
    "post_fiu_block_2024": "2024-01-13",
    "post_wazirx_hack": "2024-07-18",
}


def load(name, date_col, value_col):
    path = os.path.join(RAW, name)
    if not os.path.exists(path):
        print(f"missing {name} (skipped)")
        return {}
    out = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                v = float(r[value_col])
            except (ValueError, TypeError):
                continue
            if v > 0:
                out[r[date_col]] = v
    return out


def prem(inr, usdinr, usd):
    if inr is None or usdinr is None or usd is None:
        return None
    return 100 * (math.log(inr) - math.log(usdinr) - math.log(usd))


def main():
    fx = load("usdinr_fred_daily.csv", "Date", "Exchange rate")
    btc_usd = load("btc_coinmetrics.csv", "time", "PriceUSD")
    usdt_usd = load("usdt_coinmetrics.csv", "time", "PriceUSD")
    btc_usdt = load("binance_btcusdt.csv", "date", "close")
    inr = {
        "coindcx_usdtinr": load("coindcx_usdtinr.csv", "date", "close"),
        "coindcx_btcinr": load("coindcx_btcinr.csv", "date", "close"),
        "wazirx_usdtinr": load("wazirx_usdtinr.csv", "date", "close"),
        "wazirx_btcinr": load("wazirx_btcinr.csv", "date", "close"),
    }

    rows = []
    for d in sorted(k for k in fx if k >= START):
        r = {"date": d, "usdinr_official": fx[d], "btc_usd": btc_usd.get(d),
             "usdt_usd": usdt_usd.get(d), "btc_usdt_binance": btc_usdt.get(d)}
        for k, series in inr.items():
            r[k] = series.get(d)
        r["prem_usdt_coindcx"] = prem(r["coindcx_usdtinr"], fx[d], r["usdt_usd"])
        r["prem_usdt_wazirx"] = prem(r["wazirx_usdtinr"], fx[d], r["usdt_usd"])
        r["prem_btc_coindcx"] = prem(r["coindcx_btcinr"], fx[d], r["btc_usd"])
        r["prem_btc_wazirx"] = prem(r["wazirx_btcinr"], fx[d], r["btc_usd"])
        for name, start in EVENTS.items():
            r[name] = int(d >= start)
        rows.append(r)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "panel_daily.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows ({rows[0]['date']} to {rows[-1]['date']}) -> {path}")
    for col in ("prem_usdt_coindcx", "prem_btc_coindcx", "prem_usdt_wazirx", "prem_btc_wazirx"):
        n = sum(r[col] is not None for r in rows)
        print(f"  {col}: {n} non-empty days")


if __name__ == "__main__":
    main()
