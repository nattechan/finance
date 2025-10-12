# Pricing and Trading Interest Rate Derivatives Notes

## Reading from: `Pricing and Trading Interest Rate Derivatives - A Practical Guide to Swaps 3E by J H M Darbyshire`

### Original Code Repository Location

- Notebook: `../book_irds3/notebooks/`
- Library: `../book_irds3/bookirds/`

### My Code

See `reference/notes/book_irds3/python_notes.ipynb` for my learning implementation.

### Preface

#### Guiding questions

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

```text
Annualized rate = (1 + PAr / f)^f - 1

PAr = Per Annum rate
f = frequency
```

#### Continuous compounding

```text
e^(DCF * CCr) = 1 + DCF * PAR

DCF = Discount Factor
CCr = Continuously Compounded rate
```

CCr are useful in derivations for financial mathematics but have limited practical use

#### Time value of money and discount factors (DFs)

No arbitrage pricing (equivalent financial scenarios should have identical values and prices)

#### Interest rate indexes

- For various currencies, there are central bank rates and overnight indexes and risk free rates (i.e., in USD, the Federal Reserve dictates the discount rate and federal funds target rate, while the ). The former is central bank dependent and the latter is market dependent and transaction based.
- Overnight index swap (OIS) rates are calculated based off of data on executed unsecured lending tranasactions. The index is a notional weighed average, and published as a daily overnight level.
- IBOR vs OIS Index differs where IBOR is an estimate of the future level while OIS is an observation of the past (both are unsecured). There is sometimes a lag between when a rate is fixed and the valuation period (i.e., 2 b.d. lag with EUR)
- Fallback method was requred to continue to settle derivative contracts which settled against IBOR after the cessation, turning the rate from a look-forward rate (IBOR) into a look-back rate (RFR).

### Chapter 3 - Basics of IRDs

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
