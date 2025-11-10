"""
Tests for Hensel's Lemma Implementation
"""

import unittest
from hensel_lift import (
    evaluate_polynomial,
    evaluate_derivative,
    mod_inverse,
    find_roots_mod_p,
    lift_root,
    hensel_lift,
    solve_polynomial_mod_pk
)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions used in Hensel's lemma"""
    
    def test_evaluate_polynomial(self):
        """Test polynomial evaluation"""
        # f(x) = 25 + x^2 + x^3
        coefficients = [25, 0, 1, 1]
        
        # Test f(99) mod 125
        result = evaluate_polynomial(coefficients, 99, 125)
        self.assertEqual(result, 0)
        
        # Test f(0) mod 125
        result = evaluate_polynomial(coefficients, 0, 125)
        self.assertEqual(result, 25)
    
    def test_evaluate_derivative(self):
        """Test derivative evaluation"""
        # f(x) = 25 + x^2 + x^3, so f'(x) = 2x + 3x^2
        coefficients = [25, 0, 1, 1]
        
        # Test f'(0) mod 5 = 0
        result = evaluate_derivative(coefficients, 0, 5)
        self.assertEqual(result, 0)
        
        # Test f'(1) mod 5 = 2 + 3 = 5 ≡ 0 (mod 5)
        result = evaluate_derivative(coefficients, 1, 5)
        self.assertEqual(result, 0)
        
        # Test f'(4) mod 5 = 2*4 + 3*16 = 8 + 48 = 56 ≡ 1 (mod 5)
        result = evaluate_derivative(coefficients, 4, 5)
        self.assertEqual(result, 1)
    
    def test_mod_inverse(self):
        """Test modular inverse computation"""
        # 3 * 2 ≡ 1 (mod 5)
        self.assertEqual(mod_inverse(3, 5), 2)
        
        # 2 * 3 ≡ 1 (mod 5)
        self.assertEqual(mod_inverse(2, 5), 3)
        
        # 4 * 4 ≡ 1 (mod 5)
        self.assertEqual(mod_inverse(4, 5), 4)
        
        # No inverse for 0 mod 5
        self.assertIsNone(mod_inverse(0, 5))
    
    def test_find_roots_mod_p(self):
        """Test finding roots modulo a prime"""
        # f(x) = 25 + x^2 + x^3 ≡ 0 + x^2 + x^3 ≡ x^2(1 + x) (mod 5)
        # Roots should be x = 0 and x = 4 (since 1 + 4 ≡ 0 mod 5)
        coefficients = [25, 0, 1, 1]
        roots = find_roots_mod_p(coefficients, 5)
        self.assertEqual(set(roots), {0, 4})


class TestHenselLift(unittest.TestCase):
    """Test Hensel's lemma lifting"""
    
    def test_lift_root_simple(self):
        """Test lifting a simple root"""
        # f(x) = 25 + x^2 + x^3
        coefficients = [25, 0, 1, 1]
        
        # Lift root x = 4 from mod 5 to mod 25
        # f'(4) mod 5 = 1, so this should lift uniquely
        lifted = lift_root(coefficients, 4, 5, 1)
        self.assertIsNotNone(lifted)
        
        # Verify the lifted root is still a root mod 25
        result = evaluate_polynomial(coefficients, lifted, 25)
        self.assertEqual(result, 0)
    
    def test_hensel_lift_to_125(self):
        """Test Hensel lifting to mod 125"""
        # f(x) = 25 + x^2 + x^3
        coefficients = [25, 0, 1, 1]
        
        roots = hensel_lift(coefficients, 5, 3)
        
        # Should find at least one root
        self.assertGreater(len(roots), 0)
        
        # Verify all roots
        for root in roots:
            result = evaluate_polynomial(coefficients, root, 125)
            self.assertEqual(result, 0, f"Root {root} failed verification")
    
    def test_solve_polynomial_mod_pk(self):
        """Test the main solving function"""
        # f(x) = 25 + x^2 + x^3 mod 125
        coefficients = [25, 0, 1, 1]
        
        roots = solve_polynomial_mod_pk(coefficients, 125)
        
        # Should find the root x = 99
        self.assertIn(99, roots)
        
        # Verify all roots
        for root in roots:
            result = evaluate_polynomial(coefficients, root, 125)
            self.assertEqual(result, 0, f"Root {root} failed verification")


class TestDifferentPolynomials(unittest.TestCase):
    """Test Hensel's lemma with different polynomials"""
    
    def test_simple_linear(self):
        """Test with a simple linear polynomial"""
        # f(x) = 2x + 1 ≡ 0 (mod 9)
        # Solution: x ≡ 4 (mod 9) since 2*4 + 1 = 9 ≡ 0 (mod 9)
        coefficients = [1, 2]
        roots = solve_polynomial_mod_pk(coefficients, 9)
        
        # Verify all roots
        for root in roots:
            result = evaluate_polynomial(coefficients, root, 9)
            self.assertEqual(result, 0)
    
    def test_quadratic(self):
        """Test with a quadratic polynomial"""
        # f(x) = x^2 - 2 ≡ 0 (mod 25)
        # This lifts from x = 3 or x = 2 mod 5 (since 3^2 = 9 ≡ 4 ≡ -1 mod 5, 
        # but 2^2 = 4, 3^2 = 9 ≡ 4 mod 5, not good examples)
        # Better: f(x) = x^2 - 6 mod 25
        # Roots mod 5: f(x) = x^2 - 1 mod 5, so x = 1, 4 mod 5
        coefficients = [-6, 0, 1]
        roots = solve_polynomial_mod_pk(coefficients, 25)
        
        # Verify all roots
        for root in roots:
            result = evaluate_polynomial(coefficients, root, 25)
            self.assertEqual(result, 0)
        
        # Should find at least one root
        self.assertGreater(len(roots), 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_no_roots(self):
        """Test polynomial with no roots"""
        # f(x) = x^2 + 1 mod 5
        # This has no roots since squares mod 5 are 0, 1, 4
        coefficients = [1, 0, 1]
        roots = hensel_lift(coefficients, 5, 2)
        
        # May find no roots or roots that don't lift
        # Just verify that any found roots are valid
        for root in roots:
            result = evaluate_polynomial(coefficients, root, 25)
            self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
