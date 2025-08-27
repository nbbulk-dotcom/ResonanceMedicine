import numpy as np
from scipy.ndimage import gaussian_filter

# === Step 1: Seed Tensor ===
def seed_tumor_tensor(volume_cm3, cell_density, energy_joules):
    tensor = np.zeros((4, 4, 4))
    resonance_value = volume_cm3 * cell_density * energy_joules
    tensor += resonance_value / (volume_cm3 + 1e-9)
    return tensor

# === Step 2: Add Noise and Normalize ===
def add_noise(tensor, std_dev=0.01):
    return tensor + np.random.normal(0, std_dev, tensor.shape)

def normalize_tensor(tensor):
    return tensor / (np.max(tensor) + 1e-9)

# === Step 3: Simulate Metastatic Spread ===
def simulate_metastatic_spread(tensor, spread_rate=0.1, seed_threshold=0.05):
    new_tensor = np.copy(tensor)
    for i in range(tensor.shape[0]):
        for j in range(tensor.shape[1]):
            for k in range(tensor.shape[2]):
                if tensor[i, j, k] > seed_threshold:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                ni, nj, nk = i + dx, j + dy, k + dz
                                if 0 <= ni < tensor.shape[0] and 0 <= nj < tensor.shape[1] and 0 <= nk < tensor.shape[2]:
                                    new_tensor[ni, nj, nk] += tensor[i, j, k] * spread_rate
    return new_tensor

# === Step 4: Collapse Logic ===
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
tensor = add_noise(tensor)
tensor = normalize_tensor(tensor)
tensor = simulate_metastatic_spread(tensor, spread_rate=0.1, seed_threshold=0.05)
tensor = collapse_tensor_multifreq(tensor)

# === Output ===
print("Metastatic spread simulated.")
print("Collapse Achieved:", np.max(tensor) < 1e-9)
print("Final Max Value:", np.max(tensor))
