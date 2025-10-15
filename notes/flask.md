# Flask Backend Guide

## Overview

Flask is a lightweight WSGI web application framework written in Python. It's designed to make getting started quick and easy, with the ability to scale up to complex applications. For quantitative finance applications, Flask serves as an excellent backend framework for serving financial data, running analytics, and providing APIs.

## What is Flask?

Flask is a micro web framework that provides:

- **Lightweight core**: Minimal boilerplate, easy to understand
- **Extensible**: Add functionality through extensions (Flask-SQLAlchemy, Flask-CORS, etc.)
- **RESTful**: Built-in support for REST API development
- **Template engine**: Jinja2 for server-side rendering (optional)
- **Development server**: Built-in server for rapid development
- **Production-ready**: Deploy with WSGI servers (Gunicorn, uWSGI)

## Installation

```bash
# Always use uv pip in this project
uv pip install flask flask-cors flask-sqlalchemy
```

## Project Structure for Finance Application

```text
/Users/nattechan/src/finance/
├── backend/
│   ├── app.py                  # Flask application factory
│   ├── config.py               # Configuration settings
│   ├── requirements.txt        # Backend dependencies
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── bonds.py            # Bond pricing endpoints
│   │   ├── curves.py           # Yield curve endpoints
│   │   ├── portfolio.py        # Portfolio optimization
│   │   └── risk.py             # Risk calculation endpoints
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── bond.py
│   │   └── portfolio.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── pricing_service.py
│   │   ├── curve_service.py
│   │   └── risk_service.py
│   ├── utils/                  # Utilities
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── serializers.py
│   └── tests/                  # Backend tests
│       ├── test_api.py
│       └── test_services.py
└── src/                        # Existing pricing libraries
    ├── curves/
    ├── portfolio/
    └── risk/
```

## Basic Flask Application

### app.py - Application Factory Pattern

```python
"""
Flask application factory for quantitative finance API.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from decimal import Decimal
import os

def create_app(config_name='development'):
    """
    Create and configure Flask application.

    Args:
        config_name: Configuration environment (development, production, testing)

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    # Enable CORS for React frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Register blueprints
    from api.bonds import bonds_bp
    from api.curves import curves_bp
    from api.portfolio import portfolio_bp
    from api.risk import risk_bp

    app.register_blueprint(bonds_bp, url_prefix='/api/bonds')
    app.register_blueprint(curves_bp, url_prefix='/api/curves')
    app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
    app.register_blueprint(risk_bp, url_prefix='/api/risk')

    # Custom JSON encoder for Decimal
    from flask.json.provider import DefaultJSONProvider

    class DecimalJSONProvider(DefaultJSONProvider):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            return super().default(obj)

    app.json = DecimalJSONProvider(app)

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'finance-api'}), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### config.py - Configuration Management

```python
"""
Configuration settings for Flask application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False

    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/data/finance.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DuckDB path for market data
    DUCKDB_PATH = BASE_DIR / "data" / "market_data.duckdb"

    # Bloomberg settings
    BLOOMBERG_ENABLED = os.environ.get('BLOOMBERG_ENABLED', 'false').lower() == 'true'

    # API settings
    API_RATE_LIMIT = "100 per minute"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    ENV = 'production'

    # Production should use environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

## API Endpoints Examples

### api/bonds.py - Bond Pricing API

```python
"""
Bond pricing and analytics API endpoints.
"""
from flask import Blueprint, request, jsonify
from decimal import Decimal
from datetime import datetime, date
from services.pricing_service import PricingService

bonds_bp = Blueprint('bonds', __name__)
pricing_service = PricingService()

@bonds_bp.route('/price', methods=['POST'])
def calculate_bond_price():
    """
    Calculate bond price given yield.

    Request body:
    {
        "coupon": 0.025,
        "maturity": "2030-12-15",
        "settlement": "2024-10-15",
        "yield": 0.030,
        "frequency": 2,
        "daycount": "ACT/ACT"
    }

    Returns:
    {
        "price": 95.432,
        "accrued_interest": 1.234,
        "dirty_price": 96.666
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required = ['coupon', 'maturity', 'settlement', 'yield']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400

        # Parse dates
        maturity = datetime.fromisoformat(data['maturity']).date()
        settlement = datetime.fromisoformat(data['settlement']).date()

        # Calculate price
        result = pricing_service.price_bond(
            coupon=Decimal(str(data['coupon'])),
            maturity=maturity,
            settlement=settlement,
            yield_rate=Decimal(str(data['yield'])),
            frequency=data.get('frequency', 2),
            daycount=data.get('daycount', 'ACT/ACT')
        )

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Calculation failed: {str(e)}'}), 500

@bonds_bp.route('/yield', methods=['POST'])
def calculate_bond_yield():
    """
    Calculate yield given bond price.

    Request body:
    {
        "coupon": 0.025,
        "maturity": "2030-12-15",
        "settlement": "2024-10-15",
        "price": 95.432,
        "frequency": 2,
        "daycount": "ACT/ACT"
    }
    """
    try:
        data = request.get_json()

        result = pricing_service.calculate_yield(
            coupon=Decimal(str(data['coupon'])),
            maturity=datetime.fromisoformat(data['maturity']).date(),
            settlement=datetime.fromisoformat(data['settlement']).date(),
            price=Decimal(str(data['price'])),
            frequency=data.get('frequency', 2),
            daycount=data.get('daycount', 'ACT/ACT')
        )

        return jsonify({'yield': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bonds_bp.route('/duration', methods=['POST'])
def calculate_duration():
    """
    Calculate bond duration and convexity.
    """
    try:
        data = request.get_json()

        result = pricing_service.calculate_duration(
            coupon=Decimal(str(data['coupon'])),
            maturity=datetime.fromisoformat(data['maturity']).date(),
            settlement=datetime.fromisoformat(data['settlement']).date(),
            yield_rate=Decimal(str(data['yield'])),
            frequency=data.get('frequency', 2)
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### api/curves.py - Yield Curve API

```python
"""
Yield curve construction and fitting API endpoints.
"""
from flask import Blueprint, request, jsonify
from services.curve_service import CurveService

curves_bp = Blueprint('curves', __name__)
curve_service = CurveService()

@curves_bp.route('/goc', methods=['GET'])
def get_goc_curve():
    """
    Get Government of Canada yield curve.

    Query params:
        date: Curve date (YYYY-MM-DD), defaults to latest
        method: Interpolation method (linear, cubic, nss), default cubic

    Returns:
    {
        "date": "2024-10-15",
        "tenors": [0.25, 0.5, 1, 2, 5, 10, 30],
        "rates": [0.0450, 0.0460, 0.0475, 0.0490, 0.0510, 0.0530, 0.0550],
        "method": "cubic"
    }
    """
    try:
        date_str = request.args.get('date')
        method = request.args.get('method', 'cubic')

        curve_date = datetime.fromisoformat(date_str).date() if date_str else None

        result = curve_service.get_curve(
            curve_type='GOC',
            curve_date=curve_date,
            method=method
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@curves_bp.route('/fit/nss', methods=['POST'])
def fit_nelson_siegel_svensson():
    """
    Fit Nelson-Siegel-Svensson model to yield curve data.

    Request body:
    {
        "tenors": [0.25, 0.5, 1, 2, 5, 10, 30],
        "yields": [0.0450, 0.0460, 0.0475, 0.0490, 0.0510, 0.0530, 0.0550]
    }

    Returns:
    {
        "parameters": {
            "beta0": 0.055,
            "beta1": -0.010,
            "beta2": -0.005,
            "beta3": 0.002,
            "tau1": 2.5,
            "tau2": 10.0
        },
        "fitted_yields": [...],
        "rmse": 0.00012
    }
    """
    try:
        data = request.get_json()

        result = curve_service.fit_nss(
            tenors=data['tenors'],
            yields=data['yields']
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### api/portfolio.py - Portfolio Optimization API

```python
"""
Portfolio optimization API endpoints.
"""
from flask import Blueprint, request, jsonify
from services.portfolio_service import PortfolioService

portfolio_bp = Blueprint('portfolio', __name__)
portfolio_service = PortfolioService()

@portfolio_bp.route('/optimize', methods=['POST'])
def optimize_portfolio():
    """
    Optimize bond portfolio.

    Request body:
    {
        "bonds": [
            {"isin": "CA123456789", "weight": 0.2},
            {"isin": "CA987654321", "weight": 0.3}
        ],
        "constraints": {
            "target_duration": 5.0,
            "max_weight": 0.25,
            "min_rating": "BBB"
        },
        "objective": "max_yield"
    }
    """
    try:
        data = request.get_json()

        result = portfolio_service.optimize(
            bonds=data['bonds'],
            constraints=data.get('constraints', {}),
            objective=data.get('objective', 'max_yield')
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Services Layer

### services/pricing_service.py - Business Logic

```python
"""
Bond pricing service - integrates with existing pricing libraries.
"""
from decimal import Decimal
from datetime import date
from typing import Dict
import sys
from pathlib import Path

# Add src directory to path to import existing libraries
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# Import existing pricing functions
# from curves.nss import nelson_siegel_svensson
# from risk.duration import calculate_modified_duration

class PricingService:
    """Service for bond pricing calculations"""

    def price_bond(
        self,
        coupon: Decimal,
        maturity: date,
        settlement: date,
        yield_rate: Decimal,
        frequency: int = 2,
        daycount: str = "ACT/ACT"
    ) -> Dict:
        """
        Calculate bond price.

        Returns dictionary with price, accrued interest, and dirty price.
        """
        # Implementation using existing pricing libraries
        # from src/curves/ or direct calculation

        # Placeholder - replace with actual implementation
        clean_price = Decimal('95.432')
        accrued = Decimal('1.234')

        return {
            'price': float(clean_price),
            'accrued_interest': float(accrued),
            'dirty_price': float(clean_price + accrued)
        }

    def calculate_yield(
        self,
        coupon: Decimal,
        maturity: date,
        settlement: date,
        price: Decimal,
        frequency: int = 2,
        daycount: str = "ACT/ACT"
    ) -> float:
        """Calculate yield to maturity"""
        # Implementation
        return 0.030

    def calculate_duration(
        self,
        coupon: Decimal,
        maturity: date,
        settlement: date,
        yield_rate: Decimal,
        frequency: int = 2
    ) -> Dict:
        """Calculate duration and convexity"""
        return {
            'macaulay_duration': 4.85,
            'modified_duration': 4.72,
            'convexity': 28.5
        }
```

## Running the Flask Application

### Development Mode

```bash
# Activate virtual environment
source /Users/nattechan/src/venv/bin/activate

# Set environment variables
export FLASK_APP=backend/app.py
export FLASK_ENV=development

# Run development server
python backend/app.py

# Or use Flask CLI
flask run --host=0.0.0.0 --port=5000
```

### Production Deployment with Gunicorn

```bash
# Install Gunicorn
uv pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "backend.app:create_app('production')"

# With auto-reload for development
gunicorn -w 1 -b 0.0.0.0:5000 --reload "backend.app:create_app('development')"
```

## Testing Flask API

### Unit Tests with pytest

```python
"""
Test bond pricing API endpoints.
"""
import pytest
from decimal import Decimal
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_bond_price_calculation(client):
    """Test bond price calculation endpoint"""
    payload = {
        'coupon': 0.025,
        'maturity': '2030-12-15',
        'settlement': '2024-10-15',
        'yield': 0.030,
        'frequency': 2
    }

    response = client.post('/api/bonds/price', json=payload)
    assert response.status_code == 200

    data = response.json
    assert 'price' in data
    assert 'accrued_interest' in data
    assert isinstance(data['price'], float)

def test_invalid_bond_request(client):
    """Test error handling for invalid requests"""
    payload = {'coupon': 0.025}  # Missing required fields

    response = client.post('/api/bonds/price', json=payload)
    assert response.status_code == 400
    assert 'error' in response.json
```

### Manual Testing with curl

```bash
# Health check
curl http://localhost:5000/health

# Calculate bond price
curl -X POST http://localhost:5000/api/bonds/price \
  -H "Content-Type: application/json" \
  -d '{
    "coupon": 0.025,
    "maturity": "2030-12-15",
    "settlement": "2024-10-15",
    "yield": 0.030,
    "frequency": 2
  }'

# Get GoC curve
curl "http://localhost:5000/api/curves/goc?date=2024-10-15&method=cubic"
```

### Testing with Python requests

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:5000/api"

# Test bond pricing
response = requests.post(
    f"{BASE_URL}/bonds/price",
    json={
        "coupon": 0.025,
        "maturity": "2030-12-15",
        "settlement": "2024-10-15",
        "yield": 0.030
    }
)

print(response.json())
```

## Best Practices for Financial APIs

### 1. Input Validation

```python
from marshmallow import Schema, fields, validate, ValidationError

class BondPriceSchema(Schema):
    """Schema for bond price calculation request"""
    coupon = fields.Decimal(required=True, validate=validate.Range(min=0, max=1))
    maturity = fields.Date(required=True)
    settlement = fields.Date(required=True)
    yield_rate = fields.Decimal(required=True, data_key='yield')
    frequency = fields.Integer(validate=validate.OneOf([1, 2, 4, 12]))
    daycount = fields.String(validate=validate.OneOf(['ACT/ACT', 'ACT/360', '30/360']))

# In endpoint
try:
    schema = BondPriceSchema()
    validated_data = schema.load(request.get_json())
except ValidationError as err:
    return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
```

### 2. Error Handling

```python
from functools import wraps
from flask import jsonify

def handle_errors(f):
    """Decorator for consistent error handling"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': f'Invalid input: {str(e)}'}), 400
        except Exception as e:
            # Log error for debugging
            app.logger.error(f'Error in {f.__name__}: {str(e)}')
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper

@bonds_bp.route('/price', methods=['POST'])
@handle_errors
def calculate_bond_price():
    # Endpoint logic
    pass
```

### 3. Rate Limiting

```bash
uv pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

@bonds_bp.route('/price', methods=['POST'])
@limiter.limit("10 per minute")
def calculate_bond_price():
    # Expensive calculation endpoint
    pass
```

### 4. Caching

```bash
uv pip install flask-caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 900  # 15 minutes
})

@curves_bp.route('/goc')
@cache.cached(timeout=900, query_string=True)
def get_goc_curve():
    # Expensive curve construction
    return jsonify(curve_data)
```

## Integration with DuckDB

```python
import duckdb
from flask import current_app

def get_duckdb_connection():
    """Get DuckDB connection from config"""
    db_path = current_app.config['DUCKDB_PATH']
    return duckdb.connect(str(db_path), read_only=True)

@bonds_bp.route('/search')
def search_bonds():
    """Search bonds using DuckDB"""
    query = request.args.get('q', '')

    conn = get_duckdb_connection()

    result = conn.execute("""
        SELECT isin, issuer, coupon, maturity, rating
        FROM bonds
        WHERE issuer LIKE ?
        ORDER BY maturity
    """, [f"%{query}%"]).fetchall()

    conn.close()

    return jsonify([
        {
            'isin': row[0],
            'issuer': row[1],
            'coupon': row[2],
            'maturity': row[3].isoformat(),
            'rating': row[4]
        }
        for row in result
    ])
```

## API Documentation

### Using Flask-RESTX (formerly Flask-RESTPlus)

```bash
uv pip install flask-restx
```

```python
from flask_restx import Api, Resource, fields

api = Api(
    app,
    version='1.0',
    title='Quantitative Finance API',
    description='Bond pricing and portfolio optimization API',
    doc='/docs'
)

# Define models
bond_price_input = api.model('BondPriceInput', {
    'coupon': fields.Float(required=True, description='Annual coupon rate'),
    'maturity': fields.Date(required=True, description='Maturity date'),
    'settlement': fields.Date(required=True, description='Settlement date'),
    'yield': fields.Float(required=True, description='Yield to maturity')
})

bond_price_output = api.model('BondPriceOutput', {
    'price': fields.Float(description='Clean price'),
    'accrued_interest': fields.Float(description='Accrued interest'),
    'dirty_price': fields.Float(description='Dirty price')
})

@api.route('/bonds/price')
class BondPrice(Resource):
    @api.expect(bond_price_input)
    @api.marshal_with(bond_price_output)
    def post(self):
        """Calculate bond price"""
        # Implementation
        pass
```

## Environment Variables

Create `.env` file in backend directory:

```bash
# Flask configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DUCKDB_PATH=/Users/nattechan/src/finance/data/market_data.duckdb

# Bloomberg
BLOOMBERG_ENABLED=false

# API settings
API_RATE_LIMIT=100
```

Load with python-dotenv (already in requirements.txt):

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
```

## Next Steps

1. **Create backend directory structure** (see Project Structure above)
2. **Implement service layer** connecting to existing src/ libraries
3. **Add authentication** using Flask-JWT-Extended for production
4. **Set up logging** for debugging and monitoring
5. **Write comprehensive tests** for all endpoints
6. **Document API** with OpenAPI/Swagger using Flask-RESTX
7. **Deploy** with Gunicorn + Nginx in production

## Resources

### Official Documentation

- Flask: <https://flask.palletsprojects.com/>
- Flask-CORS: <https://flask-cors.readthedocs.io/>
- Flask-SQLAlchemy: <https://flask-sqlalchemy.palletsprojects.com/>
- Gunicorn: <https://gunicorn.org/>

### Related Guides

- **React Frontend**: See `notes/react.md` for frontend setup
- **Streamlit Alternative**: See `notes/streamlit.md` for rapid prototyping
- **API Design**: RESTful best practices for financial data
- **Testing**: pytest integration for Flask applications

---

**Last Updated**: 2025-10-15
**Python Environment**: `/Users/nattechan/src/venv`
**Framework Version**: Flask 3.x
