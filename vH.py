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

# === Step 4: Apply Resistance Mask ===
def apply_stochastic_resistance(tensor, resistance_rate=0.1, resistance_factor=1.5):
    mask = np.random.choice([1.0, resistance_factor], size=tensor.shape, p=[1 - resistance_rate, resistance_rate])
    return tensor * mask

# === Step 5: Collapse Logic ===
def collapse_tensor_multifreq(tensor, energy_inputs=[0.0001, 0.0005, 0.001], scale=1.0, iterations=200, sigma=1.0):
    for _ in range(iterations):
        for freq in energy_inputs:
            tensor -= np.abs(np.sin(tensor / freq)) * scale
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
tensor = apply_stochastic_resistance(tensor, resistance_rate=0.1, resistance_factor=1.5)
tensor = collapse_tensor_multifreq(tensor)

# === Output ===
print("Stochastic resistance applied.")
print("Collapse Achieved:", np.max(tensor) < 1e-9)
print("Final Max Value:", np.max(tensor))
