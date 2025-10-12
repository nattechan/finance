# Treasury Curve Flatteners and Steepeners

## Executive Summary

Curve flattener and steepener trades exploit changes in the **slope of the yield curve** by taking offsetting long/short positions in different maturity bonds. These are **duration-neutral** or **dollar-duration-neutral** trades that profit from relative value moves rather than parallel shifts.

**Key Characteristics:**

- **Flattener**: Bet that long-term rates fall relative to short-term rates (curve flattens)
  - Long long-dated bonds, short short-dated bonds
- **Steepener**: Bet that long-term rates rise relative to short-term rates (curve steepens)
  - Long short-dated bonds, short long-dated bonds
- **Duration-neutral**: Offsets interest rate risk, isolates curve risk
- **Carry**: Critical component - funding costs vs. coupon income
- **Convexity**: Asymmetric exposure to large rate moves

---

## Part 1: Trade Structure & Mechanics

### Case Example 1: 2s10s Flattener (Betting Curve Flattens)

**Market Setup (as of trade date):**

```text
2-Year Treasury: Yield = 4.50%, Price = 99.50, Duration = 1.95
10-Year Treasury: Yield = 4.00%, Price = 96.80, Duration = 8.75
Curve Spread (10s-2s): 4.00% - 4.50% = -50 bps (inverted)

Your View: Curve will flatten (spread becomes more negative or less positive)
- Fed will cut rates → 2Y yields fall more than 10Y
- OR 10Y yields rise less than 2Y
```

**Trade Construction (Duration-Neutral):**

To make the trade duration-neutral, you need:

```text
Dollar Duration Balance:
Short 2Y: $10M notional × 1.95 duration = $19.5M DV01
Long 10Y: $X notional × 8.75 duration = $19.5M DV01

Solve for X: $19.5M / 8.75 = $2.23M

Trade Structure:
- Short $10.0M of 2-Year Treasury at 4.50% yield
- Long $2.23M of 10-Year Treasury at 4.00% yield
- Net duration: ~0 (neutral to parallel shifts)
- Net notional: Short $7.77M
```

***Alternative: DV01-Neutral Sizing***

```text
DV01 = Modified Duration × Price × Notional / 10,000

2Y DV01: 1.95 × 99.50 × $10M / 10,000 = $19,403 per bp
10Y DV01: 8.75 × 96.80 × $2.23M / 10,000 = $18,887 per bp

Adjust 10Y notional to $2.29M for exact DV01 match
```

---

## Part 2: P&L Attribution

### Scenario 1: Curve Flattens 25 bps (Your Bet Wins)

**Rate Changes:**

```text
2-Year: 4.50% → 4.25% (-25 bps)
10-Year: 4.00% → 3.90% (-10 bps)
Curve spread: -50 bps → -65 bps (flattened by 15 bps)
```

**P&L Calculation:**

**Short 2Y Position (LOSE money as yields fall):**

```text
Price Change: Duration × Yield Change × Price
ΔPrice = -1.95 × (-0.25%) × 99.50 = +$0.48 per $100
New Price: 99.50 → 99.98

Loss on Short: -$10M × 0.48% = -$48,000
```

**Long 10Y Position (MAKE money as yields fall):**

```text
ΔPrice = -8.75 × (-0.10%) × 96.80 = +$0.85 per $100
New Price: 96.80 → 97.65

Gain on Long: +$2.23M × 0.85% = +$18,955
```

**Net P&L:**

```text
2Y Loss: -$48,000
10Y Gain: +$18,955
Net Loss: -$29,045

Wait... this is NEGATIVE! Why?
```

***The Problem: Curve flattened but BOTH yields fell***

The trade is designed to profit from **relative moves**, but absolute direction matters:

- 2Y fell 25 bps (hurts short position more than expected)
- 10Y fell only 10 bps (helps long position less)
- Net effect: Duration mismatch in absolute terms

***Better Outcome: Curve Flattens via 2Y Falling, 10Y Rising***

```text
2-Year: 4.50% → 4.25% (-25 bps)
10-Year: 4.00% → 4.10% (+10 bps)
Curve spread: -50 bps → -15 bps (flattened by 35 bps)

2Y P&L: Short loses -$48,000
10Y P&L: Long loses -$19,465 (8.75 × 0.10% × 96.80 × $2.23M)
Net P&L: Still -$67,465!

Still losing because BOTH positions moved against us in absolute terms.
```

***Optimal Scenario: Curve Flattens via 10Y Falling MORE***

```text
2-Year: 4.50% → 4.50% (unchanged)
10-Year: 4.00% → 3.50% (-50 bps)
Curve spread: -50 bps → -100 bps (flattened by 50 bps)

2Y P&L: $0 (no yield change)
10Y P&L: -8.75 × (-0.50%) × 96.80 × $2.23M = +$94,493
Net P&L: +$94,493 ✓

Now we're making money!
```

---

### Scenario 2: Curve Steepens 25 bps (Your Bet Loses)

**Rate Changes:**

```text
2-Year: 4.50% → 4.40% (-10 bps)
10-Year: 4.00% → 4.15% (+15 bps)
Curve spread: -50 bps → -25 bps (steepened by 25 bps)
```

**P&L Calculation:**

**Short 2Y:**

```text
ΔPrice = -1.95 × (-0.10%) × 99.50 = +$0.19
Loss: -$10M × 0.19% = -$19,403
```

**Long 10Y:**

```text
ΔPrice = -8.75 × (+0.15%) × 96.80 = -$1.27
Loss: +$2.23M × (-1.27%) = -$28,321
```

**Net P&L:**

```text
2Y Loss: -$19,403
10Y Loss: -$28,321
Net Loss: -$47,724

Curve steepened against us, both positions lost money.
```

---

## Part 3: Carry & Funding Implications

### Daily Carry Calculation

**Funding Costs (Repo Financing):**

**Short 2Y Position:**

- You borrow $10M of 2Y Treasuries to short
- Pay repo rate on borrowed securities
- Typical repo rate: SOFR + 10 bps = 4.60%
- **Daily funding cost: $10M × 4.60% / 360 = $1,278**

**Long 10Y Position:**

- You own $2.23M of 10Y Treasuries
- Finance purchase via reverse repo (lend cash, receive bonds)
- Earn repo rate: SOFR + 5 bps = 4.55%
- **Daily funding cost: $2.23M × 4.55% / 360 = $282**

**Coupon Income:**

**Short 2Y:**

- Pay 4.50% coupon on borrowed bonds (semi-annual)
- **Daily cost: $10M × 4.50% / 360 = $1,250**

**Long 10Y:**

- Receive 4.00% coupon on owned bonds (semi-annual)
- **Daily income: $2.23M × 4.00% / 360 = $248**

**Net Daily Carry:**

```text
Costs:
- 2Y repo funding: -$1,278
- 2Y coupon payment: -$1,250
- 10Y repo funding: -$282
Total costs: -$2,810

Income:
- 10Y coupon income: +$248

Net Daily Carry: -$2,562

Annual Carry Cost: -$2,562 × 360 = -$922,320
As % of notional: -$922k / $12.23M = -7.54%
```

**Carry is HEAVILY NEGATIVE!**

This is typical for flattener trades when:

- You're net short (short more notional than long)
- Curve is inverted (short-term rates > long-term rates)
- Funding costs eat into P&L every day

**Breakeven Analysis:**

```text
To break even over 3 months (90 days):
Need P&L from curve move: +$230,580 (90 × $2,562)

10Y DV01 ≈ $18,887
Need 10Y to outperform 2Y by: $230,580 / $18,887 = 12.2 bps

If curve currently at -50 bps, need it to reach -62.2 bps to break even.
```

---

### Improving Carry: Steepener Trade

***Reverse Trade: 2s10s Steepener***

```text
Trade Structure:
- Long $10.0M of 2-Year Treasury at 4.50%
- Short $2.23M of 10-Year Treasury at 4.00%
- Bet: Curve will steepen (2Y yields rise relative to 10Y)
```

**Net Daily Carry:**

```text
Income:
- 2Y coupon income: +$1,250
- 10Y repo earnings: +$282

Costs:
- 2Y repo funding: -$1,278
- 10Y coupon payment: -$248

Net Daily Carry: +$6

Nearly flat carry! Much better risk/reward.
```

**Why Better Carry?**

- Net long notional (collecting more coupon than paying)
- Inverted curve helps: earning 4.50% on 2Y vs. paying 4.00% on 10Y
- Funding roughly nets out

---

## Part 4: Duration & Convexity Analysis

### Duration Profile

**Flattener Trade:**

```text
Net Modified Duration: ~0 (by construction)
Key Rate Durations (KRD):
- 2Y KRD: -$19,403 per bp (short $10M)
- 5Y KRD: $0
- 10Y KRD: +$18,887 per bp (long $2.23M)
- 30Y KRD: $0

Interpretation:
- Profit if 10Y rates fall relative to 2Y
- Loss if 2Y rates fall relative to 10Y
- Neutral to parallel shifts (all rates move together)
```

**Testing Duration Neutrality:**

***Scenario: Parallel +50 bp Shift***

```text
All yields rise by 50 bps:
2Y: 4.50% → 5.00%
10Y: 4.00% → 4.50%

2Y P&L: -1.95 × (+0.50%) × 99.50 × $10M = -$97,013
10Y P&L: -8.75 × (+0.50%) × 96.80 × $2.23M = -$94,493

Net P&L: -$2,520 (small loss due to rounding)

Nearly flat! Duration neutrality working as intended.
```

---

### Convexity Exposure

**Convexity** measures the curvature of the price-yield relationship. Longer bonds have higher convexity.

**Convexity Profile:**

```text
2Y Convexity: 0.038 (per 100 bp yield change)
10Y Convexity: 0.847 (per 100 bp yield change)

Net Convexity Exposure:
Short 2Y: -$10M × 0.038 = -$380,000
Long 10Y: +$2.23M × 0.847 = +$1,888,810

Net Convexity: +$1,508,810 (LONG convexity)
```

**Implication:**

**You are LONG convexity** - benefit from large rate moves in EITHER direction.

***Example: Large Parallel Shift (+200 bps)***

```text
2Y: 4.50% → 6.50%
10Y: 4.00% → 6.00%

Linear Duration P&L (ignoring convexity):
2Y: -1.95 × 2.00% × 99.50 × $10M = -$388,050
10Y: -8.75 × 2.00% × 96.80 × $2.23M = -$377,973
Net: -$10,077 (roughly flat)

Actual P&L (including convexity):
2Y: -$388,050 + (0.5 × 0.038 × (2.00%)² × $10M) = -$388,050 + $7,600 = -$380,450
10Y: -$377,973 + (0.5 × 0.847 × (2.00%)² × $2.23M) = -$377,973 + $37,772 = -$340,201

Net: -$40,651 + convexity gain ≈ -$10,077 + $30,172 = +$20,095

Convexity helped! Made money on large parallel shift.
```

**Large Parallel Shift Down (-200 bps):**

```text
Same analysis, convexity still helps:
Net P&L ≈ +$20,095

Convexity is ALWAYS positive for long convexity trades.
```

**Summary:**

- **Small moves**: Carry and curve directionality dominate
- **Large moves**: Convexity provides cushion and can turn losers into winners

---

## Part 5: Butterfly Trades (Extension)

### 2s5s10s Butterfly

A **butterfly** trade is a more sophisticated curve bet involving THREE points on the curve.

**Trade Structure:**

```text
- Long 2Y and 10Y (the "wings")
- Short 5Y (the "body")
- Duration-neutral across all three
```

**Sizing for Duration Neutrality:**

```text
Notional Weights (approx.):
2Y: $10M (Duration 1.95)
5Y: $8.5M (Duration 4.50)
10Y: $5M (Duration 8.75)

DV01 Balance:
2Y: +$19,403
5Y: -$38,250
10Y: +$43,750

Not quite balanced - adjust 10Y to $4.46M for exact match.
```

***View: Curve "Bows" (Middle Rates Fall Relative to Wings)***

***Scenario: Rates Change***

```text
2Y: 4.50% → 4.60% (+10 bps)
5Y: 3.90% → 3.60% (-30 bps)
10Y: 4.00% → 4.10% (+10 bps)

Curve has "bowed" - 5Y fell while wings rose.

P&L:
2Y: -1.95 × 0.10% × 99.50 × $10M = -$19,403
5Y: -4.50 × (-0.30%) × 98.00 × $8.5M = +$112,455
10Y: -8.75 × 0.10% × 96.80 × $4.46M = -$37,794

Net P&L: +$55,258

Butterfly profit!
```

**Carry Characteristics:**

- More complex - depends on curve shape
- Generally lower carry than flattener (more balanced)
- Lower directionality risk

---

## Part 6: Risk Management & Hedging

### Key Risks

***1. Curve Risk (Primary Exposure)***

```text
Risk: Curve moves opposite to your bet
Hedge: Monitor key rate durations, adjust sizing if curve moves against you
Example: If 2s10s curve at -50 bps and moves to -40 bps (steepening), consider:
- Reducing position size
- Adding wings (butterfly structure)
- Switching to steepener
```

***2. Basis Risk***

```text
Risk: Using futures vs. cash bonds creates tracking error
Hedge: Use cash bonds for large notional or long-dated trades
Example: 10Y Treasury futures (TY) vs. cheapest-to-deliver (CTD) bond
- CTD may change over time
- Delivery options create value discrepancies
```

***3. Funding Risk***

```text
Risk: Repo rates spike, increasing negative carry
Hedge:
- Lock in term repo (e.g., 3-month GC repo)
- Use interest rate swaps to hedge funding rate exposure
- Example: Pay fixed on 3M SOFR swap to lock in funding cost
```

***4. Volatility Risk***

```text
Risk: Market volatility increases bid-ask spreads and reduces liquidity
Hedge:
- Buy Treasury options (puts on 2Y, calls on 10Y for flattener)
- Size positions smaller in high-vol environments
```

---

### Position Monitoring

**Daily P&L Attribution:**

```text
Day 1 P&L Breakdown:
Carry: -$2,562
Curve Move (10s-2s): +15 bps → P&L +$28,887
Total: +$26,325

Track components separately to understand sources of return.
```

**Key Metrics:**

```text
DV01 Mismatch: <$500 per bp (acceptable)
Convexity Exposure: +$1.5M (good)
Daily Carry: -$2,562 (high - need curve move soon)
Days to Breakeven: 90 days (curve needs to move 12 bps)
Max Loss (1 std curve move): ~$150k (2σ = 40 bps curve steepening)
```

---

## Part 7: Comprehensive Case Studies

### Case Study 1: Fed Hiking Cycle (2022-2023)

**Trade Setup (Jan 2022):**

```text
Market: Fed signaling rate hikes to combat inflation
2Y: 0.75%, 10Y: 1.50%, Curve: +75 bps (normal)
Trade: Long 2s10s flattener (bet curve inverts)

Sizing:
- Short $10M 2Y at 0.75%
- Long $2.5M 10Y at 1.50%
```

**Outcome (Sep 2023):**

```text
2Y: 5.10% (+435 bps)
10Y: 4.30% (+280 bps)
Curve: -80 bps (inverted by 155 bps)

P&L Calculation:
2Y Loss: -1.95 × 4.35% × 99.50 × $10M = -$843,825
10Y Gain: -8.75 × 2.80% × 96.80 × $2.5M = -$594,950

Net P&L: -$1,438,775

WAIT - this is a LOSS despite curve flattening 155 bps!
```

**Why Did This Lose Money?**

The trade was **duration-neutral**, but:

- 2Y yields rose MUCH more in absolute terms (+435 bps vs. +280 bps)
- Short 2Y position lost $843k
- Long 10Y position ALSO lost $595k (yields rose, bond prices fell)
- **Both legs lost money**

**Lesson:** Duration-neutral ≠ immune to large parallel shifts when sizing isn't perfect.

**Better Trade Structure (In Hindsight):**

- Use **ratio spread** instead: Short $10M 2Y, Long $5M 10Y
- Over-weight long duration to capture more flattening benefit
- Accept some net duration exposure

---

### Case Study 2: COVID-19 Crash (Mar 2020)

**Trade Setup (Feb 2020):**

```text
Market: Curve at +15 bps (relatively flat)
2Y: 1.40%, 10Y: 1.55%
Trade: Long 2s10s steepener (bet curve steepens in recession)

Sizing:
- Long $10M 2Y at 1.40%
- Short $2.1M 10Y at 1.55%
```

**Outcome (Mar 2020):**

```text
2Y: 0.25% (-115 bps)
10Y: 0.70% (-85 bps)
Curve: +45 bps (steepened by 30 bps)

P&L:
2Y Gain: -1.95 × (-1.15%) × 99.50 × $10M = +$223,463
10Y Loss: -8.75 × (-0.85%) × 96.80 × $2.1M = +$151,479

Net P&L: +$374,942

Profit! Curve steepened as expected.
```

**Carry Over 30 Days:**

```text
Daily carry: +$6 (nearly flat)
30-day carry: +$180 (negligible)

Total Return: $374,942 + $180 = $375,122
Return on margin: ~15% in 30 days (assuming $2.5M margin posted)
```

**Why This Worked:**

- Correct directionality (curve steepened)
- Both legs made money (yields fell on both)
- Positive carry environment (inverted curve)
- Fed cuts benefited front end more

---

### Case Study 3: Long-Term Flattener (2019)

**Trade Setup (Jan 2019):**

```text
Market: Late-cycle expansion, curve flattening trend
2Y: 2.50%, 10Y: 2.70%, Curve: +20 bps
Trade: Long 2s10s flattener (bet inversion)

Sizing:
- Short $10M 2Y at 2.50%
- Long $2.3M 10Y at 2.70%
- Expected hold: 6 months
```

**Daily Carry:**

```text
Net daily carry: -$1,800
6-month carry: -$324,000

Need curve to flatten by: $324k / $18,887 DV01 = 17 bps just to break even.
```

**Outcome (July 2019):**

```text
2Y: 1.85% (-65 bps)
10Y: 2.05% (-65 bps)
Curve: +20 bps (UNCHANGED!)

P&L:
2Y: -1.95 × (-0.65%) × 99.50 × $10M = +$126,144
10Y: -8.75 × (-0.65%) × 96.80 × $2.3M = +$130,634

Net P&L: +$256,778
Less carry: -$324,000
Total Return: -$67,222

LOSS despite both legs making money!
```

**Lesson:** **Negative carry kills you if curve doesn't move.**

Even though both positions were profitable, the daily bleed from funding and coupon payments exceeded the gains. This is the danger of flattener trades in inverted curves.

---

## Part 8: Trading Strategies & Optimal Entry Points

### When to Enter Flatteners

**Ideal Conditions:**

1. **Fed is hiking or expected to hike**
   - Front end rises faster than long end
   - Curve typically flattens during tightening cycles

2. **Curve is steep (>100 bps)**
   - More room to flatten
   - Better carry (earning more on long end)

3. **Volatility is low**
   - Bid-ask spreads tighter
   - Easier to scale in/out

4. **Technical levels**
   - Curve near historical wides
   - Mean reversion opportunity

**Risk/Reward Assessment:**

```text
Entry: 2s10s at +120 bps
Target: Flatten to +80 bps (40 bp move)
Expected P&L: 40 bps × $18,887 DV01 = $755,480
Daily carry: -$2,500
Hold period: 60 days
Carry cost: -$150,000

Net Expected: $605,480
Risk (2σ move against): -$377,740 (curve steepens 40 bps)
Risk/Reward: 1.6:1 (acceptable)
```

---

### When to Enter Steepeners

**Ideal Conditions:**

1. **Fed is cutting or expected to cut**
   - Front end falls faster than long end
   - Curve typically steepens in easing cycles

2. **Curve is flat or inverted (<0 bps)**
   - Carry is flat or positive
   - High probability of normalization

3. **Recession fears**
   - Flight to quality steepens curve
   - Front end rallies on rate cut expectations

4. **Post-inversion**
   - Historically, curve steepens after inversion
   - Average time: 12-18 months

**Example Entry:**

```text
Entry: 2s10s at -50 bps (inverted)
Target: Steepen to 0 bps (50 bp move)
Expected P&L: 50 bps × $18,887 DV01 = $944,350
Daily carry: +$6 (nearly flat)
Hold period: 120 days
Carry cost: +$720

Net Expected: $945,070
Risk (2σ move against): -$755,480 (curve flattens further 40 bps)
Risk/Reward: 1.25:1 (excellent)
```

---

## Part 9: Advanced Variations

### Box Trades (Curve Neutrality)

**Concept:** Combine flattener and steepener across different curve segments.

***Example: 2s5s10s Box***

```text
Trade 1: Long 2s5s flattener
- Short 2Y, Long 5Y

Trade 2: Long 5s10s steepener
- Long 5Y, Short 10Y

Net Position:
- Short 2Y: -$10M
- Long 5Y: +$8.5M + $8.5M = +$17M (doubled up)
- Short 10Y: -$5M

View: 5Y outperforms both 2Y and 10Y (curve "bows" around 5Y)
```

**Use Case:** When you expect middle of curve to outperform wings.

---

### Weighted Steepeners (Convexity Harvesting)

**Concept:** Over-weight long-duration leg to harvest more convexity.

**Example:**

```text
Standard Steepener:
- Long $10M 2Y
- Short $2.3M 10Y
- Net duration: 0

Weighted Steepener:
- Long $10M 2Y
- Short $1.5M 10Y (under-weight short leg)
- Net duration: +3.0 (slightly long)

Benefit: Capture more convexity on long end, tolerate some duration risk.
```

---

## Summary & Key Takeaways

### Flattener Trades

**Best For:**

- Fed hiking cycles
- Steep curves (>80 bps)
- Expectation of inversion
- Shorter holding periods (carry drag)

**Risks:**

- Negative carry (especially when inverted)
- Need significant curve move to overcome carry
- Duration mismatch risk in large parallel shifts

**Typical Sizing:**

- Short $10M 2Y, Long $2-2.5M 10Y
- Adjust for exact duration neutrality

---

### Steepener Trades

**Best For:**

- Fed cutting cycles
- Flat/inverted curves (<20 bps)
- Recession hedging
- Longer holding periods (flat carry)

**Risks:**

- Curve can stay inverted for extended periods
- Timing risk (early entry in hiking cycle)
- Opportunity cost if carry is negative

**Typical Sizing:**

- Long $10M 2Y, Short $2-2.5M 10Y
- Often slightly over-weight long end for convexity

---

### Key Metrics to Monitor

| Metric | Target | Action if Breached |
|--------|--------|-------------------|
| DV01 Mismatch | <$500/bp | Rebalance positions |
| Daily Carry | Minimize | Consider rolling or exiting |
| Curve Spread | Track vs. entry | Take profit at target or stop loss |
| Days to Breakeven | <90 days | Exit if carry too negative |
| Convexity | Net positive | Add wings if too low |

---

### Practical Tips

1. **Start Small:** Test with 20-30% of intended size, scale up after validating thesis
2. **Monitor Carry Daily:** Set alerts if daily bleed exceeds threshold
3. **Use Futures Initially:** Cash bonds for long-term (>6 months), futures for short-term
4. **Hedge Tail Risk:** Buy wings (butterfly) if large parallel shift risk
5. **Roll Strategically:** If carry negative, consider rolling to next contract or exiting
6. **Combine with Outright:** Pair steepener with long 10Y for net duration exposure

---

**Next Steps:**

- Implement in `/src/strategies/curve_trades.py`
- Backtest historical 2s10s trades (2010-2024)
- Build real-time monitoring dashboard with DuckDB + Streamlit
- Add risk limits to portfolio optimizer

**References:**

- "Fixed Income Securities" by Bruce Tuckman (Chapter on curve trades)
- "The Handbook of Fixed Income Securities" by Fabozzi (Yield curve strategies)
- Federal Reserve historical data: <https://www.federalreserve.gov/data.htm>
