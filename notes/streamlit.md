# Streamlit Frontend Guide

## Overview

Streamlit is a Python framework for building data applications with minimal code. For quantitative finance, Streamlit provides the fastest path from analysis to interactive dashboard, making it ideal for rapid prototyping, internal tools, and proof-of-concept applications.

## What is Streamlit?

Streamlit is a rapid application framework that provides:

- **Pure Python**: No HTML, CSS, or JavaScript required
- **Instant feedback**: Auto-reload on code changes
- **Built-in widgets**: Interactive components out of the box
- **Native charts**: Integration with Plotly, Altair, matplotlib
- **Data-centric**: Designed for data science and analytics
- **Fast development**: Build apps in hours, not weeks

## Why Streamlit for Finance?

### Advantages

- **Speed**: Build dashboards 10x faster than React
- **Python-native**: Reuse existing pricing/analytics code directly
- **No frontend expertise**: Data scientists can build UIs
- **Built-in caching**: Optimize expensive calculations automatically
- **Data tables**: Excellent display for bond portfolios and risk reports
- **Real-time updates**: WebSocket support for live market data

### Trade-offs vs React

| Feature | Streamlit | React + Flask |
|---------|-----------|---------------|
| Development Speed | Very Fast (hours) | Slower (days/weeks) |
| Learning Curve | Low (Python only) | High (JS, TS, React) |
| Customization | Limited | Full control |
| Performance | Good for prototypes | Better for production |
| Mobile Support | Basic | Excellent |
| Use Case | Internal tools, POCs | Production apps |

## Installation

```bash
# Already in requirements.txt
# uv pip install streamlit

# Verify installation
streamlit --version
```

## Basic Streamlit Application

### app.py - Main Application

```python
"""
Streamlit application for bond pricing and portfolio analytics.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decimal import Decimal
from datetime import date, datetime
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import existing pricing libraries
# from curves.nss import nelson_siegel_svensson
# from risk.duration import calculate_modified_duration

# Page configuration
st.set_page_config(
    page_title="Quantitative Finance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Bond Pricer", "Yield Curves", "Portfolio", "Analytics"]
)

# Main content
if page == "Dashboard":
    show_dashboard()
elif page == "Bond Pricer":
    show_bond_pricer()
elif page == "Yield Curves":
    show_yield_curves()
elif page == "Portfolio":
    show_portfolio()
elif page == "Analytics":
    show_analytics()

def show_dashboard():
    """Main dashboard view"""
    st.title("📈 Quantitative Finance Dashboard")
    st.markdown("---")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Portfolio Value",
            value="$10.5M",
            delta="$125K"
        )

    with col2:
        st.metric(
            label="Duration",
            value="5.2",
            delta="-0.3"
        )

    with col3:
        st.metric(
            label="Yield",
            value="4.85%",
            delta="0.12%"
        )

    with col4:
        st.metric(
            label="DV01",
            value="$54,600",
            delta="$1,200"
        )

    st.markdown("---")

    # Recent activity
    st.subheader("Recent Portfolio Changes")

    df_activity = pd.DataFrame({
        'Date': ['2024-10-15', '2024-10-14', '2024-10-13'],
        'Action': ['Buy', 'Sell', 'Buy'],
        'ISIN': ['CA123456789', 'CA987654321', 'CA456789123'],
        'Quantity': [1000000, 500000, 750000],
        'Price': [98.75, 101.25, 99.50]
    })

    st.dataframe(df_activity, use_container_width=True)

if __name__ == "__main__":
    pass  # Streamlit handles execution
```

## Bond Pricing Page

### pages/bond_pricer.py

```python
"""
Bond pricing calculator page.
"""
import streamlit as st
from decimal import Decimal
from datetime import date, timedelta

def show_bond_pricer():
    """Interactive bond pricing calculator"""
    st.title("🧮 Bond Price Calculator")

    st.markdown("""
    Calculate bond prices, yields, and risk metrics for Canadian fixed income securities.
    """)

    # Input form in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bond Characteristics")

        coupon = st.number_input(
            "Coupon Rate (%)",
            min_value=0.0,
            max_value=20.0,
            value=2.5,
            step=0.125,
            format="%.3f"
        ) / 100

        maturity = st.date_input(
            "Maturity Date",
            value=date.today() + timedelta(days=365*5),
            min_value=date.today()
        )

        settlement = st.date_input(
            "Settlement Date",
            value=date.today(),
            max_value=maturity
        )

        frequency = st.selectbox(
            "Payment Frequency",
            options=[1, 2, 4, 12],
            index=1,
            format_func=lambda x: {
                1: "Annual",
                2: "Semi-annual",
                4: "Quarterly",
                12: "Monthly"
            }[x]
        )

        daycount = st.selectbox(
            "Day Count Convention",
            options=["ACT/ACT", "ACT/360", "30/360", "ACT/365"],
            index=0
        )

    with col2:
        st.subheader("Calculation Type")

        calc_type = st.radio(
            "Calculate",
            ["Price from Yield", "Yield from Price"]
        )

        if calc_type == "Price from Yield":
            yield_input = st.number_input(
                "Yield to Maturity (%)",
                min_value=0.0,
                max_value=20.0,
                value=3.0,
                step=0.01,
                format="%.3f"
            ) / 100
        else:
            price_input = st.number_input(
                "Bond Price",
                min_value=0.0,
                max_value=200.0,
                value=95.432,
                step=0.001,
                format="%.4f"
            )

    # Calculate button
    if st.button("Calculate", type="primary"):
        with st.spinner("Calculating..."):
            try:
                if calc_type == "Price from Yield":
                    result = calculate_bond_price(
                        coupon=Decimal(str(coupon)),
                        maturity=maturity,
                        settlement=settlement,
                        yield_rate=Decimal(str(yield_input)),
                        frequency=frequency,
                        daycount=daycount
                    )

                    st.success("Calculation Complete!")

                    # Display results
                    st.markdown("---")
                    st.subheader("Results")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Clean Price",
                            f"{result['price']:.4f}"
                        )

                    with col2:
                        st.metric(
                            "Accrued Interest",
                            f"{result['accrued']:.4f}"
                        )

                    with col3:
                        st.metric(
                            "Dirty Price",
                            f"{result['dirty_price']:.4f}"
                        )

                    # Risk metrics
                    st.markdown("---")
                    st.subheader("Risk Metrics")

                    risk_metrics = calculate_risk_metrics(
                        coupon=Decimal(str(coupon)),
                        maturity=maturity,
                        settlement=settlement,
                        yield_rate=Decimal(str(yield_input)),
                        frequency=frequency
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Modified Duration",
                            f"{risk_metrics['modified_duration']:.2f}"
                        )

                    with col2:
                        st.metric(
                            "Macaulay Duration",
                            f"{risk_metrics['macaulay_duration']:.2f}"
                        )

                    with col3:
                        st.metric(
                            "Convexity",
                            f"{risk_metrics['convexity']:.2f}"
                        )

                    # DV01 calculation
                    par_value = st.number_input(
                        "Par Value for DV01 Calculation",
                        value=1000000,
                        step=100000,
                        format="%d"
                    )

                    dv01 = (par_value / 100) * risk_metrics['modified_duration'] * 0.01
                    st.metric("DV01", f"${dv01:,.2f}")

                else:  # Yield from Price
                    result = calculate_bond_yield(
                        coupon=Decimal(str(coupon)),
                        maturity=maturity,
                        settlement=settlement,
                        price=Decimal(str(price_input)),
                        frequency=frequency,
                        daycount=daycount
                    )

                    st.success("Calculation Complete!")
                    st.metric(
                        "Yield to Maturity",
                        f"{result * 100:.3f}%"
                    )

            except Exception as e:
                st.error(f"Calculation failed: {str(e)}")

    # Information expander
    with st.expander("ℹ️ About Bond Pricing"):
        st.markdown("""
        ### Day Count Conventions
        - **ACT/ACT**: Actual days over actual days (GoC bonds)
        - **ACT/360**: Actual days over 360 (money market)
        - **30/360**: Assumes 30-day months (corporates)
        - **ACT/365**: Actual days over 365 (some swaps)

        ### Payment Frequency
        - **Semi-annual**: Standard for GoC bonds
        - **Annual**: Some corporate bonds
        - **Quarterly/Monthly**: Rare for bonds

        ### Accrued Interest
        Accrued interest is calculated from the last coupon date
        to the settlement date and is paid by the buyer to the seller.
        """)

# Calculation functions (integrate with existing libraries)
def calculate_bond_price(coupon, maturity, settlement, yield_rate, frequency, daycount):
    """Calculate bond price - integrate with existing pricing library"""
    # Placeholder - replace with actual implementation from src/
    return {
        'price': 95.432,
        'accrued': 1.234,
        'dirty_price': 96.666
    }

def calculate_bond_yield(coupon, maturity, settlement, price, frequency, daycount):
    """Calculate yield - integrate with existing library"""
    return 0.030  # 3.0%

def calculate_risk_metrics(coupon, maturity, settlement, yield_rate, frequency):
    """Calculate risk metrics"""
    return {
        'modified_duration': 4.72,
        'macaulay_duration': 4.85,
        'convexity': 28.5
    }
```

## Yield Curve Visualization

### pages/yield_curves.py

```python
"""
Yield curve visualization and fitting page.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

def show_yield_curves():
    """Interactive yield curve viewer"""
    st.title("📊 Yield Curve Analysis")

    # Curve selection
    col1, col2 = st.columns([2, 1])

    with col1:
        curve_type = st.selectbox(
            "Curve Type",
            ["Government of Canada", "Provincial", "Corporate"]
        )

    with col2:
        curve_date = st.date_input(
            "Curve Date",
            value=date.today()
        )

    # Load curve data
    if st.button("Load Curve Data"):
        with st.spinner("Loading curve data..."):
            curve_data = load_curve_data(curve_type, curve_date)

            # Plot curve
            fig = create_curve_chart(curve_data)
            st.plotly_chart(fig, use_container_width=True)

            # Data table
            st.subheader("Curve Data")
            df = pd.DataFrame({
                'Tenor': curve_data['tenors'],
                'Yield (%)': [y * 100 for y in curve_data['yields']]
            })
            st.dataframe(df, use_container_width=True)

    # Curve fitting section
    st.markdown("---")
    st.subheader("Curve Fitting")

    fitting_method = st.selectbox(
        "Fitting Method",
        ["Nelson-Siegel-Svensson", "Cubic Spline", "Linear Interpolation"]
    )

    if st.button("Fit Curve"):
        with st.spinner("Fitting curve..."):
            fitted_params = fit_curve(curve_data, fitting_method)

            st.success("Curve fitted successfully!")

            # Display parameters
            if fitting_method == "Nelson-Siegel-Svensson":
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("β₀", f"{fitted_params['beta0']:.4f}")
                    st.metric("β₁", f"{fitted_params['beta1']:.4f}")

                with col2:
                    st.metric("β₂", f"{fitted_params['beta2']:.4f}")
                    st.metric("β₃", f"{fitted_params['beta3']:.4f}")

                with col3:
                    st.metric("τ₁", f"{fitted_params['tau1']:.4f}")
                    st.metric("τ₂", f"{fitted_params['tau2']:.4f}")

            st.metric("RMSE", f"{fitted_params['rmse']:.6f}")

def create_curve_chart(curve_data):
    """Create interactive yield curve chart"""
    fig = go.Figure()

    # Actual data points
    fig.add_trace(go.Scatter(
        x=curve_data['tenors'],
        y=[y * 100 for y in curve_data['yields']],
        mode='markers+lines',
        name='Actual',
        marker=dict(size=8, color='blue'),
        line=dict(color='blue', width=2)
    ))

    # If fitted curve available
    if 'fitted_yields' in curve_data:
        fig.add_trace(go.Scatter(
            x=curve_data['tenors'],
            y=[y * 100 for y in curve_data['fitted_yields']],
            mode='lines',
            name='Fitted',
            line=dict(color='red', width=2, dash='dash')
        ))

    fig.update_layout(
        title="Yield Curve",
        xaxis_title="Tenor (years)",
        yaxis_title="Yield (%)",
        hovermode='x unified',
        template='plotly_white'
    )

    return fig

def load_curve_data(curve_type, curve_date):
    """Load curve data - integrate with existing data sources"""
    # Placeholder - replace with actual data loading
    return {
        'tenors': [0.25, 0.5, 1, 2, 5, 10, 30],
        'yields': [0.045, 0.046, 0.0475, 0.049, 0.051, 0.053, 0.055]
    }

def fit_curve(data, method):
    """Fit curve using specified method"""
    # Placeholder - integrate with existing curve fitting libraries
    return {
        'beta0': 0.055,
        'beta1': -0.010,
        'beta2': -0.005,
        'beta3': 0.002,
        'tau1': 2.5,
        'tau2': 10.0,
        'rmse': 0.00012
    }
```

## Portfolio Management

### pages/portfolio.py

```python
"""
Portfolio management and optimization page.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

def show_portfolio():
    """Portfolio management dashboard"""
    st.title("💼 Portfolio Management")

    # Portfolio summary
    st.subheader("Portfolio Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Value", "$10.5M")
    with col2:
        st.metric("Duration", "5.2")
    with col3:
        st.metric("Avg Yield", "4.85%")
    with col4:
        st.metric("Positions", "12")

    # Holdings table
    st.markdown("---")
    st.subheader("Holdings")

    df_holdings = pd.DataFrame({
        'ISIN': ['CA123456789', 'CA987654321', 'CA456789123'],
        'Issuer': ['Government of Canada', 'Ontario', 'Toronto-Dominion Bank'],
        'Coupon': [2.5, 3.0, 4.25],
        'Maturity': ['2030-12-15', '2028-06-02', '2029-09-20'],
        'Quantity': [1000000, 1500000, 750000],
        'Price': [98.75, 101.25, 99.50],
        'Market Value': [987500, 1518750, 746250],
        'Weight (%)': [32.5, 50.0, 24.5],
        'Duration': [5.2, 4.8, 5.5]
    })

    # Add selection column
    df_display = df_holdings.copy()
    df_display.insert(0, 'Select', False)

    # Editable dataframe
    edited_df = st.data_editor(
        df_display,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select"),
            "Market Value": st.column_config.NumberColumn(
                "Market Value",
                format="$%d"
            ),
            "Weight (%)": st.column_config.NumberColumn(
                "Weight (%)",
                format="%.1f%%"
            )
        }
    )

    # Portfolio actions
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Analyze Risk"):
            st.info("Risk analysis feature coming soon")

    with col2:
        if st.button("⚖️ Optimize"):
            st.info("Portfolio optimization feature coming soon")

    with col3:
        if st.button("📈 Backtest"):
            st.info("Backtesting feature coming soon")

    # Portfolio allocation chart
    st.markdown("---")
    st.subheader("Allocation by Issuer")

    fig = px.pie(
        df_holdings,
        values='Market Value',
        names='Issuer',
        title='Portfolio Allocation'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Duration distribution
    st.subheader("Duration Distribution")

    fig = px.bar(
        df_holdings,
        x='Issuer',
        y='Duration',
        color='Duration',
        title='Duration by Position'
    )
    st.plotly_chart(fig, use_container_width=True)
```

## Data Caching for Performance

```python
"""
Caching strategies for expensive operations.
"""
import streamlit as st
import pandas as pd

@st.cache_data(ttl=900)  # Cache for 15 minutes
def load_market_data(date):
    """Load market data with caching"""
    # Expensive database query
    return pd.read_sql(f"SELECT * FROM market_data WHERE date = '{date}'", conn)

@st.cache_data
def calculate_yield_curve(tenors, yields):
    """Cache curve fitting results"""
    # Expensive curve fitting operation
    return fit_nelson_siegel_svensson(tenors, yields)

@st.cache_resource
def get_database_connection():
    """Cache database connection"""
    import duckdb
    return duckdb.connect('/Users/nattechan/src/finance/data/market_data.duckdb')
```

## File Upload and Download

```python
"""
File upload and download functionality.
"""
import streamlit as st
import pandas as pd
import io

def upload_portfolio():
    """Upload portfolio from CSV"""
    uploaded_file = st.file_uploader(
        "Upload Portfolio (CSV)",
        type=['csv'],
        help="Upload a CSV file with ISIN, Quantity columns"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df)} positions")
        st.dataframe(df, use_container_width=True)
        return df

    return None

def download_results(df):
    """Download results as CSV or Excel"""
    col1, col2 = st.columns(2)

    with col1:
        # CSV download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="portfolio_analysis.csv",
            mime="text/csv"
        )

    with col2:
        # Excel download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        st.download_button(
            label="Download Excel",
            data=buffer.getvalue(),
            file_name="portfolio_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
```

## Real-time Updates with WebSocket

```python
"""
Real-time market data updates.
"""
import streamlit as st
import asyncio
import websockets

async def subscribe_to_market_data():
    """Subscribe to real-time market data"""
    uri = "ws://localhost:5000/ws/market_data"

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            # Update Streamlit state
            st.session_state.market_data = message

# In main app
if 'market_data' not in st.session_state:
    st.session_state.market_data = None

# Display real-time data
if st.session_state.market_data:
    st.json(st.session_state.market_data)
```

## Running Streamlit Applications

### Development Mode

```bash
# Activate environment
source /Users/nattechan/src/venv/bin/activate

# Run Streamlit app
streamlit run app.py

# Runs on http://localhost:8501
```

### Production Deployment

```bash
# Run on specific port
streamlit run app.py --server.port 8080

# With custom config
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

### Configuration File

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## Deployment Options

### Option 1: Streamlit Cloud (Free)

```bash
# Push to GitHub
git push origin main

# Deploy on streamlit.io
# Connect GitHub repo
```

### Option 2: Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Best Practices

### 1. Session State Management

```python
# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Update state
st.session_state.portfolio.append(new_position)

# Access state
current_portfolio = st.session_state.portfolio
```

### 2. Error Handling

```python
try:
    result = expensive_calculation()
    st.success("Calculation complete!")
    st.write(result)
except ValueError as e:
    st.error(f"Invalid input: {str(e)}")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.exception(e)  # Show full traceback in debug mode
```

### 3. Progress Indicators

```python
with st.spinner("Calculating..."):
    time.sleep(2)  # Long operation

# Or with progress bar
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)
```

### 4. Data Validation

```python
def validate_inputs(coupon, maturity, settlement):
    """Validate user inputs"""
    errors = []

    if coupon < 0 or coupon > 1:
        errors.append("Coupon must be between 0% and 100%")

    if settlement >= maturity:
        errors.append("Settlement must be before maturity")

    return errors

errors = validate_inputs(coupon, maturity, settlement)
if errors:
    for error in errors:
        st.error(error)
else:
    # Proceed with calculation
    pass
```

## Integration with Flask Backend

```python
"""
Call Flask API from Streamlit.
"""
import streamlit as st
import requests

API_BASE_URL = "http://localhost:5000/api"

@st.cache_data(ttl=300)
def get_bond_price(params):
    """Call Flask API for bond pricing"""
    response = requests.post(f"{API_BASE_URL}/bonds/price", json=params)
    response.raise_for_status()
    return response.json()

# In Streamlit app
if st.button("Calculate"):
    try:
        result = get_bond_price({
            'coupon': coupon,
            'maturity': maturity.isoformat(),
            'settlement': settlement.isoformat(),
            'yield': yield_input
        })
        st.success("Calculation complete!")
        st.write(result)
    except requests.exceptions.HTTPError as e:
        st.error(f"API error: {e}")
```

## When to Choose Streamlit vs React

### Choose Streamlit When:

- Building internal tools for quant teams
- Creating proof-of-concept dashboards
- Rapid prototyping of analytics
- Python-only team without frontend expertise
- Focus on data analysis over UI polish
- Need to deploy quickly (hours/days)

### Choose React + Flask When:

- Building client-facing applications
- Need pixel-perfect custom design
- High performance requirements
- Mobile app needed
- Complex user interactions
- Long-term production application

### Hybrid Approach:

1. **Start with Streamlit** for rapid prototyping
2. **Test with users** to validate functionality
3. **Migrate to React** if needed for production

## Resources

### Official Documentation

- Streamlit: <https://docs.streamlit.io/>
- Streamlit Gallery: <https://streamlit.io/gallery>
- Plotly: <https://plotly.com/python/>

### Related Guides

- **Flask Backend**: See `notes/flask.md` for API integration
- **React Frontend**: See `notes/react.md` for production UIs
- **Deployment**: Streamlit Cloud, Docker, AWS

---

**Last Updated**: 2025-10-15
**Python Environment**: `/Users/nattechan/src/venv`
**Streamlit Version**: 1.50+
