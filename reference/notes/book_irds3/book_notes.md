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
Alpha receives $100mm 5y IRS @ 2.15% from Delta, uncollaterlaized

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

To satisfy the no arbitrage principle, the valuation of any derivative must be calculated using discount factors built specifically for the type of collateral under the terms of the CSA. Here, we suppose the existence of single-CSA discount curves and illustrate a way to combine these individual curves. By combining the individual curves, we create a discount curve for a CSA that permits multiple choices (multi-CSA discount curve). Combining single-CSA curves is teh less difficult process of selecting the cheapest daily rate from any of the individual curves, and progressively building up a new one. This is essentially a bootstrapping process constructed one day after the next.

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

Occasionally CSAs exists which requires only one counterparty to post collateral, which creates a peculiar pricing dynamic. For assets like this which are heavily ITM, then it is more statistically certain that the asset is either collateralized or uncollateralized (as standard market movements are unlikely to alter this binary determination). Its value can then be assumed to be broadly equivalent to the discounting of the cashflows assumed in either the case of a collateralized derivative or an uncollateralized one. For assets with values close to zero, then the eimpact of unilateral CSA becomes very significant, because the binary dtermination is potentially subject to fluctuate with market movements. This represents a different kind of option held by the counterparty who never needs to post collateral. Modern derivative pricing should take this into account, again through scenario analysis, but it is very complex.

#### Credit Risk

##### Credit exposure (CE)

The immediate potential loss in the event of a counterparty defaulting on its obligations (sometimes also called current exposure). Exchange traded or cleared derivatives can be said not to possess CE because the legal counterparty of those trades is a clearing house (only valid if assumed that a clearing house cannot default). For bilateral trades (face counterparty directly), there is an important distinction between collateralized and uncollateralized derivatives in the context of CE (mitigates against loss by providing security for assets), but there are a few elements which are not protected by collateral;

1. Collateral valuation lag: even the most frequent collateral exchanges can only be posted one day in arrears, after the previous day'sclosing valuations have been exchanged and agreed between counterparties. This lag represents the time period between the date of the valuation for the most recently submitted collateral posting and the notice of bankruptcy filing, with a potential market move in between
2. Uncollateralized valuation adjustment through period of transition: when a counterapty defaults, the fair value of the asset must be ascertained by the agrieved party, which is usally done using official daily closing curves to provide a legal demonstratoiin of validity ahead of liquidation proceedings. This creates a period of time where valuation changes will occur wintout being colalteralized any further (time between notice of bankruptcy filing and final derivative valuation)
3. Replacement cost of risk: which is required as the defaulted derivative contract effectively ceases to exist. The cost of replacement can be made up of bid/offer spread and misaligned timing with respect to the foramlization of the fair value claim on the original derivative, particularly if it is expected totake a reasonable amount of time to execute suitable replacement trades. Basel II and III regualtions are particularly keen to stress this factor when measuring the risks on derivative assets for the purpose of regulatory reporting

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
| Daily market move | -1bp | -7bp | -21bp |

Alpha will submit a claim to Lima's bankruptcy administrators for a total of 6mm, which represents the claim of 13.1mm minus the kept collateral of 7.1mm. The 6mm is made up of a 1.5mm collateral lag and a 4.5mm uncollateralized valuation adjustment on the day of the declared bankruptcy. In addition Alpha suffers a loss of 0.6mm due to risk replacement. If recovery rates are, for example 30% then Alpha's loss may be finalised as 4.8mm, ignoring any other costs (such as legal, operational or administrative).

Portfolios containing multiple trades with a single counterparty are usually subject to netting agreements, which state that the agregate PV of all derivatives is the value used in legal claims. Wihtout a netting agreement, the CE is usually far higher because each derivative is treated individually and a different treatement of assets comapred to liabilities has large impact. Additionally, an institution may choose to model the valuaiton lag and change through tranisition slightly differently. Before notification of bankruptcy, financial markets will be funcitoning normlaly, but after an announcement, panic and consolidation may impact the liquidity, meaning a more conservative approach would be to consider the voalitlity after the notification having increased (mainly used larger, more influential organizations).

Calculating CE becomes a task synonymous with VaR. It requires statistical analysis to make predictions about viable market movements and then to ascertain values deemed to be expected within a specific c.i.. Suppose we wish to calculate the CE which is expected to be only $\alpha\text{\%}$ of the time, that is to a $(1-\alpha)\text{\%}$ c.i., then:

$$CE_{\alpha\text{\%}} = RC_{mtm} + C_{lag, \alpha\text{\%}} + C_{tran, \alpha\text{\%}} + RC_{risk, \alpha\text{\%}}$$

where,

$$
\begin{align*}
RC_{mtm} &:= \begin{cases}
0, & \text{(if collateralised)} \\
\max\{\text{asset PV}, 0\}, & \text{(if uncollateralised)}
\end{cases} \\
C_{lag,\alpha\text{\%}} &:= \begin{cases}
\text{the cost of collateral lag,} & \text{(if collateralised)} \\
0, & \text{(if uncollateralised)}
\end{cases} \\
C_{tran,\alpha\text{\%}} &:= \text{the cost of valuation change through transition,} \\
RC_{risk,\alpha\text{\%}} &:= \text{the replacement cost of risk,}
\end{align*}
$$

with all statistical values measured to a $(1-\alpha)\text{\%}$ c.i.

*Example 5.9:*

Continuing from example 5.8, at the close of day -1, Alpha considers its CE with a 95% c.i. to Lima, and calculates it to be, $CE_{5\text{\%}} = 9,200,000$

$$
\begin{align*}
RC_{mtm} &:= 0 \text{ (the asset is collateralised),} \\
C_{lag,5\text{\%}} &= 1,500,000 \text{ (is an observed value),} \\
C_{tran,5\text{\%}} &= 6,500,000 \text{ (through statistical model),} \\
RC_{risk,5\text{\%}} &= 1,200,000 \text{ (through expected charges),}
\end{align*}
$$

At this point, it is well worth flagging recovery rates and loss given default (LGD), which are terms for the same concept. Some of the CE will generally be expected to be recovered via the liquidation of assets of the defaulting entity, and this does play a part in CVA and regulatory reporitng. But, as a value, CE seeks to indicate the immediate risk to a counterparty defauling on its obligations and it is useful as an individual metric to compare exposure on different trades or portfolios to different counterparties, wihtout specifically factoring in or estimating the LGD.

##### Potential future exposure (PFE)

Where CE is a metric for immediate credit exposure, PFE seeks to present a metric for exposure in the future (calculation requires more simulation than for CE). For a specific future date, $m_i$, we obtain the future CE by considering:

$$CE_{\alpha\text{\%}}(m_i) = [RC_{mtm, \alpha\text{\%}} + C_{lag, \alpha\text{\%}} + C_{tran, \alpha\text{\%}} + RC_{risk, \alpha\text{\%}}](m_i)$$

where the major difference is that the uncollateralized asset value, $RC_{mtm, \alpha\%}$, has to be statiscally modeled as its future value is dependent upon the unkown progression of market rates. Minor differences being that the other three elements of the formula need to be statistically modeled in the context of future volatilities. For example, if one were tyring to calculate the CE of a trade five years into the future, then one might choose to use higher volatilities, which are more conservative than those used to calculate today's CE. Once enough future dates have been assessed, the reported PFE is simply the maximum of any values:

$$PFE_{\alpha\text{\%}} = \max_{i}{[CE_{\alpha\text{\%}}(m_i)]}$$

Notice that the future CE values are future values, as opposed to present value calculations.

*Example 5.10:*

Alpha executes a collateralised £100mm 10Y IRS with Bravo and analyses the PFE. Alpha uses the following parameters in the model;

(i) five sampled future dates as well as the immediate CE,
(ii) the expected future delta risk of the remaining swap at each date,
(iii) a predicted market volatility for the remaining swap at each date
(iv) a multiplier, $DM$, for the consideration of distressed markets to estimate $C_{tran,5\text{\%}}^{1D}$,
(v) no expected cost of risk replacement but a variance of 1bp of delta risk to this variable, in respect of when the replacement trade might be executed,
(vi) a c.l. of 95%.

| $m_i$ | $E[pv01]$ | $Vol_{c.l}^{1D}$ | $C_{lag,5\text{\%}}^{1D}$ | $DM$ | $C_{tran,5\text{\%}}^{1D}$ | $RC_{risk,5\text{\%}}$ | $CE(m_i)$  |
| ----- | --------- | ---------------- | ------------------ | ---- | ------------------- | --------------- | ---------- |
| 0y    | £92,000   | 4.5bp            | 681,000            | 1.5  | 1,021,000           | 151,000         | £1,853,000 |
| 2y    | £75,000   | 5.5bp            | 679,000            | 1.5  | 1,018,000           | 123,000         | £1,820,000 |
| 4y    | £57,000   | 6.5bp            | 609,000            | 1.5  | 914,000             | 94,000          | £1,617,000 |
| 6y    | £38,000   | 6.5bp            | 406,000            | 1.5  | 609,000             | 63,000          | £1,078,000 |
| 8y    | £19,000   | 6.5bp            | 203,000            | 1.5  | 305,000             | 31,000          | £539,000   |
| 10y   | £0        | 0bp              | 0                  | 0    | 0                   | 0               | £0         |

$$PFE = £1,853,000$$

In example 5.10 the PFE is the same as the CE. This is often the case with collateralised swaps, whose delta risk profile typically declines as the swap progresses through its life. However, changing the parameters can, of course, influence the results. Two swaps, whose risk increases as the swap start date becomes ever closer, is another example where this is not necessarily true. Once the swap begins, though, the risk steadily declines with each passing swap period and falls back to the above case.

*Example 5.11:*

Alpha pays an uncollateralised £100mm start-2Y tenor-8Y IRS with Bravo, and analyses the PFE. Alpha uses the following model parameters:

(i) five sampled future dates as well as the immediate CE,
(ii) the expected future delta of the remaining swap at each date,
(iii) Monte Carlo analysis to produce $RC_{mtm,5\text{\%}}$,
(iv) a predicted market volatility for the remaining swap at each date to estimate $C_{tran,5\text{\%}}^{1D}$,
(v) no expected cost of risk replacement but a variance of 1bp of delta risk to this variable, in respect of when the replacement trade might be executed,
(vi) a c.l. of 95%

| $m_i$ | $E[pv01]$ | $RC_{mtm,5\text{\%}}$ | $Vol_{c.l}^{1D}$ | $C_{tran,5\text{\%}}^{1D}$ | $RC_{risk,5\text{\%}}$ | $CE(m_i)$   |
| ----- | --------- | -------------- | ---------------- | ------------------- | --------------- | ----------- |
| 0y    | £73,000   | 540,000        | 4.5bp            | 540,000             | 120,000         | £1,200,000  |
| 2y    | £75,000   | 12,500,000     | 5.5bp            | 679,000             | 123,000         | £13,302,000 |
| 4y    | £57,000   | 17,800,000     | 6.5bp            | 609,000             | 94,000          | £18,503,000 |
| 6y    | £38,000   | 15,200,000     | 6.5bp            | 406,000             | 63,000          | £15,669,000 |
| 8y    | £19,000   | 9,000,000      | 6.5bp            | 203,000             | 31,000          | £9,234,000  |
| 10y   | £0        | 0              | 0bp              | 0                   | 0               | £0          |

$$PFE = £18,503,000$$

In example 5.11 the effect of the valuation of the swap has significant and the dominant impact. With respect to PFE the key term is *potential*. The swap is clearly not expected to have greater than £17.8mm PV four years into its life, but the potential for that to happen exists 5% of the time. If the counterparty were then to file for bankruptcy in this circumstance it would be quite unfortunate. This impact to the credit risk consideration highlights the difference between collateralised and uncollateralised derivatives. Regulators aim to capture all of these aspects when assessing RWA values for derivative trades.

##### Expected exposure (EE)

Conservatively speaking, we can write EE as:

$$EE = E^+[RC_{mtm}] + E^+[C_{lag}] + E^+[C_{tran}] + E^+[RC_{risk}]$$

where $E^+[..]$ represents the expectation of the random variable whose value is taken to be zero if negative. Note that for a normal distribution (as an approximation) $X \sim N(0, \sigma^2), E^+[X] = \frac{\sigma}{\sqrt{2 \pi}}$

*Example 5.12:*



*Example 5.13:*

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
