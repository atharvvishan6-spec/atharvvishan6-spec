# Data log

## Status (6 Oct 2026)

| File | Source | Coverage | Status |
|---|---|---|---|
| `raw/usdinr_fred_daily.csv` | FRED `DEXINUS` (NY noon buying rate), via the `datasets/exchange-rates` GitHub mirror | 1973-01-02 → 2026-10-02, US business days | ✅ collected |
| `raw/btc_coinmetrics.csv` | Coin Metrics Community data (`PriceUSD`, volumes, exchange flows) | price 2010-07-18 → 2026-05-23 | ✅ collected (the mirror stops at 23 May 2026) |
| `raw/usdt_coinmetrics.csv` | Coin Metrics Community data (`PriceUSD`, for USDT depeg correction) | 2014-10-06 → 2026-05-23 | ✅ collected |
| `raw/coindcx_usdtinr.csv`, `raw/coindcx_btcinr.csv` | CoinDCX public API | 2021 → today | ❌ host blocked in this environment |
| `raw/wazirx_usdtinr.csv`, `raw/wazirx_btcinr.csv` | WazirX API | 2021 → Jul 2024 | ❌ host blocked |
| `raw/binance_btcusdt.csv` | Binance public API | 2021 → today | ❌ host blocked (Coin Metrics covers the global price meanwhile) |
| RBI forex reserves, LRS outflows | RBI DBIE / RBI Bulletin | weekly / monthly | ⏳ to do (manual download from RBI) |
| FBIL reference rate | FBIL / RBI DBIE | daily | ⏳ to do (FRED is the stand-in for now) |

**The INR-quoted exchange prices are the critical missing piece.** Without them there is no premium.

## How to run

```bash
python3 crypto-premium-india/scripts/fetch_data.py   # downloads everything it can reach
python3 crypto-premium-india/scripts/build_panel.py  # -> data/processed/panel_daily.csv
```

`processed/panel_daily.csv` has one row per FX trading day from 2021. It includes the price columns, the premium columns (`prem_*`, in log points × 100 ≈ %) and 0/1 dummies for each policy date (Budget Feb 2022, 30% tax Apr 2022, 1% TDS Jul 2022, TCS 20% Oct 2023, FIU blocking Jan 2024, WazirX hack Jul 2024).

## Caveats to note in the paper
- **Time stamps differ:** FRED is the 12:00 New York rate, Coin Metrics is the 00:00 UTC daily reference rate, and exchange candles are UTC daily closes. Once FBIL is added, switch to it and test the time alignment as a robustness check.
- Do not use CoinGecko's "INR price" as the Indian price. It is the USD price converted at the official rate, so the premium comes out as zero by construction.
- The FIU-blocking dummy date (13 Jan 2024) is approximate. Check it against the press reports before finalising.
