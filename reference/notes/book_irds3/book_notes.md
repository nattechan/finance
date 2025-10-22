# Pricing and Trading Interest Rate Derivatives Notes

## Reading from: `Pricing and Trading Interest Rate Derivatives - A Practical Guide to Swaps 3E by J H M Darbyshire`

### Original Code Repository Location

- Notebook: `../book_irds3/notebooks/`
- Library: `../book_irds3/bookirds/`

### My Code

See `reference/notes/book_irds3/python_notes.ipynb` for my learning implementation.

### Preface

#### Guiding questions of the book

1. What makes up the set of linear IRD products?
2. How does one trade IRDs physically, practically, and sensibly?
3. How are each of the IRDs priced and what factors influence their prices?
4. What are the risks of trading IRDs and how are they risk managed?
5. Who trades IRDs and why?
6. What are the drivers of IRarkets at large?
7. What does the future hold for IRD risk management and trading?

### Chapter 1 - Mathematical Review

The book relies on  mathematical topics from calculus, linear algebra and matrices, random variables and statistical distributions (normal, log-normal), confidence intervals, correlation and covariance, and optimization. Below are some examples of python libraries used.

```python
import numpy as np
import pandas as pd
from scipy.stats import norm
```

### Chapter 2 - Interest Rates

#### Day count conventions

For example, ACT/ACT, ACT/365, 30/360 etc.

#### Business day calendars and modified following

- Business day calendars (and to an extent holiday calendars) determine which dates are able to be used for payments, accruals, resets, etc.
- Following (F) and previous (P) determine what to do if an action date lands on a holiday.
- Modified ('M' preceeding the date rules) denotes what to do if an adjustment goes on to the next month.

#### Per annum interest rates and annualized interest rates

The relationship between per annum rates and annualized rates:

$$\text{Annualized rate} = \left(1 + \frac{PAR}{f}\right)^f - 1$$

Where:

- $PAR$ = Per Annum rate
- $f$ = frequency (number of compounding periods per year)

#### Continuous compounding

The relationship between continuously compounded rates and simple rates:

$$e^{DCF \times CCr} = 1 + DCF \times PAR$$

Where:

- $DCF$ = Day Count Fraction (time period in years)
- $CCr$ = Continuously Compounded rate
- $PAR$ = Per Annum rate (simple rate)

Continuously compounded rates are useful in derivations for financial mathematics but have limited practical use

#### Time value of money and discount factors (DFs)

No arbitrage pricing (equivalent financial scenarios should have identical values and prices)

#### Interest rate indexes

- For various currencies, there are central bank rates and overnight indexes and risk free rates (i.e., in USD, the Federal Reserve dictates the discount rate and federal funds target rate, while the ). The former is central bank dependent and the latter is market dependent and transaction based.
- Overnight index swap (OIS) rates are calculated based off of data on executed unsecured lending tranasactions. The index is a notional weighed average, and published as a daily overnight level.
- IBOR vs OIS Index differs where IBOR is an estimate of the future level while OIS is an observation of the past (both are unsecured). There is sometimes a lag between when a rate is fixed and the valuation period (i.e., 2 b.d. lag with EUR)
- Fallback method was requred to continue to settle derivative contracts which settled against IBOR after the cessation, turning the rate from a look-forward rate (IBOR) into a look-back rate (RFR).

### Chapter 3 - Basics of IRDs

#### Guiding Questions

1. How any IRD can be physically traded and the associated mechanisms.
2. Each of the basic interest rate products including their mathematical pricing formulae.

#### Trading mechanisms

##### Trading on exchange

- Futures and options exchange, swap execution facility (SEF), designated contract market (DCM), Made available to trade (MAT).
- SEF and DCM are legal entities that act as a record keeper and general ledger for IRD transactions, but do not act as a full fledged exchange as they do not service accounts or maintain margin.
- MATs are typically common, liquid swaps that have to be traded on SEF or DCM and through a clearing house

##### Trading off exchange

- Transaction directly between two parties or brokered by an intermediary (does not need to go through an exchange or clearing house).
- Requires a pre-signed documentation of terms (ISDA).
- Can be settled bilaterally or through an clearing house.

##### Clearing house

- A legal counterparty between which the two IRD counterparties are facing (market and collateral neutral), acting as a centralized trade depository, mitigating credit risk.

##### Margin

- Cash as insurance required by a clearing house when there is an open, at risk, traded position with a counterparty.
- Initial margin is the margin required to make new positions/trades, variation/maintenance margin is the margin required to keep open positions active (re-calculated daily).

##### Forward rate agreements (FRAs)

- Obsolete or becoming obsolete post IBOR cessation
- A cash for difference derivative, settled against a particular IBOR index of some future benchmark fixing.

**FRA pricing formula:**

The present value of an FRA from the perspective of the buyer/payer of the contract:

$$P = v_{i-1} \frac{N d_i (r_i - R)}{1 + d_i r_i}$$

Where:

- $P$ = Present value of the FRA
- $v_{i-1}$ = Discount factor to the settlement date
- $N$ = Notional amount
- $d_i$ = Day count fraction for the accrual period
- $r_i$ = Floating rate (actual IBOR fixing)
- $R$ = Fixed rate (agreed FRA rate)

The numerator represents the undiscounted cash settlement: the buyer receives $(r_i - R)$ on notional $N$ over period $d_i$.
The denominator discounts this payment from the end of the accrual period back to the settlement date using the actual floating rate $r_i$.

**FRA quoting convention:**

- 'Currency, Index, Start-month x End-month, Roll-date' i.e., 'GBP, LIBOR, 5 x 8, 23rd, FRA'.
- Start-month and end-month are the numbers of month from the current month.

##### STIR futures (IBOR)

- Obsolete or becoming obsolete post IBOR cessation.
- Similar to FRAs as tey are cash settled against a future benchmark but they differ in a few ways.
- SITR futures are traded on exchanges, FRAs are off exchange.
- Size of single contract on STIR future is set to notioanl sizes according to exchange rules (0.5mm or 1mm), vs. FRAs which can have bespoke notionals.
- STIR futures are quoted in price terms, FRAs are quoted in yield terms.
- STIR futures start and settle on specific dates set by exchange, FRAs can be written for any business day.

- STIR futures settle only against 3M-IBOR tenors and only for value start dates that fall on International Monetary Market (IMM) dates.

**STIR future pricing:**

The 3M-IBOR fixing rate implied by a STIR future is:

$$r_{i} = 100 - q_{i}$$

where $q_{i}$ is the price of the future. The PV of a single STIR future contract (from POV of the buyer) is:

$$P = N (q_{i} - Q_{i})$$

where $N$ is the value of one lot per unit increment, and $Q_{i}$ the orignally traded price.

**Settlement:**

Exchange delivery settlement price (EDSP):

$$EDSP = 100 - \text{3M-IBOR fixing}$$

##### STIR futures (RFR)

- Similar to STIR futures (IBOR), with the same properties to IMM dates, fixed notional, and pricing conventions.
- Fixings of RFR STIR within the period must occur before the EDSP can be produced (i.e., a March contract cannot be settled in March).

**EDSP:**

EDSP one month rate:

$$EDSP\ one\ month\ rate = 100 \times \left(\frac{1}{d}\sum_{k=1}^{T_1}\left(r_k d_k\right)\right)$$

EDSP three month rate:

$$EDSP\ three\ month\ rate = 100 \times \left(\frac{1}{d}\prod_{k=1}^{T_1}\left(1 + r_k d_k\right) - 1\right)$$

Where:

- $T_1$ = the number of fixings that make up the period
- $d$ = the three month rate settles for a compounded rate, albeit both of these definitions describe the EDSP in terms of the exchange specifying the contracts and they may differ
- $r_k$ = RFR fixings
- $d_k$ = day count fraction for each published fixing

- Since the front month contract does not settle until all the RFR fixings are published, it continues to trade mid period.
- Reduces its volatility substantially midway through its periods since proportions of the EDSP is already known, and with each published fixing becomes less variable.
- RFR SITR futures experience convexity adjustments.

##### IRSs and OIS

### Chapter 4 - Users of IRDs

### Chapter 5 - Cash, Collateral, and Credit

### Chapter 6 - Single Currency Curve Modeling

### Chapter 7 - Multi-Currency Curve Modeling

### Chapter 8 - Term Structure of Interest Rate Curves

### Chapter 9 - Delta and Basis Risk

### Chapter 10 - Risk Models

### Chapter 11 - Quant Library and Automatic Differentiation

### Chapter 12 - Advanced Curve Building

### Chapter 13 - Multi-Currency Risk

### Chapter 14 - Value at Risk

### Chapter 15 - Principal Component Analysis

### Chapter 16 - Customised Risk Management

### Chapter 17 - Regulatory Capital, Leverage, and Liquidity

### Chapter 18 - Market-Making and Price-Taking

### Chapter 19 - Electoric Trading

### Chapter 20 - Swaptions and Volatility

### Chapter 21 - Gamma and Cross-Gamma Risk

### Chapter 22 - Analytic Cross-Gamma

### Chapter 23 - Constructing Trade Strategies

### Chapter 24 - Reset Risk
