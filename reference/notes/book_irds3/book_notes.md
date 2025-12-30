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

$$DCF = \text{Day count fractions}$$

Interest payable:

$$\text{Interest payable} = notional \times DCF \times \text{interest rate per annum}$$

Actual 365 fixed (ACT/365F):

$$DCF_{ACT/365F} := \frac{\text{accrual end date} - \text{accrual start date}}{365}$$

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
- Overnight index swap (OIS) rates are calculated based off of data on executed unsecured lending tranasactions. The index is a notional weighed average, and published as a daily overnight level.
- IBOR vs OIS Index differs where IBOR is an estimate of the future level while OIS is an observation of the past (both are unsecured). There is sometimes a lag between when a rate is fixed and the valuation period (i.e., 2 b.d. lag with EUR)
- Fallback method was requred to continue to settle derivative contracts which settled against IBOR after the cessation, turning the rate from a look-forward rate (IBOR) into a look-back rate (RFR).

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

$$P = - R \sum_{i=1}^{T_1} N_i d_i v_i + \sum_{j=1}^{T_2} N_j d_j r_j v_j$$

Where:

- $T_1, T_2$ = number of periods in the fixed and float leg respectively
- $N$ = notional (for standard IRS), $N_i$ = notional per period (for customised IRS)
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
- Exchange a series of flaoting cashflows, almost exclusively of one index against another (i.e., 3M-IBOR cashflows for 6M-IBOR cashflows)
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

- Similar to STIRutures in that they trade on exchanges in price terms, with margining principles applied, and a single contract is a predetermined notional (typically 0.1mm) set by the exchange
- Standard IMM only settlement days (frequently March, June, September, December), physically settled (parties with open positions at expiry will enter into a OTC IRS)
- In order to complete teh action of settlement at expiry, counterparties either pay or receive an amount of cash to the clearing house dependent upon the EDSP of the contract (final trading price of the contract before expiry)
- IRS futures are not particularly liquid or well traded

Mathematical formulae:

Where a party has bought an IRS future that translates to the duration of receiving fixed on the physically settled IRS. The amount of cash payable to the exchange on settlement of a single contract corresponds to:

$$P = \frac{EDSP - 100}{100} \times {N}$$

Where $N$ is a single contract notional.

Similarly the live price of an IRS future is determined by the market PV of the contract specified IRS (from the point of view of the receiver).

$$q = 100 + 100 \times \frac{P}{N}$$

*Example 3.6:*

A trader buys 10 {USD 0.1mm Z16 10Y SOFRRS 1.5%} IRS futures contracts at a price of 100.00.

The market values and yields fall by 15bps from 1.5% to 1.35% so that the PV of the IRS represented by a single contract is now $1,386. The price of the IRS future is then 101.38 (or quoted in 32nds: 101-12+). To reflect the profit in a simple expression, MTM the exchange credits trader's account with 10 × $1,386 = $13,860. The future expires with an EDSP of the same price and the trader's open position is physically settled. He pays $13,860 to the exchange and enters an IRS for $1mm notional with the clearing house which necessarily possesses a PV of $13,860. The clearing house posts this amount to the trader as collateral.

#### Non-MTM cross-currency swaps (XCSs)

- A non-MTM cross-currency swap (XCS) is a swap similar to single currency bassis swaps, except instead of swapping different tenor indices or different indexes in the same currency, the coutnerparties exchange indexes (usually RFRs) in two different currencies
- To balance the legs so that, at mid-market (at inception), the sum of each is zero, requires a fixed spread (or annuity) to be attached to one of the floating legs (usually the non-USD or least liquid currency). In these examples, the spread is applied to the first currency in a currency pair (i.e., EUR in EUR/USD)
- XCSs involve notional exchange at the start and end of the swap in the two currencies, which in the case of non-MTM XCSs will always be the same value, which is based on an initially agreed FX rate (usually the spot FX at the time of execution)

Mathematical formulae:

The PV of, for examplee, a EUR/USD non-MTM XCS from the POV of the payer of the spread (B in figure 3.4) is:

$$PV = N F_0 w_0^* - NF_0 \sum_{i=1}^{T_1} (r_i^* + Z^*) d_i^* w_i^* - N F_0 w_{T_1}^* - N f_0 v_0 + N f_0 \sum_{j=1}^{T_2} r_j d_j v_j + N f_0 v_{T_2}$$

where $v_i$ represents the discount factor of a USD cashflow and $w_i^*$ the discount factor of the EUR cashflow. $f_0$ represents the FX rate which was fixed at the time of execution and $F_0$ represents the current spot FX rate. $N$ is the notional of the domestic currency where the bp spread is attached, so in this case is in EUR. It is also usual (although not necessary) to assume that $f_0 = F_0$ when pricing a new trade. The rates $r_i^*, r_j$ are determined according to equation 3.1 when RFRs are the leg indexes.

Customization:

- The above describes one of the more common floating-floating swaps, but these are also completely bespoke and can be customized (date schedule. fixing schedule, day count conventions), similar to an IRS
- It is also possible and common to have one or two fixed legs, where in the formula, $r_i^*$ and $r_j$ are replaced by $R^*$ and $R$, creating a swap where coutnerparties exchange a fixed series of payments in one currency for a floating series of payments in another
- Notionals can be varied each period and variable across each leg (ie..e, amortization in case of swaps hedging loans)

Quoting convention:

$\text{'Currencies, Index(es), Start-date, End-date,}$ $\text{Frequency}^1$, $\text{Frequency}^2$, $\text{Fixed/Floating}^1$, $\text{Fixed/Floating,}^2$ $\text{Roll-date, Stub-type, MTM or non-MTM'}$

#### MTM cross-currency swaps (XCSs)

- Most common form of XCS. It is the stardard XCS product traded in the interbank market. It's purpose and difference to non-MTM XCSs is to reduce credit exposure (CE) to counterparties by continually 'resetting' the notional on one leg throughout the length of the swap, in light of fluctuating exchange rates. This mitigates the overall PV of the derivative by restricting the impact of FX fluctuations
- In non-MTM XCSs, FX fluctuations can have a far greater impact on the PV of those derivatives than the actual underlying XCS market prices, and hence the affinity toward MTM XCSs

Mathematical formulae:

The PV of, for example, a EUR/USD MTM XCS from the POV of the payer of the spread is:

$$PV = N F_0 w_0^* - NF_0 \sum_{i=1}^{T_1} (r_i^* + Z^*) d_i^* w_i^* - N F_0 w_{T_1}^* - N f_0 v_0 + N f_0 \sum_{j=1}^{T_2} f_{j-1} r_j d_j v_j + N \sum_{j=1}^{T_2} (f_j-1 - f_j) v_j + N f_{T_2} v_{T_2}$$

It is common that one might seek to determine a mid-market spread, $Z^{*mid}$, for a XCS. To do this, the forecast rates and DFs in each currency need to be obtained from a multi-currency cureveste. The PV can then be set to zero and the formula rearranged in terms of $Z^{*mid}$. The same type of customizations are available as for non-MTM XCSs as are the quoting convetions.

#### FX Swaps

- FX swaps (or currency swaps) are agreements to complete two, offsetting FX exchanges: one exchange on a particular date and a re-exchange at a future date for an agreed price difference
- I.e., one CP may agree to sell EUR100mm for USD at a spot at an exchange rate of 1.2500 and then after one month, purchase EUR100mm from USD at an exchange rate of 1.2480

Mathmatical formulae:

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
- Pensions have an annuity obligation when members retire. To fulfuil this, pension funds invest cash, exchanged for the annuity, into euqities or other securities. If future expectations of interest rates fall then the implicit amount of growth assumed over many years may be insufficient to pay the annuity. Thus, a pension fund may choose to hedge long dated interest rates by receiving fixed on IRSs

#### Central governments

- The treasury and debt management office (DMO) are responsible for public finances. As the DMO raises funds through taxes and sovereign issuance, the latter of which represents a supply of fixed rates, they may want to rate lock their funding by either reciving fixed on an IRS if they believe rates will fall, or paying fixed if they believe rates will rise
- Hedging bonds with IRSs is not a one-for-one hedge, which is known as an asset swap. Asset swaps come with a type of basis risk called asset swap spread risk (not dissimilar to single currency basis risk between two indexes), which is the risk that IRS rates will move more or less than the yields on the bonds to the same respective maturity that they are hedging
- A treasury does not necessarily have to raise money in the domestic currency (can issue in USD), widening its pool of potential investors. In this case, the DMO will want to hedge all market risk exposures so that its overall exposure is to its domestic currency only (usually through a fixed/fixed XCS)

#### Central banks

#### Non-financial corporations (NFCs)

#### Asset managers

#### Hedge funds and speculators

#### Banks

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
