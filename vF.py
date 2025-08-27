import numpy as np
from scipy.ndimage import gaussian_filter

# === Step 1: Seed Tensor ===
def seed_tumor_tensor(volume_cm3, cell_density, energy_joules):
    tensor = np.zeros((4, 4, 4))
    resonance_value = volume_cm3 * cell_density * energy_joules
    tensor += resonance_value / (volume_cm3 + 1e-9)
    return tensor

# === Step 2: Add Noise ===
def add_noise(tensor, std_dev=0.01):
    noise = np.random.normal(loc=0.0, scale=std_dev, size=tensor.shape)
    return tensor + noise

# === Step 3: Normalize ===
def normalize_tensor(tensor):
    max_val = np.max(tensor)
    return tensor / (max_val + 1e-9)

# === Step 4: Adaptive Frequency Collapse ===
def collapse_tensor_adaptive(tensor, base_freq=0.0001, scale=1.0, iterations=200, sigma=1.0):
    for _ in range(iterations):
        adaptive_freq = base_freq + (np.max(tensor) * 0.001)
        tensor -= np.abs(np.sin(tensor / adaptive_freq)) * scale
        tensor = gaussian_filter(tensor, sigma=sigma)
        tensor = np.clip(tensor, 0, None)
        if np.max(tensor) < 1e-9:
            break
    return tensor

# === Execution ===
volume = 3.2
density = 1.2e9
energy = 0.003

tensor = seed_tumor_tensor(volume, density, energy)
tensor = add_noise(tensor, std_dev=0.01)
tensor = normalize_tensor(tensor)
tensor = collapse_tensor_adaptive(tensor)

# === Output ===
print("Adaptive frequency sweep applied.")
print("Collapse Achieved:", np.max(tensor) < 1e-9)
print("Final Max Value:", np.max(tensor))
