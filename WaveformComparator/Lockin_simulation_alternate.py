import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Simulation parameters
fs = 600  # Sampling frequency (Hz)
T = 10       # Duration (s)
t = np.linspace(0, T, int(fs * T), endpoint=False)  # Time array

# Signal parameters
signal_freq = 300  # Hz
# reference_freq = 100  # Should match signal frequency
signal_amplitude = 1.0
noise_amplitude = 1
Drift_amplitude = 2
# Generate the signal (sine wave)
pure_signal = signal_amplitude * np.arange(len(t)) % 2 ## Alternating signal
noise = noise_amplitude * np.random.normal(size=t.shape)+ Drift_amplitude * np.linspace(0,1,len(t))
input_signal = pure_signal + noise

# Square wave reference (in-phase only)
# square_ref = square(2 * np.pi * reference_freq * t)

# Mix signal with square wave reference
# mixed_signal = input_signal * square_ref

# Simple low-pass filter (moving average)
# def low_pass(signal, window_size):
#     return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

window_size = 300
filtered_output = np.zeros(len(t))
index = (-1.0) ** (np.arange(len(t))+1)
# for i in range(window_size//2,len(t)-window_size//2):
for i in range(window_size//2,len(t)-window_size//2):    
    filtered_output[i] = sum((input_signal*index)[i-window_size//2:i+window_size//2])/window_size


# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, input_signal, label='Input Signal (with noise)', alpha=0.6)
plt.plot(t, pure_signal, '.', label='Pure Signal')
plt.title('Noisy Input Signal')
plt.legend()

# plt.subplot(3, 1, 2)
# plt.plot(t, square_ref, color='orange')
# plt.title('Square Wave Reference')

plt.subplot(3, 1, 2)
plt.plot(t, input_signal, color='purple')
plt.title('Input Signal (Input × Reference)')

plt.subplot(3, 1, 3)
plt.plot(t, filtered_output, color='red')
plt.title('Low-pass Filtered Output (Extracted Signal)')
plt.xlabel('Time [s]')

plt.tight_layout()
plt.show()

#%%

