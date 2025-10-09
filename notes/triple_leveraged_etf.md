# Triple-Leveraged ETF Structuring for Equity Derivatives Client

## Executive Summary

A triple-leveraged ETF structure for a client involves creating a **synthetic 3x exposure** to an underlying index through total return swaps (TRS) or funded equity swaps. As the dealer, you're providing 3x daily leverage on the reference index with daily rebalancing to maintain constant leverage.

**Typical All-In Cost to Client:**
- Funding spread: **OIS + 50-150 bps** on the borrowed portion (2x notional)
- Management fee: **75-150 bps annually** on notional
- Rebalancing costs: **10-30 bps annually** (volatility-dependent)
- **Total: ~300-500 bps annually** depending on structure and rates

---

## Part 1: Trade Structure & Economics

### Case Example 1: $10M Notional 3x S&P 500 Exposure

**Initial Setup:**
```
Client Investment: $10,000,000 (100% cash collateral)
Gross Exposure: $30,000,000 (3x leverage)
Dealer Funding Required: $20,000,000

Client receives: 3x daily S&P 500 returns
Client pays: Funding costs + management fees
```

**Cash Flow Breakdown:**

**Day 0 - Trade Inception:**
- Client posts: $10M cash to you
- You borrow: $20M in repo/funding markets at OIS + 30 bps
- You purchase: $30M S&P 500 futures or delta-one basket
- Net dealer funding: $20M at cost of carry

**Daily Economics (assuming OIS = 4.5%, Your Funding Spread = 100 bps):**

```
Daily Funding Charge to Client:
- Borrowed amount: $20M
- Rate: 4.5% + 1.0% = 5.5% annually
- Daily cost: $20M × 5.5% / 360 = $3,055.56

Daily Management Fee:
- Fee: 1.0% annually on $10M notional
- Daily cost: $10M × 1.0% / 360 = $277.78

Total Daily Cost to Client: $3,333.34
```

**Your Revenue & Margin:**

```
Revenue (What you charge client):
- Funding: 5.5% on $20M = $1,100,000/year
- Management fee: 1.0% on $10M = $100,000/year
- Total revenue: $1,200,000/year

Costs (What you pay):
- Funding cost: 4.8% on $20M = $960,000/year (OIS + 30 bps)
- Rebalancing costs: ~$20,000/year (execution slippage)
- Total costs: $980,000/year

Net Margin: $220,000/year = 220 bps on client notional
ROE: ~22% on $10M capital (if fully collateralized)
```

---

## Part 2: Daily Rebalancing Mechanics & Path Dependency

### Why Daily Rebalancing is Required

The leverage ratio drifts as markets move. You must rebalance daily to maintain exactly 3x exposure.

**Example Day 1: S&P 500 +2%**

```
Before Market Close:
- Client NAV: $10M → $10.6M (+6% from 3x exposure)
- Exposure: $30M → $30.6M (now only 2.89x the new NAV)
- Target exposure: $10.6M × 3 = $31.8M

Rebalancing Required:
- Must BUY: $31.8M - $30.6M = $1.2M additional exposure
- Funding increases: Borrow additional $1.2M
- New funded amount: $21.2M

After Rebalance:
- Client NAV: $10.6M
- Exposure: $31.8M (exactly 3x again)
- Your funding: $21.2M
```

**Example Day 2: S&P 500 -3%**

```
Before Market Close:
- Client NAV: $10.6M → $9.646M (-9% from 3x exposure)
- Exposure: $31.8M → $30.846M (now 3.20x the new NAV)
- Target exposure: $9.646M × 3 = $28.938M

Rebalancing Required:
- Must SELL: $30.846M - $28.938M = $1.908M exposure
- Funding decreases: Repay $1.908M
- New funded amount: $19.292M

After Rebalance:
- Client NAV: $9.646M
- Exposure: $28.938M (exactly 3x again)
- Your funding: $19.292M
```

### Path Dependency & Volatility Drag

**Critical Issue:** Due to daily rebalancing, the 3x product does NOT deliver 3x the cumulative return over multi-day periods.

**Example: Volatile Markets**

```
Scenario 1: Low Volatility
Day 1: Index +1%, 3x ETF +3%
Day 2: Index +1%, 3x ETF +3%
Cumulative: Index +2.01%, 3x ETF +6.09% (≈3x)

Scenario 2: High Volatility (same cumulative index return)
Day 1: Index +5%, 3x ETF +15%
Day 2: Index -2.86%, 3x ETF -8.58%
Cumulative: Index +2.01%, 3x ETF +5.13% (only 2.55x)

Volatility drag: ~1% underperformance
```

This creates **convexity exposure** for you as the dealer - you're effectively short gamma.

---

## Part 3: Margin Calculation & Regulatory Capital

### Initial Margin (IM) Requirements

**For the Client:**
- Typically **100% of notional** posted as cash collateral
- Sometimes 105-110% to cover small adverse moves
- In your example: $10M cash posted

**For You (Dealer) - Regulatory Capital:**

Under **SA-CCR (Standardized Approach for Counterparty Credit Risk):**

```
Replacement Cost (RC): $0 (fully collateralized by client)

Potential Future Exposure (PFE):
- Notional: $30M gross exposure
- Supervisory Delta: +1.0 (linear equity exposure)
- Supervisory Factor: 32% for equity derivatives
- Maturity Factor: ~1.0 for short-dated
- PFE ≈ $30M × 0.32 × 1.0 = $9.6M

Exposure at Default (EAD): RC + PFE = $9.6M
Risk-Weighted Assets (RWA): $9.6M × 100% = $9.6M
Capital Required (8%): $9.6M × 8% = $768,000

Capital charge as % of notional: 7.68%
```

### Variation Margin (VM) - Daily Settlement

**You mark-to-market daily with the client:**

```
Day 1: S&P 500 +2%
- Client profit: $10M × 3 × 2% = $600,000
- You owe client: $600,000 in cash
- Client NAV increases to $10.6M
- No margin call (client already fully funded)

Day 2: S&P 500 -3%
- Client loss: $10.6M × 3 × -3% = -$954,000
- Client owes you: $954,000
- Deducted from their collateral balance
- New NAV: $9.646M
```

**Margin Call Triggers:**
- If client NAV falls below maintenance threshold (e.g., 20% of original)
- Client must post additional cash or position is liquidated
- For $10M notional with 3x leverage, ~33% index decline wipes out NAV

---

## Part 4: Your Risk Exposures as Dealer

### 1. **Funding Risk**

**Exposure:** You're borrowing $20M at OIS + 30 bps but charging client OIS + 100 bps. If your funding costs spike, your margin compresses.

**Quantification:**
```
Funding Basis Risk:
- Borrowed: $20M at floating OIS + 30 bps
- Revenue: $20M at OIS + 100 bps
- Spread: 70 bps = $140,000/year

If OIS rises 1%:
- Your cost rises: +$200,000/year
- Client payment rises: +$200,000/year
- Net impact: $0 (naturally hedged)

BUT if your credit spread widens 50 bps:
- Your cost rises: +$100,000/year
- Client payment unchanged
- Net loss: $100,000/year (margin compression)
```

**Mitigation:** Lock in funding through term repo or interest rate swaps.

### 2. **Path-Dependency Risk (Short Gamma)**

**Exposure:** Daily rebalancing in volatile markets creates negative convexity. You're forced to "buy high, sell low."

**Quantification:**
```
High Volatility Period:
Day 1: Index +5%
- Client up 15% → NAV = $11.5M
- Must buy $1.5M additional exposure at elevated prices

Day 2: Index -5%
- Client down 15% → NAV = $9.775M
- Must sell $1.7M exposure at depressed prices

Rebalancing Loss: Transaction costs + adverse selection
- Bid-ask spread: 2-5 bps
- Market impact: 3-10 bps (size dependent)
- Total: ~$3,000-$7,000 per rebalancing cycle

Annual cost in 30% vol environment: $30,000-$50,000
This exceeds your budgeted rebalancing allowance!
```

**Mitigation:** 
- Charge higher fees for high-volatility underlyings
- Use options overlays to hedge gamma exposure
- Implement rebalancing bands (±5% tolerance) rather than daily

### 3. **Counterparty Credit Risk**

**Exposure:** Client could default when deeply out-of-the-money to you.

**Scenario:**
```
Market crashes 35% over 5 days:
- Client NAV: $10M → effectively $0
- Your position: Long $30M exposure → Down $10.5M
- Net exposure: $10.5M loss vs. $10M collateral
- Uncollateralized loss: $500,000

Gap Risk: Time between margin call and liquidation
```

**Mitigation:**
- Conservative margin thresholds (liquidate at 25-30% loss)
- Daily or intra-day margin calls
- Price credit risk into fees (higher spread for weaker credits)

### 4. **Operational & Model Risk**

**Exposure:** Errors in daily NAV calculation, rebalancing execution, or index tracking.

**Example Operational Loss:**
```
Failure to rebalance on Day 1:
- Should have bought $1.2M additional exposure
- Delay by 1 day
- Day 2: Index moves another +2%
- Loss from under-hedged position: $1.2M × 2% = $24,000
```

---

## Part 5: Hedging Strategies

### Hedge 1: **Delta Hedging with Futures**

**Most Common Approach**

**Implementation:**
```
Daily Rebalancing via S&P 500 Futures:
- Contract size: $50 × S&P 500 Index
- Index at 4,000: Notional per contract = $200,000
- For $30M exposure: 150 contracts

Day 0: Buy 150 ES futures contracts
- Margin required: ~10% = $3M (from client's $10M collateral)
- Balance $7M earns interest

Daily Adjustments:
Day 1 (+2%): Buy 3 additional contracts
Day 2 (-3%): Sell 4.5 contracts (round to 5)
```

**Advantages:**
- Highly liquid, tight spreads (0.5-1 bps)
- Low margin requirements (~10%)
- Easy to scale and rebalance

**Disadvantages:**
- Basis risk (futures vs. spot index)
- Roll costs every quarter ($10,000-$30,000 annually)
- No protection against volatility drag

**Cash Flows:**
```
Initial:
- Post $3M margin to exchange (from client collateral)
- Earn OIS on remaining $7M cash: $7M × 4.5% = $315,000/year

Daily:
- VM settled in cash (gains/losses paid daily)
- Rebalancing transaction costs: ~$500/day average
```

---

### Hedge 2: **Delta-One Basket Replication**

**For Tighter Tracking**

**Implementation:**
```
Buy physical basket of S&P 500 stocks:
- Top 50 holdings: ~70% index weight
- Track with 0.98+ correlation
- $30M basket, weighted by market cap

Rebalancing:
- Add/remove positions as NAV changes
- Rebalance portfolio weightings monthly
- Use futures for intra-month adjustments
```

**Advantages:**
- Capture dividend income (~1.5% yield on $30M = $450k/year)
- No roll costs
- Better tracking than futures (no basis risk)

**Disadvantages:**
- Higher transaction costs (5-10 bps per rebalance)
- Requires stock loan/borrow for liquidity
- More operational complexity
- Tied up capital in physical holdings

**Economics:**
```
Annual Dividend Income: $450,000
Less: Rebalancing costs: -$60,000
Less: Stock borrow fees: -$30,000
Net benefit vs. futures: +$360,000/year

Improves margin by 360 bps on notional
```

---

### Hedge 3: **Variance Swaps / Volatility Overlay**

**To Hedge Path-Dependency Risk**

**Problem:** You're short gamma - daily rebalancing costs increase with volatility.

**Solution:** Buy volatility protection via variance swaps or VIX call options.

**Implementation:**
```
1-Year Variance Swap:
- Notional: $30M
- Strike: 20% annualized volatility
- Current implied variance: 18%
- Cost: ~$200,000 premium (if vol spikes)

Payoff:
If realized vol = 30%:
- Variance swap pays: $30M × (30²% - 20²%) = $1.5M
- This offsets increased rebalancing costs

If realized vol = 15%:
- You lose premium paid: -$200,000
- But rebalancing costs are minimal anyway
```

**Alternative: VIX Call Spread**
```
Buy VIX 25/35 call spread (6-month):
- Protects if volatility spikes above 25
- Cost: ~$50,000 per quarter
- Caps your rebalancing losses in crisis scenarios
```

**Advantages:**
- Direct hedge of path-dependency risk
- Protects in tail events (market crashes)
- Relatively cheap insurance (~50-100 bps/year)

**Disadvantages:**
- Negative carry in low-vol environments
- Basis risk (VIX vs. realized vol of your rebalancing)
- Requires sophisticated vol trading desk

---

### Hedge 4: **Dynamic Hedging with Options**

**For Large Notional or Long-Dated Structures**

**Implementation:**
```
Sell OTM Put Options (30 delta, 1-month tenor):
- Generates premium income
- Offsets funding costs
- Notional: $10M of puts (33% of exposure)
- Premium: ~2% = $200,000

Buy ATM Call Options (50 delta, 1-month):
- Reduces downside gap risk
- Costs: ~4% = $400,000
- Net delta: Still +1.0 (delta-neutral)

Net Cost: -$200,000/year
- This increases your all-in cost but provides tail protection
```

**Advantages:**
- Convex payoff in tail scenarios
- Reduces gap risk from client default
- Can be structured to minimize capital charges

**Disadvantages:**
- Expensive (~200 bps drag on margin)
- Requires monthly rolling and rebalancing
- Introduces vega and theta exposures

---

## Part 6: Balance Sheet & Funding Implications

### Balance Sheet Impact

**Assets:**
```
$30M Equity Exposure (S&P 500 futures or physical)
$10M Client Cash Collateral
```

**Liabilities:**
```
$20M Repo Borrowing (funding)
$10M Synthetic Short Position to Client (TRS liability)
$9.6M RWA for regulatory capital
```

**Leverage Ratio:**
```
Gross Notional: $30M
Tier 1 Capital Required (3%): $900,000
With $10M client cash: Leverage = 3:1

If funded entirely from balance sheet:
Tier 1 Capital Required: $900,000 (SLR)
+ Risk-Based Capital: $768,000 (RWA)
Total Capital: ~$1.7M for $10M trade

ROE: $220,000 margin / $1.7M capital = 12.9%
```

### Funding Sources & Costs

**Option 1: Repo Market (Cheapest)**
```
Overnight GC Repo:
- Rate: SOFR + 10-30 bps
- Term: Daily rollover
- Margin: 102% (must post $20.4M securities)
- Cost: 4.6% all-in

Risk: Rollover risk if repo market dislocates
```

**Option 2: Prime Brokerage Credit Line**
```
Committed facility from bank:
- Rate: SOFR + 100 bps
- Term: 364-day committed
- Margin: Cash-settled daily
- Cost: 5.5% all-in

Benefit: Guaranteed funding, no rollover risk
```

**Option 3: Balance Sheet (Most Expensive)**
```
Use bank's own capital:
- Cost of equity: 10-12%
- Regulatory capital: $1.7M
- Opportunity cost: $170,000-$204,000/year

Only viable for strategic clients or bundled with other business
```

---

## Part 7: Comprehensive Case Studies

### Case Study 1: Stable Market (Low Volatility, Trending Up)

**Parameters:**
- Notional: $10M
- Period: 252 trading days (1 year)
- Index: S&P 500 starts at 4,000
- Scenario: +12% annual return, 15% realized vol

**Performance:**
```
Index Return: +12% → 4,480
Client 3x Return: ~+38% (with vol drag) → NAV $13.8M
Your Hedging: S&P futures tracking index

Cash Flows:
Revenue:
- Funding fees: $20M × 5.5% = $1,100,000
- Management fees: $10M × 1.0% = $100,000
- Total: $1,200,000

Costs:
- Funding: $20M × 4.8% = $960,000
- Rebalancing: 150 bps × 252 days × 0.5 bps = $15,000
- Futures roll: $25,000
- Total: $1,000,000

Net Profit: $200,000 (200 bps on notional)
ROE: 11.8% on $1.7M capital
```

**Outcome:** Clean profit, client happy with 38% return.

---

### Case Study 2: High Volatility, Sideways Market (Worst Case)

**Parameters:**
- Notional: $10M
- Period: 252 trading days
- Index: Oscillates between 3,800-4,200 (ends flat at 4,000)
- Realized vol: 35% (market whipsaw)

**Performance:**
```
Index Return: 0%
Client 3x Return: -15% (volatility drag!) → NAV $8.5M
Your Hedging: Delta-hedged but losses from rebalancing

Cash Flows:
Revenue:
- Funding fees: Average $19M × 5.5% = $1,045,000
- Management fees: Average $9.25M × 1.0% = $92,500
- Total: $1,137,500

Costs:
- Funding: $19M × 4.8% = $912,000
- Rebalancing: High vol → 5 bps × 252 days = $126,000
- Slippage in volatile markets: $75,000
- Total: $1,113,000

Net Profit: $24,500 (25 bps on notional)
ROE: 1.4% on $1.7M capital
```

**Outcome:** Marginal profit for you, but client suffers volatility decay. Risk of complaints/litigation.

**Mitigation for Next Time:**
- Increase rebalancing cost estimate to 50 bps
- Add 50 bps volatility surcharge to management fee
- Buy variance swap protection

---

### Case Study 3: Market Crash (-30% Index Drop in 10 Days)

**Parameters:**
- Notional: $10M
- Scenario: Flash crash, index 4,000 → 2,800
- Client NAV: $10M → $1M (90% loss)

**Performance:**
```
Client Position:
- Day 10 NAV: ~$1M (before approaching zero)
- You liquidate at $2M NAV (30% maintenance margin)
- Client loses $8M of $10M invested

Your Position:
Revenue:
- Funding fees (10 days): $3,000
- Management fees: $275
- Total: $3,275

Costs:
- Funding: $2,600
- Emergency liquidation of $30M hedge: -$450,000 (slippage!)
- Total: -$452,600

Net Loss: -$449,325

Gap Risk:
- Client owes you based on contract but is bankrupt
- You may recover only partial collateral
- Legal/workout costs: $100,000
```

**Outcome:** Significant loss due to:
1. Illiquidity in crash (can't rebalance fast enough)
2. Client default with insufficient collateral
3. Slippage on emergency hedge liquidation

**Prevention:**
- More conservative margin thresholds (liquidate at 40% loss)
- Intraday monitoring and margin calls
- Tail risk insurance via put options
- Client suitability assessment (ensure they understand risk)

---

## Part 8: Regulatory & Compliance Considerations

### Suitability Requirements

**KYC/AML:** Client must be:
- Institutional or qualified investor
- Demonstrated understanding of leverage and daily rebalancing
- Signed risk disclosure (path dependency, margin calls, total loss possible)

### Trade Reporting

**Dodd-Frank / EMIR Requirements:**
- Report TRS to swap data repository
- If notional >$50M: Post initial margin to third party
- Daily valuation and reconciliation

### Capital Treatment

**Basel III / Dodd-Frank:**
- RWA: $9.6M (as calculated above)
- Supplementary Leverage Ratio: 3% × $30M = $900k capital
- Total: ~$1.7M capital required per $10M trade

**Profitability Threshold:**
Must generate >$170k profit for 10% ROE hurdle
Your $220k margin exceeds this (12.9% ROE)

---

## Summary & Recommendations

### Optimal Structure

**For Standard Client ($10M notional):**

1. **Pricing:**
   - Funding: OIS + 100 bps on borrowed portion (2x)
   - Management: 100 bps on notional
   - Total cost: ~450 bps annually
   - Your net margin: 200-220 bps

2. **Hedging:**
   - Primary: Delta hedge with S&P 500 futures (150 contracts)
   - Secondary: 6-month VIX call spread for tail protection (optional)
   - Rebalancing: Daily EOD, executed via futures

3. **Margin:**
   - Client posts: 100% cash ($10M)
   - Your capital: $1.7M regulatory
   - Liquidation trigger: 70% loss (NAV $3M)

4. **Funding:**
   - Source: Overnight GC repo at SOFR + 30 bps
   - Alternative: Prime brokerage line (more expensive but safer)

### Deal Economics Summary

```
Per $10M Client Notional:

Annual Revenue: $1,200,000 (1,200 bps)
Annual Costs: $980,000 (980 bps)
Net Margin: $220,000 (220 bps)

Capital Required: $1,700,000
ROE: 12.9%
Risk-Adjusted ROE: ~10% (after expected losses)

Break-Even Revenue: ~$1,070,000 (1,070 bps) for 10% ROE
Your Margin: 130 bps above break-even
```

This structure provides attractive economics while managing your key risks through delta hedging, conservative margining, and appropriate fee capture for the leverage and rebalancing services you provide.