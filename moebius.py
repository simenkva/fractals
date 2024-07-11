import numpy as np

def moebius(z, a, b, c, d):
    """ Compute Moebius transformation. 
    
    $$ f(z) = \frac{a z + b}{c z + d} $$
    
    
    Args:
        z: complex number or array of complex numbers
        a, b, c, d: complex numbers
        
    Returns:
        complex number or array of transformed complex numbers
        
    """
    return (a*z + b) / (c*z + d)

def compose_moebius(a1, b1, c1, d1, a2, b2, c2, d2):
    """ Compose two Moebius transformations.
    
    $$ f(z) = \frac{a1 z + b1}{c1 z + d1} $$
    $$ g(z) = \frac{a2 z + b2}{c2 z + d2} $$
    $$ f(g(z)) = \frac{a z + b}{c z + d} $$
    
    Args:
        a1, b1, c1, d1: complex numbers
        a2, b2, c2, d2: complex numbers
        
    Returns:
        a, b, c, d: complex numbers
    
    """
    a = a1*a2 + b1*c2
    b = a1*b2 + b1*d2
    c = c1*a2 + d1*c2
    d = c1*b2 + d1*d2
    return a, b, c, d

def inverse_moebius(a, b, c, d):
    """ Compute inverse of Moebius transformation.
    
    $$ f(z) = \frac{a z + b}{c z + d} $$    
    $$ f^{-1}(z) = \frac{-d}{a d - b c} z + \frac{b}{a d - b c} $$
    
    We scale the inverse with the determinant of [a, b; c, d], so that inverting
    twice gives the original function parameters since Moeibus transformations are
    not unique.
    
    Args:
        a, b, c, d: complex numbers

    Returns:
        a_inv, b_inv, c_inv, d_inv: complex numbers
        
    """
    det = a*d - b*c
    a_inv = -d/det
    b_inv = b/det
    c_inv = c/det
    d_inv = -a/det
    return a_inv, b_inv, c_inv, d_inv



def parameterized_moebius(z1, z2, z3, w1, w2, w3):
    """ Compute Moebius transformation parameters that take
    z1 to w1, z2 to w2, z3 to w3.
    
    Args:
        z1, z2, z3: complex numbers
        w1, w2, w3: complex numbers
        
    Returns:
        a, b, c, d: complex numbers
    
    """
    
    k1 = (z2 - z3)/(z2 - z1)
    a1 = k1
    b1 = -z1 * k1
    c1 = 1
    d1 = -z3
    
    k2 = (w2 - w3)/(w2 - w1)
    a2 = k2
    b2 = -w1 * k2
    c2 = 1
    d2 = -w3
    a3, b3, c3, d3 = inverse_moebius(a2, b2, c2, d2)
    
    a, b, c, d = compose_moebius(a3, b3, c3, d3, a1, b1, c1, d1)

    return a, b, c, d

def inverse_circle(z, r):
    """ Compute circle inversion with respect to unit circle."""
    
    R = np.abs(z)
    phi = np.angle(z)
    
    r_inv = np.abs(1/(R-r) - 1/(R+r)) / 2
    z_inv = (1/(R-r) + 1/(R+r)) / 2
    z_inv = z_inv * np.exp(-1j*phi)
    return z_inv, r_inv

def moebius_circle(z, r, a, b, c, d):
    """ Compute Moebius transformation of circle.
    
    We factorize the Moebius transformation f(z) = (a*z + b) / (c*z + d) into
    three transformations: w1 = c*z + d, w2 = 1/w1, w3 = (b - ad/c)*w2 +  a/c.
    Hence, f = w3 o w2 o w1.
    
    w1 and w3 are affine, with simple rules for circles. w2 is inversion, and we will use
    the function inverse_circle to compute the inverse circle.
    
    Args:
        z: complex number
        r: radius of circle
        a, b, c, d: complex numbers
        
    Returns:
        transformed_z: complex number
        transformed_r: radius of transformed circle
    
    """
    
    # special case for c = 0
    if np.isclose(c, 0):
        transformed_z = a/d * z + b/d
        transformed_r = np.abs(a/d) * r
    else:
        z1 = c * z + d
        r1 = np.abs(c) * r
        z2, r2 = inverse_circle(z1, r1)
        transformed_z = (b - a*d/c)*z2 + a/c
        transformed_r = np.abs(b - a*d/c) * r2

    return transformed_z, transformed_r