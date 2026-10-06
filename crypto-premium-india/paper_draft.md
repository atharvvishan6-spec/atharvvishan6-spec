# The Crypto Premium as a Shadow Exchange Rate: Testing Capital Controls and the Law of One Price in India, 2021–2026

*Working draft and research blueprint. The `[TODO]` items are the parts you still have to fill in with your own data and results.*

---

## 0. Critical analysis of the original idea (read this first)

The idea is strong and fits Open Macro well. Before you start, fix these points:

| # | Issue in the original pitch | Correction / what to do |
|---|---|---|
| 1 | "The July 2022 tax regime (30% tax + 1% TDS)" treats it as one shock. | It is **three dates**: **1 Feb 2022** (Budget announcement), **1 Apr 2022** (30% tax on VDA gains, Sec. 115BBH, no loss set-off), **1 Jul 2022** (1% TDS, Sec. 194S). Model them as separate events. This is better because you can tell the announcement effect apart from the implementation effect. |
| 2 | The premium's sign under the tax is assumed to be obvious. | It is not. TDS mostly **widens the no-arbitrage band**, because arbitrage now costs 1% per sell leg plus 30% tax on profits with no loss offset. So the cleanest prediction is about the **size and persistence** of the premium (larger \|premium\|, slower mean reversion), not its sign. |
| 3 | BTC is the main asset. | **USDT/INR is the better "shadow exchange rate"**, because USDT ≈ $1, so `USDT_INR / official ₹/$ − 1` *is* the implied FX premium. Use BTC as a robustness check. |
| 4 | Data source: WazirX. | WazirX was **hacked on 18 July 2024** and trading was suspended for a long period. Use **CoinDCX** (and/or Zebpay, Mudrex, CoinSwitch) as the main source and treat WazirX as pre-July-2024 only. Also check P2P USDT prices, where a lot of volume moved after the TDS. |
| 5 | Official rate: "RBI reference rate". | Since July 2018 the reference rate is published by **FBIL** (Financial Benchmarks India Ltd.), fixed around 1:30 pm IST. Line up your crypto price **timestamps** with it (use the 1:30 pm IST price, or the daily close for both series plus FRED `DEXINUS` as a robustness check). |
| 6 | Only one policy shock. | You get extra natural experiments for free: **Oct 2023** (LRS TCS raised to 20%, which tightens the official outflow channel and should *raise* demand for the crypto leak), **Dec 2023 / Jan 2024** (FIU notices and URL blocking of offshore exchanges such as Binance), and the **2022 rupee pressure** episode (Fed hikes, RBI reserves falling from about $640bn to about $525bn). |
| 7 | "Compute in Excel". | Excel is fine for building the series and the charts. For HAC (Newey–West) standard errors, break tests and AR models, use Python, R, Stata or gretl (gretl is free and easy). |
| 8 | "Not done yet". | Correct framing: the **Kimchi premium** (Korea) is well studied, and cross-country crypto flow work exists (IMF; Graf von Luckner, Reinhart and Rogoff 2023). An **India-specific, tax-shock-based** study is much less covered. Run the SSRN/Google Scholar search in Step 2 below before you claim novelty. |

---

## Title page

**Title:** The Crypto Premium as a Shadow Exchange Rate: Testing Capital Controls and the Law of One Price in India, 2021–2026
**Author:** [Your name], [Institution]
**JEL codes:** F31 (Foreign Exchange), F32 (Current Account Adjustment; Short-term Capital Movements), F38 (International Financial Policy: Financial Transactions Tax; Capital Controls), G15 (International Financial Markets), H26 (Tax Evasion and Avoidance)
**Keywords:** law of one price, capital controls, crypto premium, Kimchi premium, monetary trilemma, India, USDT, TDS, natural experiment

---

## Abstract (≈200 words, write last)

> Bitcoin and USDT trade on Indian exchanges in rupees and on global exchanges in dollars. Under perfect capital mobility, the rupee price should equal the dollar price times the official ₹/$ rate. We construct a daily "crypto premium" for India from [start date] to [end date] using prices quoted on Indian exchanges, and we interpret it as a shadow exchange rate that measures how binding India's capital controls are. We find [TODO: mean premium, its persistence]. Using India's 2022 crypto tax regime (a 30% tax on gains from April 2022 and a 1% TDS on transfers from July 2022) as a natural experiment, we show [TODO: change in size and persistence of the premium, change in domestic volume]. The premium co-moves with [TODO: rupee depreciation, reserve losses, the NDF–onshore spread], which is consistent with crypto acting as a "leak" in India's capital controls, much like over- and under-invoicing under Bretton Woods. The results speak to the monetary trilemma: India's managed float and independent monetary policy rely on capital-account restrictions that are [TODO: partially / largely] effective.

---

## 1. Introduction

1. **Hook:** Under the law of one price, an identical asset should have the same price everywhere once converted at the market exchange rate. Bitcoin and USDT are about as close to identical global assets as exist, so persistent gaps across borders point to frictions, chiefly capital controls and taxes.
2. **Motivation (trilemma):** India runs a managed float and an independent monetary policy. By the trilemma it must therefore restrict capital mobility (LRS cap of $250,000 per year, TCS on remittances, FEMA rules). How well do these restrictions work in practice?
3. **The idea:** The crypto premium is a high-frequency, market-based **shadow exchange rate**. It is today's version of the **parallel-market premium** used in the classic capital-controls literature (Kiguel and O'Connell 1995; Reinhart and Rogoff 2004).
4. **Identification:** India's 2022 crypto tax regime is a sharp, exogenous policy shock that raised the cost of cross-border crypto arbitrage.
5. **Contributions (3 bullets):**
   - First India-focused daily premium series built from **actual INR-quoted prices** (not CoinGecko conversions).
   - Event-study and persistence evidence on how a **transaction tax widens the no-arbitrage band**.
   - Evidence on whether crypto is a **leak in capital controls** during periods of rupee pressure.
6. **Preview of results:** [TODO]
7. **Roadmap:** Section 2 covers the background, Section 3 the literature, Section 4 the theory and hypotheses, Section 5 the data, Section 6 the methods, Section 7 the results, Section 8 robustness, Section 9 policy implications, and Section 10 concludes.

---

## 2. Institutional background

### 2.1 India's capital-account regime
- FEMA 1999; the current account is convertible, the capital account is only partly convertible.
- **Liberalised Remittance Scheme (LRS):** residents may remit up to USD 250,000 per financial year. **TCS** on LRS was raised to 20% for most purposes from **1 Oct 2023**.
- Managed float: RBI intervenes using forex reserves. Note the 2022 drawdown.
- The offshore **NDF market** (Singapore, Dubai, London) and the NDF–onshore forward spread are a traditional measure of how well capital controls bind.

### 2.2 Timeline of crypto regulation (build this as a table in the paper)

| Date | Event | Expected effect |
|---|---|---|
| Apr 2018 | RBI bars banks from serving crypto firms | (pre-sample context) |
| 4 Mar 2020 | Supreme Court strikes down the RBI circular | (pre-sample context) |
| 2021 | Bull market; Indian exchange volumes boom | baseline |
| **1 Feb 2022** | Budget announces 30% tax + 1% TDS | announcement effect |
| **1 Apr 2022** | 30% tax on VDA gains in force (no loss offset) | higher cost of arbitrage |
| **1 Jul 2022** | 1% TDS on VDA transfers in force | band widens; volume moves offshore |
| Mar 2023 | VDA service providers brought under PMLA, FIU registration required | compliance cost |
| 1 Oct 2023 | LRS TCS raised to 20% | official outflow channel costlier, so crypto leak demand rises |
| Dec 2023 – Jan 2024 | FIU notices to offshore exchanges; URLs blocked | volume returns onshore? |
| 18 Jul 2024 | WazirX hack; trading suspended | data break; drop the exchange or add a dummy |
| [TODO] 2025–26 | Any later changes (check Budget 2025, Budget 2026, the crypto discussion paper) | |

*(Check every date against the official notification, CBDT circular or press release before you submit.)*

---

## 3. Literature review

Organise it by **strands** and end each one with the gap your paper fills.

### 3.1 Law of one price and PPP
- Isard (1977) shows large and persistent LOP failures in traded goods.
- Rogoff (1996), the "PPP puzzle": real-exchange-rate deviations have half-lives of 3–5 years.
- *Gap:* tests on goods are muddied by transport costs and differences between products. Crypto is a **perfectly identical, costlessly shippable** asset, so any deviation isolates **financial and regulatory frictions**.

### 3.2 Capital controls: effectiveness and leakage
- Dooley (1996) surveys the literature: controls create wedges but leak over time.
- Bhagwati (1964) and the mis-invoicing literature: controls are evaded through over- and under-invoicing of trade. This is the "leaky controls" story from the Fixed vs Floating chapter.
- Magud, Reinhart and Rogoff (2018), "Capital controls: myth and reality".
- Measurement: Chinn and Ito (2006) (KAOPEN de jure index); Fernández, Klein, Rebucci, Schindler and Uribe (2016) (capital control dataset).
- Parallel-market premium as a market measure of controls: Kiguel and O'Connell (1995); Reinhart and Rogoff (2004).
- India: Patnaik and Shah (2012) find India's capital controls were not effective as a macro policy tool.
- *Gap:* de jure indices are slow-moving and coarse. A **daily market-based** measure of how binding controls are is missing for India.

### 3.3 Trilemma
- Obstfeld, Shambaugh and Taylor (2005), "The trilemma in history".
- Rey (2013), "Dilemma not trilemma": the global financial cycle.
- *Link:* the premium shows how much "capital mobility" India actually gives up.

### 3.4 Crypto arbitrage and cross-border premia
- **Makarov and Schoar (2020, JFE):** large, recurring arbitrage gaps, much bigger *across* countries than within them, and they co-move. Capital controls (e.g., Korea) are the main barrier. **This is your core reference.**
- Choi, Lehar and Stauffer (working paper), "Bitcoin microstructure and the Kimchi premium". [verify publication status]
- Pieters and Vivanco (2017, *Information Economics and Policy*): prices differ across markets, and more so where regulation is looser or tighter.
- Pieters (2016, SSRN): Bitcoin implied exchange rates reveal unofficial exchange rates and capital controls (e.g., Argentina). [verify exact title]
- Kroeger and Sarkar (2017): "Law of one Bitcoin price?" [verify]
- Krückeberg and Scholz (2020, *Financial Analysts Journal*): arbitrage in Bitcoin markets.
- Hautsch, Scheuch and Voigt (2024, *Review of Finance*): settlement latency limits arbitrage.
- *Gap:* almost all of this is on Korea, Japan, or cross-country panels. **There is no India-specific study using a tax shock as identification.**

### 3.5 Crypto as a capital-flight / capital-flow channel
- Ju, Lu and Tu (2016): capital flight from China and Bitcoin regulation. [verify journal]
- Graf von Luckner, Reinhart and Rogoff (2023, *Journal of Monetary Economics*), "Decrypting new age international capital flows": crypto is used for cross-border capital flight.
- IMF (2023), *Elements of Effective Policies for Crypto Assets*; IMF–FSB Synthesis Paper (2023, under India's G20 presidency). Also look for recent IMF working papers on crypto and capital flows.
- *Gap:* cross-country evidence exists, but an India-specific, high-frequency link to rupee pressure is missing.

### 3.6 Transaction taxes and market quality
- The Tobin-tax / securities transaction tax literature: taxes reduce volume and can widen mispricing.
- On India's TDS specifically: industry and think-tank impact reports (e.g., Esya Centre, 2023) estimate a large shift of volume to offshore exchanges. [verify; cite as grey literature]
- *Gap:* no peer-reviewed estimate of what the TDS did to **price efficiency** (the premium), as opposed to volume.

> **Literature table (put it in the paper):** Author | Year | Market | Data | Method | Key finding | How my paper differs.

---

## 4. Theory and hypotheses

### 4.1 Definitions
Let `P_t^INR` be the INR price on an Indian exchange, `P_t^USD` the USD (USDT) price on a global exchange, and `S_t` the official ₹/$ rate (FBIL).

- **Crypto premium:** `π_t = ln(P_t^INR) − ln(S_t) − ln(P_t^USD)` (≈ percent deviation)
- **Implied (shadow) exchange rate:** `S_t^crypto = P_t^INR / P_t^USD`, so `π_t = ln(S_t^crypto / S_t)`
- For USDT: `π_t^USDT = ln(P_t^{USDT/INR}) − ln(S_t) − ln(P_t^{USDT/USD})`, where the last term corrects for depegs.

### 4.2 No-arbitrage band
Arbitrage is profitable only if `|π_t| > c_t`, where `c_t` is the round-trip cost: exchange fees, bid–ask spread, withdrawal and network fees, banking and LRS/TCS cost, legal risk, and **after Jul 2022, the 1% TDS on each sell leg plus 30% tax on gains with no loss offset.**
So inside the band, `π_t` can wander freely. **The tax regime raised `c_t`, which widens the band.**

### 4.3 Hypotheses
- **H1 (LOP failure):** `π_t` is economically and statistically different from zero, and its average absolute size is larger than plausible transaction costs before 2022.
- **H2 (capital-control / flight channel):** `π_t` rises when there is pressure on the rupee (depreciation, falling reserves, a wider NDF–onshore spread, higher LRS outflows). Residents pay more for an asset that lets them move money out.
- **H3 (tax shock widens the band):** after 1 Apr and 1 Jul 2022, (a) `|π_t|` rises, (b) persistence rises (the AR(1) coefficient goes up and the half-life gets longer), and (c) volume on Indian exchanges falls.
- **H4 (leak substitution):** when the official channel became costlier (TCS hike, Oct 2023), the premium and crypto demand rose. When the offshore channel was blocked (Jan 2024), domestic volume recovered.

---

## 5. Data

| Variable | Source (free) | Frequency | Notes |
|---|---|---|---|
| BTC/INR, USDT/INR | CoinDCX public API; WazirX API (pre-Jul 2024); CryptoCompare/CCData (free key, exchange-level INR pairs); Kaggle datasets | daily (hourly if available) | **Must be INR-quoted on an Indian exchange.** Do **not** use CoinGecko's INR price, which is just the USD price × FX, so the premium is ≈ 0. |
| BTC/USDT, BTC/USD | Binance public klines API; Coinbase API; CoinGecko | daily/hourly | Use the same timestamp as the INR series. |
| USDT/USD | Kraken / Coinbase USDT-USD | daily | Corrects for depegs. |
| ₹/$ official | FBIL reference rate (via RBI DBIE); FRED `DEXINUS` | daily | FBIL ≈ 1:30 pm IST. |
| Forex reserves | RBI DBIE, weekly statistical supplement | weekly | |
| LRS outflows | RBI Bulletin, monthly | monthly | |
| NDF ₹/$ (1M) | Investing.com or similar | daily | Optional, but a strong robustness check. |
| Controls | VIX, DXY (FRED); global BTC return | daily | |
| Volume | the same exchange APIs | daily | Watch for wash trading. |

**Sample:** 1 Jan 2021 to latest available (≈ 2026). Pre-period ≈ 13 months before the announcement.

**Cleaning rules (write them down in the paper):** align time zones (IST vs UTC); drop days with zero or very thin volume; winsorise at the 1% level; flag exchange outages, the WazirX suspension and USDT depeg days.

---

## 6. Methodology

1. **Descriptive analysis:** plot `π_t` (BTC and USDT) with vertical lines at the policy dates, plus `S_t` and reserves. Report summary stats for the pre- and post-period.
2. **Is the premium zero? (H1):** t-test on the mean using **Newey–West** standard errors. ADF test for stationarity.
3. **Event study (H3):** rolling or window means of `π_t` and `|π_t|` around each date (±30 and ±60 days). **Chow** and **Bai–Perron** structural break tests, so you can check whether the data choose the policy dates on their own.
4. **Regression (H2, H3):**
   `π_t = α + β1·Post_Apr22 + β2·Post_Jul22 + β3·Δln S_t + β4·ΔReserves_t + β5·NDFspread_t + β6·r_t^BTC + β7·VIX_t + ε_t` (HAC standard errors). Run it for both `π_t` and `|π_t|`.
5. **Persistence (H3b):** estimate `π_t = ρ·π_{t−1} + u_t` before and after, and report the half-life `ln(0.5)/ln(ρ)`. *Advanced:* a threshold AR (TAR) model estimates the band width `c` directly. Check whether `c` goes up after the tax.
6. **Difference-in-differences (optional, strong):** compare India's premium with the premium in a country that did **not** change crypto tax in 2022 (e.g., Korea, Turkey, Indonesia USDT premia):
   `|π_{it}| = α_i + γ_t + δ·(India_i × Post_t) + ε_it`. Check parallel pre-trends.
7. **Volume (H3c, H4):** log domestic volume on the post dummies, with global volume as a control.

---

## 7. Results  [TODO]
- Table 1: summary statistics, pre vs post.
- Figure 1: premium over time with the event lines (**this is your headline chart**).
- Figure 2: premium vs ₹/$ depreciation and reserves.
- Table 2: event-study / break-test results.
- Table 3: main regression.
- Table 4: AR(1) persistence and half-lives, pre vs post.
- Interpretation through the trilemma: a large and persistent premium means controls bind, so India keeps monetary autonomy and a managed rate by giving up mobility. A premium that spikes with rupee pressure means the controls leak.

## 8. Robustness  [TODO]
- BTC vs USDT; CoinDCX vs WazirX vs others.
- FBIL vs FRED rate; 1:30 pm IST price vs daily close.
- Exclude the hack and depeg periods (e.g., FTX collapse, Nov 2022).
- Weekly averages instead of daily data.
- Placebo dates (e.g., pretend the shock happened on 1 Jan 2022 or 1 Oct 2022).

## 9. Policy implications
- How effective India's capital controls are in the crypto era.
- The tax as a de facto capital control. Trade-off: it pushed activity offshore and to P2P, which reduced visibility (a tax-base and AML concern).
- Implications for RBI's FX management and for the debate on India's crypto regulation.

## 10. Limitations
- Exchange-quoted prices may include wash trading. P2P prices are not fully observable.
- Possible confounders in 2022: the global crypto crash (Terra/Luna in May 2022, FTX in Nov 2022) and Fed tightening. The DiD and the global controls address this.
- Taxes affect *who* trades, not only *the price*. Be careful with causal language.

## 11. Conclusion  [TODO, 1 paragraph]

---

## References (starter list — check every entry and format it in APA/Harvard)

- Bhagwati, J. (1964). On the underinvoicing of imports. *Bulletin of the Oxford University Institute of Statistics*, 27(4).
- Chinn, M. D., & Ito, H. (2006). What matters for financial development? Capital controls, institutions, and interactions. *Journal of Development Economics*, 81(1), 163–192.
- Choi, K. J., Lehar, A., & Stauffer, R. Bitcoin microstructure and the Kimchi premium. Working paper, SSRN. [verify]
- Dooley, M. P. (1996). A survey of literature on controls over international capital transactions. *IMF Staff Papers*, 43(4).
- Fernández, A., Klein, M. W., Rebucci, A., Schindler, M., & Uribe, M. (2016). Capital control measures: A new dataset. *IMF Economic Review*, 64(3), 548–574.
- Graf von Luckner, C., Reinhart, C. M., & Rogoff, K. (2023). Decrypting new age international capital flows. *Journal of Monetary Economics*, 138, 104–122.
- Hautsch, N., Scheuch, C., & Voigt, S. (2024). Building trust takes time: Limits to arbitrage for blockchain-based assets. *Review of Finance*.
- IMF (2023). *Elements of Effective Policies for Crypto Assets*. IMF Policy Paper.
- IMF & FSB (2023). *Synthesis Paper: Policies for Crypto-Assets*.
- Isard, P. (1977). How far can we push the "law of one price"? *American Economic Review*, 67(5), 942–948.
- Ju, L., Lu, T., & Tu, Z. (2016). Capital flight and Bitcoin regulation. *International Review of Economics & Finance*. [verify]
- Kiguel, M., & O'Connell, S. A. (1995). Parallel exchange rates in developing countries. *World Bank Research Observer*, 10(1), 21–52.
- Kroeger, A., & Sarkar, A. (2017). Law of one Bitcoin price? Working paper. [verify]
- Krückeberg, S., & Scholz, P. (2020). Decentralized efficiency? Arbitrage in Bitcoin markets. *Financial Analysts Journal*, 76(3).
- Magud, N. E., Reinhart, C. M., & Rogoff, K. S. (2018). Capital controls: Myth and reality. *Annals of Economics and Finance*, 19(1).
- Makarov, I., & Schoar, A. (2020). Trading and arbitrage in cryptocurrency markets. *Journal of Financial Economics*, 135(2), 293–319.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). The trilemma in history. *Review of Economics and Statistics*, 87(3), 423–438.
- Patnaik, I., & Shah, A. (2012). Did the Indian capital controls work as a tool of macroeconomic policy? *IMF Economic Review*, 60(3), 439–464.
- Pieters, G. (2016). Bitcoin reveals unofficial exchange rates and detects capital controls. SSRN working paper. [verify title]
- Pieters, G., & Vivanco, S. (2017). Financial regulations and price inconsistencies across Bitcoin markets. *Information Economics and Policy*, 39, 1–14.
- Reinhart, C. M., & Rogoff, K. S. (2004). The modern history of exchange rate arrangements: A reinterpretation. *Quarterly Journal of Economics*, 119(1), 1–48.
- Rey, H. (2013). Dilemma not trilemma: The global financial cycle and monetary policy independence. Jackson Hole Symposium.
- Rogoff, K. (1996). The purchasing power parity puzzle. *Journal of Economic Literature*, 34(2), 647–668.
- Government of India: Finance Act 2022 (Sec. 115BBH, Sec. 194S); CBDT circulars on TDS on VDAs; RBI Master Direction on LRS.

---

## Appendix A: Step-by-step action plan

| Week | Task | Output |
|---|---|---|
| 1 | Novelty check: search SSRN (papers.ssrn.com), Google Scholar, IDEAS/RePEc, NBER and IMF eLibrary for "India crypto premium", "INR bitcoin arbitrage", "TDS crypto India", "Kimchi premium capital controls". Read Makarov–Schoar in full. | List of 15–25 papers + literature table |
| 2 | Get the data: CoinDCX/CCData INR pairs, Binance USD pairs, FBIL/FRED FX, RBI reserves/LRS. Check that the INR price is **not** just USD × FX. | Raw CSVs |
| 3 | Clean and merge in Excel: align dates and timestamps; compute `π_t` for BTC and USDT. | Master sheet |
| 4 | Charts: premium with event lines; premium vs ₹/$; summary stats pre/post. | Fig 1–2, Table 1 |
| 5 | Econometrics in gretl/Python/R: tests, event study, regressions, AR(1) half-life. | Tables 2–4 |
| 6 | Write sections 1–5 (intro, background, lit review, theory, data). | Draft v1 |
| 7 | Write results, robustness, policy and conclusion; abstract last. | Draft v2 |
| 8 | Get feedback from your professor, revise, check every citation, then post to SSRN (Economics Research Network: international finance / capital controls). | Final paper + SSRN upload |
