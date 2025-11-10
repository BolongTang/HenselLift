"""
Examples of using Hensel's Lemma to solve polynomial equations modulo prime powers.
"""

from hensel_lift import solve_polynomial_mod_pk, evaluate_polynomial


def example_1():
    """
    Example 1: Solve x^3 + x^2 + 25 = 0 (mod 125)
    
    This is the main example from the problem statement.
    """
    print("=" * 60)
    print("Example 1: x^3 + x^2 + 25 ≡ 0 (mod 125)")
    print("=" * 60)
    
    # Coefficients: [a0, a1, a2, a3] for a0 + a1*x + a2*x^2 + a3*x^3
    coefficients = [25, 0, 1, 1]
    modulus = 125
    
    print(f"Finding roots of f(x) = x^3 + x^2 + 25 modulo {modulus}")
    print()
    
    # Note: 125 = 5^3, so we use prime p = 5 and lift to power 3
    print("Step 1: Recognize that 125 = 5^3")
    print("Step 2: Find roots modulo 5")
    print("        f(x) ≡ x^3 + x^2 (mod 5)")
    print("        Testing: f(0) = 0, f(1) = 2, f(2) = 2, f(3) = 2, f(4) = 0")
    print("        Roots mod 5: x = 0, 4")
    print()
    print("Step 3: Check which roots can be lifted (f'(r) ≠ 0 mod 5)")
    print("        f'(x) = 3x^2 + 2x")
    print("        f'(0) = 0 (mod 5) - cannot lift uniquely")
    print("        f'(4) = 48 + 8 = 56 ≡ 1 (mod 5) - can lift!")
    print()
    print("Step 4: Lift x = 4 from mod 5 to mod 25 to mod 125")
    
    roots = solve_polynomial_mod_pk(coefficients, modulus)
    
    print()
    print(f"Final roots modulo {modulus}:")
    for root in roots:
        print(f"  x = {root}")
    
    # Verify
    print()
    print("Verification:")
    for root in roots:
        value = root**3 + root**2 + 25
        print(f"  f({root}) = {root}^3 + {root}^2 + 25 = {value} ≡ {value % modulus} (mod {modulus})")
    print()


def example_2():
    """
    Example 2: Solve x^2 - 6 = 0 (mod 25)
    """
    print("=" * 60)
    print("Example 2: x^2 - 6 ≡ 0 (mod 25)")
    print("=" * 60)
    
    coefficients = [-6, 0, 1]  # -6 + 0*x + 1*x^2
    modulus = 25
    
    print(f"Finding roots of f(x) = x^2 - 6 modulo {modulus}")
    print()
    print("Note: 25 = 5^2, so we use prime p = 5 and lift to power 2")
    print("Roots mod 5: x^2 ≡ 6 ≡ 1 (mod 5), so x = 1, 4")
    
    roots = solve_polynomial_mod_pk(coefficients, modulus)
    
    print()
    print(f"Roots modulo {modulus}:")
    for root in roots:
        print(f"  x = {root}")
    
    print()
    print("Verification:")
    for root in roots:
        value = root**2 - 6
        print(f"  f({root}) = {root}^2 - 6 = {value} ≡ {value % modulus} (mod {modulus})")
    print()


def example_3():
    """
    Example 3: Solve 2x + 1 = 0 (mod 27)
    """
    print("=" * 60)
    print("Example 3: 2x + 1 ≡ 0 (mod 27)")
    print("=" * 60)
    
    coefficients = [1, 2]  # 1 + 2*x
    modulus = 27
    
    print(f"Finding roots of f(x) = 2x + 1 modulo {modulus}")
    print()
    print("Note: 27 = 3^3, so we use prime p = 3 and lift to power 3")
    
    roots = solve_polynomial_mod_pk(coefficients, modulus)
    
    print()
    print(f"Roots modulo {modulus}:")
    for root in roots:
        print(f"  x = {root}")
    
    print()
    print("Verification:")
    for root in roots:
        value = 2 * root + 1
        print(f"  f({root}) = 2*{root} + 1 = {value} ≡ {value % modulus} (mod {modulus})")
    print()


def example_4():
    """
    Example 4: Custom polynomial - x^4 + 2x + 3 = 0 (mod 49)
    """
    print("=" * 60)
    print("Example 4: x^4 + 2x + 3 ≡ 0 (mod 49)")
    print("=" * 60)
    
    coefficients = [3, 2, 0, 0, 1]  # 3 + 2*x + 0*x^2 + 0*x^3 + 1*x^4
    modulus = 49
    
    print(f"Finding roots of f(x) = x^4 + 2x + 3 modulo {modulus}")
    print()
    print("Note: 49 = 7^2, so we use prime p = 7 and lift to power 2")
    
    roots = solve_polynomial_mod_pk(coefficients, modulus)
    
    print()
    if roots:
        print(f"Roots modulo {modulus}:")
        for root in roots:
            print(f"  x = {root}")
        
        print()
        print("Verification:")
        for root in roots:
            value = evaluate_polynomial(coefficients, root, modulus)
            print(f"  f({root}) ≡ {value} (mod {modulus})")
    else:
        print(f"No roots found modulo {modulus}")
    print()


if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
    example_4()
    
    print("=" * 60)
    print("Custom Usage")
    print("=" * 60)
    print()
    print("To solve your own polynomial equation:")
    print("1. Define coefficients as [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...")
    print("2. Specify the modulus (must be a prime power p^k)")
    print("3. Call solve_polynomial_mod_pk(coefficients, modulus)")
    print()
    print("Example code:")
    print("    from hensel_lift import solve_polynomial_mod_pk")
    print("    coefficients = [25, 0, 1, 1]  # x^3 + x^2 + 25")
    print("    roots = solve_polynomial_mod_pk(coefficients, 125)")
    print("    print(roots)")
    print()
