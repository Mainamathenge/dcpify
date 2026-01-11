import numpy as np
from scipy.special import iv as BesselI
from scipy.special import kv as BesselK
from scipy.special import jv as BesselJ
from scipy.special import yv as BesselY
from scipy.special import struve as StruveH
from scipy.special import modstruve as StruveL
from scipy.integrate import nquad
from scipy.constants import mu_0, epsilon_0

# input set of frequencies
freq = np.linspace(50E6, 300E6, 6)

# Voltage fuction - calculates the induced voltage signal for a given frequency along with some other arguments
def V(f, v_x, v_y, R, L, M, n, a, b, l, w, h, m, W, H, D):

    ω = 2*np.pi*f

    threshold = 30

    def f1(x, y, z, k, ω, n, a, b, l) :
        term1 = ((z-b)/np.sqrt((y-b)**2+(z-b)**2)) * (np.sin(k*l/2)/k) * np.cos(k*(x-2*b-l/2))
        arg = np.sqrt(ω**2 * mu_0 * epsilon_0 - k**2)
        # Use asymptotic expansion for large arguments
        if arg * a > threshold:
            # Asymptotic expansion
            term2_a = -np.sqrt(2/(np.pi*arg*np.sqrt((y-b)**2+(z-b)**2))) * np.sin(arg*np.sqrt((y-b)**2+(z-b)**2) + np.pi/4)
            term2_b = -3/8 * np.sqrt(2/(np.pi*arg**3*np.sqrt((y-b)**2+(z-b)**2)**3)) * np.cos(arg*np.sqrt((y-b)**2+(z-b)**2) + np.pi/4)
            term2 = term2_a + term2_b
            term3_a = np.sqrt(2 / (np.pi * (arg * a))) * np.cos(arg * a - np.pi/4)
            term3_b = np.sqrt(2 / (np.pi * (arg * b))) * np.cos(arg * b - np.pi/4)
            term3 = np.pi * (term3_a - term3_b) / (2 * arg)
        else:
            # Regular form
            term2 = BesselY(1, arg * np.sqrt((y-b)**2+(z-b)**2))
            term3 = np.pi * (
                BesselJ(0, arg * a) * StruveH(1, arg * a) * a
                - BesselJ(1, arg * a) * StruveH(0, arg * a) * a
                - BesselJ(0, arg * b) * StruveH(1, arg * b) * b
                + BesselJ(1, arg * b) * StruveH(0, arg * b) * b
            ) / (2 * arg)
        return term1 * term2 * term3

    def f2(x, y, z, k, ω, n, a, b, l) :
        term1 = -(2/np.pi) * ((z-b)/np.sqrt((y-b)**2+(z-b)**2)) * (np.sin(k*l/2)/k) * np.cos(k*(x-2*b-l/2))
        arg = np.sqrt(k**2 - ω**2 * mu_0 * epsilon_0)
        # Use asymptotic expansion for large arguments
        if arg * a > threshold:
            # Asymptotic expansion
            term2 = 1
            term3_a = np.sqrt(b/(4*np.sqrt((y-b)**2+(z-b)**2))) * (1/arg**2 + 1/(8*arg**3)*(3/np.sqrt((y-b)**2+(z-b)**2)-7/b)) * np.exp(-arg*(np.sqrt((y-b)**2+(z-b)**2)-b))
            term3_b = np.sqrt(a/(4*np.sqrt((y-b)**2+(z-b)**2))) * (1/arg**2 + 1/(8*arg**3)*(3/np.sqrt((y-b)**2+(z-b)**2)-7/a)) * np.exp(-arg*(np.sqrt((y-b)**2+(z-b)**2)-a))
            term3 = term3_a + term3_b
        else:
            # Regular form
            term2 = BesselK(1, arg * np.sqrt((y-b)**2+(z-b)**2))
            term3 = np.pi * (
                BesselI(0, arg * a) * StruveL(1, arg * a) * a
                - BesselI(1, arg * a) * StruveL(0, arg * a) * a
                - BesselI(0, arg * b) * StruveL(1, arg * b) * b
                + BesselI(1, arg * b) * StruveL(0, arg * b) * b
            ) / (2 * arg)
        return term1 * term2 * term3

    def f3(x, y, z, k, ω, n, a, b, l) :
        term1 = ((z-b)/np.sqrt((y-b)**2+(z-b)**2)) * (np.sin(k*l/2)/k) * np.cos(k*(x-2*b-l/2))
        arg = np.sqrt(ω**2 * mu_0 * epsilon_0 - k**2)
        # Use asymptotic expansion for large arguments
        if arg * a > threshold:
            # Asymptotic expansion
            term2_a = -np.sqrt(2/(np.pi*arg*np.sqrt((y-b)**2+(z-b)**2))) * np.cos(arg*np.sqrt((y-b)**2+(z-b)**2) + np.pi/4)
            term2_b = 3/8 * np.sqrt(2/(np.pi*arg**3*np.sqrt((y-b)**2+(z-b)**2)**3)) * np.sin(arg*np.sqrt((y-b)**2+(z-b)**2) + np.pi/4)
            term2 = term2_a + term2_b
            term3_a = np.sqrt(2 / (np.pi * (arg * a))) * np.cos(arg * a - np.pi/4)
            term3_b = np.sqrt(2 / (np.pi * (arg * b))) * np.cos(arg * b - np.pi/4)
            term3 = np.pi * (term3_a - term3_b) / (2 * arg)
        else:
            # Regular form
            term2 = BesselJ(1, arg * np.sqrt((y-b)**2+(z-b)**2))
            term3 = np.pi * (
                BesselJ(0, arg * a) * StruveH(1, arg * a) * a
                - BesselJ(1, arg * a) * StruveH(0, arg * a) * a
                - BesselJ(0, arg * b) * StruveH(1, arg * b) * b
                + BesselJ(1, arg * b) * StruveH(0, arg * b) * b
            ) / (2 * arg)
        return term1 * term2 * term3


    def g1(x, y, z, k, ω, n, a, b, l) :
        term1 = ((z-b)/np.sqrt((x-b)**2+(z-b)**2)) * (np.sin(k*l/2)/k) * np.cos(k*(y-2*b-l/2))
        arg = np.sqrt(ω**2 * mu_0 * epsilon_0 - k**2)
        # Use asymptotic expansion for large arguments
        if arg * a > threshold:
            # Asymptotic expansion
            term2_a = -np.sqrt(2/(np.pi*arg*np.sqrt((x-b)**2+(z-b)**2))) * np.sin(arg*np.sqrt((x-b)**2+(z-b)**2) + np.pi/4)
            term2_b = -3/8*np.sqrt(2/(np.pi*arg**3*np.sqrt((x-b)**2+(z-b)**2)**3)) * np.cos(arg*np.sqrt((x-b)**2+(z-b)**2) + np.pi/4)
            term2 = term2_a + term2_b
            term3_a = np.sqrt(2 / (np.pi * (arg * a))) * np.cos(arg * a - 0.25 * np.pi)
            term3_b = np.sqrt(2 / (np.pi * (arg * b))) * np.cos(arg * b - 0.25 * np.pi)
            term3 = np.pi * (term3_a - term3_b) / (2 * arg)
        else:
            # Regular forms
            term2 = BesselY(1, arg * np.sqrt((x-b)**2 + (z-b)**2))
            term3 = np.pi * (
                BesselJ(0, arg * a) * StruveH(1, arg * a) * a
                - BesselJ(1, arg * a) * StruveH(0, arg * a) * a
                - BesselJ(0, arg * b) * StruveH(1, arg * b) * b
                + BesselJ(1, arg * b) * StruveH(0, arg * b) * b
            ) / (2 * arg)
        return term1 * term2 * term3

    def g2(x, y, z, k, ω, n, a, b, l) :
        term1 = -(2/np.pi) * ((z-b)/np.sqrt((x-b)**2+(z-b)**2)) * (np.sin(k*l/2)/k) * np.cos(k*(y-2*b-l/2))
        arg = np.sqrt(k**2 - ω**2 * mu_0 * epsilon_0)
        # Use asymptotic expansion for large arguments
        if arg * a > threshold:
            # Asymptotic expansion
            term2 = 1
            term3_a = np.sqrt(b/(4*np.sqrt((x-b)**2+(z-b)**2))) * (1/arg**2 + 1/(8*arg**3)*(3/np.sqrt((x-b)**2+(z-b)**2)-7/b)) * np.exp(-arg*(np.sqrt((x-b)**2+(z-b)**2)-b))
            term3_b = np.sqrt(a/(4*np.sqrt((x-b)**2+(z-b)**2))) * (1/arg**2 + 1/(8*arg**3)*(3/np.sqrt((x-b)**2+(z-b)**2)-7/a)) * np.exp(-arg*(np.sqrt((x-b)**2+(z-b)**2)-a))
            term3 = term3_a + term3_b
        else:
            # Regular forms
            term2 = BesselK(1, arg * np.sqrt((x-b)**2+(z-b)**2))
            term3 = np.pi * (
                BesselI(0, arg * a) * StruveL(1, arg * a) * a
                - BesselI(1, arg * a) * StruveL(0, arg * a) * a
                - BesselI(0, arg * b) * StruveL(1, arg * b) * b
                + BesselI(1, arg * b) * StruveL(0, arg * b) * b
            ) / (2 * arg)
        return term1 * term2 * term3

    def g3(x, y, z, k, ω, n, a, b, l) :
        term1 = ((z-b)/np.sqrt((x-b)**2+(z-b)**2)) * (np.sin(k*l/2)/k) * np.cos(k*(y-2*b-l/2))
        arg = np.sqrt(ω**2 * mu_0 * epsilon_0 - k**2)
        # Use asymptotic expansion for large arguments
        if arg * a > threshold:
            # Asymptotic expansion
            term2_a = -np.sqrt(2/(np.pi*arg*np.sqrt((x-b)**2+(z-b)**2))) * np.cos(arg*np.sqrt((x-b)**2+(z-b)**2) + np.pi/4)
            term2_b = 3/8 * np.sqrt(2/(np.pi*arg**3*np.sqrt((x-b)**2+(z-b)**2)**3)) * np.sin(arg*np.sqrt((x-b)**2+(z-b)**2) + np.pi/4)
            term2 = term2_a + term2_b
            term3_a = np.sqrt(2 / (np.pi * (arg * a))) * np.cos(arg * a - 0.25 * np.pi)
            term3_b = np.sqrt(2 / (np.pi * (arg * b))) * np.cos(arg * b - 0.25 * np.pi)
            term3 = np.pi * (term3_a - term3_b) / (2 * arg)
        else:
            # Regular forms
            term2 = BesselJ(1, arg * np.sqrt((x-b)**2+(z-b)**2))
            term3 = np.pi * (
                BesselJ(0, arg * a) * StruveH(1, arg * a) * a
                - BesselJ(1, arg * a) * StruveH(0, arg * a) * a
                - BesselJ(0, arg * b) * StruveH(1, arg * b) * b
                + BesselJ(1, arg * b) * StruveH(0, arg * b) * b
            ) / (2 * arg)
        return term1 * term2 * term3

    # Calculate voltage in first antenna element
    V1_g1, _ = nquad(g1, [[w+m, w+m+D], [w/4, w/4+W], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V1_g2, _ = nquad(g2, [[w+m, w+m+D], [w/4, w/4+W], [h, h+H], [ω*np.sqrt(mu_0*epsilon_0), np.inf]], args=(ω, n, a, b, l))
    V1_g3, _ = nquad(g3, [[w+m, w+m+D], [w/4, w/4+W], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V1 = (mu_0 * n * (complex(R, ω*L)*v_y - complex(0, ω*M*v_x)) / (complex(R, ω*L)**2 + (ω*M)**2)) * (V1_g1 + V1_g2 + 1j*V1_g3)

    # Calculate voltage in second antenna element
    V2_f1, _ = nquad(f1, [[w/4, w/4+W], [w+m, w+m+D], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V2_f2, _ = nquad(f2, [[w/4, w/4+W], [w+m, w+m+D], [h, h+H], [ω*np.sqrt(mu_0*epsilon_0), np.inf]], args=(ω, n, a, b, l))
    V2_f3, _ = nquad(f3, [[w/4, w/4+W], [w+m, w+m+D], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V2 = (-mu_0 * n * (complex(R, ω*L)*v_x - complex(0, ω*M*v_y)) / (complex(R, ω*L)**2 + (ω*M)**2)) * (V2_f1 + V2_f2 + 1j*V2_f3)

    # Calculate voltage in third antenna element
    V3_g1, _ = nquad(g1, [[-m-D, -m], [3*w/4, 3*w/4+W], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V3_g2, _ = nquad(g2, [[-m-D, -m], [3*w/4, 3*w/4+W], [h, h+H], [ω*np.sqrt(mu_0*epsilon_0), np.inf]], args=(ω, n, a, b, l))
    V3_g3, _ = nquad(g3, [[-m-D, -m], [3*w/4, 3*w/4+W], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V3 = (mu_0 * n * (complex(R, ω*L)*v_y - complex(0, ω*M*v_x)) / (complex(R, ω*L)**2 + (ω*M)**2)) * (V3_g1 + V3_g2 + 1j*V3_g3)

    # Calculate voltage in fourth antenna element
    V4_f1, _ = nquad(f1, [[3*w/4, 3*w/4+W], [-m-D, -m], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V4_f2, _ = nquad(f2, [[3*w/4, 3*w/4+W], [-m-D, -m], [h, h+H], [ω*np.sqrt(mu_0*epsilon_0), np.inf]], args=(ω, n, a, b, l))
    V4_f3, _ = nquad(f3, [[3*w/4, 3*w/4+W], [-m-D, -m], [h, h+H], [0, ω*np.sqrt(mu_0*epsilon_0)]], args=(ω, n, a, b, l))
    V4 = (-mu_0 * n * (complex(R, ω*L)*v_x - complex(0, ω*M*v_y)) / (complex(R, ω*L)**2 + (ω*M)**2)) * (V4_f1 + V4_f2 + 1j*V4_f3)

    # Return the total voltage induced in the antenna
    return V1 + V2 + V3 + V4


# Arguments - satellite antenna and magnetorquer dimensions that go into the voltage function
args = [
    -1,         # v_x   x-coil voltage          [Volts]
    1,          # v_y   y-coil voltage          [Volts]
    2,          # R     coil resistance         [Ohms]
    0.2,        # L     coil self-inductance    [Henries]
    0.000008,   # M     coil mutual inductance  [Henries]
    10000000,   # n     coil turn density       [meters^-3]
    0.0049,     # a     coil inner radius       [meters]
    0.005,      # b     coil outer radius       [meters]
    0.7,        # l     coil length             [meters]
    0.1,        # w     board width             [meters]
    0.05,       # h     board-antenna height    [meters]
    0.04,       # m     antenna mast            [meters]
    0.0001,     # W     antenna width           [meters]
    0.0035,     # H     antenna height          [meters]
    0.25,       # D     antenna length          [meters]
]

# computational loop - calculate voltage induced for each frequency
results = []
for f in freq:
    results.append(V(f, *args))


# Plot results
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import numpy as np

# Extract real and imaginary parts
real_part = np.real(results)
imag_part = np.imag(results)

# Generate smooth interpolation
freq_smooth = np.linspace(min(freq), max(freq), 500)  # New, denser x-axis

# Spline interpolation for real and imaginary parts
spline_real = make_interp_spline(freq, real_part)(freq_smooth)
spline_imag = make_interp_spline(freq, imag_part)(freq_smooth)

# Plot the smooth lines
plt.plot(freq_smooth, spline_real, color='blue', label='Real Part')
plt.plot(freq_smooth, spline_imag, color='red', label='Imaginary Part')

plt.xlabel('Frequency [Hz]')
plt.ylabel('Complex voltage [V]')
plt.title('Real and Imaginary Parts of Results')
plt.legend()
plt.show()