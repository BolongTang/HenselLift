# HenselLift

Hensel's Lemma allows lifting a root of f(x) uniquely from mod p^k to mod p^{k+1}, as long as f'(r) ≠ 0 (the root is simple). A root with multiplicity ≠ 1 may lift nonuniquely or fail to lift.

## Overview

This repository implements Hensel's lemma in Python to solve polynomial equations modulo prime powers. The implementation can solve equations like f(x) = x³ + x² + 25 ≡ 0 (mod 125) by:

1. Finding a small prime that divides the modulus (e.g., 5 for 125 = 5³)
2. Finding roots modulo the prime
3. Lifting roots from p to p², p³, etc., checking that f'(r) ≢ 0 (mod p)
4. Returning all valid roots modulo the target power

## Usage

### Basic Example

```python
from hensel_lift import solve_polynomial_mod_pk

# Solve x^3 + x^2 + 25 = 0 (mod 125)
# Coefficients: [a0, a1, a2, a3] for a0 + a1*x + a2*x^2 + a3*x^3
coefficients = [25, 0, 1, 1]
modulus = 125

roots = solve_polynomial_mod_pk(coefficients, modulus)
print(f"Roots: {roots}")  # Output: Roots: [99]
```

### Running Examples

```bash
python3 hensel_lift.py      # Run the main example
python3 examples.py          # Run multiple examples
python3 -m unittest test_hensel_lift  # Run tests
```

## How It Works

The algorithm follows these steps:

1. **Find the prime base**: Factor the modulus as p^k
2. **Find roots mod p**: Test all values 0 to p-1 to find roots
3. **Check liftability**: For each root r, verify f'(r) ≢ 0 (mod p)
4. **Lift iteratively**: Use Hensel's formula to lift from p^k to p^(k+1):
   ```
   r_(k+1) = r_k - f(r_k) / f'(r_k) mod p^(k+1)
   ```
5. **Verify**: Check that lifted roots are still valid

## API Reference

### Main Functions

- `solve_polynomial_mod_pk(coefficients, modulus)` - Solve polynomial equation modulo a prime power
- `hensel_lift(coefficients, p, target_power)` - Lift roots from mod p to mod p^target_power
- `evaluate_polynomial(coefficients, x, modulus)` - Evaluate polynomial at x
- `evaluate_derivative(coefficients, x, modulus)` - Evaluate derivative at x

### Input Format

Coefficients are specified as a list `[a0, a1, a2, ...]` representing:
```
f(x) = a0 + a1*x + a2*x^2 + a3*x^3 + ...
```

For example, x³ + x² + 25 is represented as `[25, 0, 1, 1]`.

## Examples

See `examples.py` for more use cases including:
- Cubic equations (x³ + x² + 25 ≡ 0 mod 125)
- Quadratic equations (x² - 6 ≡ 0 mod 25)
- Linear equations (2x + 1 ≡ 0 mod 27)
- Higher degree polynomials

## Limitations

- The modulus must be a prime power (p^k)
- Roots with f'(r) ≡ 0 (mod p) cannot be lifted uniquely
- For large primes, finding roots mod p uses brute force
