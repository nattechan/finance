# Finance Project - Context & Configuration

This project-specific CLAUDE.md file supplements the global configuration at `~/.claude/CLAUDE.md`.

## Project Overview

**Purpose**: Quantitative finance analytics and trading system for Canadian fixed income markets

**Tech Stack**:

- Python 3.11 (`/Users/nattechan/src/venv`)
- DuckDB for data storage and querying
- Polars for data transformations
- QuantLib for derivatives pricing
- xbbg for Bloomberg integration

## Current Focus Areas

### Active Development

1. **Yield Curve Modeling**
   - Nelson-Siegel-Svensson fitting for GoC curves
   - Cubic spline interpolation for corporate bonds
   - Multi-curve framework for derivatives

2. **Portfolio Optimization**
   - CVXPY-based optimization engine
   - Duration-neutral strategies
   - Credit spread maximization

3. **Risk Analytics**
   - Key rate duration calculations
   - Credit spread risk attribution
   - Scenario analysis and stress testing

### Planned Features

- [ ] Inflation swap pricing module
- [ ] MBS prepayment modeling
- [ ] Real-time risk dashboard with Streamlit
- [ ] Backtesting framework integration

## Data Sources & Locations

### Market Data

- **Bloomberg**: Via xbbg package
  - Bond prices: `PX_LAST`, `YLD_YTM_MID`
  - Swap rates: `SWAP_RATE_MID`
  - FX rates: `PX_LAST` for currency pairs

- **Local Databases**:
  - Market data: `/Users/nattechan/src/finance/data/market_data.duckdb`
  - Historical prices: `/Users/nattechan/src/finance/data/bond_prices.parquet`
  - Risk reports: `/Users/nattechan/src/finance/data/risk.duckdb`

### Static Data

- Bond master: `/Users/nattechan/src/finance/data/bond_master.csv`
- Calendar definitions: `/Users/nattechan/src/finance/data/calendars/`
- Curve configurations: `/Users/nattechan/src/finance/config/curves.yaml`

## Project Structure

```text
/Users/nattechan/src/finance/
├── src/
│   ├── curves/           # Yield curve construction
│   │   ├── nss.py        # Nelson-Siegel-Svensson
│   │   ├── spline.py     # Cubic spline
│   │   └── bootstrap.py  # QuantLib bootstrap
│   ├── portfolio/        # Portfolio optimization
│   │   ├── optimizer.py  # CVXPY optimization
│   │   └── constraints.py
│   ├── risk/            # Risk calculations
│   │   ├── duration.py   # Duration analytics
│   │   ├── convexity.py
│   │   └── scenarios.py  # Stress testing
│   ├── data/            # Data loaders and ETL
│   │   ├── bloomberg.py  # xbbg integration
│   │   ├── duckdb_ops.py # DuckDB utilities
│   │   └── validators.py # Data quality
│   └── utils/           # Shared utilities
│       ├── calendar.py   # Business day logic
│       ├── daycount.py   # Day count conventions
│       └── cashflows.py  # Cash flow generation
├── tests/               # Unit tests
├── notebooks/           # Jupyter analysis
├── data/               # Local data storage
└── config/             # Configuration files
```

## Key Conventions

### Canadian Fixed Income Markets

**Government Bonds (GoC)**:

- Day count: ACT/ACT
- Settlement: T+1
- Coupon: Semi-annual
- Holidays: Canadian banking calendar
- Benchmark tenors: 2Y, 5Y, 10Y, 30Y

**Corporate Bonds**:

- Day count: 30/360 (most common) or ACT/ACT
- Settlement: T+2
- Coupon: Semi-annual or annual
- Quotes: Price or spread over GoC

**Interest Rate Swaps**:

- Day count: ACT/365 (fixed), ACT/365 (float)
- Settlement: T+2
- Frequency: Semi-annual (fixed), varies (float)
- Index: CORRA (replacing CDOR)

### Code Conventions

**Pricing Functions**:

```python
def price_bond(
    coupon: Decimal,
    maturity: date,
    settlement: date,
    yield_rate: Decimal,
    frequency: int = 2,
    daycount: str = "ACT/ACT"
) -> Decimal:
    """
    Price a Canadian government bond.

    Args:
        coupon: Annual coupon rate (e.g., Decimal("0.0250") for 2.5%)
        maturity: Bond maturity date
        settlement: Settlement date (T+1 for GoC)
        yield_rate: Yield to maturity
        frequency: Coupon payments per year (2 for semi-annual)
        daycount: Day count convention

    Returns:
        Bond price per 100 of face value
    """
```

**Risk Functions**:

```python
def calculate_duration(
    bond: Bond,
    yield_curve: YieldCurve,
    duration_type: Literal["macaulay", "modified", "key_rate"] = "modified"
) -> Union[float, Dict[str, float]]:
    """
    Calculate bond duration.

    Returns modified duration by default, or dict of key rate durations.
    """
```

## Testing Standards

### Required Tests

1. **Financial Calculations**
   - Compare against QuantLib benchmarks
   - Validate with known market prices
   - Test edge cases (zero rates, flat curves)

2. **Data Quality**
   - Mock Bloomberg responses
   - Test missing data handling
   - Validate data type conversions

3. **Performance**
   - Benchmark critical calculations
   - Test with realistic data sizes
   - Memory profiling for large portfolios

### Test Data Locations

- Mock market data: `/tests/fixtures/market_data.json`
- QuantLib benchmarks: `/tests/fixtures/quantlib_benchmarks.csv`
- Test bonds: `/tests/fixtures/test_bonds.yaml`

## Environment Setup

### Activate Environment

```bash
source /Users/nattechan/src/venv/bin/activate
```

### Install Dependencies

```bash
# Always use uv pip, never standard pip
uv pip install -r requirements.txt
```

### Environment Variables

```bash
# Set in ~/.claude/.env (already configured)
ANTHROPIC_API_KEY=<set>
BRAVE_API_KEY=<set>
GITHUB_API_KEY=<set>

# Bloomberg terminal must be running for xbbg
```

## Common Workflows

### Adding a New Financial Product

1. **Research phase**:

   ```bash
   /agent-research "Research [product] pricing conventions for Canadian markets"
   ```

2. **Implementation**:
   - Create product class in `src/products/`
   - Add pricing function in `src/pricing/`
   - Implement risk calculations in `src/risk/`

3. **Testing**:
   - Write unit tests with QuantLib benchmarks
   - Add integration tests with mock data
   - Run `/agent-validate src/products/new_product.py`

4. **Documentation**:
   - Update this CLAUDE.md with conventions
   - Add examples to notebooks/
   - Document in product class docstring

### Running Backtests

```bash
/backtest "Bond momentum strategy on Canadian corporates 2020-2024"
```

### Fitting Yield Curves

```bash
/curve-fit "GoC curve as of 2024-09-29 using NSS"
```

### Pre-commit Validation

```bash
/pre-commit-check "Validate src/curves/ before committing"
```

## Performance Optimization Notes

### DuckDB Usage

- Use for all aggregations and joins
- Query market data instead of loading into Pandas
- Export to Polars for downstream calculations

### Vectorization

- NumPy operations for price/yield calculations
- Polars for data transformations
- Avoid Python loops on bond portfolios

### Caching Strategy

- Cache yield curves (15-minute TTL)
- Cache Bloomberg data (until market close)
- Invalidate on new data arrival

## Known Issues & Limitations

1. **Bloomberg Dependency**
   - Requires Bloomberg terminal running
   - Rate limits: ~10 requests/second
   - Some fields not available for all securities

2. **Calendar Handling**
   - Canadian holiday calendar hardcoded
   - Need to update annually for new holidays
   - Provincial holidays not fully supported

3. **Performance**
   - Large portfolio optimization (>1000 bonds) slow
   - Need to implement parallel processing
   - Memory usage high for Monte Carlo (>10k paths)

## Reference Links

### Online Resources

- **QuantLib Python**: <https://quantlib-python-docs.readthedocs.io/>
- **QuantLib Guide**: <https://www.quantlibguide.com/>
- **rateslib Documentation**: <https://rateslib.com/py/en/latest/index.html>
- **xbbg Documentation**: <https://github.com/alpha-xone/xbbg>
- **CORRA Information**: <https://www.bankofcanada.ca/rates/interest-rates/corra/>
- **IIROC Bond Rules**: <https://www.iiroc.ca/>
- **OSFI Guidelines**: <https://www.osfi-bsif.gc.ca/>

### Local Reference Documents

- **Interest Rate Instruments & Market Conventions**: `reference/Interest-Rate-Instruments-and-Market-Conventions.pdf`
  - Day count conventions (ACT/ACT, ACT/360, 30/360, ACT/365)
  - Settlement conventions by market and instrument type
  - Business day adjustment rules and calendar handling
  - Coupon frequency and payment date conventions
  - Benchmark instrument specifications
  - Use this reference when implementing or validating market conventions

- **QuantLib Python Cookbook**: `reference/quantlibpythoncookbook.pdf`
  - Comprehensive examples for yield curve construction
  - Bond pricing, swap pricing, and derivative valuation
  - Date handling, calendars, and day count conventions
  - Greeks calculation and risk analytics
  - Numerical methods and optimization techniques
  - Use this reference when implementing QuantLib-based pricing engines

## Questions or Issues?

- Check global configuration: `~/.claude/CLAUDE.md`
- Review custom commands: `~/.claude/commands/`
- Run project status: `/project-status`
- Research with agent: `/agent-research "your question"`

---

**Last Updated**: 2025-09-29
**Maintainer**: Financial Engineering Team
**Python Environment**: `/Users/nattechan/src/venv`
