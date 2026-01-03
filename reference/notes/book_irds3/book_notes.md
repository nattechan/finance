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
- IBOR vs OIS Index differs where IBOR is an estimate of the future level while OIS is an observation of the past (both are unsecured). There is sometimes a lag between when a rate is fixed and the valuation period (i.e., 2 b.d. lag with EUR)
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

$$r_j = \frac{1}{d_j}\prod_{k=1}^{T_j} (1 + d_k r_k) - 1, \quad T_j = \text{number of business days in period } j$$

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

$$P = - \sum_{i=1}^{T_1} N_i d_i (r_i^1 + Z) v_i + \sum_{j=1}^{T_2} N_j v_j \left(\prod_{k=1}^{T_j} (1 + d_k \tilde{r}_k^2) - 1\right)$$

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

$\text{'Currencies, Index(es), Start-date, End-date,}$ $\text{Frequency}^1$, $\text{Frequency}^2$, $\text{Fixed/Floating}^1$, $\text{Fixed/Floating,}^2$ $\text{Roll-date, Stub-type, MTM or non-MTM'}$

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

- Convention adjustments: if the fixed leg and floating leg have different conventions (i.e., day count conventions or different frequencies), the same bp spread on one leg is not equivalent to the same spread on the other
- Coupon adjustment: if the coupon on the bond is not set to be the same as the priced YTM, the bond price is not exactly par. Usually the coupon is set to be lower than the YTM (bond prices at discount). The issuer typically wants to receive par however, so an economic upfront payment value known as the make to par is embedded into the swap. The lower coupon rate applied to the fixed rate of the swap offsets this in part but the economics are not exact
- Market-maker's margin: this is a fee for facilitating the transaction embedded into the issuer swap

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

Here the example interest rate of 0.8% on the cash balance is not equal to the RFR period rate published at 0.8996%. This is a very important distinction. For cleared and regularly collateralized derivates, these will be the same rates, but in this specific contract's case, 0.8% reflects the physically attainable rate of interest on the cash balance over the term, for example, there is a non-standard remuneration agreement on collateral here, which we will come on to.

##### Cash balance profiles

A cash balance profile details the expected cash balance of a portfolio at differing future dates. It is measured by aggregating all cashflows on a given day including accumulated interest amounts from previous days' balance. In the previous example, the cash balance at the 9M point would be $50,100 after the accrual of some interest each day after the initial receipt of $50,000.

For simple, mid-market IRDs, the expected cash balance profile is often easy to qualitatively describe. Firstly, for any derivative which has only a single cashflow date, there will never be any expectation of any cash balance (mid-market FRAs, ZCSs, single period IRSs/OISs). Thi is because any floating or fixed cashflows paid or received will be priced to net to zero, and therefore no net cashflows will ever be forecast to be exchanged. The trades still have risk, of course, and net cashflows will arise as market movements give rise to MTM PnL, we are just stating the expected nature of a zero cash balance profile for certain trade types executed at mid-market.

Secondly, where derivatives have multiple cashflows, there is generally a particular structure to the IR curve that allows a qualitative assessment (flat, upward sloping, downward sloping, bowing). Any derivative whose initial PV is zero will always have an expected final cash balance of zero. This is because a derivative with zero PV cannot be expected to gain or lose an amount of cash after its maturity. The interim, forecast, cash balance, however can feasibly have any pattern. These depend on the structure of all of the interim cashflows that take place. Cash balances are central to considering future discounting risk and the impact to PnL if discounting basis changes or the terms of a CSA is restructured.

##### Daily PnL accounting

- IRDs are unlike securities in the sense that on inception, you do not expect them to yield any return (vs. a bond that yields 2% per annum for example). In fact, if you receive a mid-market 1Y IRS @ 2%, based on the expectation of future forecast floating rates, you expect that the IRS will mature with zero PnL
- Derivatives are risk management and speculative, leveraged instruments. Trading these result in PnL only when market rates deviate from forecasts

#### Collateral

**Introduction:**

##### Credit support annexes (CSAs)

##### Pricing derivatives with different CSAs

##### Cheapest to deliver (CTD) discount curves

##### Standard CSAs for benchmark valuation

##### Optionality

##### Unilateral CSAs

#### Credit Risk

##### Credit exposure (CE)

##### Potential future exposure (PFE)

##### Expected exposure (EE)

##### EPE, EE, and EEPE

##### Credit valuation adjustment (CVA)

#### Funding valuation adjustment (FVA)

### Chapter 6 - Single Currency Curve Modeling

#### General curveset construction

##### Introduction and principles

##### Foundation of a curve

##### Collection of curves

##### Market data and knots

##### Interpolation styles of a curve

##### Numerical solver

##### Risk consideration

##### Practice example

##### Accuracy and value considerations

##### Opening and closing curvesets

#### Centrally cleared counterparty (CPP) adjustments

##### Impact of CPP basis on curve construction

**Appendix:**

##### Summary of interpolation styles

##### Log-linear DF interpolation

##### Log-cubic DF interpolation

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

##### A note on centrally cleared counterparties (CPPs)

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
