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

#### Forward rate agreements (FRAs)

- Obsolete or becoming obsolete post IBOR cessation
- A cash for difference derivative, settled against a particular IBOR index of some future benchmark fixing.

##### FRA pricing formula

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

##### FRA quoting convention

- 'Currency, Index, Start-month x End-month, Roll-date' i.e., 'GBP, LIBOR, 5 x 8, 23rd, FRA'.
- Start-month and end-month are the numbers of month from the current month.

#### STIR futures (IBOR)

- Obsolete or becoming obsolete post IBOR cessation.
- Similar to FRAs as tey are cash settled against a future benchmark but they differ in a few ways.
- SITR futures are traded on exchanges, FRAs are off exchange.
- Size of single contract on STIR future is set to notioanl sizes according to exchange rules (0.5mm or 1mm), vs. FRAs which can have bespoke notionals.
- STIR futures are quoted in price terms, FRAs are quoted in yield terms.
- STIR futures start and settle on specific dates set by exchange, FRAs can be written for any business day.

- STIR futures settle only against 3M-IBOR tenors and only for value start dates that fall on International Monetary Market (IMM) dates.

##### STIR future pricing

The 3M-IBOR fixing rate implied by a STIR future is:

$$r_{i} = 100 - q_{i}$$

where $q_{i}$ is the price of the future. The PV of a single STIR future contract (from POV of the buyer) is:

$$P = N (q_{i} - Q_{i})$$

where $N$ is the value of one lot per unit increment, and $Q_{i}$ the orignally traded price.

##### Settlement

Exchange delivery settlement price (EDSP):

$$EDSP = 100 - \text{3M-IBOR fixing}$$

#### STIR futures (RFR)

- Similar to STIR futures (IBOR), with the same properties to IMM dates, fixed notional, and pricing conventions.
- Fixings of RFR STIR within the period must occur before the EDSP can be produced (i.e., a March contract cannot be settled in March).

##### EDSP

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

#### IRSs and OIS

##### IRS

- An agreement to exchange a series of fixed rate payments for a series of floating rate payments by an RFR index (previously an IBOR index). We treat OIS and IRS as semantically the same now as RFRs are overnight indices.
- The main component of an IRS is the date schedule, incouding payment dates, accrual periods, fixing dates for determination of floating rates, and notional amounts.

Example IRS

*Example cashflows of a standard 6M semi-quarterly IRS starting on 8th February 2016 and ending 8th August 2016. It details one fixed cashflow and two floating cash flows:*

| Notional | Accrual date | Accrual end date | Fixing date | Value date | Value end date | Payment date | Rate | Cashflow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100,000,000 | 2016-02-08 | 2016-08-08 | - | - | - | 2016-08-08 | 2.025% | 1,009,726 |
| 100,000,000 | 2016-02-08 | 2016-05-09 | 2016-02-04 | 2016-02-08 | 2016-05-09 | 2016-05-09 | 1.961% | -488,907 |
| 100,000,000 | 2016-05-09 | 2016-08-08 | 2016-05-05 | 2016-05-09 | 2016-08-09 | 2016-08-08 | 2.061% | -513,838 |

To obtain the PV, multiply the cashflows with approriate DF relevatn to the payment date. The floating payments are unknown until all of the relevant fixing publications have been made, so market movements will cause valuation changes.

*For a standard (or vanilla) IRS:*

- The same notional, $N$, for every individual period of the IRS either on the floating or fixed leg
- A consecutive structure so that each period comes immediately after another without overlapping or creating gaps
- An alignment between the fixed and floating legs (subject to the frequency) so that accrual periods and payment dates on each are the same
- An alignment of the fixing date and flaoting rate tenor to the given accrual schedule and payment schedule for the floating leg. Payments are made in arrears, that is, at the end of each period, usually on the accrual end date
- Standard day count conventions and fied leg frequency in each specified currency

Customization:

Stub periods:

When start and end dates are specified wihtout an associated relationship, it creates stub periods, placed in IRS either at the start, end, or both, so that the remianing part of the leg follows teh speciifed frequency and reverts to the form of a standard IRS.

Mathematical formulae:

The present value of a **standard IRS**:

$$P = N \left(-R \sum_{i=1}^{T_1} d_i v_i + \sum_{j=1}^{T_2} d_j r_j v_j \right)$$

The present value of a **customised IRS**:

$$P = \sum_{i=1}^{T_1} N_i d_i v_i + \sum_{j=1}^{T_2} N_j d_j r_j v_j$$

Where:

- $T_1, T_2$ = number of periods in the fixed and float leg respectively
- $N$ = notional (for standard IRS), $N_i$ = notional per period (for customised IRS)
- $R$ = fixed rate
- $d_i$ = day count fraction for period $i$
- $v_i$ = discount factor to payment date $i$
- $r_j$ = floating rate for period $j$

In the case of OISs and other compounded RFRs the period floating rates, $r_j$, are determined from the individual published RFRs, $\tilde{r}_k$, for the period such that:

$$r_j = \left(\prod_{k=1}^{T_j} (1 + \tilde{r}_k d_k) - 1\right) / d_j, \quad T_j = \text{number of business days in period } j$$

*Example 3.4:*

Assume that last day RFR fixings make up a single OIS period and that on Thursday, Friday and Monday the fixings are published at 2.00%, 2.10% and 2.15%. Then the compounded rate over the period from Thursday to Tuesday, which represents three business days, is:

$$\left(\left[\prod_{k=1}^{3} (1 + \tilde{r}_k d_k)\right] - 1 \right) / d_j = \left(\left[\left(1 + \frac{1}{365}(1)\right) \left(1 + \frac{2.1}{365}(1)\right) \left(1 + \frac{2.15}{365}(1)\right)\right] - 1\right) \times \frac{365}{5} = 2.0092\%$$

In this example Friday's OIS fixing has not been applied for the weekend days, so that the DCF becomes effectively longer. Very often in OISs, particularly for Christmas day and New Year's day and the periods immediately before and after the fixings can dominate the equation and become important considerations around holiday periods such as Easter and other religious holidays.

Mid-market pricing:

The mid-market price for any IRS, $R_0$, is by definition the price for which the PV is zero. Given that one can conditionally, in the case of IRSs against RFRs, we have a direct mechanism where the floating leg itself has a precise value (often zero), or in the case of conventional swaps, forecast what the future floating rates will be, and we have a direct relationship between the two such that,

$$R_0 = \left(\frac{v_0 - v_{T_1}}{d_1}\right) / d_1$$

Thus in the case of a standard IRS (the day count fraction of the floating leg and its discount) we have:

$$R^{mid} = \frac{\sum_{j=1}^{T_2} d_j r_j v_j}{\sum_{i=1}^{T_1} d_i v_i} = \frac{v_0 - v_{T_1}}{\sum_{i=1}^{T_1} d_i v_i}$$

Quoting convention:

'Currency, Start-date, End-date, Fixed-frequency, Float-frequency, Roll-date, Stub-type'

*Example:*

'USD SOFR, 3rd Jun '18, 29th Jul '28, Annual, Semi, 15th, Long-front short-back, IRS'

This represents a USD IRS with a floating leg that settles against SOFR for periods which start dates as of the 15th of each month of Jan and Jul. The long-front stub on the floating leg runs from 3rd Jun '18 to 15th Jan '19, and the short-back stub from 15th Jul '28 to 29th Jul '28. The fixed leg's long-front stub is slightly different to account for the different frequency and runs from 3rd Jun '18 to 15th Jul '19.

*Figure 3.2: Stub period types:*

```text
(a) Short-front                    (b) Long-front
┌────┬────┬────┬────┐              ┌──┬──┬────┬────┬────┐
│////│    │    │    │              │//|//│    │    │    │
│////│Reg │Reg │Reg │              │//|//│Reg │Reg │Reg │
└────┴────┴────┴────┘              │//|//│    │    │    │
START              END             └──┴──┴────┴────┴────┘
                                   START               END

(c) Short-back                     (d) Long-back
┌────┬────┬────┬────┐              ┌────┬────┬────┬──┬──┐
│    │    │    │////│              │    │    │    │//|//│
│Reg │Reg │Reg │////│              │Reg │Reg │Reg │//|//│
└────┴────┴────┴────┘              │    │    │    │//|//│
START              END             └────┴────┴────┴──┴──┘
                                   START               END
```

*Figure 3.2 shows short and back stub types (which can be combined) either side of swap periods which take place with regular frequency, such as annual, semi-annual, quarterly or monthly.*

Historically, stub periods, being non-standard tenors, meant that they had to settle against interpolated IBOR rates.

*Figure 3.3: Schedule diagram for the example IRS:*

```text
                     Fixed Leg
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬──┐
│/////│     │     │     │     │     │     │     │     │     │//│
│/////│     │     │     │     │     │     │     │     │     │//│ ←─ Annual
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴──┘
START                                                 END
┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│//|  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │//│
│//|  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │//│ ←─ Semi-annual
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
START                                                               END
                     Float Leg
```

*Figure 3.3: Depicting the schedule of a 'USD SOFR, 3rd Jun '18, 29th Jul '28, Annual, Semi, 15th, Long-front short-back, IRS'.*

The hatched/shaded areas (////) represent stub periods at the start (long-front) and end (short-back) of the swap.

#### Single currency basis swaps (SBSs)

- Obsolete or becoming obsolete post IBOR cessation (for some currencies)
- Exchange a series of flaoting cashflows, almost exclusively of one index against another (i.e., 3M-IBOR cashflows for 6M-IBOR cashflows)
- a bp spread amount (or annuity) is attached to one of the legs to get NPV = 0 at inception (spread is the effective mid-market price), and is usually added to the index of the shortest tenor of either of either of the legs to result in a positive spread
- To exchange an IBOR index for OIS, it is easier to attach the spread to the IBOR leg because of the compounding of the OIS rate fixings

Mathematical formulae:

The PV of a basis swap (from the point of view of the buyer / payer of the spread on leg $i=1$ or $i=2$ refer to different IBOR tenors or indexes):

*IBOR/IBOR basis swap:*

$$P = \sum_{i=1}^{T_1} N_i d_i (r_i^1 + Z) v_i + \sum_{j=1}^{T_2} N_j d_j r_j^2 v_j$$

*IBOR/OIS basis swap:*

$$P = \sum_{i=1}^{T_1} N_i d_i (r_i^1 + Z) v_i + \sum_{j=1}^{T_2} N_j v_j \left(\prod_{k=1}^{T_j} (1 + d_k \tilde{r}_k^2) - 1\right)$$

Where:

- $Z$ = spread (basis points added to one leg)
- $r_i^1$ = floating rate for leg 1
- $r_j^2$ = floating rate for leg 2
- $\tilde{r}_k^2$ = individual OIS rate fixings
- Other notation as per IRS formulae

As with IRSs and OISs to determine the mid-market price $Z^{\text{mid}}$, it simply requires manipulation of the formulae setting $P = 0$, so that for a standard IBOR/IBOR SBS with constant notional in every period):

$$Z^{\text{mid}} = \frac{\sum_{i=1}^{T_1} d_i r_i^1 v_i - \sum_{j=1}^{T_2} d_j r_j^2 v_j}{\sum_{i=1}^{T_1} d_i v_i}$$

Quoting convention:

'Currency, Index(es), Start-date, End-date, Float-frequency¹, Float-frequency², Roll-date, Stub-type'

#### Zero coupon swaps (ZCSs)

- Similar to IRS except payments are not made after each accrual period. Instead, payments due for each periiod, on each leg of the swap, are compounded up to be paid as a single cashflow at the maturity of the swap
- The fixed and floating leg both have a single cashflow, payable on the same day in the future for standard ZCSs

#### IRS futures

#### Non-MTM cross-currency swaps (XCSs)

#### MTM cross-currency swaps (XCSs)

#### FX Swaps

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
