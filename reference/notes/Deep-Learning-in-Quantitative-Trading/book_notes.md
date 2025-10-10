# Deep Learning in Quantitative Trading Notes

## Reading from: Deep Learning in Quantitative Trading

### Original Code Repository Location

- GitHub: [zcakhaa/Deep-Learning-in-Quantitative-Trading](https://github.com/zcakhaa/Deep-Learning-in-Quantitative-Trading)
- Local submodule: `reference/Deep-Learning-in-Quantitative-Trading/`
- Notebooks by chapter: `reference/Deep-Learning-in-Quantitative-Trading/Chapter{2-7}/`
- Utilities: `reference/Deep-Learning-in-Quantitative-Trading/Utilis/`
- Data: `reference/Deep-Learning-in-Quantitative-Trading/Data/`

### My Code

See `reference/notes/Deep-Learning-in-Quantitative-Trading/python_notes.ipynb` for my learning implementation adapted to Canadian fixed income markets.

---

## Book Structure

### Part 1: Foundations

#### Chapter 2 - Fundamentals of Financial Time-Series
**Notebooks:**
- `Chapter2/01_statistics.ipynb` - Statistical analysis and hypothesis testing
- `Chapter2/02_time_series_models.ipynb` - Classical time-series models (AR, MA, ARMA, ARIMA)
- `Chapter2/03_volatility_clustering.ipynb` - GARCH models and volatility analysis

**Key Concepts:**
- Time-series properties: stationarity, autocorrelation, partial autocorrelation
- Statistical tests: ADF test, KPSS test, Ljung-Box test
- Classical forecasting: AR, MA, ARMA, ARIMA models
- Volatility modeling: GARCH, EGARCH, GJR-GARCH
- Correlation analysis and cointegration

**Application to Canadian Fixed Income:**
- Analyzing GoC yield curve dynamics
- Modeling CORRA rate time-series
- Credit spread volatility clustering
- Provincial bond spread correlation

#### Chapter 3 - Deep Learning Algorithms
**Notebooks:**
- Fully connected neural networks (dense layers)
- Convolutional neural networks (CNNs) for feature extraction
- Recurrent neural networks (RNNs, LSTMs, GRUs) for sequential data
- Advanced architectures: WaveNet, Encoder-Decoders, Transformers

**Key Concepts:**
- Supervised learning fundamentals
- Activation functions and optimization
- Backpropagation and gradient descent
- Regularization techniques (dropout, batch normalization)
- Sequence modeling with attention mechanisms

**Application to Canadian Fixed Income:**
- Bond return prediction using LSTMs
- Yield curve shape classification with CNNs
- Transformer models for multi-asset prediction
- Attention mechanisms for credit spread forecasting

#### Chapter 4 - Model Training and Deployment
**Key Concepts:**
- Data collection and preprocessing
- Train/validation/test splits
- Cross-validation for hyperparameter tuning
- Overfitting detection and mitigation
- Model evaluation metrics
- Production deployment considerations

**Application to Canadian Fixed Income:**
- Walk-forward validation for bond strategies
- Time-series cross-validation
- Performance metrics: Sharpe ratio, information ratio, max drawdown
- Production constraints: latency, data availability

---

### Part 2: Applications

#### Chapter 5 - Momentum Trading Strategies
**Notebooks:**
- `Chapter5/01_time_series_momentum.ipynb` - Time-series momentum (trend-following)
- `Chapter5/02_cross_sectional_momentum.ipynb` - Cross-sectional momentum (relative value)
- `Chapter5/03_deep_momentum_strategy.ipynb` - End-to-end neural networks optimized for Sharpe ratio

**Key Concepts:**
- Time-series momentum: trend-following strategies
- Cross-sectional momentum: relative strength across assets
- Deep momentum networks: direct position output
- End-to-end optimization for performance metrics
- Risk-adjusted return maximization

**Application to Canadian Fixed Income:**
- GoC bond duration momentum
- Provincial bond relative value momentum
- Corporate credit spread momentum
- Cross-asset momentum (bonds vs equity)

#### Chapter 6 - Portfolio Optimization
**Notebooks:**
- `Chapter6/01_classical_portfolio_optimization.ipynb` - Mean-variance optimization, Black-Litterman
- `Chapter6/02_deep_portfolio_optimization.ipynb` - Neural network portfolio optimizers

**Key Concepts:**
- Classical mean-variance optimization
- Black-Litterman model
- Risk parity and minimum variance portfolios
- Deep learning for covariance matrix estimation
- Neural networks for portfolio weight optimization
- End-to-end portfolio construction

**Application to Canadian Fixed Income:**
- GoC bond portfolio optimization with duration constraints
- Credit portfolio optimization with sector limits
- Multi-asset allocation (bonds, swaps, credit)
- Dynamic rebalancing with transaction costs

#### Chapter 7 - High-Frequency Trading and Microstructure
**Notebooks:**
- `Chapter7/01_limit_order_books.ipynb` - Order book dynamics and features
- `Chapter7/02_predictive_signal_lob.ipynb` - Deep learning for LOB prediction

**Key Concepts:**
- Limit order book (LOB) structure and dynamics
- Microstructure features: bid-ask spread, depth, imbalance
- Hybrid neural networks for LOB prediction
- Reinforcement learning for trade execution
- Generative models for financial data

**Application to Canadian Fixed Income:**
- GoC bond auction dynamics
- Corporate bond liquidity prediction
- Optimal execution for illiquid bonds
- Market impact modeling

---

## Key Takeaways for Quantitative Fixed Income

### Data Considerations
- **Time-series properties**: Fixed income returns exhibit lower volatility than equities but significant autocorrelation
- **Regime changes**: Interest rate cycles require regime-aware models
- **Illiquidity**: Canadian corporate bonds have sparse data; need to handle missing observations
- **Calendar effects**: Month-end, quarter-end, auction days

### Model Architecture Choices
- **LSTMs**: Good for yield curve forecasting and credit spread prediction
- **CNNs**: Effective for pattern recognition in correlation matrices
- **Transformers**: Powerful for multi-asset prediction with attention on key features
- **Ensemble methods**: Combine classical finance models with deep learning

### Risk Management
- **Duration risk**: Neural networks should respect duration constraints
- **Credit risk**: Models should account for default probability
- **Liquidity risk**: Transaction costs and market impact
- **Model risk**: Validation against classical models and market benchmarks

### Production Considerations
- **Latency**: Bond markets are slower than equities; daily rebalancing often sufficient
- **Data quality**: Bloomberg data availability and reliability
- **Regulatory**: OSFI capital requirements for model-based strategies
- **Interpretability**: Black-box models require robust validation

---

## Implementation Notes

### Python Environment
```bash
# Book uses:
# - TensorFlow / PyTorch for deep learning
# - pandas, numpy for data manipulation
# - matplotlib, seaborn for visualization

# My adaptations use:
# - PyTorch (preferred over TensorFlow)
# - Polars for large datasets
# - QuantLib for fixed income pricing
# - rateslib for curve construction
```

### Data Sources for Canadian Markets
- **Bloomberg (xbbg)**: GoC bonds, provincial bonds, corporate bonds, swap rates
- **Bank of Canada**: CORRA rates, policy rates
- **IIROC**: Trade reporting data (if available)
- **FTSE Russell**: Canadian bond indices

### Key Adaptations for Fixed Income
1. **Returns**: Use yield changes or spread changes instead of price returns
2. **Features**: Include curve features (slope, curvature), credit features (rating, sector)
3. **Constraints**: Duration-neutral, sector limits, rating limits
4. **Costs**: Bid-ask spreads significantly wider than equities
5. **Benchmarks**: Compare to passive indices (e.g., FTSE Canada Universe Bond Index)

---

## Questions to Explore

1. How do deep learning models compare to classical factor models for Canadian credit?
2. Can transformers capture regime changes in interest rate cycles?
3. What is the optimal lookback period for fixed income momentum?
4. How to handle data sparsity in illiquid corporate bonds?
5. Can reinforcement learning improve execution in illiquid markets?
6. How to combine fundamental credit analysis with deep learning?
7. What features are most important for predicting credit spread changes?

---

## Related Reading

- **QuantLib Python Cookbook**: `reference/quantlibpythoncookbook.pdf`
- **Interest Rate Instruments**: `reference/Interest-Rate-Instruments-and-Market-Conventions.pdf`
- **Pricing and Trading IRDs**: `reference/notes/book_irds3/book_notes.md`
- **QuantFinanceBook**: `reference/notes/QuantFinanceBook/book_notes.md`

---

**Last Updated**: 2025-10-09
**Status**: Initial setup - ready for study
