import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
fs = 500  # Sampling rate in Hz
T = 100       # Duration in seconds
t = np.linspace(0, T, int(fs * T), endpoint=False)  # Time array

# Signal parameters
signal_freq = 100  # Hz - frequency of the signal to extract
reference_freq = signal_freq  # Hz - reference signal (must match signal frequency)
signal_amplitude = 1.0
noise_amplitude = 1
Drift_amplitude = 0
# Generate the input signal (signal + noise)
pure_signal = signal_amplitude * np.sin(2 * np.pi * signal_freq * t)
noise = noise_amplitude * np.random.normal(size=t.shape) + Drift_amplitude * np.linspace(0,1,len(t))
input_signal = pure_signal + noise

# Reference signals (in-phase and quadrature)
ref_sin = np.sin(2 * np.pi * reference_freq * t)  # In-phase reference
ref_cos = np.cos(2 * np.pi * reference_freq * t)  # Quadrature reference

# Mix (multiply input signal with references)
mixed_sin = input_signal * ref_sin
mixed_cos = input_signal * ref_cos

# Low-pass filter (simple moving average)
def low_pass(signal, window_size):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

window_size = 100  # Adjust to simulate filtering strength
X = low_pass(mixed_sin, window_size)
Y = low_pass(mixed_cos, window_size)

# Calculate amplitude and phase
amplitude = np.sqrt(X**2 + Y**2)*2
phase = np.arctan2(Y, X)

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, input_signal, label='Input Signal (with noise)', alpha=0.6)
plt.plot(t, pure_signal, label='Pure Signal', linestyle='--')
plt.legend()
plt.title('Input Signal')

plt.subplot(3, 1, 2)
plt.plot(t, X, label='In-phase (X)')
plt.plot(t, Y, label='Quadrature (Y)')
plt.legend()
plt.title('Mixed and Filtered Components')

plt.subplot(3, 1, 3)
plt.plot(t, amplitude, label='Amplitude (Envelope)', color='r')
plt.title('Extracted Signal Amplitude')
plt.xlabel('Time [s]')
plt.tight_layout()
plt.show()
