from moebius import *
from icecream import ic
import matplotlib.pyplot as plt

def random_complex(shape=()):
    return np.random.rand(*shape) + 1j * np.random.rand(*shape) - 0.5 - 0.5j


def test1():
    """ Test moebius_circle, to see if it correctly maps a circle to another circle."""
    
    # Define a random circle
    z1 = random_complex()
    r1 = np.random.rand()
    r1 = 0.01
    ic(z1, r1)
    
    # Define a random Moebius transformation
    a, b, c, d = random_complex((4,))
    ic(a, b, c, d)
    
    # Compute the image of the circle under the Moebius transformation
    z2, r2 = moebius_circle(z1, r1, a, b, c, d)
    ic(z2, r2)
    
    # Compute the circle as a set of points
    t = np.linspace(0, 2*np.pi, 100)
    circle_z = z1 + r1 * np.exp(1j*t)
    circle_z2 = moebius(circle_z, a, b, c, d)
    
    # Transform the circle points and check that they lie on the transformed circle
    distance = np.abs(circle_z2 - z2) - r2
    ic(np.linalg.norm(distance))
    assert(np.allclose(distance, 0))


    # # plot the circles    
    # plt.figure()
    # plt.plot(np.real(circle_z), np.imag(circle_z), label='Original circle')
    # plt.plot(np.real(circle_z2), np.imag(circle_z2), label='Transformed circle')             
    # plt.plot(np.real(z2) + r2 * np.cos(t), np.imag(z2) + r2 * np.sin(t), linestyle='--', label='Transformed circle (analytical)')
    # plt.axis('equal')
    # plt.legend()
    # plt.show()
    
    
def test2():
    """ Test parameterized_moebius, to see if it correctly maps z1, z2, z3 to w1, w2, w3."""
    # Generate 2 sets of 3 random complex numbers
    z1 = random_complex()
    z2 = random_complex()
    z3 = random_complex()
    w1 = random_complex()
    w2 = random_complex()
    w3 = random_complex()
    ic(z1, z2, z3, w1, w2, w3)
    
    # Compute the Moebius transformation that maps z1, z2, z3 to w1, w2, w3
    a,b,c,d = parameterized_moebius(z1, z2, z3, w1, w2, w3)
    ic(a, b, c, d)
    
    # Test that the Moebius transformation is correct
    
    distance1 = np.abs(moebius(z1, a, b, c, d) - w1)
    distance2 = np.abs(moebius(z2, a, b, c, d) - w2)
    distance3 = np.abs(moebius(z3, a, b, c, d) - w3)
    ic(np.linalg.norm(distance1))
    ic(np.linalg.norm(distance2))
    ic(np.linalg.norm(distance3))
    
    assert(np.isclose(w1, moebius(z1, a, b, c, d)))
    assert(np.isclose(w2, moebius(z2, a, b, c, d)))
    assert(np.isclose(w3, moebius(z3, a, b, c, d)))
    
    
    

if __name__ == "__main__":
    np.random.seed(666)
    
    for k in range(10):
        test1()
        test2()