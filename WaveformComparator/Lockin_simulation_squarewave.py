import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Simulation parameters
fs = 500  # Sampling frequency (Hz)
T = 100       # Duration (s)
t = np.linspace(0, T, int(fs * T), endpoint=False)  # Time array

# Signal parameters
signal_freq = 100  # Hz
reference_freq = 100  # Should match signal frequency
signal_amplitude = 1.0
noise_amplitude = 1.0

# Generate the signal (sine wave)
pure_signal = signal_amplitude * square(2 * np.pi * signal_freq * t)
noise = noise_amplitude * np.random.normal(size=t.shape)
input_signal = pure_signal + noise

# Square wave reference (in-phase only)
square_ref = square(2 * np.pi * reference_freq * t)

# Mix signal with square wave reference
mixed_signal = input_signal * square_ref

# Simple low-pass filter (moving average)
def low_pass(signal, window_size):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

window_size = 100
filtered_output = low_pass(mixed_signal, window_size)

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(t, input_signal, label='Input Signal (with noise)', alpha=0.6)
plt.plot(t, pure_signal, '.', label='Pure Signal')
plt.title('Noisy Input Signal')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(t, square_ref, color='orange')
plt.title('Square Wave Reference')

plt.subplot(4, 1, 3)
plt.plot(t, mixed_signal, color='purple')
plt.title('Mixed Signal (Input × Reference)')

plt.subplot(4, 1, 4)
plt.plot(t, filtered_output, color='red')
plt.title('Low-pass Filtered Output (Extracted Signal)')
plt.xlabel('Time [s]')

plt.tight_layout()
plt.show()

#%%
pure_signal = signal_amplitude * square(2 * np.pi * signal_freq * t)
diff_new = np.zeros(len(t))
for i in range(window_size//2,len(t)-window_size//2):
    print(i)
    even_list = range(i-window_size//2,i+window_size//2,2)
    odd_list = range(i-window_size//2+1,i+window_size//2+1,2)
    # print(sum(input_signal[odd_list]),)
    diff_new[i] = (sum(input_signal[odd_list])-sum(input_signal[even_list]))/window_size
    
plt.figure()
plt.plot(t,diff_new)
