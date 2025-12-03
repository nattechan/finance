import numpy as np
from scipy.special import perm

n_values = np.arange(1, 61)

# Calculate in log space to avoid overflow
log_perm = np.array([np.log(perm(60, n, exact=True)) for n in n_values])
log_prob = log_perm - n_values * np.log(60)
prob_success = np.exp(log_prob)

expected_values = prob_success * n_values * 1_000_000

# Find the maximum (store index once)
optimal_idx = np.argmax(expected_values)
optimal_n = n_values[optimal_idx]
max_ev = expected_values[optimal_idx]

print(f"Optimal n: {optimal_n}")
print(f"Maximum Expected Value: ${max_ev:,.2f}")
print(f"Probability of success at optimal n: {prob_success[optimal_idx]:.4f}")