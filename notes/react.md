# React Frontend Guide

## Overview

React is a JavaScript library for building user interfaces, particularly well-suited for creating interactive, data-driven financial applications. For quantitative finance, React provides a powerful framework for building responsive dashboards, real-time data visualization, and complex portfolio management interfaces.

## What is React?

React is a component-based UI library that provides:

- **Component-based architecture**: Reusable, composable UI components
- **Virtual DOM**: Efficient rendering and updates
- **Declarative**: Describe what UI should look like, React handles updates
- **Ecosystem**: Rich ecosystem of libraries for routing, state management, charts
- **TypeScript support**: Strong typing for financial calculations
- **Hot reloading**: Fast development with instant feedback

## Installation Options

### Option 1: Vite (Recommended - Fast and Modern)

```bash
# Create new React app with Vite
npm create vite@latest frontend -- --template react-ts

cd frontend
npm install
npm run dev  # Runs on http://localhost:5173
```

### Option 2: Create React App (CRA)

```bash
# Create new React app with TypeScript
npx create-react-app frontend --template typescript

cd frontend
npm start  # Runs on http://localhost:3000
```

**Note**: Vite is recommended for this project due to faster build times and better performance.

## Project Structure for Finance Application

```text
/Users/nattechan/src/finance/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── api/                    # API integration
│   │   │   ├── client.ts           # Axios client configuration
│   │   │   ├── bonds.ts            # Bond API endpoints
│   │   │   ├── curves.ts           # Curve API endpoints
│   │   │   └── portfolio.ts        # Portfolio API endpoints
│   │   ├── components/             # Reusable components
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── bonds/
│   │   │   │   ├── BondPricer.tsx
│   │   │   │   ├── BondList.tsx
│   │   │   │   └── BondDetails.tsx
│   │   │   ├── curves/
│   │   │   │   ├── YieldCurveChart.tsx
│   │   │   │   └── CurveFitter.tsx
│   │   │   └── portfolio/
│   │   │       ├── PortfolioOptimizer.tsx
│   │   │       ├── PortfolioSummary.tsx
│   │   │       └── RiskMetrics.tsx
│   │   ├── pages/                  # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Bonds.tsx
│   │   │   ├── Curves.tsx
│   │   │   ├── Portfolio.tsx
│   │   │   └── Analytics.tsx
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── useBondPricing.ts
│   │   │   ├── useYieldCurve.ts
│   │   │   └── useWebSocket.ts
│   │   ├── store/                  # State management (Zustand/Redux)
│   │   │   ├── bondStore.ts
│   │   │   ├── portfolioStore.ts
│   │   │   └── curveStore.ts
│   │   ├── types/                  # TypeScript types
│   │   │   ├── bond.ts
│   │   │   ├── curve.ts
│   │   │   └── portfolio.ts
│   │   ├── utils/                  # Utility functions
│   │   │   ├── formatters.ts       # Number/date formatting
│   │   │   ├── validators.ts       # Input validation
│   │   │   └── calculations.ts     # Client-side calculations
│   │   ├── App.tsx                 # Main app component
│   │   ├── main.tsx                # Entry point
│   │   └── index.css               # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env                        # Environment variables
└── backend/                        # Flask backend (see flask.md)
```

## TypeScript Types for Financial Data

### types/bond.ts

```typescript
/**
 * Type definitions for bond-related data structures.
 */

export interface Bond {
  isin: string;
  issuer: string;
  coupon: number;
  maturity: string;  // ISO date string
  rating: string;
  price?: number;
  yield?: number;
  duration?: number;
  convexity?: number;
}

export interface BondPriceRequest {
  coupon: number;
  maturity: string;
  settlement: string;
  yield: number;
  frequency?: 1 | 2 | 4 | 12;
  daycount?: 'ACT/ACT' | 'ACT/360' | '30/360';
}

export interface BondPriceResponse {
  price: number;
  accrued_interest: number;
  dirty_price: number;
}

export interface DurationMetrics {
  macaulay_duration: number;
  modified_duration: number;
  convexity: number;
  key_rate_durations?: Record<string, number>;
}
```

### types/curve.ts

```typescript
/**
 * Type definitions for yield curve data.
 */

export interface YieldCurve {
  date: string;
  tenors: number[];
  rates: number[];
  method: 'linear' | 'cubic' | 'nss';
}

export interface NSSParameters {
  beta0: number;
  beta1: number;
  beta2: number;
  beta3: number;
  tau1: number;
  tau2: number;
}

export interface CurveFitResult {
  parameters: NSSParameters;
  fitted_yields: number[];
  rmse: number;
}
```

### types/portfolio.ts

```typescript
/**
 * Type definitions for portfolio data.
 */

export interface PortfolioPosition {
  isin: string;
  quantity: number;
  weight: number;
  market_value: number;
}

export interface Portfolio {
  id: string;
  name: string;
  positions: PortfolioPosition[];
  total_value: number;
  duration: number;
  yield: number;
  created_at: string;
}

export interface OptimizationConstraints {
  target_duration?: number;
  max_weight?: number;
  min_rating?: string;
  sector_limits?: Record<string, number>;
}

export interface OptimizationRequest {
  bonds: PortfolioPosition[];
  constraints: OptimizationConstraints;
  objective: 'max_yield' | 'min_risk' | 'max_sharpe';
}
```

## API Client Setup

### api/client.ts - Axios Configuration

```typescript
/**
 * API client configuration with axios.
 */
import axios, { AxiosInstance, AxiosError } from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }

    const errorMessage =
      (error.response?.data as { error?: string })?.error ||
      'An error occurred';

    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;
```

### api/bonds.ts - Bond API Functions

```typescript
/**
 * Bond pricing and analytics API functions.
 */
import apiClient from './client';
import type {
  Bond,
  BondPriceRequest,
  BondPriceResponse,
  DurationMetrics
} from '../types/bond';

export const bondApi = {
  /**
   * Calculate bond price from yield
   */
  calculatePrice: async (
    request: BondPriceRequest
  ): Promise<BondPriceResponse> => {
    const response = await apiClient.post<BondPriceResponse>(
      '/bonds/price',
      request
    );
    return response.data;
  },

  /**
   * Calculate yield from price
   */
  calculateYield: async (params: {
    coupon: number;
    maturity: string;
    settlement: string;
    price: number;
    frequency?: number;
  }): Promise<{ yield: number }> => {
    const response = await apiClient.post('/bonds/yield', params);
    return response.data;
  },

  /**
   * Calculate duration and convexity
   */
  calculateDuration: async (params: {
    coupon: number;
    maturity: string;
    settlement: string;
    yield: number;
    frequency?: number;
  }): Promise<DurationMetrics> => {
    const response = await apiClient.post<DurationMetrics>(
      '/bonds/duration',
      params
    );
    return response.data;
  },

  /**
   * Search bonds by criteria
   */
  searchBonds: async (query: string): Promise<Bond[]> => {
    const response = await apiClient.get<Bond[]>('/bonds/search', {
      params: { q: query },
    });
    return response.data;
  },
};
```

### api/curves.ts - Curve API Functions

```typescript
/**
 * Yield curve API functions.
 */
import apiClient from './client';
import type { YieldCurve, CurveFitResult } from '../types/curve';

export const curveApi = {
  /**
   * Get Government of Canada yield curve
   */
  getGoCCurve: async (params?: {
    date?: string;
    method?: 'linear' | 'cubic' | 'nss';
  }): Promise<YieldCurve> => {
    const response = await apiClient.get<YieldCurve>('/curves/goc', {
      params,
    });
    return response.data;
  },

  /**
   * Fit Nelson-Siegel-Svensson model
   */
  fitNSS: async (params: {
    tenors: number[];
    yields: number[];
  }): Promise<CurveFitResult> => {
    const response = await apiClient.post<CurveFitResult>(
      '/curves/fit/nss',
      params
    );
    return response.data;
  },
};
```

## Component Examples

### components/bonds/BondPricer.tsx

```typescript
/**
 * Bond pricing calculator component.
 */
import React, { useState } from 'react';
import { bondApi } from '../../api/bonds';
import type { BondPriceRequest, BondPriceResponse } from '../../types/bond';

const BondPricer: React.FC = () => {
  const [formData, setFormData] = useState<BondPriceRequest>({
    coupon: 0.025,
    maturity: '2030-12-15',
    settlement: new Date().toISOString().split('T')[0],
    yield: 0.030,
    frequency: 2,
    daycount: 'ACT/ACT',
  });

  const [result, setResult] = useState<BondPriceResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await bondApi.calculatePrice(formData);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Calculation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: ['coupon', 'yield'].includes(name)
        ? parseFloat(value)
        : name === 'frequency'
        ? parseInt(value)
        : value,
    }));
  };

  return (
    <div className="bond-pricer">
      <h2>Bond Price Calculator</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Coupon Rate (%)</label>
          <input
            type="number"
            name="coupon"
            value={formData.coupon * 100}
            onChange={(e) => handleChange({
              ...e,
              target: { ...e.target, value: (parseFloat(e.target.value) / 100).toString() }
            })}
            step="0.001"
            required
          />
        </div>

        <div className="form-group">
          <label>Maturity Date</label>
          <input
            type="date"
            name="maturity"
            value={formData.maturity}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Settlement Date</label>
          <input
            type="date"
            name="settlement"
            value={formData.settlement}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Yield (%)</label>
          <input
            type="number"
            name="yield"
            value={formData.yield * 100}
            onChange={(e) => handleChange({
              ...e,
              target: { ...e.target, value: (parseFloat(e.target.value) / 100).toString() }
            })}
            step="0.001"
            required
          />
        </div>

        <div className="form-group">
          <label>Payment Frequency</label>
          <select name="frequency" value={formData.frequency} onChange={handleChange}>
            <option value={1}>Annual</option>
            <option value={2}>Semi-annual</option>
            <option value={4}>Quarterly</option>
            <option value={12}>Monthly</option>
          </select>
        </div>

        <div className="form-group">
          <label>Day Count Convention</label>
          <select name="daycount" value={formData.daycount} onChange={handleChange}>
            <option value="ACT/ACT">ACT/ACT</option>
            <option value="ACT/360">ACT/360</option>
            <option value="30/360">30/360</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Calculating...' : 'Calculate Price'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="results">
          <h3>Results</h3>
          <div className="result-grid">
            <div className="result-item">
              <label>Clean Price:</label>
              <span className="value">{result.price.toFixed(4)}</span>
            </div>
            <div className="result-item">
              <label>Accrued Interest:</label>
              <span className="value">{result.accrued_interest.toFixed(4)}</span>
            </div>
            <div className="result-item">
              <label>Dirty Price:</label>
              <span className="value">{result.dirty_price.toFixed(4)}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BondPricer;
```

### components/curves/YieldCurveChart.tsx

```typescript
/**
 * Yield curve visualization component using Recharts.
 */
import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { curveApi } from '../../api/curves';
import type { YieldCurve } from '../../types/curve';

const YieldCurveChart: React.FC = () => {
  const [curve, setCurve] = useState<YieldCurve | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCurve();
  }, []);

  const loadCurve = async () => {
    try {
      const data = await curveApi.getGoCCurve({ method: 'cubic' });
      setCurve(data);
    } catch (error) {
      console.error('Failed to load curve:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading curve data...</div>;
  if (!curve) return <div>No curve data available</div>;

  // Transform data for Recharts
  const chartData = curve.tenors.map((tenor, index) => ({
    tenor,
    rate: curve.rates[index] * 100,  // Convert to percentage
  }));

  return (
    <div className="yield-curve-chart">
      <h2>Government of Canada Yield Curve</h2>
      <p className="curve-date">As of: {curve.date}</p>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="tenor"
            label={{ value: 'Tenor (years)', position: 'insideBottom', offset: -5 }}
          />
          <YAxis
            label={{ value: 'Yield (%)', angle: -90, position: 'insideLeft' }}
            domain={['auto', 'auto']}
          />
          <Tooltip
            formatter={(value: number) => `${value.toFixed(3)}%`}
            labelFormatter={(label) => `${label}Y`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="rate"
            stroke="#8884d8"
            strokeWidth={2}
            dot={{ r: 4 }}
            name="Yield"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default YieldCurveChart;
```

## Custom Hooks

### hooks/useBondPricing.ts

```typescript
/**
 * Custom hook for bond pricing operations.
 */
import { useState, useCallback } from 'react';
import { bondApi } from '../api/bonds';
import type { BondPriceRequest, BondPriceResponse } from '../types/bond';

export const useBondPricing = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<BondPriceResponse | null>(null);

  const calculatePrice = useCallback(async (request: BondPriceRequest) => {
    setLoading(true);
    setError(null);

    try {
      const data = await bondApi.calculatePrice(request);
      setResult(data);
      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Calculation failed';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return {
    loading,
    error,
    result,
    calculatePrice,
    reset,
  };
};
```

### hooks/useWebSocket.ts

```typescript
/**
 * Custom hook for WebSocket real-time data.
 */
import { useEffect, useRef, useState } from 'react';

interface WebSocketOptions {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
}

export const useWebSocket = <T = any>(options: WebSocketOptions) => {
  const { url, reconnectInterval = 5000, maxReconnectAttempts = 5 } = options;

  const [data, setData] = useState<T | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ws = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);

  useEffect(() => {
    const connect = () => {
      try {
        ws.current = new WebSocket(url);

        ws.current.onopen = () => {
          setIsConnected(true);
          setError(null);
          reconnectAttempts.current = 0;
        };

        ws.current.onmessage = (event) => {
          try {
            const parsed = JSON.parse(event.data);
            setData(parsed);
          } catch (err) {
            console.error('Failed to parse WebSocket message:', err);
          }
        };

        ws.current.onerror = (event) => {
          setError('WebSocket error occurred');
        };

        ws.current.onclose = () => {
          setIsConnected(false);

          // Attempt reconnect
          if (reconnectAttempts.current < maxReconnectAttempts) {
            setTimeout(() => {
              reconnectAttempts.current++;
              connect();
            }, reconnectInterval);
          }
        };
      } catch (err) {
        setError('Failed to connect to WebSocket');
      }
    };

    connect();

    return () => {
      ws.current?.close();
    };
  }, [url, reconnectInterval, maxReconnectAttempts]);

  const send = (message: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  };

  return { data, isConnected, error, send };
};
```

## State Management with Zustand

```bash
npm install zustand
```

### store/bondStore.ts

```typescript
/**
 * Bond state management with Zustand.
 */
import { create } from 'zustand';
import type { Bond } from '../types/bond';

interface BondState {
  bonds: Bond[];
  selectedBond: Bond | null;
  loading: boolean;
  error: string | null;

  // Actions
  setBonds: (bonds: Bond[]) => void;
  selectBond: (bond: Bond | null) => void;
  addBond: (bond: Bond) => void;
  updateBond: (isin: string, updates: Partial<Bond>) => void;
  removeBond: (isin: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useBondStore = create<BondState>((set) => ({
  bonds: [],
  selectedBond: null,
  loading: false,
  error: null,

  setBonds: (bonds) => set({ bonds }),

  selectBond: (bond) => set({ selectedBond: bond }),

  addBond: (bond) => set((state) => ({
    bonds: [...state.bonds, bond],
  })),

  updateBond: (isin, updates) => set((state) => ({
    bonds: state.bonds.map((b) =>
      b.isin === isin ? { ...b, ...updates } : b
    ),
  })),

  removeBond: (isin) => set((state) => ({
    bonds: state.bonds.filter((b) => b.isin !== isin),
  })),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),
}));
```

## Styling Options

### Option 1: Tailwind CSS (Recommended)

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Option 2: Material-UI

```bash
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/x-charts  # For financial charts
```

### Option 3: Ant Design

```bash
npm install antd
```

## Charting Libraries

### Recharts (Recommended for finance)

```bash
npm install recharts
```

### Plotly.js (Interactive 3D surfaces)

```bash
npm install react-plotly.js plotly.js
```

### TradingView Lightweight Charts

```bash
npm install lightweight-charts
```

## Running the Application

### Development Mode

```bash
# Start React dev server (Vite)
cd frontend
npm run dev  # Runs on http://localhost:5173

# Or with CRA
npm start  # Runs on http://localhost:3000
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create `.env` file in frontend directory:

```bash
# API configuration
VITE_API_URL=http://localhost:5000/api

# WebSocket (if using)
VITE_WS_URL=ws://localhost:5000/ws

# Feature flags
VITE_ENABLE_BLOOMBERG=false
```

## Integration with Flask Backend

### Complete Workflow Example

```typescript
/**
 * Example: Complete bond pricing workflow with error handling
 */
import React, { useState } from 'react';
import { useBondPricing } from '../hooks/useBondPricing';
import type { BondPriceRequest } from '../types/bond';

const BondPricingWorkflow: React.FC = () => {
  const { loading, error, result, calculatePrice } = useBondPricing();

  const [formData, setFormData] = useState<BondPriceRequest>({
    coupon: 0.025,
    maturity: '2030-12-15',
    settlement: new Date().toISOString().split('T')[0],
    yield: 0.030,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await calculatePrice(formData);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {/* Form fields */}
        <button type="submit" disabled={loading}>
          Calculate
        </button>
      </form>

      {loading && <div>Calculating...</div>}
      {error && <div className="error">{error}</div>}
      {result && (
        <div>
          <p>Price: {result.price.toFixed(4)}</p>
          <p>Accrued: {result.accrued_interest.toFixed(4)}</p>
        </div>
      )}
    </div>
  );
};
```

## Testing React Components

```bash
npm install -D @testing-library/react @testing-library/jest-dom vitest
```

### Example Test

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import BondPricer from '../components/bonds/BondPricer';
import { bondApi } from '../api/bonds';

// Mock API
vi.mock('../api/bonds', () => ({
  bondApi: {
    calculatePrice: vi.fn(),
  },
}));

describe('BondPricer', () => {
  it('calculates bond price on submit', async () => {
    const mockResult = {
      price: 95.432,
      accrued_interest: 1.234,
      dirty_price: 96.666,
    };

    vi.mocked(bondApi.calculatePrice).mockResolvedValue(mockResult);

    render(<BondPricer />);

    // Fill form
    fireEvent.change(screen.getByLabelText(/coupon/i), {
      target: { value: '2.5' },
    });

    // Submit
    fireEvent.click(screen.getByText(/calculate/i));

    // Wait for result
    await waitFor(() => {
      expect(screen.getByText(/95.432/)).toBeInTheDocument();
    });
  });
});
```

## Best Practices for Financial UIs

### 1. Number Formatting

```typescript
// utils/formatters.ts
export const formatPrice = (price: number): string => {
  return price.toFixed(4);
};

export const formatYield = (yield_val: number): string => {
  return `${(yield_val * 100).toFixed(3)}%`;
};

export const formatDuration = (duration: number): string => {
  return duration.toFixed(2);
};

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-CA', {
    style: 'currency',
    currency: 'CAD',
  }).format(amount);
};
```

### 2. Input Validation

```typescript
// utils/validators.ts
export const validateCoupon = (coupon: number): boolean => {
  return coupon >= 0 && coupon <= 1;
};

export const validateDate = (date: string): boolean => {
  const parsed = new Date(date);
  return !isNaN(parsed.getTime());
};

export const validateYield = (yield_val: number): boolean => {
  return yield_val >= -0.01 && yield_val <= 1;  // Allow negative yields
};
```

### 3. Error Boundaries

```typescript
// components/common/ErrorBoundary.tsx
import React, { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            Reload Application
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

## Performance Optimization

### 1. React.memo for Expensive Components

```typescript
import React from 'react';

const YieldCurveChart = React.memo<YieldCurveChartProps>(
  ({ curve }) => {
    // Expensive rendering logic
    return <div>...</div>;
  },
  (prevProps, nextProps) => {
    // Custom comparison
    return prevProps.curve.date === nextProps.curve.date;
  }
);
```

### 2. useMemo for Expensive Calculations

```typescript
const portfolioMetrics = useMemo(() => {
  return calculatePortfolioMetrics(positions);
}, [positions]);
```

### 3. Code Splitting

```typescript
import { lazy, Suspense } from 'react';

const Portfolio = lazy(() => import('./pages/Portfolio'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Portfolio />
    </Suspense>
  );
}
```

## Next Steps

1. **Set up project**: Create React app with Vite
2. **Configure TypeScript**: Add types for all financial data
3. **Integrate with Flask**: Connect to backend API
4. **Build components**: Start with bond pricer and curve charts
5. **Add state management**: Use Zustand for complex state
6. **Implement testing**: Write tests for critical components
7. **Optimize performance**: Profile and optimize rendering

## Resources

### Official Documentation

- React: <https://react.dev/>
- TypeScript: <https://www.typescriptlang.org/>
- Vite: <https://vite.dev/>
- Recharts: <https://recharts.org/>
- Zustand: <https://github.com/pmndrs/zustand>

### Related Guides

- **Flask Backend**: See `notes/flask.md` for API setup
- **Streamlit Alternative**: See `notes/streamlit.md` for rapid prototyping
- **Testing**: React Testing Library best practices

---

**Last Updated**: 2025-10-15
**Node Version**: 18+ recommended
**Package Manager**: npm or pnpm
