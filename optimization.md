# Optimization Guide

A comprehensive guide to optimization theory and practice for quantitative finance applications.

## Table of Contents
1. [Fundamental Concepts](#fundamental-concepts)
2. [Constrained vs Unconstrained Optimization](#constrained-vs-unconstrained-optimization)
3. [Linear vs Nonlinear Programming](#linear-vs-nonlinear-programming)
4. [Convex Optimization](#convex-optimization)
5. [Relationships and Hierarchy](#relationships-and-hierarchy)
6. [Python Implementation Examples](#python-implementation-examples)
7. [Financial Applications](#financial-applications)

---

## Fundamental Concepts

### What is Optimization?

Optimization is the process of finding the "best" solution from a set of feasible alternatives. Mathematically, we seek to:

**Minimize (or Maximize):** An objective function f(x)
**Subject to:** Constraints on x

General form:
```
minimize    f(x)
subject to  g_i(x) ≤ 0,  i = 1,...,m    (inequality constraints)
            h_j(x) = 0,  j = 1,...,p    (equality constraints)
            x ∈ X                        (domain constraints)
```

Where:
- **x** is the decision variable (can be scalar or vector)
- **f(x)** is the objective function
- **g_i(x)** are inequality constraint functions
- **h_j(x)** are equality constraint functions

---

## Constrained vs Unconstrained Optimization

### Unconstrained Optimization

**Definition:** Optimization problems with no restrictions on the decision variables (except possibly domain X = ℝⁿ).

**Form:**
```
minimize f(x)
where x ∈ ℝⁿ
```

**Characteristics:**
- Simplest form of optimization
- Solution found where gradient vanishes: ∇f(x*) = 0
- Only consider interior points (no boundary effects)
- Easier to solve numerically

**Solution Methods:**
- **Gradient Descent:** Iteratively move in direction of steepest descent
- **Newton's Method:** Use second-order information (Hessian)
- **Quasi-Newton Methods:** Approximate Hessian (BFGS, L-BFGS)
- **Conjugate Gradient:** For large-scale problems

**Example:** Finding the minimum of f(x) = x₁² + x₂² - 2x₁ - 4x₂

```python
import numpy as np
from scipy.optimize import minimize

def objective(x):
    return x[0]**2 + x[1]**2 - 2*x[0] - 4*x[1]

# Unconstrained optimization
x0 = [0, 0]  # Initial guess
result = minimize(objective, x0, method='BFGS')
print(f"Optimal x: {result.x}")  # [1, 2]
print(f"Optimal value: {result.fun}")  # -5
```

### Constrained Optimization

**Definition:** Optimization with restrictions on feasible values of decision variables.

**Form:**
```
minimize    f(x)
subject to  g_i(x) ≤ 0,  i = 1,...,m
            h_j(x) = 0,  j = 1,...,p
```

**Characteristics:**
- More complex than unconstrained problems
- Optimal solution may lie on constraint boundaries
- Requires constraint handling in solution methods
- Introduces Lagrange multipliers (dual variables)

**Solution Methods:**
- **Lagrange Multipliers:** For equality constraints
- **KKT Conditions:** Generalization for inequality constraints
- **Penalty Methods:** Convert to unconstrained problem
- **Interior Point Methods:** Stay strictly feasible
- **Sequential Quadratic Programming (SQP)**

**Example:** Same function with constraint x₁ + x₂ ≤ 2

```python
from scipy.optimize import minimize

def objective(x):
    return x[0]**2 + x[1]**2 - 2*x[0] - 4*x[1]

def constraint(x):
    return 2 - x[0] - x[1]  # g(x) ≥ 0 form for scipy

# Constrained optimization
x0 = [0, 0]
cons = {'type': 'ineq', 'fun': constraint}
result = minimize(objective, x0, method='SLSQP', constraints=cons)
print(f"Optimal x: {result.x}")  # On boundary: x₁ + x₂ = 2
```

**Key Differences:**

| Aspect | Unconstrained | Constrained |
|--------|--------------|-------------|
| Feasible set | Entire space ℝⁿ | Subset of ℝⁿ |
| Optimality condition | ∇f(x*) = 0 | KKT conditions |
| Solution location | Interior point | May be on boundary |
| Complexity | Lower | Higher |
| Methods | Gradient-based | Lagrangian-based |

---

## Linear vs Nonlinear Programming

### Linear Programming (LP)

**Definition:** Optimization where both objective and constraints are linear functions.

**Standard Form:**
```
minimize    c'x
subject to  Ax ≤ b
            x ≥ 0
```

Where:
- **c** ∈ ℝⁿ is the cost vector
- **A** ∈ ℝᵐˣⁿ is the constraint matrix
- **b** ∈ ℝᵐ is the right-hand side vector

**Characteristics:**
- **Convex:** Any local minimum is global minimum
- **Polyhedral feasible region:** Defined by linear inequalities
- **Vertex solution:** Optimal solution at vertex of feasible region
- **Efficiently solvable:** Polynomial time algorithms exist
- **No gradient needed:** Simplex method uses vertices

**Solution Methods:**
- **Simplex Method:** Walk along edges of polytope
- **Interior Point Methods:** Move through interior
- **Dual Simplex:** Solve dual problem

**Example:** Portfolio optimization with linear constraints

```python
import cvxpy as cp
import numpy as np

# Data
n = 4  # Number of assets
expected_returns = np.array([0.10, 0.12, 0.08, 0.15])
prices = np.array([100, 50, 75, 125])
budget = 10000

# Decision variables
weights = cp.Variable(n)

# LP formulation
objective = cp.Maximize(expected_returns @ weights)
constraints = [
    cp.sum(weights) == 1,      # Fully invested
    weights >= 0,               # No short selling
    weights <= 0.4              # Position limits
]

problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK)  # LP solver

print(f"Optimal weights: {weights.value}")
print(f"Expected return: {problem.value:.2%}")
```

### Nonlinear Programming (NLP)

**Definition:** Optimization where objective or constraints are nonlinear functions.

**General Form:**
```
minimize    f(x)
subject to  g_i(x) ≤ 0,  i = 1,...,m
            h_j(x) = 0,  j = 1,...,p
```

Where f, g_i, or h_j are nonlinear functions.

**Characteristics:**
- **More expressive:** Can model complex relationships
- **Non-convex:** May have multiple local minima
- **Harder to solve:** May require good initial guess
- **Gradient-based:** Usually requires derivatives
- **No global optimality guarantee:** Unless special structure (convex)

**Types:**
- **Quadratic Programming (QP):** Quadratic objective, linear constraints
- **Quadratically Constrained (QCQP):** Quadratic objective and constraints
- **General NLP:** Arbitrary smooth nonlinear functions

**Solution Methods:**
- **Sequential Quadratic Programming (SQP)**
- **Interior Point Methods**
- **Augmented Lagrangian Methods**
- **Trust Region Methods**

**Example:** Mean-variance portfolio optimization (quadratic)

```python
import cvxpy as cp
import numpy as np

# Data
n = 4
mu = np.array([0.10, 0.12, 0.08, 0.15])  # Expected returns
Sigma = np.array([  # Covariance matrix
    [0.04, 0.01, 0.02, 0.01],
    [0.01, 0.06, 0.01, 0.02],
    [0.02, 0.01, 0.03, 0.01],
    [0.01, 0.02, 0.01, 0.08]
])

# Decision variables
w = cp.Variable(n)
gamma = 2.0  # Risk aversion parameter

# Quadratic program (special case of NLP)
objective = cp.Minimize(cp.quad_form(w, Sigma) - gamma * (mu @ w))
constraints = [
    cp.sum(w) == 1,
    w >= 0
]

problem = cp.Problem(objective, constraints)
problem.solve()  # Uses QP solver

print(f"Optimal weights: {w.value}")
print(f"Portfolio variance: {cp.quad_form(w, Sigma).value:.4f}")
print(f"Expected return: {(mu @ w.value):.2%}")
```

**Key Differences:**

| Aspect | Linear | Nonlinear |
|--------|--------|-----------|
| Objective | Linear: c'x | Nonlinear: f(x) |
| Constraints | Linear: Ax ≤ b | Nonlinear: g(x) ≤ 0 |
| Feasible region | Polyhedron | Curved surface |
| Optimality | Global | Possibly local |
| Solving difficulty | Easier | Harder |
| Solution time | Polynomial | Exponential (worst case) |

---

## Convex Optimization

### Definition

**Convex optimization** is optimization of a convex objective over a convex feasible set.

**Form:**
```
minimize    f(x)
subject to  g_i(x) ≤ 0,  i = 1,...,m
            Ax = b
```

Where:
- **f(x)** is a convex function
- **g_i(x)** are convex functions
- Equality constraints **Ax = b** are affine (linear)

### Convex Sets

A set C is **convex** if for any x, y ∈ C and 0 ≤ θ ≤ 1:
```
θx + (1-θ)y ∈ C
```

**Examples:**
- **Halfspaces:** {x | a'x ≤ b}
- **Polyhedra:** Intersection of halfspaces
- **Norm balls:** {x | ||x|| ≤ r}
- **Ellipsoids:** {x | (x-c)'P(x-c) ≤ 1}

### Convex Functions

A function f is **convex** if its domain is convex and for all x, y and 0 ≤ θ ≤ 1:
```
f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)
```

**Graphically:** The line segment between any two points on the graph lies above the graph.

**Second-order condition:** For twice differentiable f, convex ⟺ Hessian ∇²f(x) ⪰ 0 (positive semidefinite)

**Examples:**
- **Affine:** a'x + b
- **Quadratic (convex):** x'Px + q'x + r, where P ⪰ 0
- **Norms:** ||x||, ||x||₁, ||x||₂, ||x||∞
- **Exponential:** e^(ax)
- **Log-sum-exp:** log(Σ e^(x_i))

### Why Convex Optimization is Special

**Fundamental Property:** Any local minimum is a global minimum.

**Proof sketch:** Suppose x* is local minimum but not global. Then ∃ y with f(y) < f(x*). By convexity, f is decreasing along line from x* to y, contradicting x* being local minimum.

**Implications:**
1. **No local minima trap:** Don't get stuck in suboptimal solutions
2. **Efficiently solvable:** Polynomial time algorithms
3. **Duality theory:** Strong duality (zero duality gap)
4. **Robust algorithms:** Provable convergence guarantees
5. **Sensitivity analysis:** Well-understood via dual variables

### Solution Methods

**General Approaches:**
- **Interior Point Methods:** Barrier methods, primal-dual methods
- **First-Order Methods:** Gradient descent, accelerated gradient
- **Proximal Methods:** For non-smooth objectives
- **ADMM:** Alternating Direction Method of Multipliers
- **Specialized Solvers:** CVXPY, MOSEK, Gurobi, ECOS

### Example: Portfolio Optimization with Risk Constraints

```python
import cvxpy as cp
import numpy as np

# Market data
n_assets = 50
np.random.seed(42)
mu = np.random.randn(n_assets) * 0.01 + 0.10  # Expected returns
F = np.random.randn(n_assets, 5)  # Factor loadings
D = np.diag(np.random.rand(n_assets) * 0.01)  # Idiosyncratic risk
Sigma = F @ F.T + D  # Covariance matrix (positive semidefinite)

# Decision variables
w = cp.Variable(n_assets)

# Convex optimization problem
target_return = 0.12
objective = cp.Minimize(cp.quad_form(w, Sigma))  # Convex: minimize variance
constraints = [
    mu @ w >= target_return,    # Return requirement
    cp.sum(w) == 1,             # Fully invested
    w >= 0,                     # Long only
    w <= 0.10,                  # Position limits
    cp.norm(w, 1) <= 1.5        # Limit turnover (convex constraint)
]

problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.OSQP)  # Convex QP solver

print(f"Optimal portfolio found: {problem.status}")
print(f"Portfolio variance: {problem.value:.6f}")
print(f"Number of positions: {np.sum(w.value > 1e-6)}")
```

---

## Relationships and Hierarchy

### The Optimization Taxonomy

```
┌─────────────────────────────────────────────────┐
│         ALL OPTIMIZATION PROBLEMS               │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │       CONSTRAINED OPTIMIZATION            │ │
│  │                                           │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │    CONVEX OPTIMIZATION              │ │ │
│  │  │                                     │ │ │
│  │  │  ┌───────────────────────────────┐ │ │ │
│  │  │  │  QUADRATIC PROGRAMMING (QP)   │ │ │ │
│  │  │  │  • Quadratic objective        │ │ │ │
│  │  │  │  • Linear constraints         │ │ │ │
│  │  │  └───────────────────────────────┘ │ │ │
│  │  │                                     │ │ │
│  │  │  ┌───────────────────────────────┐ │ │ │
│  │  │  │  LINEAR PROGRAMMING (LP)      │ │ │ │
│  │  │  │  • Linear objective           │ │ │ │
│  │  │  │  • Linear constraints         │ │ │ │
│  │  │  └───────────────────────────────┘ │ │ │
│  │  │                                     │ │ │
│  │  │  ┌───────────────────────────────┐ │ │ │
│  │  │  │  SECOND-ORDER CONE (SOCP)     │ │ │ │
│  │  │  └───────────────────────────────┘ │ │ │
│  │  │                                     │ │ │
│  │  │  ┌───────────────────────────────┐ │ │ │
│  │  │  │  SEMIDEFINITE PROGRAM (SDP)   │ │ │ │
│  │  │  └───────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  │                                           │ │
│  │  NONLINEAR PROGRAMMING (NLP)              │ │
│  │  • Non-convex region                      │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  UNCONSTRAINED OPTIMIZATION                     │
│  • Special case of constrained                  │
└─────────────────────────────────────────────────┘
```

### Subset Relationships

**LP ⊂ QP ⊂ SOCP ⊂ SDP ⊂ Convex ⊂ NLP**

1. **Linear Programming ⊂ Quadratic Programming**
   - Any LP can be written as QP with zero quadratic term
   - QP with P = 0 reduces to LP

2. **Quadratic Programming ⊂ Convex Optimization**
   - QP with P ⪰ 0 is convex
   - Convex optimization includes non-quadratic objectives

3. **Convex ⊂ Nonlinear Programming**
   - Convex problems are special case of NLP
   - NLP includes non-convex problems

4. **Unconstrained ⊂ Constrained**
   - Unconstrained is constrained with no constraints
   - Can add constraint x ∈ ℝⁿ to make it constrained

### Decision Tree: Which Problem Type?

```
Start
  │
  ├─ No constraints?
  │    └─ YES → UNCONSTRAINED
  │    └─ NO → Continue
  │
  ├─ All functions linear?
  │    └─ YES → LINEAR PROGRAM (LP)
  │    └─ NO → Continue
  │
  ├─ Quadratic objective + linear constraints?
  │    └─ YES → QUADRATIC PROGRAM (QP)
  │    └─ NO → Continue
  │
  ├─ Convex objective + convex constraints?
  │    └─ YES → CONVEX OPTIMIZATION
  │    └─ NO → NONLINEAR PROGRAM (NLP)
```

---

## Python Implementation Examples

### Example 1: All Four Problem Types

```python
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize

# Shared data
n = 3
np.random.seed(123)

# ============================================
# 1. UNCONSTRAINED OPTIMIZATION
# ============================================
print("=" * 50)
print("1. UNCONSTRAINED OPTIMIZATION")
print("=" * 50)

def unconstrained_obj(x):
    """Simple quadratic function"""
    return x[0]**2 + 2*x[1]**2 + x[2]**2 + x[0]*x[1]

x0 = np.ones(n)
result_unc = minimize(unconstrained_obj, x0, method='BFGS')
print(f"Solution: {result_unc.x}")
print(f"Objective: {result_unc.fun:.6f}\n")

# ============================================
# 2. LINEAR PROGRAMMING
# ============================================
print("=" * 50)
print("2. LINEAR PROGRAMMING")
print("=" * 50)

x_lp = cp.Variable(n)
c = np.array([1, 2, 3])  # Linear objective coefficients

objective_lp = cp.Minimize(c @ x_lp)
constraints_lp = [
    x_lp >= 0,              # Non-negativity
    x_lp <= 10,             # Upper bounds
    cp.sum(x_lp) >= 5,      # Total minimum
    x_lp[0] + 2*x_lp[1] + x_lp[2] <= 15  # Linear constraint
]

prob_lp = cp.Problem(objective_lp, constraints_lp)
prob_lp.solve(solver=cp.GLPK)

print(f"Solution: {x_lp.value}")
print(f"Objective: {prob_lp.value:.6f}\n")

# ============================================
# 3. QUADRATIC PROGRAMMING (Convex)
# ============================================
print("=" * 50)
print("3. QUADRATIC PROGRAMMING (Convex)")
print("=" * 50)

x_qp = cp.Variable(n)
P = np.array([[2, 0.5, 0], [0.5, 2, 0], [0, 0, 1]])  # Positive definite
q = np.array([1, 1, 1])

objective_qp = cp.Minimize(0.5 * cp.quad_form(x_qp, P) + q @ x_qp)
constraints_qp = [
    cp.sum(x_qp) == 1,
    x_qp >= 0
]

prob_qp = cp.Problem(objective_qp, constraints_qp)
prob_qp.solve(solver=cp.OSQP)

print(f"Solution: {x_qp.value}")
print(f"Objective: {prob_qp.value:.6f}\n")

# ============================================
# 4. NONLINEAR PROGRAMMING (Non-convex)
# ============================================
print("=" * 50)
print("4. NONLINEAR PROGRAMMING (Non-convex)")
print("=" * 50)

def nonlinear_obj(x):
    """Non-convex objective with local minima"""
    return np.sin(x[0]) + np.cos(x[1]) + x[2]**4 - x[2]**2

def nonlinear_constraint(x):
    """Nonlinear inequality: x₀² + x₁² ≤ 4"""
    return 4 - x[0]**2 - x[1]**2

x0_nlp = np.array([0.5, 0.5, 0.5])
cons_nlp = {'type': 'ineq', 'fun': nonlinear_constraint}

result_nlp = minimize(nonlinear_obj, x0_nlp, method='SLSQP', constraints=cons_nlp)
print(f"Solution: {result_nlp.x}")
print(f"Objective: {result_nlp.fun:.6f}")
print(f"Note: May be local minimum (non-convex problem)\n")
```

### Example 2: Portfolio Optimization Comparison

```python
import numpy as np
import cvxpy as cp

# Market parameters
n_assets = 10
np.random.seed(456)
mu = np.random.randn(n_assets) * 0.02 + 0.10
Sigma = np.random.randn(n_assets, n_assets)
Sigma = Sigma @ Sigma.T / 100  # Ensure positive semidefinite

# ============================================
# Linear: Maximize return (ignore risk)
# ============================================
w_lp = cp.Variable(n_assets)
prob_lp = cp.Problem(
    cp.Maximize(mu @ w_lp),
    [cp.sum(w_lp) == 1, w_lp >= 0, w_lp <= 0.3]
)
prob_lp.solve()
print("LINEAR: Max return portfolio")
print(f"  Return: {mu @ w_lp.value:.4f}")
print(f"  Risk:   {np.sqrt(w_lp.value @ Sigma @ w_lp.value):.4f}")
print(f"  Positions: {np.sum(w_lp.value > 0.01)}\n")

# ============================================
# Quadratic: Mean-variance optimization
# ============================================
w_qp = cp.Variable(n_assets)
gamma = 3.0  # Risk aversion
prob_qp = cp.Problem(
    cp.Minimize(cp.quad_form(w_qp, Sigma) - gamma * mu @ w_qp),
    [cp.sum(w_qp) == 1, w_qp >= 0]
)
prob_qp.solve()
print("QUADRATIC: Mean-variance portfolio")
print(f"  Return: {mu @ w_qp.value:.4f}")
print(f"  Risk:   {np.sqrt(w_qp.value @ Sigma @ w_qp.value):.4f}")
print(f"  Positions: {np.sum(w_qp.value > 0.01)}\n")

# ============================================
# Convex: Min variance with return target
# ============================================
w_conv = cp.Variable(n_assets)
prob_conv = cp.Problem(
    cp.Minimize(cp.quad_form(w_conv, Sigma)),
    [
        cp.sum(w_conv) == 1,
        mu @ w_conv >= 0.11,
        w_conv >= 0,
        cp.norm(w_conv, 1) <= 1.6  # L1 regularization
    ]
)
prob_conv.solve()
print("CONVEX: Min variance with L1 regularization")
print(f"  Return: {mu @ w_conv.value:.4f}")
print(f"  Risk:   {np.sqrt(w_conv.value @ Sigma @ w_conv.value):.4f}")
print(f"  Positions: {np.sum(w_conv.value > 0.01)}\n")
```

---

## Financial Applications

### Bond Portfolio Optimization

**Problem Type:** Quadratic Programming (Convex)

```python
import cvxpy as cp
import numpy as np

# Bond portfolio data
n_bonds = 20
durations = np.random.uniform(1, 30, n_bonds)
yields = 0.02 + 0.03 * durations / 30 + np.random.randn(n_bonds) * 0.005
spreads = np.random.uniform(0.5, 2.0, n_bonds)
target_duration = 7.0
target_yield = 0.04

# Covariance of spread changes
spread_vol = 0.20 * spreads  # Spread volatility
rho = 0.3  # Correlation
Sigma = np.outer(spread_vol, spread_vol) * rho
np.fill_diagonal(Sigma, spread_vol**2)

# Optimization
w = cp.Variable(n_bonds)

objective = cp.Minimize(cp.quad_form(w, Sigma))  # Minimize spread risk
constraints = [
    cp.sum(w) == 1,                    # Fully invested
    durations @ w == target_duration,   # Duration matching
    yields @ w >= target_yield,         # Yield requirement
    w >= 0,                            # Long only
    w <= 0.15                          # Position limits
]

problem = cp.Problem(objective, constraints)
problem.solve()

print("Bond Portfolio Optimization Results:")
print(f"  Portfolio duration: {durations @ w.value:.2f} years")
print(f"  Portfolio yield: {yields @ w.value:.4f}")
print(f"  Spread risk (std dev): {np.sqrt(problem.value):.4f}")
print(f"  Number of bonds: {np.sum(w.value > 0.001)}")
```

### Swap Portfolio Risk Management

**Problem Type:** Convex Optimization with Cone Constraints

```python
import cvxpy as cp
import numpy as np

# Interest rate swap portfolio
n_swaps = 15
pv01s = np.random.randn(n_swaps) * 10000  # PV01 (dollar duration)
current_positions = np.random.randint(-5, 5, n_swaps)  # Current notionals

# Risk factor sensitivities (key rate durations)
n_tenors = 5
tenor_sensitivities = np.random.randn(n_tenors, n_swaps)
risk_factor_vol = np.array([0.20, 0.25, 0.30, 0.35, 0.40])  # bp per day

# Hedge optimization: minimize total risk
hedge_trades = cp.Variable(n_swaps)
total_position = current_positions + hedge_trades

# Risk calculation
risk_by_tenor = tenor_sensitivities @ total_position
weighted_risk = cp.multiply(risk_factor_vol, risk_by_tenor)

objective = cp.Minimize(cp.norm(weighted_risk, 2))  # Minimize total risk
constraints = [
    cp.sum(pv01s @ total_position) <= 1000,  # Net PV01 limit
    cp.norm(hedge_trades, 1) <= 50,          # Limit trading
    hedge_trades >= -10,                      # Trade size limits
    hedge_trades <= 10
]

problem = cp.Problem(objective, constraints)
problem.solve()

print("Swap Hedging Results:")
print(f"  Pre-hedge risk: {np.linalg.norm(risk_factor_vol * (tenor_sensitivities @ current_positions)):.2f}")
print(f"  Post-hedge risk: {problem.value:.2f}")
print(f"  Risk reduction: {(1 - problem.value / np.linalg.norm(risk_factor_vol * (tenor_sensitivities @ current_positions))):.1%}")
print(f"  Number of hedge trades: {np.sum(np.abs(hedge_trades.value) > 0.1)}")
```

### Asset-Liability Matching

**Problem Type:** Linear Programming

```python
import cvxpy as cp
import numpy as np

# Liability cash flows (e.g., pension obligations)
periods = 30
liabilities = 1000000 * (1.03 ** -np.arange(1, periods+1))  # Declining over time

# Available bonds
n_bonds = 10
bond_cashflows = np.zeros((n_bonds, periods))
for i in range(n_bonds):
    maturity = np.random.randint(5, 30)
    coupon = np.random.uniform(0.02, 0.05)
    bond_cashflows[i, :maturity] = coupon * 100
    bond_cashflows[i, maturity-1] += 100  # Principal at maturity

bond_prices = np.random.uniform(90, 110, n_bonds)

# Optimization: minimize cost of liability matching
face_amounts = cp.Variable(n_bonds, nonneg=True)

# Asset cash flows must meet or exceed liabilities
asset_cashflows = bond_cashflows.T @ face_amounts

objective = cp.Minimize(bond_prices @ face_amounts)
constraints = [
    asset_cashflows >= liabilities  # Meet all liabilities
]

problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK)

print("Asset-Liability Matching Results:")
print(f"  Total cost: ${problem.value:,.0f}")
print(f"  Bonds purchased: {np.sum(face_amounts.value > 0.01)}")
print(f"  Surplus in period 1: ${(asset_cashflows.value[0] - liabilities[0]):,.0f}")
print(f"  Surplus in period {periods}: ${(asset_cashflows.value[-1] - liabilities[-1]):,.0f}")
```

---

## Summary Table

| Property | Unconstrained | Constrained | Linear | Convex | Nonlinear |
|----------|---------------|-------------|--------|---------|-----------|
| **Constraints** | None | Yes | Linear | Convex | Arbitrary |
| **Objective** | Any | Any | Linear | Convex | Arbitrary |
| **Feasible Region** | All ℝⁿ | Subset | Polyhedron | Convex set | Arbitrary |
| **Local = Global** | No | No | Yes | Yes | No |
| **Solution Method** | Gradient | Lagrangian | Simplex | Interior point | NLP solver |
| **Difficulty** | Easy | Medium | Easy | Medium | Hard |
| **Guarantees** | None | None | Optimal | Optimal | Local only |

---

## Further Reading

### Books
- **Boyd & Vandenberghe** - *Convex Optimization* (free PDF available)
- **Nocedal & Wright** - *Numerical Optimization*
- **Bertsimas & Tsitsiklis** - *Introduction to Linear Optimization*
- **Cornuejols & Tütüncü** - *Optimization Methods in Finance*

### Python Libraries
- **CVXPY** - Convex optimization modeling
- **SciPy.optimize** - General optimization
- **Pyomo** - Algebraic modeling language
- **GEKKO** - Nonlinear optimization
- **Google OR-Tools** - Combinatorial optimization

### Online Resources
- CVXPY documentation: https://www.cvxpy.org/
- Boyd's course: https://web.stanford.edu/~boyd/cvxbook/
- NEOS Guide: https://neos-guide.org/content/optimization-tree

---

**Created:** 2025-09-30
**Environment:** `/Users/nattechan/src/finance`
**Dependencies:** NumPy, SciPy, CVXPY
