import numpy as np

# === Step 1: Seed Tensor ===
def seed_tumor_tensor(volume_cm3, cell_density, energy_joules):
    tensor = np.zeros((4, 4, 4))
    resonance_value = volume_cm3 * cell_density * energy_joules
    tensor += resonance_value / (volume_cm3 + 1e-9)
    return tensor

# === Step 2: Add Symbolic Noise ===
def add_noise(tensor, std_dev=0.01):
    noise = np.random.normal(loc=0.0, scale=std_dev, size=tensor.shape)
    return tensor + noise

# === Step 3: Normalize Tensor ===
def normalize_tensor(tensor):
    max_val = np.max(tensor)
    return tensor / (max_val + 1e-9)

# === Step 4: Apply Spatial Gradient ===
def add_spatial_gradient(tensor):
    x, y, z = np.indices(tensor.shape)
    center = np.array(tensor.shape) / 2
    distance = np.sqrt((x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2)
    gradient = 1 - (distance / np.max(distance))
    return tensor * gradient

# === Execution ===
volume = 3.2
density = 1.2e9
energy = 0.003

tensor = seed_tumor_tensor(volume, density, energy)
tensor = add_noise(tensor, std_dev=0.01)
tensor = normalize_tensor(tensor)
tensor = add_spatial_gradient(tensor)

# === Output ===
print("Spatial gradient applied.")
print("Max value after gradient:", np.max(tensor))
