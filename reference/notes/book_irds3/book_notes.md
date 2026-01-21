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
6. What are the drivers of IR markets at large?
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

$$DCF = \text{Day count fractions}$$

Interest payable:

$$\text{Interest payable} = notional \times DCF \times \text{interest rate per annum}$$

Actual 365 fixed (ACT/365F):

$$DCF_{ACT/365F} := \frac{\text{accrual end date} - \text{accrual start date}}{365}$$

#### Business day calendars and modified following

- Business day calendars (and to an extent holiday calendars) determine which dates are able to be used for payments, accruals, resets, etc.
- Following (F) and previous (P) determine what to do if an action date lands on a holiday.
- Modified ('M' preceding the date rules) denotes what to do if an adjustment goes on to the next month.

#### Per annum interest rates and annualized interest rates

The relationship between per annum rates and annualized rates:

$$\text{Annualized rate} = \left(1 + \frac{PAR}{f}\right)^f - 1$$

Where:

- $PAR$ = Per Annum rate
- $f$ = frequency (number of compounding periods per year)

#### Continuous compounding

The relationship between continuously compounded rates and simple rates:

$$e^{DCF \times \text{CC rate}} = 1 + DCF \times PAR$$

Where:

- $DCF$ = Day Count Fraction (time period in years)
- $\text{CC rate}$ = Continuously Compounded rate
- $PAR$ = Per Annum rate (simple rate)

Continuously compounded rates are useful in derivations for financial mathematics but have limited practical use

#### Time value of money and discount factors (DFs)

No arbitrage pricing (equivalent financial scenarios should have identical values and prices)

#### Interest rate indexes

- For various currencies, there are central bank rates and overnight indexes and risk free rates (i.e., in USD, the Federal Reserve dictates the discount rate and federal funds target rate, while the ). The former is central bank dependent and the latter is market dependent and transaction based.
- Overnight index swap (OIS) rates are calculated based off of data on executed unsecured lending transactions. The index is a notional weighed average, and published as a daily overnight level.
- IBOR vs. OIS Index differs where IBOR is an estimate of the future level while OIS is an observation of the past (both are unsecured). There is sometimes a lag between when a rate is fixed and the valuation period (i.e., 2 b.d. lag with EUR)
- Fallback method was required to continue to settle derivative contracts which settled against IBOR after the cessation, turning the rate from a look-forward rate (IBOR) into a look-back rate (RFR).

#### Derivation of CC rates formula

Continuously compounded interest rates are the result of taking the limit of more and more discrete interest payments over shorter and shorter time intervals, but all yielding the same total at maturity. Mathematically then,

$$\lim_{n \to \infty} \left(1 + DCF \times \frac{CC\ rate}{n}\right)^n = 1 + DCF \times per\ annum\ rate$$

Let,

$$L = \lim_{n \to \infty} \left(1 + DCF \times \frac{CC\ rate}{n}\right)^n$$

$$log(L) = \lim_{n \to \infty} n \log\left(1 + DCF \times \frac{CC\ rate}{n}\right)$$

$$\approx \lim_{n \to \infty} n \left(0 + DCF \times \frac{CC rate}{n} + O(\frac{1}{n^2})\right)$$

$$= DCF \times CC\ rate$$

Thus,

$$L = e^{DCF \times CC\ rate}$$

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

$$P = v_{i-1} \frac{N d_i (r_i - R)}{(1 + d_i r_i)}$$

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
- STIR futures are traded on exchanges, FRAs are off exchange.
- Size of single contract on STIR future is set to notional sizes according to exchange rules (0.5mm or 1mm), vs. FRAs which can have bespoke notionals.
- STIR futures are quoted in price terms, FRAs are quoted in yield terms.
- STIR futures start and settle on specific dates set by exchange, FRAs can be written for any business day.

- STIR futures settle only against 3M-IBOR tenors and only for value start dates that fall on International Monetary Market (IMM) dates.

##### STIR future pricing

The 3M-IBOR fixing rate implied by a STIR future is:

$$r_{i} = 100 - q_{i}$$

where $q_{i}$ is the price of the future. The PV of a single STIR future contract (from POV of the buyer) is:

$$P = N (q_{i} - Q_{i})$$

where $N$ is the value of one lot per unit increment, and $Q_{i}$ the originally traded price.

##### Settlement

Exchange delivery settlement price (EDSP):

$$EDSP = 100 - \text{3M-IBOR fixing}$$

#### STIR futures (RFR)

- Similar to STIR futures (IBOR), with the same properties to IMM dates, fixed notional, and pricing conventions.
- Fixings of RFR STIR within the period must occur before the EDSP can be produced (i.e., a March contract cannot be settled in March).

##### EDSP

EDSP one month rate:

$$EDSP\ one\ month\ rate = 100 \times \left(\frac{1}{d_1}\sum_{k=1}^{T_1}\left(r_k d_k\right)\right)$$

EDSP three month rate:

$$EDSP\ three\ month\ rate = 100 \times \left(\frac{1}{d_1}\prod_{k=1}^{T_1}\left(1 + r_k d_k\right) - 1\right)$$

Where:

- $T_1$ = the number of fixings that make up the period
- $d_1$ = the three month rate settles for a compounded rate, albeit both of these definitions describe the EDSP in terms of the exchange specifying the contracts and they may differ
- $r_k$ = RFR fixings
- $d_k$ = day count fraction for each published fixing

- Since the front month contract does not settle until all the RFR fixings are published, it continues to trade mid period.
- Reduces its volatility substantially midway through its periods since proportions of the EDSP is already known, and with each published fixing becomes less variable.
- RFR STIR futures experience convexity adjustments.

#### IRSs and OIS

##### IRS

- An agreement to exchange a series of fixed rate payments for a series of floating rate payments by an RFR index (previously an IBOR index). We treat OIS and IRS as semantically the same now as RFRs are overnight indices.
- The main component of an IRS is the date schedule, including payment dates, accrual periods, fixing dates for determination of floating rates, and notional amounts.

Example IRS

*Example cashflows of a standard 6M semi-quarterly IRS starting on 8th February 2016 and ending 8th August 2016. It details one fixed cashflow and two floating cash flows:*

| Notional | Accrual date | Accrual end date | Fixing date | Value date | Value end date | Payment date | Rate | Cashflow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100,000,000 | 2016-02-08 | 2016-08-08 | - | - | - | 2016-08-08 | 2.025% | 1,009,726 |
| 100,000,000 | 2016-02-08 | 2016-05-09 | 2016-02-04 | 2016-02-08 | 2016-05-09 | 2016-05-09 | 1.961% | -488,907 |
| 100,000,000 | 2016-05-09 | 2016-08-08 | 2016-05-05 | 2016-05-09 | 2016-08-09 | 2016-08-08 | 2.061% | -513,838 |

To obtain the PV, multiply the cashflows with appropriate DF relevant to the payment date. The floating payments are unknown until all of the relevant fixing publications have been made, so market movements will cause valuation changes.

*For a standard (or vanilla) IRS:*

- The same notional, $N$, for every individual period of the IRS either on the floating or fixed leg
- A consecutive structure so that each period comes immediately after another without overlapping or creating gaps
- An alignment between the fixed and floating legs (subject to the frequency) so that accrual periods and payment dates on each are the same
- An alignment of the fixing date and floating rate tenor to the given accrual schedule and payment schedule for the floating leg. Payments are made in arrears, that is, at the end of each period, usually on the accrual end date
- Standard day count conventions and fixed leg frequency in each specified currency

Customization:

Stub periods:

When start and end dates are specified without an associated relationship, it creates stub periods, placed in IRS either at the start, end, or both, so that the remaining part of the leg follows the specified frequency and reverts to the form of a standard IRS.

Mathematical formulae:

The present value of a **standard IRS**:

$$P = N \left(-R \sum_{i=1}^{T_1} d_i v_i + \sum_{j=1}^{T_2} d_j r_j v_j \right)$$

The present value of a **customized IRS**:

$$P = - R \sum_{i=1}^{T_1} N_i d_i v_i + \sum_{j=1}^{T_2} N_j d_j r_j v_j$$

Where:

- $T_1, T_2$ = number of periods in the fixed and float leg respectively
- $N$ = notional (for standard IRS), $N_i$ = notional per period (for customized IRS)
- $R$ = fixed rate
- $d_i$ = day count fraction for period $i$
- $v_i$ = discount factor to payment date $i$
- $r_j$ = floating rate for period $j$

In the case of OISs and other compounded RFRs the period floating rates, $r_j$, are determined from the individual published RFRs, $\tilde{r}_k$, for the period such that:

$$r_j = \frac{1}{d_j}\left(\prod_{k=1}^{T_j} (1 + d_k r_k) - 1\right), \quad T_j = \text{number of business days in period } j$$

*Example 3.4:*

Assume that last day RFR fixings make up a single OIS period and that on Thursday, Friday and Monday the fixings are published at 2.00%, 2.10% and 2.15%. Then the compounded rate over the period from Thursday to Tuesday, which represents three business days, is:

$$\left(\left[\prod_{k=1}^{T_j} (1 + d_k r_k)\right] - 1 \right) * \frac{1}{d_j} = \left(\left[\left(1 + \frac{1}{365}(0.02)\right) \left(1 + \frac{3}{365}(0.021)\right) \left(1 + \frac{1}{365}(0.0215)\right)\right] - 1\right) \times \frac{365}{5} = 2.0092\%$$

In this example Friday's OIS fixing has not been applied for the weekend days, so that the DCF becomes effectively longer. Very often in OISs, particularly for Christmas day and New Year's day and the periods immediately before and after the fixings can dominate the equation and become important considerations around holiday periods such as Easter and other religious holidays.

Mid-market pricing:

Pricing the mid-market rate for any IRSs of course relies on rearranging the equation to solve for $R^mid$ when the PV is zero. Given that one can use a curveset to forecast each $r_i, v_i, v_j$ we do just that below. Additionally, in the case of IRSs against RFRs, the discounting curve and the rates forecasting curve (often) depend upon the same forecast fixing rates so we may have a direct relationship between the two such that,

$$r_j = \left(\frac{v_{j-1}}{v_j} - 1\right) \frac{1}{d_j}$$

Thus in the case of a standard IRS (the day count fraction of the floating leg are consistent) we have:

$$R^{mid} = \frac{\sum_{j=1}^{T_2} d_j r_j v_j}{\sum_{i=1}^{T_1} d_i v_i} = \frac{\sum_{j=1}^{T_2} (v_{j-1}-v_j)}{\sum_{i=1}^{T_1} d_i v_i} = \frac{v_0 - v_{T_2}}{\sum_{i=1}^{T_1} d_i v_i}$$

where $v_0$ is the DF at the start of the IRS and $v_{T_2}$ is the DF at the end.

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
- Exchange a series of floating cashflows, almost exclusively of one index against another (i.e., 3M-IBOR cashflows for 6M-IBOR cashflows)
- a bp spread amount (or annuity) is attached to one of the legs to get NPV = 0 at inception (spread is the effective mid-market price), and is usually added to the index of the shortest tenor of either of either of the legs to result in a positive spread
- To exchange an IBOR index for OIS, it is easier to attach the spread to the IBOR leg because of the compounding of the OIS rate fixings

Mathematical formulae:

The PV of a basis swap (from the point of view of the buyer / payer of the spread on leg $i=1$ or $i=2$ refer to different IBOR tenors or indexes):

*IBOR/IBOR basis swap:*

$$P = - \sum_{i=1}^{T_1} N_i d_i (r_i^1 + Z) v_i + \sum_{j=1}^{T_2} N_j d_j r_j^2 v_j$$

*IBOR/OIS basis swap:*

$$P = - \sum_{i=1}^{T_1} N_i d_i (r_i^1 + Z) v_i + \sum_{j=1}^{T_2} N_j v_j \left(\prod_{k=1}^{T_j} (1 + d_k r_k^2) - 1\right)$$

Where:

- $Z$ = spread (basis points added to one leg)
- $r_i^1$ = floating rate for leg 1
- $r_j^2$ = floating rate for leg 2
- $r_k^2$ = individual OIS rate fixings
- Other notation as per IRS formulae

As with IRSs and OISs to determine the mid-market price $Z^{\text{mid}}$, it simply requires manipulation of the formulae setting $P = 0$, so that for a standard IBOR/IBOR SBS with constant notional in every period):

$$Z^{\text{mid}} = \frac{\sum_{i=1}^{T_1} d_i r_i^1 v_i - \sum_{j=1}^{T_2} d_j r_j^2 v_j}{\sum_{i=1}^{T_1} d_i v_i}$$

Quoting convention:

'Currency, Index(es), Start-date, End-date, Float-frequency¹, Float-frequency², Roll-date, Stub-type'

#### Zero coupon swaps (ZCSs)

- Similar to IRS except payments are not made after each accrual period. Instead, payments due for each period, on each leg of the swap, are compounded up to be paid as a single cashflow at the maturity of the swap
- The fixed and floating leg both have a single cashflow, payable on the same day in the future for standard ZCSs (this results in only one net payment regardless of maturity or tenor)
- Can be easily quoted in actual fixed amount of cash or in rate terms as an IRR
- The floating leg is uniquely defined. A ZCS compounds all of the relevant index fixings to make a single payment at maturity

Mathematical formulae:

The PV of a ZCS (from the point of the view of the payer) is, firstly with the fixed leg specified as an interest cashflow on top of notional and secondly in IRR terms:

$$P = -(N + C)v_{T_1} + Nv_{T_1} \prod_{i=1}^{T_1} (1 + d_{i}r_i) \quad \text{(RFR or IBOR)}$$

$$P = -Nv_{T_1} \left(1 + \frac{R^{\text{IRR}}}{f}\right)^{f(D_{T_1}-D_0)} + Nv_{T_1} \prod_{i=1}^{T_1} (1 + d_{i}r_i) \quad \text{(RFR or IBOR)}$$

Quoting convention:

'Currency, Index(es), Start-date, End-date, IRR-frequency¹, Float-frequency², Roll-date, Stub-type'

*Example 3.5:*

A trader has received a 20Y ZCS at a semi-annual IRR of 2.40% on a notional of €100mm. He calculates the single, fixed interest cashflow payable after 20Y as:

$$C = €100\text{mm} \times \left[\left(1 + \frac{2.40\%}{2}\right)^{2(20-0)} - 1\right] = €61,146,360$$

The next 5Y worth of RFR fixings are forecast to be 2.10% and any subsequent fixing is forecast to be 2.15%. The floating leg's forecast interest cashflow, payable in 20Y is calculated (ignoring business day calendars) as:

$$C = -€100\text{mm} \times \left[\left(1 + \frac{2.10\%}{360}\right)^{1527} \left(1 + \frac{2.15\%}{360}\right)^{5479} - 1\right] = -€54,307,963$$

The DF for the payment date, $v_{20} = 0.6690$, and thus the PV of the ZCS is:

$$P = 0.6690 \times (61,146,360 - 54,307,963) = €4,574,888$$

The current mid-market IRR can also be determined from the floating leg's forecast interest cashflow. If we assume the fixed leg has the equal and opposite semi-annual cashflow then the semi-annual IRR that will return this cashflow is 2.1807%. This has an effective day count convention of act/act ICMA, whilst the ESTR leg has act/360 are not directly comparable.

#### IRS futures

- Similar to STIR futures in that they trade on exchanges in price terms, with margining principles applied, and a single contract is a predetermined notional (typically 0.1mm) set by the exchange
- Standard IMM only settlement days (frequently March, June, September, December), physically settled (parties with open positions at expiry will enter into a OTC IRS)
- In order to complete the action of settlement at expiry, counterparties either pay or receive an amount of cash to the clearing house dependent upon the EDSP of the contract (final trading price of the contract before expiry)
- IRS futures are not particularly liquid or well traded

Mathematical formulae:

Where a party has bought an IRS future that translates to the duration of receiving fixed on the physically settled IRS. The amount of cash payable to the exchange on settlement of a single contract corresponds to:

$$P = \frac{EDSP - 100}{100} \times {N}$$

Where $N$ is a single contract notional.

Similarly the live price of an IRS future is determined by the market PV of the contract specified IRS (from the point of view of the receiver).

$$q = 100 + 100 \times \frac{P}{N}$$

*Example 3.6:*

A trader buys 10 {USD 0.1mm Z16 10Y SOFR IRS 1.5%} IRS futures contracts at a price of 100.00.

The market values and yields fall by 15bps from 1.5% to 1.35% so that the PV of the IRS represented by a single contract is now $1,386. The price of the IRS future is then 101.38 (or quoted in 32nds: 101-12+). To reflect the profit in a simple expression, MTM the exchange credits trader's account with 10 × $1,386 = $13,860. The future expires with an EDSP of the same price and the trader's open position is physically settled. He pays $13,860 to the exchange and enters an IRS for $1mm notional with the clearing house which necessarily possesses a PV of $13,860. The clearing house posts this amount to the trader as collateral.

#### Non-MTM cross-currency swaps (XCSs)

- A non-MTM cross-currency swap (XCS) is a swap similar to single currency basis swaps, except instead of swapping different tenor indices or different indexes in the same currency, the counterparties exchange indexes (usually RFRs) in two different currencies
- To balance the legs so that, at mid-market (at inception), the sum of each is zero, requires a fixed spread (or annuity) to be attached to one of the floating legs (usually the non-USD or least liquid currency). In these examples, the spread is applied to the first currency in a currency pair (i.e., EUR in EUR/USD)
- XCSs involve notional exchange at the start and end of the swap in the two currencies, which in the case of non-MTM XCSs will always be the same value, which is based on an initially agreed FX rate (usually the spot FX at the time of execution)

Mathematical formulae:

The PV of, for example, a EUR/USD non-MTM XCS from the POV of the payer of the spread (B in figure 3.4) is:

$$PV = N F_0 w_0^\ast - NF_0 \sum_{i=1}^{T_1} (r_i^\ast + Z^\ast) d_i^\ast w_i^\ast - N F_0 w_{T_1}^\ast - N f_0 v_0 + N f_0 \sum_{j=1}^{T_2} r_j d_j v_j + N f_0 v_{T_2}$$

where $v_i$ represents the discount factor of a USD cashflow and $w_i^\ast$ the discount factor of the EUR cashflow. $f_0$ represents the FX rate which was fixed at the time of execution and $F_0$ represents the current spot FX rate. $N$ is the notional of the domestic currency where the bp spread is attached, so in this case is in EUR. It is also usual (although not necessary) to assume that $f_0 = F_0$ when pricing a new trade. The rates $r_i^\ast, r_j$ are determined according to equation 3.1 when RFRs are the leg indexes.

Customization:

- The above describes one of the more common floating-floating swaps, but these are also completely bespoke and can be customized (date schedule. fixing schedule, day count conventions), similar to an IRS
- It is also possible and common to have one or two fixed legs, where in the formula, $r_i^\ast$ and $r_j$ are replaced by $R^\ast$ and $R$, creating a swap where counterparties exchange a fixed series of payments in one currency for a floating series of payments in another
- Notionals can be varied each period and variable across each leg (ie..e, amortization in case of swaps hedging loans)

Quoting convention:

'Currencies, Index(es), Start-date, End-date, Frequency<sup>1</sup>, Frequency<sup>2</sup>, Fixed/Floating<sup>1</sup>, Fixed/Floating<sup>2</sup>, Roll-date, Stub-type, MTM or non-MTM'

#### MTM cross-currency swaps (XCSs)

- Most common form of XCS. It is the standard XCS product traded in the interbank market. It's purpose and difference to non-MTM XCSs is to reduce credit exposure (CE) to counterparties by continually 'resetting' the notional on one leg throughout the length of the swap, in light of fluctuating exchange rates. This mitigates the overall PV of the derivative by restricting the impact of FX fluctuations
- In non-MTM XCSs, FX fluctuations can have a far greater impact on the PV of those derivatives than the actual underlying XCS market prices, and hence the affinity toward MTM XCSs

Mathematical formulae:

The PV of, for example, a EUR/USD MTM XCS from the POV of the payer of the spread is:

$$PV = N F_0 w_0^\ast - NF_0 \sum_{i=1}^{T_1} (r_i^\ast + Z^\ast) d_i^\ast w_i^\ast - N F_0 w_{T_1}^\ast - N f_0 v_0 + N \sum_{j=1}^{T_2} f_{j-1} r_j d_j v_j + N \sum_{j=1}^{T_2} (f_{j-1} - f_j) v_j + N f_{T_2} v_{T_2}$$

It is common that one might seek to determine a mid-market spread, $Z^{*mid}$, for a XCS. To do this, the forecast rates and DFs in each currency need to be obtained from a multi-currency curveset. The PV can then be set to zero and the formula rearranged in terms of $Z^{*mid}$. The same type of customizations are available as for non-MTM XCSs as are the quoting conventions.

#### FX Swaps

- FX swaps (or currency swaps) are agreements to complete two, offsetting FX exchanges: one exchange on a particular date and a re-exchange at a future date for an agreed price difference
- I.e., one CP may agree to sell EUR100mm for USD at a spot at an exchange rate of 1.2500 and then after one month, purchase EUR100mm from USD at an exchange rate of 1.2480

Mathematical formulae:

Supposed the example from above: *buying the 1M €100mm EURUSD FX Swap at -20 points, i.e., EURUSD rates of 1.2500 and then 1.2480*. This equates to the following simple cashflows defined by the notional, initial FX rate and swap price:

| Date | USD | EUR |
| --- | --- | --- |
| 1st Jan 2022 | +$125mm | -€100mm |
| 1st Feb 2022 | -$124.8mm | +€100mm |

FX swaps are economically equivalent to single-period, fixed-fixed XCSs where the fixed rate on one currency is set to 0%, and the other currency is determined by a specified rate defined by the swap price.

Quoting convention:

Currency pair, start date, tenor, notional, swap points (the price), and an agreed initial FX rate

#### Swaptions

Swaptions are not classified as linear IRD products. Chapter 20 exclusively outlines these products and their pricing formulae.

### Chapter 4 - Users of IRDs

#### Household sector and general banking

- Households and general banking customers want to purchase items on credit (mortgages, credit cards, vehicles), and in doing so, they would like to pay fixed interest rates. Banks facilitate this spending by providing credit, however, they are payers of floating rates. This forms an implicit IRS where banks are receiving fixed interest payments (households pay fixed). To hedge this, banks must pay fixed on IRS to offset their exposure (they naturally pay floating)
- For current deposits, banks profit from the difference between the central bank deposit rate and the rate paid for deposits (marginal rate). A bank can hedge the marginal rate by receiving fixed on an IRS
- Pensions have an annuity obligation when members retire. To fulfil this, pension funds invest cash, exchanged for the annuity, into equities or other securities. If future expectations of interest rates fall then the implicit amount of growth assumed over many years may be insufficient to pay the annuity. Thus, a pension fund may choose to hedge long dated interest rates by receiving fixed on IRSs

#### Central governments

- The treasury and debt management office (DMO) are responsible for public finances. As the DMO raises funds through taxes and sovereign issuance, the latter of which represents a supply of fixed rates, they may want to rate lock their funding by either receiving fixed on an IRS if they believe rates will fall, or paying fixed if they believe rates will rise
- Hedging bonds with IRSs is not a one-for-one hedge, which is known as an asset swap. Asset swaps come with a type of basis risk called asset swap spread risk (not dissimilar to single currency basis risk between two indexes), which is the risk that IRS rates will move more or less than the yields on the bonds to the same respective maturity that they are hedging
- A treasury does not necessarily have to raise money in the domestic currency (can issue in USD), widening its pool of potential investors. In this case, the DMO will want to hedge all market risk exposures so that its overall exposure is to its domestic currency only (usually through a fixed/fixed XCS)

#### Central banks

- Central banks preside over their own domestic currency, and as a defensive measure, they build up foreign reserves. This is done by buying foreign currency with domestic currency, which when done with enough nominal size, will depreciate the domestic currency. This is usually supportive of inflation for two reasons: import prices rise, and the economy can be stimulated by foreign investment increasing growth and wages
- In order to facilitate a functional financial system, any domestic central bank is expected to provide liquidity to its domestic banks through some standing facilities (and given the globalized nature of modern finance, domestic banks often need to access to liquidity in foreign currencies). Central banks must have this foreign reserve available, but as they are not keen to offer this from their variable foreign exchange reserves, central banks have created swap lines between themselves to exchange each other's domestic currency. Swap lines represent XCSs, so by utilizing these derivatives, a central bank gains access to a foreign currency but does not change the FX exposure of their foreign exchanges reserves account (neither central bank is exposed to the movement of FX rates via the transaction)
- A central bank with the right amount of FX exposure invested in government bonds of a foreign currency may believe interest rates in that foreign currency to rise, and rather to sell the FX reserves, it may be better to hedge this change in rates using IRSs

#### Non-financial corporations (NFCs)

- Although NFCs can have a multitude of reasons to access financial markets (surplus cash management, revenue smoothing, hedging, tax optimization strategies), their primary action in the IR market is to issue debt. Sovereign debt is usually easier and cheaper to issue compared to NFC debt (greater credit quality, size of market and liquidity)
- NFCs are concerned with and sensitive to a number of factors when it comes to debt issuance: credit spreads, liquidity, and international IRD rates and international credit spreads
- The credit spread is the difference between YTM of the credit bond and some conventional benchmark reference rate. For most countries (US, UK, Canada), common convention is to measure the credit spread relative to government bonds. In the EU area, the convention is to benchmark relative to IRSs because of the complication of multiple countries' sovereign bonds having quite different overall yield levels. The goal is to issue with as tight or low a credit spread as possible, both relative to peers (relative credit spread) as well as the general level of spreads taken across all domestic NFCs (domestic credit spread)
- To expand on liquidity, an NFC would generally like to issue in reasonable size to promote secondary market activity. Past performance of successful and oversubscribed issuances carry psychological benefits, creating positive momentum and allowing for higher pricing (tighter spreads)
- NFCs must pay attention to international IRD rates and international credit spreads. It may be cheaper to issue in foreign currencies based off of supply and demand factors of XCSs markets

*Example 4.1:*
Suppose Alpha Corp., a EUR domesticated NFC, is considering issuing a bond. It considers either domestic issuance or foreign issuance, in USD, swapped back to EUR. If Alpha swaps the issuance it will execute IRDs. The IRDs have three purposes: switch the USDhat investors pay for the bonds to EURor Alpha, allow Alpha to pay fixed EUR interest, while the investors receive USD interest cashflows, and as maturity permit Alpha to pay back the original USD sum whilst the investors receive the original USD sum, all without exposing any party to the FX risk.

Figure 4.1 demonstrates netted legs from the POV of Alpha Corp. if it pursues foreign issuance. The rightmost legs of the figure do not net and reflect outstanding commitments; a fixed EUR interest outflow and EUR notional exchanges, as required. The final notional exchange and repayment of principal to investors is not shown - it is the opposite of all initial changes.

*Figure 4.1: Netted Cash Flows for Alpha Corp. Foreign Issuance:*

```text
┌──────────────────────────────────────────────────────────────────────┐
│                  Three IRD Products Netted Together:                 │
│                                                                      │
│   EUR IRS          USD IRS            Non-MTM EUR/USD XCS            │
│  ┌───────┐       ┌─────────┐            ┌──────────┐                 │
│  │  Pay  │       │ Receive │            │          │                 │
│  │ Fixed │       │  Fixed  │            │          │                 │
│  │  EUR  │       │   USD   │            │          │                 │
│  └───┬───┘       └────┬────┘            └─────┬────┘                 │
│      │                │                       │                      │
│      │ ┌──────────────▼───────────────┐       │                      │
│      │ │    USD Bond Issue            │       │                      │
│      │ │  (Receive Fixed USD from     │       │                      │
│      │ │   investors + USD credit spl)│       │                      │
│      │ └──────────────┬───────────────┘       │                      │
│      │                │                       │                      │
│      │                │ ┌─────────────────────▼────┐                 │
│      │                └─│  Pay Floating USD        │                 │
│      │                  │  to USD IRS              │                 │
│      │                  └──────────┬───────────────┘                 │
│      │                             │                                 │
│      │                    ┌────────▼──────────┐                      │
│      │                    │ Receive Floating  │                      │
│      │                    │ USD from XCS      │                      │
│      │                    └────────┬──────────┘                      │
│      │                             │ (Nets to zero)                  │
│      │                             │                                 │
│      │                    ┌────────▼──────────┐                      │
│      └────────────────────│ Receive Floating  │                      │
│                           │ EUR from EUR IRS  │                      │
│                           └────────┬──────────┘                      │
│                                    │                                 │
│                           ┌────────▼──────────┐                      │
│                           │ Pay Fixed EUR to  │  ← Outstanding       │
│                           │ XCS (EUR IRS rate)│     commitment       │
│                           └───────────────────┘                      │
│                                                                      │
│  Net Result = EUR IRS rate + USD credit spread + EUR/USD XCS spread  │
│                                                                      │
│  Outstanding Commitments (Right-most legs that don't net):           │
│  • Pay fixed EUR interest                                            │
│  • EUR notional exchanges                                            │
└──────────────────────────────────────────────────────────────────────┘
```

If Alpha chooses to issue domestically then it pays a fixed rate equal to EUR IRS rate (RFR benchmark) + EUR credit spread (say 1% and +40bps for a total of 1.40%). For foreign issuance the figure demonstrates the net payment is equal to EUR IRS rate (RFR) + USD credit spread + EUR/USD XCS spread (non-MTM). Supposing the two spreads were +50bps and -30bps resp., then the overall fixed rate for comparison is 1.2%, so it is advantageous for Alpha to consider swapped foreign issuance.

- It is common for a bank to facilitate this service to NFCs by providing a single non-MTM fixed/fixed XCS that replaces the three individual IRSs. Upon hedging, the bank will usually expose itself to cross-gamma risks due to different terms of the CSAs of the interbank trade hedges, and due to the build up on non-MTM XCSs hedged with interbank MTM XCSs (further explored in chapter 21)
- NFCs do not always desire to have fixed rate exposure on their bonds, however investors generally prefer fixed rate bonds. If the issuer were to issue fixed rate but choose to receive fixed on an IRS, then this would convert the issue to floating rate (only from the issuers POV). In figure 4.1, for the foreign issuance, this could be achieved by omitting to pay fixed on the EUR IRS

##### Issuance swaps

A domestic issuer chooses to 'swap to floating' its issuance by receiving fixed on an IRS. The issuer does not execute a benchmark interbank IRS to hedge its market risk exposure, instead, it executes an IRS that precisely matches the dates and specific cashflows of its bond (done to classify its issuance and derivative under the IFRS 9 cashflow hedge accounting designation). Since the transactions are large, with the IRS notional being the same as the issue size, there is often the requirement for a third party validation of the pricing given by a market-maker (screen references). The screen reference uses interbank brokers' electronically published prices to validate the mid-market of benchmark swaps. Since these benchmark swaps do not precisely match the issuer's customized IRS, there are also adjustments that need to be agreed.

*Example 4.2:*

Alpha Corp decides to issue domestically. It chooses to issue a new 7Y fixed rate bond, with settlement T+5 b.d.s, and swap it to floating RFR. With everything complete, Alpha Corp. will have issued bonds priced at some yield to maturity and received fixed on an IRS with the same fixed rate and conventions as the bond cashflows to pay RFR plus a bp spread. We outline the process of calculation of that spread.

The bond is typically priced by specifying its YTM as the forward adjusted, mid-market 7Y RFR IRS rate + a credit spread. Say the standard 7Y RFR IRS from some official screen source is 0.995%. The fact that the bond settles T+5 means that the dates on the swap are customized. The standard 7Y RFR IRS has a fixed rate 0.5bps lower than the equivalent IRS starting T+5 (called the forward adjustment). Thus the referenced mid-market rate for the purpose of pricing the bond is equal to the screen price plus the forward adjustment (0.5bps), making 1.00%. Adding the credit spread (40bps agreed between investors, issuer, syndicate banks), this makes the issuance priced at a YTM of 1.40%.

| Description | Value |
| --- | --- |
| Screen reference T+1 and swap | 0.995% |
| T+5 forward adjustment | 0.005% |
| Bond credit spread | 0.400% |
| Priced yield to maturity | 1.400% |

If the coupon on the bond were matched at 1.400%, the bond would price at par. If Alpha Corp. received 1.400% on the IRS with standard conventions, the RFR floating rate spread would match the credit spread at 40bps. However, there are three adjustments which might exists which can result in that spread that the issuer pays differing from 40bps;

1. Convention adjustments: if the fixed leg and floating leg have different conventions (i.e., day count conventions or different frequencies), the same bp spread on one leg is not equivalent to the same spread on the other
2. Coupon adjustment: if the coupon on the bond is not set to be the same as the priced YTM, the bond price is not exactly par. Usually the coupon is set to be lower than the YTM (bond prices at discount). The issuer typically wants to receive par however, so an economic upfront payment value known as the make to par is embedded into the swap. The lower coupon rate applied to the fixed rate of the swap offsets this in part but the economics are not exact
3. Market-maker's margin: this is a fee for facilitating the transaction embedded into the issuer swap

The coupon is set at 1.375% and the issuer receives a T+5 7Y RFR fixed at 1.375% with conventions, Annual ACT/ACT ICMA, and pays floating rate plus 38.1bps, which equates to 37.5bps standard spread plus 0.3bps convention adjustment minus 0.2bps make to par coupon adjustment plus a market maker fee of 0.5bps. The swap includes an upfront make to par payment.

#### Asset managers

- Wealth management funds and pension fund providers need to hold physical products/securities as investments of their capital. They will utilize IRDs to hedge or get IR exposure correlated with other assets, diversifying their portfolios
- One way asset managers will utilize IRDs is to gain specific exposure to credit risk (i.e., buying a corporate bond and paying fixed on an IRS, so that any PnL generated is coming from the credit spread of the bond). This, however, introduces asset swap spread risk. Another way the asset manager can hedge IR delta risk is to sell a benchmark government bond, allowing the manager to capture just credit spread risk

Asset managers may choose to hedge by paying IRSs for the following reasons:

1. Short selling government bonds means that they must be sourced using repo transactions (an overhead operationally and at times can become expensive if those bonds go 'special'). This type of transaction is subject to rollover risk, where short tenor repos prove difficult to repeat for an extended period of time
2. Underlying credit bond might be benchmarked against IRSs rather than government bonds. In Euro area this is particularly common. Tom compare corporations in the Euro area, benchmarking tends to be done against a common ESTR index
3. The asset manager might be comfortable to won the swap spread risk, particularly if initiated at historically favorable levels

For this type of bond hedging, there are three specific types of IRS that are often chosen:

1. Matched maturity or yield-yield asset swap: two names for the same IRS. It is a swap with the same maturity as the maturity of the bond. It has a front stub on both fixed and floating legs until the next bond coupon payment, and the rate will be the same as the mid-market rate as with any other IRS. The notional on the swap is chosen to match the IR delta on the bond, so it is often not the same as the bond notional. The conventions of a yield-yield swap are typical of standard IRSs of the given currency
2. Par-par asset swap: more complicated than the above. An investor pays a price of par (i.e., 100) for the bond (either including accrued interest or, less commonly, excluding it by choice) and pays the fixed leg on an IRS with notional and convention to match the bond coupon cashflows. The floating leg has a short front stub with maturity mimicking the bond's, and the same notional as the fixed leg (and therefore also the bond). A bp spread is applied to the floating leg to equate the economics
3. Net proceeds swap: probably the most complicated swap to execute against a bond. In this case, the investor pays the dirty price (i.e., the clean price plus accrued interest) of the bond. The fixed leg of the IRS is the same as with the par-par swap, whereby the bond's cashflows are replicated. But, the floating leg is different in one respect - the notional is set to be reflective of the dirty price $\left(\frac{\text{dirty price}}{100} \times \text{fixed notional}\right)$, with a bp spread applicable to the floating RFR component to equate the economics

Why are three forms of asset swap used? The first is the easiest measure, for calculation and tracking. The second and third provide measures designed to see the actual floating interest rate payments received relative to RFR, albeit on marginally different terms, and can be representative of accounting structures. It is an example of subjectivity of trade construction and risk management. Note as the notionals are different, the delta risks of the IRSs are also different. The different volatilities of the bond assets relative to associated swaps will result in one type providing the best delta hedge, however which will differ in different market conditions.

*Example 4.3:*

Two different investors of Alpha Corp.'s domestic issuance choose to purchase the bond on asset swap in €50mm each. At pricing, Alpha Corp.'s bond was in fact issued with a 1.375% coupon against a yield to maturity struck at 1.4%. This means that the new bond priced at €99.85, instead of par.

The first investor enters a yield-yield asset swap. He pays fixed at 1.000% and receives RFR floating leg. The yield-yield asset swap spread is defined as 40bps. The only adjustment factored here relative to the benchmark mid-market 7Y is the forward adjustment (+0.5bps on fixed leg). The notional on the IRS is €49.6mm to give analytic delta neutrality.

The second investor enters a par-par asset swap. The investor pays a fixed leg of 1.375% replicating the bond cashflows and receives RFR + 37.6bps. The adjustments that have been factored into the RFR leg are the standard spread (+37.5bps), convention adjustment (+0.3bps), and make to par coupon adjustment (+0.2bps). The notional on this IRS is €50mm and the analytic delta is not neutral.

Since no market-making fee was added in either case each swap has a MTM value of zero at inception. Even though their terms are different, their initial values are identical.

#### Hedge funds and speculators

- Hedge funds and speculators use derivatives to create leverage. With relatively small amounts of invested capital, they are able to participate in relatively large returns and exposure (if markets move the right way)
- One particular type of speculator, called a commodity trading account (CTA), trades exclusively on exchanges. STIR futures are an example of a product they would treat as a 'commodity' and engage in buying and selling its contracts, possibly as part of larger strategies involving non-IR products. As swap futures become more liquid in exchanges, it is likely that the CTAs will also expand, applying their algorithmic trading strategies to these products too

#### Banks

- Banks have the most use of IRDs. Not only are they facilitating most of the activities of the parties above, they also have their own risks to manage. Not only do they partake in debt raising (similar to the parties above), as a cross-asset, market making bank, they will accrue multiple IR risks from countless areas and activities, some straightforward while others complex.

### Chapter 5 - Cash, Collateral, and Credit

- What is a cash balance and why is it important in the context of an IRD portfolio
- How accounting principles work to record trading profits and not cash balance interest profits
- What collateral is and how the terms are legally set out in CSAs
- How and why CSAs must be considered in the accurate pricing of IRDs and the concept of the CTD collateral
- Why the counterparty of a trade is an important consideration
- In what ways the credit risk of a counterparty can be expressed
- What credit valuation adjustments (CVAs) and funding valuation adjustments (FVAs) are

#### Cash balances

**Introduction:**

Cash balances form an important part of any derivatives portfolio. Consider the following example:

*Example 5.1:*

1. A trader creates an empty IRDs portfolio
2. Executes a single trade paying fixed on $100mm 1Y semi-semi IRS at the mid-market rate of 1.0% (records PV of the trade as zero)
3. The compounded RFR fixings during the 6M period yield 1.1% exactly as initially forecast (at the 6M point, the trader receives a net cashflow of $50,000)
4. The compounded RFR fixings during the second 6M period yield 0.8996%, exactly as initially forecast (at the 1Y point, the trader pays a net cashflow of $50,200)

At first, it looks like the trader has lost $200, which violates our claim, however, with time value of money, the trader has kept his NPV of 0 as the interest received (0.8%) on the cash balance of $50,000 received at the 6M point equals the difference between the two net cash payments (6M and 1Y).

Derivatives are always priced assuming cash can be funded or invested at a specific rate of interest. This is the rate that determines the DF for any given day. For an IRD valued at zero, to actually recognize no gain or loss at its ultimate maturity, two events must occur;

1. The original forecast floating rates must publish as predicted
2. The DFs used for the initial pricing must be attained when funding or investing real cash balances

Here the example interest rate of 0.8% on the cash balance is not equal to the RFR period rate published at 0.8996%. This is a very important distinction. For cleared and regularly collateralized derivatives, these will be the same rates, but in this specific contract's case, 0.8% reflects the physically attainable rate of interest on the cash balance over the term, for example, there is a non-standard remuneration agreement on collateral here, which we will come on to.

##### Cash balance profiles

A cash balance profile details the expected cash balance of a portfolio at differing future dates. It is measured by aggregating all cashflows on a given day including accumulated interest amounts from previous days' balance. In the previous example, the cash balance at the 9M point would be $50,100 after the accrual of some interest each day after the initial receipt of $50,000.

For simple, mid-market IRDs, the expected cash balance profile is often easy to qualitatively describe. Firstly, for any derivative which has only a single cashflow date, there will never be any expectation of any cash balance (mid-market FRAs, ZCSs, single period IRSs/OISs). Thi is because any floating or fixed cashflows paid or received will be priced to net to zero, and therefore no net cashflows will ever be forecast to be exchanged. The trades still have risk, of course, and net cashflows will arise as market movements give rise to MTM PnL, we are just stating the expected nature of a zero cash balance profile for certain trade types executed at mid-market.

Secondly, where derivatives have multiple cashflows, there is generally a particular structure to the IR curve that allows a qualitative assessment (flat, upward sloping, downward sloping, bowing). Any derivative whose initial PV is zero will always have an expected final cash balance of zero. This is because a derivative with zero PV cannot be expected to gain or lose an amount of cash after its maturity. The interim, forecast, cash balance, however can feasibly have any pattern. These depend on the structure of all of the interim cashflows that take place. Cash balances are central to considering future discounting risk and the impact to PnL if discounting basis changes or the terms of a CSA is restructured.

##### Daily PnL accounting

- IRDs are unlike securities in the sense that on inception, you do not expect them to yield any return (vs. a bond that yields 2% per annum for example). In fact, if you receive a mid-market 1Y IRS @ 2%, based on the expectation of future forecast floating rates, you expect that the IRS will mature with zero PnL
- Derivatives are risk management and speculative, leveraged instruments. Trading these result in PnL only when market rates deviate from forecasts, so it is important to take into consideration cash balances for accounting purposes. Take for example a derivatives portfolio with a very positive cash balance (perhaps from previously successful trades), that has no open trades or the ability to enter into any more derivatives. This presents a conflict of interest as the portfolio will naturally increase via accrued interest on its cash balance, however, a derivative portfolio should only report derivative trading PnL (not interest accrued on previous profits)

One should be aware that the cash balance of a derivative portfolio is necessarily made up of these two components, expressly;

1. The PV of future cashflows, where the cash balance either funds or recoups, negative or positive cashflows respectively
2. PnL, where a positive or negative cash balance has been generated as the result of successful or unsuccessful trading, respectively

Good accounting practice isolates the PnL component of any cash balance so that it cannot accrue any further interest gains or losses that would be misrepresented as derivative trading PnL (the definition of PnL here is MTM PnL, which is the sum of realized plus any unrealized PnL). The following is designed for monitoring of a derivatives portfolio on a daily basis, only.

*Example 5.2:*

We outline a sample balance sheet and profit and loss statement of a derivatives portfolio.

| Balance Sheet (000's) | Day 1 | Day 2 | Day 3 |
| --- | --- | --- | --- |
| *Previous closing values* <br> [A1=previous(E1)] PV of previous derivative contracts <br> [A2=-A1=previous(E4)] Total cash balance*|  <br> 80,000 <br> -80,000 | <br> 75,711 <br> -75,711 | <br> 76,635 <br> -76,635 |
| *Day's schedule cashflow exchange* <br> [B1= $\alpha$ A2] O/N interest on previous cash balance* <br> [B2] Net previous derivative contracts' cashflows* <br> [B3=-B2] PV change of previous derivative contracts| <br> -2 <br> 5,000 <br> -5,000 | <br> -2 <br> -1,000 <br> 1,000 | <br> -2 <br> 7,000 <br> -7,000 |
| *Previous derivative contracts' valuation changes* <br> [C1 $\approx$ -B1] O/N carry from previous close to open<sup>2</sup> <br> [C2] PV due to market movements from open to close | <br> -2 <br> 965 | <br> -2 <br> -110 | <br> -2 <br> 30 |
| *New trading activity* <br> [D1] PV of derivative contracts acquired/disposed <br> [D2] Day's cash payments due to [D1]* <br> [D3] Other imposed cost-of-carry<sup>3</sup> | <br> -256 <br> 354 <br> 0 | <br> 33 <br> -10 <br> 0 | <br> 612 <br> -432 <br> 0 |
| *Closing values* <br> [E1=A1+B3+C1+C2+D1] PV of all derivative contracts <br> [E2=A2+B1+B2+D2] Intermediate cash balance* <br> [E3=-(E1+E2)+D3] Balancing PnL cash transfer* (Dividend) <br> [E4=E2+E3] Total cash balance carried forward* | <br> 75,711 <br> -74,648 <br> -1,063 <br> -75,711 | <br> 76,636 <br> -76,723 <br> 87 <br> -76,636 | <br> 70,279 <br> -70,069 <br> -210 <br> -70,279 |
| | | | |

| Profit and Loss Statement (000's) | Day 1 | Day 2 | Day 3 |
| --- | --- | --- | --- |
| *PnL Itemized* <br> [F1=B1+C1] Funding inconsistencies (interest vs. carry) <br> [F2=C2] Market movements from open to close <br> [F3=D1+D2+D3] New daily activity | <br> 0 <br> 965 <br> 98 | <br> 0 <br> -110 <br> 23 | <br> 0 <br> 30 <br> 180 |
| *Total* <br> [G1=F1+F2+F3=-E3] Recorded PnL | 1,063 | -87 | 210 |

The *day's schedule cashflow exchange* lists payments and receipts that are written into the derivative contracts and already known on the previous day (if cash is exchanged, the value of derivatives must move in the opposite direction). The *previous derivative contracts' valuation changes* determines the change in the value measured between the previous close and today's close, subdivided into previous close to today's open and today's open to today's close. How the open curves are produced differs across institutions (if open curves are produced as in chapter 6, then the overnight carry value is synonymous with interest and reflects the fact that each future cashflow is one day closer to realization and therefore, each future cashflow is valued with a slightly different DF). *New trading activity* captures all entering and terminating trades on a given day, and *closing values* are determined as the sums of the items above.

Transfer of PnL is an effective dividend to a governing entity, an isolation step that ensures any PnL made do not generate interest directly for the derivatives portfolio. Profits paid as cash sums to the governing entity can generate interest instead for the governing entity.

#### Collateral

**Introduction:**

Collateral is an obligation (cash or other financial asset) attached to some derivative contracts, with the purpose of mitigating one party against loss in the event of a default by the counterparty (acts as protection or insurance).

*Example 5.3:*

Day 1: Alpha reports a PnL of $710,000 due to the following two trades
Alpha pays $100mm 5y IRS @ 2.0% to Bravo collateralized with USD cash
Alpha receives $100mm 5y IRS @ 2.15% from Delta, uncollateralized

Day 2: Global event moves rates 100bps lower
Alpha records the IRS with Delta as an asset worth $5.51mm
Alpha records the IRS with Bravo as a liability worth $4.8mm

Although accounting wise, Alpha still records the same profit, it cannot source funds to post $4.8mm collateral to Bravo, because the asset with Delta is specifically uncollateralized (Alpha defaults, which could lead to bankruptcy and subsequent problems for Bravo). This simplified example illustrates how a destructive chain of events can start through the default of obligations. Since 2007, regulators and governments have imposed much stricter controls in the hope of limiting such catastrophes (clearing, capital reserves, stress tests), especially for banks.

##### Credit support annexes (CSAs)

A CSA is a legal document which regulates collateral posting for a derivative transactions (one of four parts that make up an ISDA master agreement, but is not mandatory). It is possible to have an ISDA agreement without a CSA but normally not a CSA without an ISDA agreement. The terms of a CSA normally include:

1. Type of collateral: cash, bonds (government or corporate), strips, bills, stocks, etc.
2. Currency of collateral
3. Country of collateral (if applicable)
4. Thresholds: the asset value above that whereby parties exchange collateral
5. Frequency of exchange: daily, weekly, monthly revaluations, etc.
6. Bilateral or unilateral: whether only one party is required to post collateral
7. Remuneration: the rates of interest paid for cash collateral
8. Haircuts: the additional collateral required above the asset value when posting value-at-risk securities such as bonds and stocks
9. Other clauses: such as permissibility of the posting counterparty to switch collateral type or post multiple types of collateral, or the permissibility of the receiving counterparty to re-use, or rehypothecate, the collateral to satisfy their own collateral obligations on other trades

##### Pricing derivatives with different CSAs

If all derivative contracts with the same headline parameters were valued equivalently, irrespective of their CSA agreements, this would lead to a concept of collateral arbitrage.

*Example 5.4:*

Derivative contract: €5bn IRS @ 1.5% start-1w tenor-3m
Alpha has bought and sold this contract with Bravo and Charlie resp., and current market rates are 1.0%

| Counterparty | Direction | Asset PV | CSA |
| --- | --- | --- | --- |
| Bravo | Paid fixed | €-6.23mm | Cash (EUR, USD) @ OIS, weekly |
| Charlie | Received fixed | €6.23mm | Cash (EUR) @ OIS, weekly |

The t+0 EURUSD FX rate is 1.2500 and the 1w XCS EUR/USD OIS spread is +22bps

The terms of the CSAs for each contract are different. Charlie has to post collateral to Alpha of €6.23mm in EUR, while Alpha can post collateral to Bravo in either EUR or USD. If Alpha posts €6.23mm, this leaves a net zero position and no PnL at the end of one week, or Alpha can receive €6.23mm 1W XCS trade at +22bps and post $7.7875mm (more complicated but results in €260.5 profit

| Date | Ccy | Amount | Description |
| --- | --- | --- | --- |
| t+0 | EUR | €6.23mm | Charlie posts to Alpha |
| t+0 | EUR | €-6.23mm | XCS notional exchange |
| t+0 | USD | $7.7875mm | XCS notional exchange |
| t+0 | USD | $-7.7875mm | Alpha posts to Bravo |
| --- | --- | --- | --- |
| t+1w | EUR | €-X | Alpha pays €OIS interest to Charlie |
| t+1w | EUR | €(X+260.5) | Alpha receives €OIS+22bps on XCS |
| t+1w | USD | $Y | Bravo pays $OIS interest to Alpha |
| t+1w | USD | $-Y | Alpha pays $OIS on XCS |
| t+1w | EUR | €6.23mm | XCS notional exchange |
| t+1w | EUR | €-6.23mm | Alpha returns to Charlie |
| t+1w | USD | $7.7875mm | Bravo returns to Alpha |
| t+1w | USD | $-7.7875mm | XCS notional exchange |

The arbitrage in the example came about because it proved better for Alpha to post USD cash collateral to Bravo, having swapped it from EUR. USD cash is the CTD collateral and in order to adhere to the no arbitrage principle, valuation of IRSs have to become CSA aware and the IRS with Bravo should be valued €260.5 higher. More generally, derivatives contracts should be valued dependent on CSAs and it is assumed that a counterparty will always posts the CTD collateral where possible.

*Example 5.5:*

Delta has a derivative liability valued at £100mm and £100mm in cash. The terms of the CSA on the derivative require GBP cash (remunerated at RFR) or UK gilts to be posted as collateral. The specified haircuts set by the CSA are 2% for gilts less than 5Y in maturity and 6% for gilts greater than 5Y in maturity. The market repo rate on any gilt is RFR+8bps with no haircut and the RFR rate is 0.75%. Delta can, however, only borrow unsecured cash at a rate of 2.5%, which creates borrowing costs.

| Delta's Strategy | Posted | Remuneration | Costs | 1D Total |
| --- | --- | --- | --- | --- |
| Post GBP cash | £100mm | @0.75% is £2055 | £0 | £2055 |
| Borrow £2mm & reverse repo any gilt $<$ 5Y maturity | 3Y gilt £102mm | @0.83% is £2319 | £-137 | £2182 |
| Borrow £6mm & reverse repo any gilt $\geq$ 5Y maturity | 15Y gilt £106mm | @0.83% is £2410 | £-411 | £1999 |

The CTD is gilts less than 5Y maturity, even with the haircuts specified in the CSA.

##### Cheapest to deliver (CTD) discount curves

To satisfy the no arbitrage principle, the valuation of any derivative must be calculated using discount factors built specifically for the type of collateral under the terms of the CSA. Here, we suppose the existence of single-CSA discount curves and illustrate a way to combine these individual curves. By combining the individual curves, we create a discount curve for a CSA that permits multiple choices (multi-CSA discount curve). Combining single-CSA curves is the less difficult process of selecting the cheapest daily rate from any of the individual curves, and progressively building up a new one. This is essentially a bootstrapping process constructed one day after the next.

*Example 5.6:*

Suppose that two single-CSA discount curves exist, containing DFs for any JPY cashflow under the terms of either a JPY cash only, or USD cash only CSA. Then we form the multi-CSA discount curve for a choice of either JPY or USD cash by taking the highest attainable daily rate of each day:

| Date | JPY CSA DF | JPY CSA O/N Rate | USD CSA DF | USD CSA O/N Rate | JPY + USD DF | JPY + USD O/N Rate |
| --- | --- | --- | --- | --- | --- | --- |
| t+0 | 1.000000 | 2.00% | 1.000000 | 2.10% | 1.000000 | 2.10% |
| t+1 | 0.999945 | 2.05% | 0.999942 | 2.10% | 0.999942 | 2.10% |
| t+2 | 0.999889 | 2.15% | 0.999885 | 2.10% | 0.999885 | 2.15% |
| t+3 | 0.999830 | 2.20% | 0.999827 | 2.10% | 0.999827 | 2.20% |
| t+4 | 0.999770 | etc. | 0.999769 | etc. | 0.999769 | etc. |

In order for the collateral posting institution to achieve the cheapest rate it will either; have USD cash available initially and post that for two days, then request its return, swap it for JPY cash via a XCS (or practically an FX swap), and then post JPY for the last two days, or, it will have JPY cash available initially but swap it for USD cash via a XCS (or FX swap) and post that for two days, then request its return, complete the XCS and post the remaining JPY for the final two days. The no arbitrage principle and pricing methodologies ensure that these two scenarios are equivalent.

In this example, two single-CSA discounting curves for JPY cashflows have products a third basic/intrinsic multi-CSA curve for JPY cashflows, assuming XCS transactions to secure the prevailing rates. Building off of this, three single-CSA curves could combine in four different ways and ten could produce 1,012 possible multi-CSA curves. For any institution to value its derivatives properly it must be able to;

1. Automate construction of all single-CSA curves for use of cashflows of a particular currency
2. Have automated processes to combine single-CSA curves to produce new, required, multi-CSA curves for cashflows of that same currency
3. Extract information about specific CSAs on individual derivative contracts to determine which discount curve to use to value and price that derivative contract accurately.

The above is operationally complex, so there is a form of collateral valuation adjustment created as an approximation of the true value of derivative assets and liabilities. Practical collateral management is also complex, so some theoretic asset/liability values might not necessarily be completely attainable (especially if the counterparty is unable to practically post the CTD collateral).

##### Standard CSAs for benchmark valuation

All cleared trades will have the same CSA by product, and it is sensible to use this as the benchmark CSA as clearing of trades is prevalent for many counterparties, and encompasses the vast majority of traded derivatives. The standard terms of these CSAs are:

1. Type of collateral: cash
2. Currency of collateral: locally specific to the product (i.e., GBP for GBP IRS)
3. Thresholds: zero, exchange on any liability
4. Frequency of exchange: daily
5. Bilateral or unilateral: bilateral
6. Remuneration: FRF

Having a benchmark allows easier comparison between non-standard and standard CSAs as well as measures of CSA risk and PnL separable from other market risks and PnL. The valuation difference between non-standard CSAs and benchmark CSAs are sometimes called the CVA (collateral valuation adjustment).

##### Optionality

When a CSA exists that allows one or both parties to post multiple currencies or types of collateral, and switch the collateral at any time, there exists an inherent option available to the posting institution (same as the institution who holds the liability side of the derivative). It is quite a complicated process to price the value of this optionality, which is dependent upon many variables:

1. Expected value: a derivative whose expected value is around 0 (one party could be equally ITM or OTM), will have minimum optionality. A derivative which is deeply OTM, and with one-sided expected value, will have a higher optionality because the collateral choice favors the poster much more than the asset holder
2. Collateral choice & time: the more choices of collateral one can post will generally increase the value of optionality, as will the longer the time to maturity
3. Expected CTD: like with the expected value of the derivative, the expected CTD collateral has an impact on the value of optionality. If the current CTD is far cheaper than other forms/currencies of collateral, there is a lower value of optionality. If they are roughly equal in value, the value of optionality will be increased
4. Market volatilities: the expectation of more volatile market movements and the probability of changing CTDs increases the optionality value
5. Frequency of exchange/switch: There can only be optionality value if the terms of the CSA permit switching of collateral to monetize changes in CTD
6. Practical expectations: the posting institution has to have the practical ability. to react to changes in CTD. Transaction costs will also decrease the value of optionality as the necessary hedging costs to pursue a theoretical CTD strategy may exceed the benefits of the strategy

Modern approaches toward CTD optionality pricing will run a simulated environment approach (Monte Carlo analysis) and assume a statistical price, with input parameters estimated for all of the above points.

##### Unilateral CSAs

Occasionally CSAs exists which requires only one counterparty to post collateral, which creates a peculiar pricing dynamic. For assets like this which are heavily ITM, then it is more statistically certain that the asset is either collateralized or uncollateralized (as standard market movements are unlikely to alter this binary determination). Its value can then be assumed to be broadly equivalent to the discounting of the cashflows assumed in either the case of a collateralized derivative or an uncollateralized one. For assets with values close to zero, then the impact of unilateral CSA becomes very significant, because the binary determination is potentially subject to fluctuate with market movements. This represents a different kind of option held by the counterparty who never needs to post collateral. Modern derivative pricing should take this into account, again through scenario analysis, but it is very complex.

#### Credit Risk

##### Credit exposure (CE)

The immediate potential loss in the event of a counterparty defaulting on its obligations (sometimes also called current exposure). Exchange traded or cleared derivatives can be said not to possess CE because the legal counterparty of those trades is a clearing house (only valid if assumed that a clearing house cannot default). For bilateral trades (face counterparty directly), there is an important distinction between collateralized and uncollateralized derivatives in the context of CE (mitigates against loss by providing security for assets), but there are a few elements which are not protected by collateral;

1. Collateral valuation lag: even the most frequent collateral exchanges can only be posted one day in arrears, after the previous day's closing valuations have been exchanged and agreed between counterparties. This lag represents the time period between the date of the valuation for the most recently submitted collateral posting and the notice of bankruptcy filing, with a potential market move in between
2. Uncollateralized valuation adjustment through period of transition: when a counterparty defaults, the fair value of the asset must be ascertained by the aggrieved party, which is usually done using official daily closing curves to provide a legal demonstration of validity ahead of liquidation proceedings. This creates a period of time where valuation changes will occur without being collateralized any further (time between notice of bankruptcy filing and final derivative valuation)
3. Replacement cost of risk: which is required as the defaulted derivative contract effectively ceases to exist. The cost of replacement can be made up of bid/offer spread and misaligned timing with respect to the formalization of the fair value claim on the original derivative, particularly if it is expected to take a reasonable amount of time to execute suitable replacement trades. Basel II and III regulations are particularly keen to stress this factor when measuring the risks on derivative assets for the purpose of regulatory reporting

Basel calls the above components (in a broad sense) the margin period of risk.

*Example 5.8:*

Alpha has a collateralized derivative with Lima, hedged by collateralized derivatives with other counterparties. On the open of day zero (i.e. after the close of day -1) Lima files for bankruptcy and makes no further collateral exchanges or payments. The table illustrates a possible scenario:

| STATEMENT of VALUATION (close on) | Day -2 | Day -1 | Day 0 |
| --- | --- | --- | --- |
| PV of Lima derivatives | 7,100,000 | 8,600,000 | 13,100,000 |
| Collateral posted by Lima | 6,900,000 | 7,100,000 | 7,100,000 |
| PV of replacement derivatives | - | - | -600,000 |
| --- | --- | --- | --- |
| PV of other derivatives | -7,100,000 | -8,600,000 | -13,100,000 |
| Collateral posted by others | -6,900,000 | -7,100,000 | -8,600,000 |
| --- | --- | --- | --- |
| Daily market move | -1bps | -7bps | -21bps |

Alpha will submit a claim to Lima's bankruptcy administrators for a total of 6mm, which represents the claim of 13.1mm minus the kept collateral of 7.1mm. The 6mm is made up of a 1.5mm collateral lag and a 4.5mm uncollateralized valuation adjustment on the day of the declared bankruptcy. In addition Alpha suffers a loss of 0.6mm due to risk replacement. If recovery rates are, for example 30% then Alpha's loss may be finalized as 4.8mm, ignoring any other costs (such as legal, operational or administrative).

Portfolios containing multiple trades with a single counterparty are usually subject to netting agreements, which state that the aggregate PV of all derivatives is the value used in legal claims. Without a netting agreement, the CE is usually far higher because each derivative is treated individually and a different treatment of assets compared to liabilities has large impact. Additionally, an institution may choose to model the valuation lag and change through transition slightly differently. Before notification of bankruptcy, financial markets will be functioning normally, but after an announcement, panic and consolidation may impact the liquidity, meaning a more conservative approach would be to consider the volatility after the notification having increased (mainly used larger, more influential organizations).

Calculating CE becomes a task synonymous with VaR. It requires statistical analysis to make predictions about viable market movements and then to ascertain values deemed to be expected within a specific c.i.. Suppose we wish to calculate the CE which is expected to be only $\alpha\\%$ of the time, that is to a $(1-\alpha)\\%$ c.i., then:

$$CE_{\alpha\\%} = RC_{mtm} + C_{lag, \alpha\\%} + C_{tran, \alpha\\%} + RC_{risk, \alpha\\%}$$

where,

$$
\begin{align*}
RC_{mtm} &:= \begin{cases}
0, & \text{(if collateralized)} \\
\max\{\text{asset PV}, 0\}, & \text{(if uncollateralized)}
\end{cases} \\
C_{lag,\alpha\\%} &:= \begin{cases}
\text{the cost of collateral lag,} & \text{(if collateralized)} \\
0, & \text{(if uncollateralized)}
\end{cases} \\
C_{tran,\alpha\\%} &:= \text{the cost of valuation change through transition,} \\
RC_{risk,\alpha\\%} &:= \text{the replacement cost of risk,}
\end{align*}
$$

with all statistical values measured to a $(1-\alpha)\\%$ c.i.

*Example 5.9:*

Continuing from example 5.8, at the close of day -1, Alpha considers its CE with a 95% c.i. to Lima, and calculates it to be, $CE_{5\\%} = 9,200,000$

$$
\begin{align*}
RC_{mtm} &:= 0 \text{ (the asset is collateralized),} \\
C_{lag,5\\%} &= 1,500,000 \text{ (is an observed value),} \\
C_{tran,5\\%} &= 6,500,000 \text{ (through statistical model),} \\
RC_{risk,5\\%} &= 1,200,000 \text{ (through expected charges),}
\end{align*}
$$

At this point, it is well worth flagging recovery rates and loss given default (LGD), which are terms for the same concept. Some of the CE will generally be expected to be recovered via the liquidation of assets of the defaulting entity, and this does play a part in CVA and regulatory reporting. But, as a value, CE seeks to indicate the immediate risk to a counterparty defaulting on its obligations and it is useful as an individual metric to compare exposure on different trades or portfolios to different counterparties, without specifically factoring in or estimating the LGD.

##### Potential future exposure (PFE)

Where CE is a metric for immediate credit exposure, PFE seeks to present a metric for exposure in the future (calculation requires more simulation than for CE). For a specific future date, $m_i$, we obtain the future CE by considering:

$$CE_{\alpha\\%}(m_i) = RC_{mtm, \alpha\\%}(m_i) + C_{lag, \alpha\\%}(m_i) + C_{tran, \alpha\\%}(m_i) + RC_{risk, \alpha\\%}(m_i)$$

where the major difference is that the uncollateralized asset value, $RC_{mtm, \alpha\\%}$, has to be statistically modeled as its future value is dependent upon the unknown progression of market rates. Minor differences being that the other three elements of the formula need to be statistically modeled in the context of future volatilities. For example, if one were trying to calculate the CE of a trade five years into the future, then one might choose to use higher volatilities, which are more conservative than those used to calculate today's CE. Once enough future dates have been assessed, the reported PFE is simply the maximum of any values:

$$PFE_{\alpha\\%} = \max_{i}{[CE_{\alpha\\%}(m_i)]}$$

Notice that the future CE values are future values, as opposed to present value calculations.

*Example 5.10:*

Alpha executes a collateralized £100mm 10Y IRS with Bravo and analyses the PFE. Alpha uses the following parameters in the model;

(i) five sampled future dates as well as the immediate CE,
(ii) the expected future delta risk of the remaining swap at each date,
(iii) a predicted market volatility for the remaining swap at each date
(iv) a multiplier, $DM$, for the consideration of distressed markets to estimate $C_{tran,5\\%}^{1D}$,
(v) no expected cost of risk replacement but a variance of 1bp of delta risk to this variable, in respect of when the replacement trade might be executed,
(vi) a c.i. of 95%.

| $m_i$ | $E[pv01]$ | $Vol_{c.l}^{1D}$ | $C_{lag,5\\%}^{1D}$ | $DM$ | $C_{tran,5\\%}^{1D}$ | $RC_{risk,5\\%}$ | $CE(m_i)$  |
| ----- | --------- | ---------------- | ------------------- | ---- | -------------------- | ---------------- | ---------- |
| 0y    | £92,000   | 4.5bps           | 681,000             | 1.5  | 1,021,000            | 151,000          | £1,853,000 |
| 2y    | £75,000   | 5.5bps           | 679,000             | 1.5  | 1,018,000            | 123,000          | £1,820,000 |
| 4y    | £57,000   | 6.5bps           | 609,000             | 1.5  | 914,000              | 94,000           | £1,617,000 |
| 6y    | £38,000   | 6.5bps           | 406,000             | 1.5  | 609,000              | 63,000           | £1,078,000 |
| 8y    | £19,000   | 6.5bps           | 203,000             | 1.5  | 305,000              | 31,000           | £539,000   |
| 10y   | £0        | 0.0bps           | 0                   | 0    | 0                    | 0                | £0         |

$PFE = £1,853,000$

In example 5.10 the PFE is the same as the CE. This is often the case with collateralized swaps, whose delta risk profile typically declines as the swap progresses through its life. However, changing the parameters can, of course, influence the results. Fwd swaps, whose risk increases as the swap start date becomes ever closer, is another example where this is not necessarily true. Once the swap begins, though, the risk steadily declines with each passing swap period and falls back to the above case.

*Example 5.11:*

Alpha pays an uncollateralized £100mm start-2Y tenor-8Y IRS with Bravo, and analyses the PFE. Alpha uses the following model parameters:

(i) five sampled future dates as well as the immediate CE,
(ii) the expected future delta of the remaining swap at each date,
(iii) Monte Carlo analysis to produce $RC_{mtm,5\\%}$,
(iv) a predicted market volatility for the remaining swap at each date to estimate $C_{tran,5\\%}^{1D}$,
(v) no expected cost of risk replacement but a variance of 1bp of delta risk to this variable, in respect of when the replacement trade might be executed,
(vi) a c.l. of 95%

| $m_i$ | $E[pv01]$ | $RC_{mtm,5\\%}$ | $Vol_{c.l}^{1D}$ | $C_{tran,5\\%}^{1D}$ | $RC_{risk,5\\%}$ | $CE(m_i)$   |
| ----- | --------- | --------------- | ---------------- | -------------------- | ---------------- | ----------- |
| 0y    | £73,000   | 540,000         | 4.5bps           | 540,000              | 120,000          | £1,200,000  |
| 2y    | £75,000   | 12,500,000      | 5.5bps           | 679,000              | 123,000          | £13,302,000 |
| 4y    | £57,000   | 17,800,000      | 6.5bps           | 609,000              | 94,000           | £18,503,000 |
| 6y    | £38,000   | 15,200,000      | 6.5bps           | 406,000              | 63,000           | £15,669,000 |
| 8y    | £19,000   | 9,000,000       | 6.5bps           | 203,000              | 31,000           | £9,234,000  |
| 10y   | £0        | 0               | 0.0bps           | 0                    | 0                | £0          |

$PFE = £18,503,000$

In example 5.11 the effect of the valuation of the swap has significant and the dominant impact. With respect to PFE the key term is *potential*. The swap is clearly not expected to have greater than £17.8mm PV four years into its life, but the potential for that to happen exists 5% of the time. If the counterparty were then to file for bankruptcy in this circumstance it would be quite unfortunate. This impact to the credit risk consideration highlights the difference between collateralized and uncollateralized derivatives. Regulators aim to capture all of these aspects when assessing RWA values for derivative trades.

##### Expected exposure (EE)

Calculating PFE required the determination of $CE_{\alpha\\%}(m_i)$, which is a specific type of statistical metric of exposure at a future date measured with a specific c.i.. Another frequently used metric is to consider the expected exposure (EE) which determines the average exposure on a specific date, $m_i$, of all simulated scenarios. Where the PFE aims to provide a kind of worst case analysis, the EE gives a more typical exposure value. In calculations, if the exposure in a scenario is accessed to be negative, that is the derivative is in fact a liability, then the exposure in that scenario is set to be zero. This ensures that EE values always express some credit risk, and is representative of the fact that if a counterparty were to file for bankruptcy and that counterparty be owed money, then that would be collected in full by the bankruptcy administrators (subject to the aforementioned netting agreement). On the other hand, if the counterparty owed money itself, then only a proportion might be recovered depending upon the LGD and distributed amount by the bankruptcy administrators.

Conservatively speaking, we can write EE as:

$$EE = E^+[RC_{mtm}] + E^+[C_{lag}] + E^+[C_{tran}] + E^+[RC_{risk}]$$

where $E^+[..]$ represents the expectation of the random variable whose value is taken to be zero if negative. Note that for a normal distribution (as an approximation) $X \sim N(0, \sigma^2), E^+[X] = \frac{\sigma}{\sqrt{2 \pi}}$

*Example 5.12:*

For the same trade in example 5.10 Alpha assesses its EE under the same parameters;

| $m_i$ | $E[pv01]$ | $Vol_{1s.d.}^{1D}$ | $E^+[C_{lag}]$ | $DM$ | $E^+[C_{tran}]$ | $E^+[RC_{risk}]$ | $EE(m_i)$ |
| ----- | --------- | ------------------ | -------------- | ---- | --------------- | ---------------- | --------- |
| 0y    | £92,000   | 4.5bps             | 165,000        | 1.5  | 248,000         | 37,000           | £450,000  |
| 2y    | £75,000   | 5.5bps             | 165,000        | 1.5  | 248,000         | 30,000           | £443,000  |
| 4y    | £57,000   | 6.5bps             | 148,000        | 1.5  | 222,000         | 23,000           | £393,000  |
| 6y    | £38,000   | 6.5bps             | 99,000         | 1.5  | 149,000         | 15,000           | £263,000  |
| 8y    | £19,000   | 6.5bps             | 49,000         | 1.5  | 74,000          | 8,000            | £131,000  |
| 10y   | £0        | 0.0bps             | 0              | 0    | 0               | 0                | £0        |

$\text{max EE}: £450,000$

*Example 5.13:*

For the same trade in example 5.11 Alpha assesses its EE under the same parameters;

| $m_i$ | $E[pv01]$ | $Vol_{1s.d.}^{1D}$ | $E^+[RC_{risk}]$ | $E^+[C_{tran}]$ | $E^+[RC_{mtm}]$ | $EE(m_i)$   |
| ----- | --------- | ------------------ | ---------------- | --------------- | --------------- | ----------- |
| 0y    | £73,000   | 4.5bps             | 29,000           | 197,000         | 131,000         | £357,000    |
| 2y    | £75,000   | 5.5bps             | 30,000           | 248,000         | 3,000,000       | £3,278,000  |
| 4y    | £57,000   | 6.5bps             | 23,000           | 222,000         | 4,800,000       | £5,045,000  |
| 6y    | £38,000   | 6.5bps             | 15,000           | 149,000         | 3,900,000       | £4,064,000  |
| 8y    | £19,000   | 6.5bps             | 8,000            | 98,000          | 1,100,000       | £1,206,000  |
| 10y   | £0        | 0.0bps             | 0                | 0               | 0               | £0          |

$\text{max EE}: £5,193,000$

##### EPE, EE, and EEPE

To be consistent with the Basel III terminology, we must include three more terms;

1. Effective expected exposure (EEE): on any date, is the highest EE that has occurred at any point until that date
2. Effective potential exposure (EPE): is the average across all time horizons of the EEs
3. Effective expected positive exposure (EEPE): is the average across all time horizons of the EEEs

The reason that these additional credit measures are used by Basel is because they believe they characterize better the risk of transactions which are subject ot rollover risk. This incorporates a sense that transactions are likely to be extended into the. future through new, on-going business.

##### Credit valuation adjustment (CVA)

With credit exposure in mind, financial institutions seek to calculate an adjustment to the market valuation of trades to reflect the chance of a counterparty defaulting and generating a loss in that scenario. Again, it is highlighted that many methods exists in practice for the determination of these adjustments. Some are more complicated and detailed than others. We can consider a standard simple model which help to present the overall idea of CVAs. Suppose that $p(m_i)$ is the modeled probability of default of the counterparty between the dates $m_i$ and $m_{i+1}$, then the CVA can be estimated as,

$$CVA = LGD \sum_{i=1}^{T} p(m_i) EE(m_i) v_i$$

where this model has chosen to adopt the EE as its base credit metric. We have also incorporated the probability of default and the LGD (or recovery ratio), which is another important estimation in the final assessment of ultimate loss if a counterparty defaulted.

*Example 5.14:*

Alpha calculates the CVA adjustment of both the collateralized (1) and the uncollateralized (2) trades from previous examples using the suggested model, with the parameters;

| $m_i$ | 0Y | 2Y | 4Y | 6Y | 8Y |
| --- | --- | --- | --- | --- | --- |
| (1) $p(m_i)$ | 0.1% | 0.1% | 0.1% | 0.1% | 0.1% |
| (2) $p(m_i)$ | 1.0% | 0.4% | 0.1% | 0.1% | 0.1% |
| $v_i$ | 1.000 | 0.963 | 0.928 | 0.906 | 0.856 |

Using LGD as 100%, for the collateralized trade, the CVA adjustment is calculated as £1,592. In the case of the uncollateralized trade, the CVA adjustment is, unsurprisingly, determined to be the much higher value of £25,593. If a standard 40% recovery ratio, i.e., 60% LGD, were to be applied to these values, then they might arguably be reduced by 40%.

CVAs are usually made at a counterparty level and not by each individual trade. If a counterparty were to default, then the complete set of trades owned by an institution facing that counterparty would be affected simultaneously. A new trade (or early termination of an old trade) should always be considered in the context of how it will affect the overall credit exposure of the institution to the counterparty as a whole (assuming netting set rules apply). Thus, the impact of a single trade could increase or decrease exposure dependent upon the other, current trades within the set. This is precisely the same concept as with the impact of new (or terminated) trades to RWA values of specific counterparties, which is covered in chapter 17. The above examples all presented the information assuming that the trade in question was isolated and was the only trade in the set. Be aware that in practice, credit exposure changes and CVA might be unintuitive, particularly without important knowledge of all of the other trades facing that same counterparty.

#### Funding valuation adjustment (FVA)

Unlike CVAs, FVAs have no dependence on the credit of the counterparty. Instead, they are completely dependent upon the institution's own funding ability. So CVAs depend on the counterparty, factoring in the economics of what happens if they were to default, and FVAs depend on the institution, factoring in the economics of how it will manage its own funding obligations on the trade. Like with CVAs, there is a grave distinction between collateralized and uncollateralized trades when considering FVAs. Collateralized trades have little consideration because funding of these trades are implicit; net cashflows that are paid to one counterparty as part of regular, intermediate settlement of derivatives will necessarily be returned, by that same counterparty, to the other due to the PV of the derivative changing by the same amount (collateral flux). Uncollateralized trades, however, are completely different; net cash outflows have to be funded and cash inflows provide an effective surplus.

When pricing an uncollateralized trade, the discount curve used to discount the cashflows is dependent on the institution's ability to borrow or utilize cash. For example, suppose rates are very low at 0.5% and an institution is about to execute a 10Y receiver IRS at 3%. The institution is getting an inflow of cash every accrual period until rates move higher nearer the maturity of the IRS when the cash starts being transferred back to the counterparty (to equate to an initial PV of zero). The cash balance profile of this trade becomes positive. What does the institution do with this received cash in the meantime (invested, utilized, etc.)? If so, at what rate of return? What if the institution were to enter the same IRS but as a payer (negative cash balance throughout the life of the IRS). In that scenario, how will the institution raise the cash to fund the trade and at what expected cost? This is precisely the information required in order to discount the IRS cashflows to price the IRS accurately. In practice, for an large institution, the rates at which it could borrow/fund cash will likely differ from those rates of return where it can utilize cash (so it not sensible to price an uncollateralized IRS with just one discount curve because it depends on upon the direction of the trade, and for more complicated IRSs, it may depend on more parameters than just direction).

The solution to the slightly complicated scenario is to invent the FVA. The technique allows an uncollateralized trade to be priced using a single, benchmark uncollateralized discount curve, and then the FVA is an after pricing adjustment which takes account of the likely cash balance of the institution and its applicable rates of funding (all institutions manage this differently and a specific way of pricing the flows in conjunction with all of the ways cash is managed as part of its on-going business). It is advantageous to have offsetting positions (i.e., paying uncollateralized cash on some derivatives and receiving uncollateralized cash on others), as this reduces funding risk and allows an institution to be in a position of engaging new business in either direction.

### Chapter 6 - Single Currency Curve Modeling

Curves make viable, and are the backbone for all derivative pricing techniques. The term *curve modeling* can have slightly different meaning in different contexts; it either means establishing the mechanical process that will generate RFR rates used for the pricing of linear IRDs, or constructing approximate, analytical mathematical models (many varieties) aimed at reflecting or proxying the movement in rates, often for use with deriving solutions to stochastic differential equations (when pricing swaptions or other structured products), or more theoretical financial applications. The focus here is on practical construction and the decisions involved in determining the mechanical process. The mathematical models aim to reflect the movement of these true mechanically generated curves, which themselves, reflect the market prices of basic IRDs. Complacency tends to exist in this field because it is quite easy to generate curves poorly, without being able to observe their weaknesses. It is rather much more difficult to design curves well and that permit accurate interbank trading. In this chapter, the items covered are;

1. Underlying properties, or foundations, or IR curves
2. What types of curves are produced and the need for synchronous relationships
3. Degrees of freedom and calibrating parameters
4. Interpolation techniques for unspecified points of curves
5. Practical considerations of the curve's use affecting its design
6. Trader's considerations when relying on curves to price derivatives

#### General curveset construction

##### Introduction and principles

Curves exist to provide interested parties with the knowledge of, for any date in the future, both of the following; the DF for that date (using a particular CSA for discounting) or a forecast RFR rate (which can be compounded together to produce an RFR tenor period). This chapter examines the most important points when creating curves for use in only a single currency, and do *not* consider the the implications of the XCS market, nor of CSAs in alternate currencies. Since the transition from IBOR, creating curvesets has become simpler since the task involves the construction of only a single curve, the RFR curve (previously, curveset/curve referred to the collection of OIS and IBOR curves for all tenors of IBOR index, i.e., 1M, 3M, etc. which were all distinct curves with their own inherent basis). A curve should;

*Figure 6.1: Considerations for the construction of a curve:*

1. Be time synchronized with the instruments that parametrizes it and with other relevant curves, see chapter 19
2. Be calibrate to market instruments and be able to replicate any mid-market price, see chapter 11
3. Be numerically efficient to calculate and derive, see chapter 12
4. Be practically maintainable and transparent so that a trader can, for example, manually update it in markets that are less liquid and so that a trader is aware of its limitations and control structure, see chapter 19
5. Consider means of hedging with respect to risk and profit and loss management, see chapter 9
6. Possess inherent structure to minimize internal volatility, i.e., 6Y expected to be proportional to 5Y and7 Y as an example, see chapter 12
7. Be useful for market analysis and not just for pricing, i.e., to provide valid historical data for chapter 14 and 15
8. Be robust to the passage of time, i.e., if a week passes, the interpolation structure should still yield consistent interpolated values for the equivalent input parameters, see chapter 12

##### Foundation of a curve

The foundation fof any single curve within a set of curves establishes how we are going to represent it mathematically. It can be designed with one of only two sensible bases; DFs and forecast rates. For RFRs, actually the two foundations are the same since there is a one-to-one equivalence, but for previous IBOR curves, this was not the case.

###### DFs based curves

The oldest and traditionally used approach. This type of curve will assign a DF for each future date on the curve and then, from that information, an appropriate rate can be determined between two given dates. This means that there is a mathematical equivalence between the rates implied by the curve and the DFs it contains. In order to derive an implied rate from a DF based curve, use the following formula;

$$r_i = \frac{1}{d_i}\left(\frac{v_{i-1}}{v_i}-1\right)$$

for $m_{i-1}$, $m_i$, the value start date and value end date respectively of the appropriate tenor rate under consideration. To calculate, for example, the forecast RFR for a particular day, one need only take that day's DF and the subsequent DF (not on a holiday) and derive the rate. We will use this DF based approach for our RFR curve construction.

###### Forecast rate based curves

Forecast rate based curve are entirely different and designed for IBOR indexes. They produce only a specific index rate attributable for any future date, with that rate being the designated purpose of the curve. For example, a 3M-$LIBOR curve will produce the set of all 3M-$LIBOR rates. This type of curve cannot have any DFs, due to mathematical inconsistencies. Consider the example:

| Value Date | Value End Date | Rate | Start DF | End DF (implied) |
| --- | --- | --- | --- | --- |
| 12-Dec-2016 | Mon 13-Mar-2017 | 1.6100% | 0.99500 | 0.99102 |
| 13-Dec-2016 | Mon 13-Mar-2017 | 1.6120% | 0.99495 | 0.99101 ! |

The mathematical inconsistency here arises due to weekends and holidays which affect value end dates so that sometimes two or more forecast rates have the same end date and there is *not* a unique DF which, given their start DF, satisfies all. Implementing forecast rate based curves negated the problem of resulting in spurious IBOR rates derived from those *repeated* DFs.

##### Collection of curves

A curveset contains more than one curve, all of which need to be synchronized with each other according to the specified market data. Synchronization is an important property of a curveset because without it, pricing of derivatives wll be timing inconsistent and will result in inaccurate prices. A typical curveset in a single currency for use in general trading will contain the following curves;

1. RFR curve
2. Discounting curves: benchmark CSA, and uncollateralized or other forms
3. Central bank rate curve
4. *Obsolete* IBOR curves: 1M, 3M, 6M, 12M

##### Market data and knots

Building a curveset that is accurate to the market requires knowledge of some of the market prices as inputs to the curveset. One must be careful which prices to choose as inputs. If too many inputs are chose, the curveset risks being overspecified and can be very difficult to calibrate the curve if some of these inputs need to be manually and synchronously updated (such as prices that are voice brokered). If too few inputs are chosen, the curve is underspecified and parts of the curve may be subject to other model assumptions and may not reflect real market prices. The preferred, modern day method is to numerically solve curvesets. The 'bootstrapping' method is old and outdated. This is because for implementing the more complicated features and flexibility of a curveset, it is either impossible or far more complicated than a numerically iterative solution. To solve numerically then, our curve must have what are termed *knots, nodes* or *pillar dates* depending on the author, with each knot typically representing a degree of freedom on a specific date of a curve for the numerical solver. Knots do not have to be positioned in exactly the same location as that implied by the calibrating input instruments, but it is known that some general knot placements can lead to ill-constrained curves. The below is a list of guidelines that would be expected of any curveset design, following the design parameters of figure 6.1;

1. The most liquid, interbank products should be included as benchmarks (these make up the majority of the important input prices)
2. Exchange traded products should be included (these usually fall in the above category as being the most liquid and they are also electronic, which allows immediate and automatic feedback)
3. The further the maturity of the curve, the sparser the inclusion of inputs becomes (because more products are usually traded at the shorter end of the curve requiring it to be calibrated to a greater degree)
4. Each currency will usually have its own nuances, meaning each curve design in each currency may have to be different to be optimally suited
5. The RFR curve will serve as the forecast curve and default curve for discounting benchmark CSA cashflows

##### Interpolation styles of a curve

Between the knots, we must use interpolation techniques to derive all of the other values on all other dates that make up the curve. Additionally, one may choose to employ one style of interpolation for one part of the curve (i.e., first year), and then switch to use another.

###### DF interpolation: log-linear or log-cubic

The common approach here is to either linearly interpolate the logarithm of DFs between knot dates or create a cubic spline function between the logarithm of the DFs. If a log-linear approach is adopted, it results in constant O/N rates for that curve between knot dates, provided they are tightly spaced. A log-cubic spline approach, which has the additional constraint that the first and second derivatives of $\log(DF)$ function are also required to be continuous at each knot, produces a much smoother curve. The resulting O/N rates are smooth throughout and do not have discontinuous jumps at knot points unlike the case with log-linear. But this smoothness comes with a caveat; it also means that the curve becomes globally dependent so that changes to any input parameters may impact the interpolation of any part of the global curve.

##### Numerical solver

In order to generate a curve where the position of each knot is such that all fo the input prices are returned exactly or as closely as possible, requires a numerical solver. In institutions, numerical solvers for the purpose of solving curvesets would have been created to prioritize both speed and accuracy. Numerical solvers rely on techniques to iterate through multiple solutions (or guesses) trying to improve the accuracy each time and can be complex and specific. We build our own curve solver using various iterative algorithms (gradient descent, Gauss-Newton, Levenberg-Marquardt) in chapter 11.

##### Risk consideration

One of the major considerations to modeling and constructing a curveset is hedging. If any curve is so complicated in its design that priced and traded products cannot be confidently or knowingly hedged with liquid, benchmark interbank trades, then the curveset is not really fit for the purpose of trading. In that case, the determination to produce such an accurate pricing curve has sacrificed the ability to risk manage traded products. Certain curve properties, such as turns (explained later), are examples of items that are complicated and difficult to hedge, but must be captured by a pricing curve. This was much more important for obsolete IBOR curves and the impact to RFRs is more muted. Other complicated effects become subjective assessments by traders, whether they feel it is better to price and sacrifice the hedging ability, or neglect them to provide risk models which better capture the PnL of market movements. Chapter 9 expands on this. 

##### Practical example

Here, a practical example is provided that demonstrates the concepts of curve design:

*Table 6.1: An overview of the model parameters for a simple dual curveset:*

| Model Considerations | Details |
| --- | --- |
| Curves in set | RFR which also serves as the benchmark CSA DF curve |
| Foundation | DF based |
| Input instruments | 3M RFR tenor rate starting t+0, <br> IMM RFR IRSs on next 8 IMM dates, <br> 3Y, 5Y, 7Y, 10Y IRS rates |
| Knot placement | 9 knots at start and maturity of IMM IRSs, <br> 4 knots at the maturity of each IRS |
| Interpolation style | One curve created with log-linear, <br> another curve created with log-cubic, <br> a final curve with mixed interpolation |
| Numerical solver | Chapter 11 and 12's Python solver |

##### Accuracy and value considerations

Since there are a variety of approaches and potential model choices (i.e., interpolation styles, knot points, calibrating instruments, etc.), there is a degree of model uncertainty. Some prices, or curve segments, will be subject to more model uncertainty than others (i.e., it is almost assured that a liquid 10Y IRS rate is an input to any curve model and therefore, with clarity over the market price, it will differ only marginally, if at all, across models). Confidence in a curve might give a trader an edge, which a lack of confidence may do the opposite. Curve models tend to have the greatest model uncertainty at points around local maxima or minima.

*Table 6.2: Data for the modeled curveset and numerically solved values:*

###### Input instruments and market prices

Deposit

| Start | Rate |
| --- | --- |
| 1-Jan-22 | 1.00% |

IMM Swaps

| Start | Rate |
| --- | --- |
| 15-Mar-22 | 1.05% |
| 15-Jun-22 | 1.12% |
| 21-Sep-22 | 1.16% |
| 21-Dec-22 | 1.21% |
| 15-Mar-23 | 1.27% |
| 21-Jun-23 | 1.45% |
| 20-Sep-23 | 1.68% |
| 20-Dec-23 | 1.92% |

IRSs

| Tenor | Rate |
| --- | --- |
| 3Y | 1.68% |
| 5Y | 2.10% |
| 7Y | 2.20% |
| 10Y | 2.07% |

###### Curve knots and numerically solved values

| Date | Log-Lin | Log-Cub | Mixed |
| --- | --- | --- | --- |
| 1-Jan-22 | 1.000000 | 1.000000 | 1.000000 |
| 15-Mar-22, $v_1$ | 0.998028 | 0.998014 | 0.998028 |
| 15-Jun-22, $v_2$ | 0.995393 | 0.995379 | 0.995393 |
| 21-Sep-22, $v_3$ | 0.992409 | 0.992391 | 0.992409 |
| 21-Dec-22, $v_4$ | 0.989547 | 0.989530 | 0.989547 |
| 15-Mar-23, $v_5$ | 0.986809 | 0.986785 | 0.986809 |
| 21-Jun-23, $v_6$ | 0.983455 | 0.983420 | 0.983455 |
| 20-Sep-23, $v_7$ | 0.979919 | 0.979881 | 0.979919 |
| 20-Dec-23, $v_8$ | 0.975832 | 0.975794 | 0.975832 |
| 15-Mar-24, $v_9$ | 0.971539 | 0.971426 | 0.971537 |
| 1-Jan-25, $v_{10}$ | 0.950978 | 0.950978 | 0.950978 |
| 1-Jan-27, $v_{11}$ | 0.900403 | 0.900403 | 0.900383 |
| 1-Jan-29, $v_{12}$ | 0.857393 | 0.857432 | 0.857419 |
| 1-Jan-32, $v_{13}$ | 0.814368 | 0.814484 | 0.814464 |

##### Opening and closing curvesets

Opening (or open) curvesets and closing (or close) curvesets are at least two curvesets that are generally saved each trading day (they represent 'snapshots' of curvesets at pre-determined times). The closing curveset of a given currency is usually measured at 1615hrs local time. The time synchronicity of all currencies and all other instruments is important to provide a consistent measure of cross market hedges (closing curvesets are the most important when it comes to calculating daily MTM value and collateral exchange, but construction of closing curvesets are identical to other curvesets). The closing curveset are often benchmarked against broker screens to assure that its accuracy falls within a tolerance to interbank traded market levels. It is especially important form a regulator's and accountant's perspective emphasized at quarter and year ends. The opening curveset is less well defined and not benchmarked. The opening curveset is usually constructed from the previous day's closing curveset but structurally altered to represent the start of the next trading day. Opening and closing curvesets are fundamentally different from each other in their purpose and important for reliable calculations of PnL (more an internal design choice and differs across institutions). We discuss two common approaches to building opening curvesets (the first; older, simpler, and flawed method, and the second; more robust method).

###### An opening curveset constructed from the previous close's input prices

This is the simplest method because it does nothing more than generate an opening curveset by taking, for the input instruments, the same prices as were used for the input instruments to generate the previous day's closing curve. This introduces two sources of inconsistencies;

1. Misaligned date schedule: the specification of the input instruments from one day to the next is different (i.e., a 10Y IRS today does not have the same accrual, reset, or payment schedule as a 10Y IRS defined as of the previous day). This adjustment inherently and erroneously introduces an amount of roll-down (ignores the change in accrual schedule)
2. An unintended distinction between fwd and par tenor (referring to derivatives tarting imminently with standard tenors) (par) instruments: if all the input instruments' prices are reused, then par instruments suffer the above problem but certain fwd instruments, like IMM rates, do not, because their date schedule specification does not change from day to day. *This* opening curve inconsistently treats some sections of the curve differently to other sections, by inherently introducing roll-down or not doing so.

This curveset approach will not affect the total daily MTM change between the closing curvesets of one day and the preceding day, but the two associated PnL numbers: *overnight carry* and *daily market movement* have sizable amounts of offsetting stochastic noise, even if its sums are equal to the daily MTM change.

###### Maintaining constant fwd rates

This second method of construction creates an opening curveset where all of the rates are set to be those that were forecast, for the appropriate dates, by the previous day's closing curveset. This is a pricing consistent approach that assumes that, between the previous day's closing curve and today's open curve, the market remains exactly the same (no inherent introduction of roll-down and can either be generated by the scaling of DFs or repricing instruments). When DFs are scaled, the chosen input instruments are ignored completely in the process and the opening curveset is generated precisely by sampling every possible DF from the previous day's curveset and reinserting them into the opening curveset appropriately. Mechanically speaking, to preserve fwd rates on a curve that has been constructed using DFs, one must divide all of the DFs of the previous closing curve by the DF attributable to today's date (which was tomorrow's DF measured yesterday). This method also preserves the precise interpolation under the closing curves knot choices. When instruments are repriced, the precise input instruments' prices, needed to generate the opening curveset, are calculated from the previous day's closing curveset, taking into account the different date schedules and other nuances of moving from one day to the next. This method uses the new day's interpolation scheme which may include a possible adjustment of knot points (see chapter 12).

As outlined, in the case where there are minor interpolation fluctuations moving from the previous day's *close* to today's *close*, because knot points or datasites have shifted, these fluctuations will either be,

1. *Not* captured in opening curveset since DFs are scaled, so the attributed interpolation fluctuation PnL must be allocated to the daily market movement component, or,
2. Captured in opening curveset since instruments are repriced and the curve rebuilt, meaning the attributed interpolation fluctuation PnL is allocated to the overnight carry component

Which way is better is subjective. The latter permits a distinction of overnight carry, which maybe useful for extracting information that is impossible in the alternate (because market movements are often so large that they dominate the component in this case). This distinction is highlighted most prominently on a n IMM roll, or when an input instrument is added or subtracted from the set of input instruments. On those rare, but important days, the interpolation fluctuation is greatest and the curve can also shift if the new instrument is priced differently ot the previous close's estimate of the instrument's price.  

#### Centrally cleared counterparty (CCP) adjustments

A notable evolution in recent years (post 2012) has been the development of a basis market for IRDs, and more prominently IRSs, which face one centrally cleared counterparty (CCP) versus another (the three largest CCPs being the London Clearing House (LCH), the Chicago Mercantile Exchange (CME), and the Eurex Exchange). The form that this basis market takes is a bp spread price assigned to par tenor IRSs. One counterparty will execute an IRS with one CCP in one direction versus the same IRS in the opposite direction with another CCP: the fixed rates differing by the agreed spread price.

*Example 6.1:*

The table identifies some example CCP basis prices for EUR IRSs. These prices are both reference versus LCH mid-market IRS rates, since that is (at the time of publication) the dominant clearing house for this product. IRS rates int he other two clearing houses have fixed rates higher than the LCH mid-market rate in this example.

a. EUR IRS Eurex/LCH price

| Tenor | CCP Basis (bp) |
| --- | --- |
| 2Y | 0.70 |
| 5Y | 1.60 |
| 10Y | 2.70 |

b. EUR IRS CME/LCH price

| Tenor | CCP Basis (bp) |
| --- | --- |
| 2Y | 0.10 |
| 5Y | 0.20 |
| 10Y | 0.35 |

Why should an IRS with similar institutions, all of negligible credit risk, have significantly different prices (all of the IRSs cleared with CCPs *have the same collateral terms*, normally cash local to the product remunerated at RFR). Assuming zero costs of trading, this would breach the no arbitrage principle, but it does not because there are other costs of trading; respective costs-of-carry of each IRS facing each CCP, specifically, the margin payments that are required to be posted to each CCP. Each CCP defines their own methodology for calculating the margin amounts that any of their counterparties must post, and while generally speaking these tend to be very similar, the "concentration charges" are noticeably different. For example, if a financial institution has a large net risk position facing the CCP (i.e., a risk position that is multiple times the expected daily executable and hedgeable volume), then that counterparty may be charged significantly higher margin amounts than would be expected through linear scaling (done to protect the CCP from significant losses in the event a counterparty defaults). There are also regulatory capital charges that should be considered also. If the basis differential reached a quantity that overcame these specific costs-of-carry, it would represent a genuine arbitrage opportunity, so there is a limit or pricing window within which these basis differentials must trade.

##### Impact of CCP basis on curve construction

The swaps traded at the different clearing houses settle against the same RFR fixing rates. It therefore warrants the question that if their mid-market prices are different, how should that value be quantifiably represented, and how should one price the effect into non-observable prices like bespoke swaps or fwd swaps. The solution is to utilize a *curve modeling approach*, where a separate curveset is created for the instrument prices derived from each CCP, acknowledging that the forecast RFRs will be different. Suppose we are creating an ESTR curve in EUR. To do this, we use the same set of calibrating instruments with their relevant prices at the different CCPs. This will produce three different curves; EUR:1D.ESTR-LCH, EUR:1D.ESTR-EUREX, EUR:1D.ESTR-CME.

| Instrument | LCH Price | Eurex Price | CME Price |
| --- | --- | --- | --- |
| ... | ... | ... | ... |
| 5Y | 2.1000% | 2.1160% | 2.1020% |
| ... | ... | ... | ... |
| 10Y | 2.0700% | 2.0960% | 2.0735% |
| ... | ... | ... | ... |

We then use each of the curves to price trades designated to the respective CCPs. At the current time, the LCH is by far the larges CCP in terms of traded volumes, and therefore, must be assumed that this is the source of truth, for the true forecast RFR fixings, and will therefore be used to price generic trades outside of CCPs. The other prices are understood to suffer biases created by the cost of capital and execution charges incurred when settling through those CCPs (further discussed in the context of the market in chapter 18).

**Appendix:**

##### Summary of interpolation styles

| Style | Details |
| --- | --- |
| DF log-linear | $log(v_i) = \left(\frac{D_{k+1} - D_i}{D_{k+1} - D_k}\right) log(v_k) + \left(\frac{D_i - D_k}{D_{k+1} - D_k}\right) log(v_{k+1})$ <br> Constant O/N rates between knots <br> Locally stable and easily implemented |
| DF log-cubic | $log(v_i) = \left(\frac{D_{k+1} - D_i}{D_{k+1} - D_k}\right) log(v_k) + \left(\frac{D_i - D_k}{D_{k+1} - D_k}\right) log(v_{k+1}) + \left(\frac{(D_{k+1} - D_i)^2 (D_i - D_k)}{(D_{k+1} - D_k)^3}\right) \alpha + \left(\frac{(D_{k+1} - D_i) (D_i - D_k)^2}{(D_{k+1} - D_k)^3}\right) \beta$ <br> Smooth, continuous O/N rates between knots <br> Global dependence and complicated to implement |

##### Log-linear DF interpolation

We show in this section that log-linear DF interpolation produces constant O/N rates obtained from resultant DFs. Suppose for $m_k \leq m_i < m_{k+1}$, where $k$ indexes a knot point with the respective DF, $v_k$, then under this interpolation style, it is true that,

$$log(v_i) = log(v_k) + \frac{D_i - D_k}{D_{k+1} - D_k}(log(v_{k+1}) - log(v_k))$$

Additionally, the DF for one day after $m_i$ is,

$$log(v_{i(+1)}) = log(v_k) + \frac{1 + D_i - D_k}{D_{k+1} - D_k}(log(v_{k+1}) - log(v_k))$$

The O/N forward rate obtained through $v_i$, $v_{i(+1)}$ is,

$$r_i^{O/N} = \frac{1}{d_i}\left(\frac{v_i}{v_{i(+1)}}-1\right)$$

Which with the substitution of the exponential of the above logarithms gives,

$$r_i^{O/N} = \frac{1}{d_i}\left(\left(\frac{v_k}{v_{k+1}}\right)^\frac{1}{D_{k+1} - {D_k}} - 1\right)$$

So for any $m_i$ between $[m_k...m_{k+1}]$ the O/N rate is always the same, dependent only upon $k$, $k+1$.

##### Log-cubic DF interpolation

We show here firstly that the above interpolation style gives rise to quadratic CC O/N rates obtained from relevant DFs. Under this interpolation style, it is true that,

$$log(v_i) = \alpha + \beta D_i + \gamma D_i^2 + \epsilon D_i^3, \text{for constants } \alpha, \beta, \gamma, \epsilon$$

Additional to this, the DF for one day after $m_i$ is,

$$log(v_{i(+1)}) = \alpha + \beta (D_i + 1) + \gamma (D_i + 1)^2 + \epsilon (D_i + 1)^3$$

Then the CC O/N rate on date, $m_i$, is,

$$\bar r_i^{O/N} = \frac{1}{d_i} log\left(\frac{v_i}{v_{i( + 1)}}\right) = \frac{1}{d_i} \left((\beta + \gamma + \epsilon) + (2 \gamma + 3 \epsilon) D_i + (3 \epsilon) D_i^2\right)$$

Which is quadratic in $D_i$. Given $r_i^{O/N} \approx \bar r_i^{O/N}$, we conclude that the O/N rate on date $m_i$ is approximately quadratic. Secondly, we show that the instantaneous CC forward rates before and after knot, $m_k$, are equal, from which we infer the smooth nature of O/N rates about $m_k$. Because the construction is necessarily a cubic spline, the derivative of each piecewise polynomial about $m_k$ is equal, therefore,

$$\bar r_{k(- \Delta)}^\Delta = \frac{log(v_{k(- \Delta)}) - log(v_k)}{\lambda \Delta} = \frac{log(v_k) - log(v_{k(+ \Delta)})}{\lambda \Delta} = \bar r_k^\Delta, \text{as } \Delta \to 0$$

### Chapter 7 - Multi-Currency Curve Modeling

#### Forward FX rates

#### Cross-currency swaps (XCSs)

#### XCSs and collateral

#### MTM and non-MTM XCSs

#### Curve structure

**Appendix:**

##### Interest rate parity restated

##### Forward FX rate equivalence

##### FX swap pricing

##### MTM XCS pricing

##### Mid-market XCS spread

##### Bootstrapping the DFs, $w_i^\ast$

### Chapter 8 - Term Structure of Interest Rate Curves

#### Transmission mechanism

##### The deposit rate

##### Standing facilities

#### Term structure

##### What drives the shape of yield curves in a single currency

##### What drives the shape and nature of the cross-currency basis

**Appendix:**

##### Term structure and volatility

### Chapter 9 - Delta and Basis Risk

#### Defining market risk

#### Calculating delta or basis risk

##### Analytic risk

##### Numeric (or automatic) risk

#### Numeric risk in detail

##### Processes

##### Design of a risk model

##### Properties of a risk model

##### Risking a trade or a portfolio

##### Risk bleed

#### Practical market risks

**Appendix:**

##### Approximating risks with numerical processes

### Chapter 10 - Risk Models

#### Using multiple risk models

#### Risking with multiple models

#### Jacobian transformations for risk

#### Par forward (fwd) based models

#### Other uses of Jacobian transformations

##### PnL estimates and market movements

##### Covariance matrices

##### Cross-gamma grids risk

#### Summary of transformation formulae

**Appendix:**

##### Jacobian transformations of market movements

##### Jacobian transformations of covariance matrices

### Chapter 11 - Quant Library and Automatic Differentiation

#### Core library objects

##### Curve

##### Schedule

##### Swap

#### Automatic differentiation and dual numbers

##### Dual

#### Curve solver

##### Analytic or numeric process

##### Objective functions

##### Optimization algorithms

##### Gradient descent method

##### Gauss-Newton method

##### Levenberg-Marquardt method

#### Risk (quant library)

**Appendix:**

##### Gradient descent method math

##### Gauss-Newton method math

##### Fixed point iteration

##### Risk of calibrating instruments

### Chapter 12 - Advanced Curve Building

#### Log-cubic spline interpolation

#### Mixed interpolation

#### Layered curvesets

#### Turns

#### Notes, knots, and instrument selection

##### Monetary policy meeting dates and log-linear interpolation

##### Par tenors and log-cubic spline interpolations

#### A practical curveset

#### Performance enhancements

#### Risk

**Appendix:**

##### B-splines

##### Spline space

### Chapter 13 - Multi-Currency Risk

#### Cross-currency basis risk

#### FX risk

#### Non-standard CSAs

#### Multi-CSAs

#### Risk management

### Chapter 14 - Value at Risk

#### Portfolio construction

#### Value at risk (VaR)

#### Historical VaR simulation model

#### Variance-covariance (CoVaR) model

##### Construction of covariance matrices

##### Covariance matrix smoothing

##### CoVar multiplier and VaR calculation

#### Using CoVaR in practice

##### Single instrument VaR minimization

##### Allocation of VaR

##### Multiple instrument VaR minimization

#### Properties of VaR

#### Expected shortfall (ES)

**Appendix:**

##### The CoVaR approach, mathematically

##### CoVaR is a subadditive

##### Deriving single instrument VaR minimization trades

##### Deriving multiple instrument VaR minimization trades

##### Comparing ES with VaR

##### Estimating covariance matrices using prices

### Chapter 15 - Principal Component Analysis

#### General application

#### PCA Risk representation

#### Drawbacks with using PCA

#### Practical uses of PCA

##### Correlation and covariance smoothing

##### Multi-variate random walks

**Appendix:**

##### Establishing PCA through eigenvalues and eigenvectors

##### Cholesky decomposition

### Chapter 16 - Customized Risk Management

#### General risk management

#### Benchmark trade combinations

##### Types of trades

##### Directionality

##### Hedging considerations

#### Trader risk models

##### Risk representation

##### PnL representation

#### Market risk management

##### Prioritization

##### Incorporating VaR

##### Simplified portfolio representation

#### Consolidating everything

### Chapter 17 - Regulatory Capital, Leverage, and Liquidity

#### Basel Accords

#### Capital

##### What is capital?

##### Why is capital important to monitor?

##### Capital ratios

##### Risk weighted assets (RWAs)

##### Basel rules for RWA calculation

##### Management of RWAs

##### Capital requirements for market risks

#### Leverage Ratio

##### Basel rules for the exposure measure calculation

##### A note on centrally cleared counterparties (CCPs)

#### Liquidity

##### Liquidity coverage ratio (LCR)

##### Net stable funding ratio (NSFR)

#### Overview

**Appendix:**

##### Aumann-Shapley allocation concept

### Chapter 18 - Market-Making and Price-Taking

#### Context of the whole market

#### Market-maker considerations

##### Curve model & pricing curves

##### Outside influence

##### Assessment of risk and margin

##### Reset risk hedging costs

##### Market risks hedging costs

##### Liquidity and volatility hedging costs

##### Regulatory capital hedging costs

##### Strategy and game theory

### Chapter 19 - Electronic Trading

#### Mid-market

##### Level 1 assets

##### Single instrument pricing algorithms

##### Least squares regression

##### Bayesian inference

#### Slow and fast calculation

#### Automated pricing model

##### Equivalence of portfolios

##### Parametrizing the model

##### Solving the system

#### Model extensions

##### Volume and market impact

##### Inventory hedging

##### Correlation

##### Liquidity and volatility

##### Other possible extensions

**Appendix:**

##### Mean intrinsic depth average

##### Bayesian inference of market movements

### Chapter 20 - Swaptions and Volatility

#### Options basics

#### Swaption pricing

##### Pricing formulae

##### Receiver-payer (put-call) parity

##### Python code for swaption pricing

##### Intrinsic and optionality value

##### Log-normal distribution and shifting

##### Implying distributions from swaption prices

#### Volatility

##### At-the-money (ATM) straddles

##### Python code for implied volatility

##### Measures of volatility

##### Volatility smiles and skew

##### Volatility surface

##### Volatility of forward rates and correlation

##### Forward volatility

#### Greeks

##### Python code for swaption greeks

#### Market-making and price-taking

##### Named strategies

#### Extraneous topics

**Appendix:**

##### IRR formula for cash settlement

##### Implying distributions from swaption prices math

##### Estimating $\sigma_n$ given ATM swaption implied $\sigma_{LN}$

##### Deriving forward volatility

### Chapter 21 - Gamma and Cross-Gamma Risk

#### Defining gamma

#### Classical description of gamma

#### Modern description of gamma

#### Defining cross-gamma

#### Gamma and cross-gamma risks in portfolios

##### STIR futures hedged with IMM IRSs

##### ZCSs hedged with IRSs

##### Cash settled swaptions hedged with physically settled swaptions, and zero-wide collars

##### Trades with different CSAs

##### Misaligned payment dates

##### Non-MTM XCSs hedged with MTM XCSs

#### Hedging gamma and cross-gamma

##### Cross-gamma grids hedging

##### Cross-gamma hedging strategies

### Chapter 22 - Analytic Cross-Gamma

#### Historical context

#### Discounting risk

#### Mathematical basis

#### Trade types

#### First order risks

#### Second order risks

#### Practical algorithms

##### New swap class

##### Forward zero coupon risks

##### Cross-gamma of fixed and non-compounded trade types

##### Jacobian transformations

#### Cross-gamma and PnL estimates

#### Gamma of IRSs

##### The value of Gamma

**Appendix:**

##### Estimating the gamma of IRSs

##### STIR Futures convexity adjustment (FCA)

##### ZCS convexity adjustment (ZCA)

##### Impact of IRS risk rather than zero coupon deposits

##### Synthetic gamma with a discrete swaption series

##### VBA code for cross-gamma of compounded trade types

### Chapter 23 - Constructing Trade Strategies

#### Hedging trade directionality

##### PCAedging

##### CoVaR hedging

##### Multivariate least squares regression (MLSR)

#### Carry and Roll

##### Cost-of-carry

##### Roll-down

#### Sharpe ratio

##### Expected PnL

##### Volatility of PnL

##### Roll-down / volatility of trade

##### Adjusted roll-down / volatility of PnL ratio

##### Efficient frontier and CAPM

##### Using other assumptions

**Appendix:**

##### PCA directionality minimization

##### Multivariate least squares regression

### Chapter 24 - Reset Risk

#### Resets and reset ladders

#### Characterizing reset risk

##### The expected path of fixings and risk apportionment

##### Continuous hedging mechanism and overall risk

##### Practical example of reset risk assessment

##### Central bank policy meeting dates

##### Reviewing

#### Benefits of a VaR based approach

**Appendix:**

##### Establishing a relationship between the cash rate and the next IMM rate

##### Deriving the IMM hedge for VaR minimization

##### Deriving the overall reset risk VaR multiplier
