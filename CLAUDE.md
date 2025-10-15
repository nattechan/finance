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

**Frontend/Backend Options**:

- **Backend**: Flask REST API (see `notes/flask.md`)
- **Frontend**: React with TypeScript (see `notes/react.md`)
- **Rapid Prototyping**: Streamlit (see `notes/streamlit.md`)

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
├── backend/            # Flask REST API (see notes/flask.md)
│   ├── app.py          # Flask application factory
│   ├── config.py       # Configuration settings
│   ├── api/            # API endpoints
│   │   ├── bonds.py    # Bond pricing endpoints
│   │   ├── curves.py   # Yield curve endpoints
│   │   ├── portfolio.py # Portfolio optimization
│   │   └── risk.py     # Risk calculation endpoints
│   ├── services/       # Business logic layer
│   │   ├── pricing_service.py
│   │   ├── curve_service.py
│   │   └── risk_service.py
│   └── tests/          # Backend API tests
├── frontend/           # React UI (see notes/react.md)
│   ├── src/
│   │   ├── api/        # API client integration
│   │   ├── components/ # React components
│   │   │   ├── bonds/
│   │   │   ├── curves/
│   │   │   └── portfolio/
│   │   ├── pages/      # Page components
│   │   ├── hooks/      # Custom React hooks
│   │   ├── store/      # State management (Zustand)
│   │   └── types/      # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── streamlit_app.py    # Streamlit dashboard (see notes/streamlit.md)
├── src/                # Core pricing libraries
│   ├── curves/         # Yield curve construction
│   │   ├── nss.py      # Nelson-Siegel-Svensson
│   │   ├── spline.py   # Cubic spline
│   │   └── bootstrap.py # QuantLib bootstrap
│   ├── portfolio/      # Portfolio optimization
│   │   ├── optimizer.py # CVXPY optimization
│   │   └── constraints.py
│   ├── risk/           # Risk calculations
│   │   ├── duration.py # Duration analytics
│   │   ├── convexity.py
│   │   └── scenarios.py # Stress testing
│   ├── data/           # Data loaders and ETL
│   │   ├── bloomberg.py # xbbg integration
│   │   ├── duckdb_ops.py # DuckDB utilities
│   │   └── validators.py # Data quality
│   └── utils/          # Shared utilities
│       ├── calendar.py # Business day logic
│       ├── daycount.py # Day count conventions
│       └── cashflows.py # Cash flow generation
├── tests/              # Unit tests
├── notebooks/          # Jupyter analysis
├── data/               # Local data storage
├── config/             # Configuration files
├── notes/              # Documentation and guides
│   ├── flask.md        # Flask backend guide
│   ├── react.md        # React frontend guide
│   └── streamlit.md    # Streamlit rapid prototyping guide
└── reference/          # Reference materials
    ├── QuantFinance/   # Git submodule: Quant finance library
    ├── Orderbook/      # Git submodule: Order book implementation
    ├── Quant-Developers-Resources/  # Git submodule: Learning resources
    ├── books/          # PDF books and documentation
    └── notes/          # Notes organized by topic/submodule
        ├── QuantFinance/
        ├── Orderbook/
        └── Quant-Developers-Resources/
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

## Frontend/Backend Architecture

### Overview

The project supports three frontend/backend approaches, each suited for different use cases:

1. **Flask + React** (Production-grade web application)
2. **Streamlit** (Rapid prototyping and internal tools)
3. **Jupyter Notebooks** (Ad-hoc analysis)

### Flask Backend

Flask provides a RESTful API for bond pricing, curve fitting, and portfolio optimization.

**Key Features**:

- RESTful API design with blueprints
- Integration with existing `src/` pricing libraries
- CORS support for React frontend
- DuckDB integration for data queries
- Comprehensive error handling and validation

**See**: `notes/flask.md` for complete setup guide

**Quick Start**:

```bash
# Install dependencies
uv pip install flask flask-cors flask-sqlalchemy

# Run development server
python backend/app.py
# API available at http://localhost:5000
```

**API Endpoints**:

- `POST /api/bonds/price` - Calculate bond price from yield
- `POST /api/bonds/yield` - Calculate yield from price
- `POST /api/bonds/duration` - Calculate duration and convexity
- `GET /api/curves/goc` - Get GoC yield curve
- `POST /api/curves/fit/nss` - Fit Nelson-Siegel-Svensson model
- `POST /api/portfolio/optimize` - Optimize portfolio

### React Frontend

React provides a modern, interactive user interface with TypeScript support.

**Key Features**:

- Component-based architecture
- TypeScript for type safety
- Recharts/Plotly for financial charts
- Zustand for state management
- Axios for API integration

**See**: `notes/react.md` for complete setup guide

**Quick Start**:

```bash
# Create React app with Vite
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install

# Install dependencies
npm install recharts axios zustand

# Run development server
npm run dev
# UI available at http://localhost:5173
```

**Key Components**:

- `BondPricer.tsx` - Interactive bond pricing calculator
- `YieldCurveChart.tsx` - Yield curve visualization
- `PortfolioOptimizer.tsx` - Portfolio optimization interface
- `RiskMetrics.tsx` - Risk analytics dashboard

### Streamlit Dashboard

Streamlit provides the fastest path from analysis to dashboard, ideal for internal tools and prototyping.

**Key Features**:

- Pure Python (no HTML/CSS/JS)
- Built-in widgets and charts
- Auto-reload on code changes
- Direct integration with existing pricing libraries
- Built-in caching for performance

**See**: `notes/streamlit.md` for complete setup guide

**Quick Start**:

```bash
# Already installed in requirements.txt
# Create Streamlit app
touch streamlit_app.py

# Run Streamlit
streamlit run streamlit_app.py
# Dashboard available at http://localhost:8501
```

**Use Cases**:

- Rapid prototyping of analytics
- Internal quant team dashboards
- Proof-of-concept applications
- One-off analysis tools

### Choosing the Right Approach

| Requirement | Flask + React | Streamlit | Jupyter |
|-------------|---------------|-----------|---------|
| Development Speed | Slow (days/weeks) | Fast (hours) | Fastest (minutes) |
| Customization | Full control | Limited | N/A |
| Production Ready | Yes | Yes (internal) | No |
| Mobile Support | Excellent | Basic | None |
| Learning Curve | High (JS/TS) | Low (Python) | Lowest |
| Use Case | Client-facing | Internal tools | Analysis |

**Recommendation**:

- Start with **Streamlit** for rapid prototyping
- Migrate to **React + Flask** for production client-facing apps
- Use **Jupyter** for ad-hoc analysis and research

### Integration Architecture

```text
┌─────────────────────────────────────────────────┐
│                 Frontend Layer                   │
├─────────────┬───────────────┬───────────────────┤
│   React UI  │  Streamlit    │  Jupyter Notebook │
│ (Port 5173) │  (Port 8501)  │  (Port 8888)      │
└──────┬──────┴───────┬───────┴────────┬──────────┘
       │              │                │
       │ HTTP/REST    │ HTTP           │ Direct Import
       │              │                │
┌──────▼──────────────▼────────────────▼──────────┐
│            Flask Backend (Port 5000)             │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │          API Endpoints Layer            │    │
│  │  /api/bonds  /api/curves  /api/portfolio│    │
│  └────────────────┬────────────────────────┘    │
│                   │                              │
│  ┌────────────────▼────────────────────────┐    │
│  │         Services Layer                  │    │
│  │  pricing_service.py  curve_service.py   │    │
│  └────────────────┬────────────────────────┘    │
│                   │                              │
└───────────────────┼──────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────┐
│              Core Pricing Libraries (src/)       │
│                                                  │
│  curves/  portfolio/  risk/  data/  utils/      │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  QuantLib, rateslib, CVXPY integration   │   │
│  └──────────────────┬───────────────────────┘   │
└─────────────────────┼───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│              Data Layer                          │
│                                                  │
│  DuckDB  │  Parquet  │  Bloomberg (xbbg)        │
└──────────────────────────────────────────────────┘
```

### Development Workflow

1. **Prototype** in Streamlit to validate functionality
2. **Implement** core logic in `src/` libraries
3. **Expose** via Flask API for production use
4. **Build** React UI for client-facing application
5. **Test** with automated tests at each layer

### Documentation References

- **Flask Backend Setup**: `notes/flask.md`
- **React Frontend Setup**: `notes/react.md`
- **Streamlit Dashboard**: `notes/streamlit.md`

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

### Reference Code Repositories (Git Submodules)

- **QuantFinance**: `reference/QuantFinance/`
  - Python-based quantitative finance library
  - Implementations of financial models and algorithms
  - Notes: `reference/notes/QuantFinance/`
  - Repository: <https://github.com/PythonCharmers/QuantFinance>

- **Orderbook**: `reference/Orderbook/`
  - Order book implementation and market microstructure tools
  - Limit order book simulation and analysis
  - Notes: `reference/notes/Orderbook/`
  - Repository: <https://github.com/Tzadiko/Orderbook>

- **Quant-Developers-Resources**: `reference/Quant-Developers-Resources/`
  - Curated collection of quantitative finance resources
  - Learning materials, libraries, and best practices
  - Notes: `reference/notes/Quant-Developers-Resources/`
  - Repository: <https://github.com/cybergeekgyan/Quant-Developers-Resources>

**Submodule Management**:

```bash
# Clone with submodules
git clone --recursive <repo-url>

# Update all submodules to latest
git submodule update --remote --merge

# Initialize submodules in existing clone
git submodule update --init --recursive
```

## Questions or Issues?

- Check global configuration: `~/.claude/CLAUDE.md`
- Review custom commands: `~/.claude/commands/`
- Run project status: `/project-status`
- Research with agent: `/agent-research "your question"`

---

**Last Updated**: 2025-10-14
**Maintainer**: Financial Engineering Team
**Python Environment**: `/Users/nattechan/src/venv`
