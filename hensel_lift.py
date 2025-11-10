"""
Hensel's Lemma Implementation

This module implements Hensel's lemma for lifting roots of polynomial equations
from mod p to mod p^k. Hensel's lemma states that if f(r) ≡ 0 (mod p^k) and 
f'(r) ≢ 0 (mod p), then there exists a unique lift of r to a root modulo p^(k+1).
"""


def evaluate_polynomial(coefficients, x, modulus):
    """
    Evaluate a polynomial at x modulo modulus.
    
    Args:
        coefficients: List of coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...
        x: The value at which to evaluate
        modulus: The modulus for the evaluation
        
    Returns:
        The value of the polynomial at x modulo modulus
    """
    result = 0
    power = 1
    for coeff in coefficients:
        result = (result + coeff * power) % modulus
        power = (power * x) % modulus
    return result


def evaluate_derivative(coefficients, x, modulus):
    """
    Evaluate the derivative of a polynomial at x modulo modulus.
    
    Args:
        coefficients: List of coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...
        x: The value at which to evaluate the derivative
        modulus: The modulus for the evaluation
        
    Returns:
        The value of the derivative at x modulo modulus
    """
    result = 0
    power = 1
    for i in range(1, len(coefficients)):
        result = (result + i * coefficients[i] * power) % modulus
        power = (power * x) % modulus
    return result


def mod_inverse(a, m):
    """
    Compute the modular inverse of a modulo m using the extended Euclidean algorithm.
    
    Args:
        a: The number to invert
        m: The modulus
        
    Returns:
        The modular inverse of a modulo m, or None if it doesn't exist
    """
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m


def find_roots_mod_p(coefficients, p):
    """
    Find all roots of a polynomial modulo a prime p by brute force.
    
    Args:
        coefficients: List of coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...
        p: The prime modulus
        
    Returns:
        List of all roots modulo p
    """
    roots = []
    for x in range(p):
        if evaluate_polynomial(coefficients, x, p) == 0:
            roots.append(x)
    return roots


def lift_root(coefficients, root, p, k):
    """
    Lift a root from mod p^k to mod p^(k+1) using Hensel's lemma.
    
    Args:
        coefficients: List of coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...
        root: The root modulo p^k
        p: The prime
        k: The current power of p
        
    Returns:
        The lifted root modulo p^(k+1), or None if lifting fails
    """
    pk = p ** k
    pk1 = p ** (k + 1)
    
    # Evaluate f(root) mod p^(k+1)
    f_root = evaluate_polynomial(coefficients, root, pk1)
    
    # Evaluate f'(root) mod p
    fprime_root = evaluate_derivative(coefficients, root, p)
    
    # Check if f'(root) ≡ 0 (mod p), which means we can't lift uniquely
    if fprime_root == 0:
        return None
    
    # Compute the inverse of f'(root) modulo p
    inv_fprime = mod_inverse(fprime_root, p)
    if inv_fprime is None:
        return None
    
    # Hensel's formula: r_(k+1) = r_k - f(r_k) / f'(r_k) mod p^(k+1)
    # We compute t = -f(r_k) / p^k mod p
    t = ((-f_root // pk) * inv_fprime) % p
    
    # The new root is r_k + t * p^k
    new_root = (root + t * pk) % pk1
    
    return new_root


def hensel_lift(coefficients, p, target_power):
    """
    Use Hensel's lemma to find all roots of a polynomial modulo p^target_power.
    
    Args:
        coefficients: List of coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...
        p: The prime
        target_power: The target power of p
        
    Returns:
        List of all roots modulo p^target_power
    """
    # Find roots modulo p
    roots = find_roots_mod_p(coefficients, p)
    
    if not roots:
        return []
    
    # Lift roots from p to p^2, p^3, ..., p^target_power
    for k in range(1, target_power):
        new_roots = []
        for root in roots:
            lifted_root = lift_root(coefficients, root, p, k)
            if lifted_root is not None:
                # Verify that the lifted root is indeed a root
                pk1 = p ** (k + 1)
                if evaluate_polynomial(coefficients, lifted_root, pk1) == 0:
                    new_roots.append(lifted_root)
        roots = new_roots
        
        if not roots:
            break
    
    return roots


def solve_polynomial_mod_pk(coefficients, modulus):
    """
    Solve a polynomial equation modulo an arbitrary modulus using Hensel's lemma.
    
    This function finds the smallest prime factor of the modulus and uses Hensel's
    lemma to lift roots.
    
    Args:
        coefficients: List of coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...
        modulus: The modulus (should be a prime power)
        
    Returns:
        List of all roots modulo the given modulus
    """
    # Find the prime base and power
    p = None
    power = 0
    
    # Try to factor the modulus as p^k
    for candidate_p in range(2, modulus + 1):
        if modulus % candidate_p == 0:
            p = candidate_p
            temp = modulus
            power = 0
            while temp % p == 0:
                temp //= p
                power += 1
            if temp == 1:  # modulus is a prime power
                break
            else:
                p = None
                power = 0
    
    if p is None or power == 0:
        raise ValueError(f"Modulus {modulus} is not a prime power")
    
    return hensel_lift(coefficients, p, power)


if __name__ == "__main__":
    # Example: Solve x^3 + x^2 + 25 = 0 (mod 125)
    # Coefficients are [a0, a1, a2, a3] for a0 + a1*x + a2*x^2 + a3*x^3
    coefficients = [25, 0, 1, 1]  # 25 + 0*x + 1*x^2 + 1*x^3
    modulus = 125
    
    print(f"Solving f(x) = x^3 + x^2 + 25 ≡ 0 (mod {modulus})")
    print()
    
    roots = solve_polynomial_mod_pk(coefficients, modulus)
    
    print(f"Roots modulo {modulus}:")
    for root in roots:
        print(f"  x = {root}")
    
    # Verify the roots
    print()
    print("Verification:")
    for root in roots:
        value = evaluate_polynomial(coefficients, root, modulus)
        print(f"  f({root}) = {root}^3 + {root}^2 + 25 ≡ {value} (mod {modulus})")
