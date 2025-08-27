import numpy as np
import random

# === Variant Functions ===
def collapse_tensor_multifreq(tensor, energy_inputs, scale, iterations, sigma):
    from scipy.ndimage import gaussian_filter
    for _ in range(iterations):
        for freq in energy_inputs:
            tensor -= np.abs(np.sin(tensor / freq)) * scale
        tensor = gaussian_filter(tensor, sigma=sigma)
        tensor = np.clip(tensor, 0, None)
        if np.max(tensor) < 1e-9:
            break
    return tensor

def apply_variant(tensor, variant, params):
    if variant == "vE":
        return collapse_tensor_multifreq(tensor, [0.0001, 0.0005, 0.001], 1.0, 200, 1.0)
    elif variant == "vG":
        mask = tensor > params["immune_boost"]
        tensor[mask] *= (1 - 0.3)
        return collapse_tensor_multifreq(tensor, [0.0001, 0.0005, 0.001], 1.0, 200, 1.0)
    elif variant == "vH":
        resistance_mask = np.random.choice([1.0, 1.5], size=tensor.shape, p=[1 - params["resistance_rate"], params["resistance_rate"]])
        tensor *= resistance_mask
        return collapse_tensor_multifreq(tensor, [0.0001, 0.0005, 0.001], 1.0, 200, 1.0)
    elif variant == "vI":
        suppression_mask = np.random.choice([0, 1], size=tensor.shape, p=[0.5, 0.5])
        tensor *= (1 - suppression_mask * 0.5)
        return collapse_tensor_multifreq(tensor, [0.0001, 0.0005, 0.001], 1.0, 200, 1.0)
    elif variant == "vJ":
        cart_mask = tensor > 0.6
        tensor[cart_mask] *= (1 - 0.4)
        return collapse_tensor_multifreq(tensor, [0.0001, 0.0005, 0.001], 1.0, 200, 1.0)
    else:
        return tensor

# === Cohort Generator ===
def generate_patient_cohort(n=100):
    cohort = []
    for _ in range(n):
        patient = {
            "volume": np.random.uniform(2.5, 4.0),
            "density": np.random.uniform(1e9, 1.5e9),
            "energy": np.random.uniform(0.002, 0.004),
            "resistance_rate": np.random.uniform(0.05, 0.2),
            "immune_boost": np.random.uniform(0.2, 0.5),
            "variant": random.choice(["vE", "vG", "vH", "vI", "vJ"])
        }
        cohort.append(patient)
    return cohort

# === Trial Execution ===
def run_trial(patient):
    tensor = np.zeros((4, 4, 4))
    resonance = patient["volume"] * patient["density"] * patient["energy"]
    tensor += resonance / (patient["volume"] + 1e-9)
    tensor /= np.max(tensor)
    tensor = apply_variant(tensor, patient["variant"], patient)
    collapsed = np.max(tensor) < 1e-9
    return {
        "variant": patient["variant"],
        "collapsed": collapsed,
        "final_max": np.max(tensor)
    }

# === Run Full Simulation ===
cohort = generate_patient_cohort(100)
results = [run_trial(p) for p in cohort]

# === Summary Output ===
success_count = sum(1 for r in results if r["collapsed"])
print(f"Collapse Success Rate: {success_count}/100")

variant_stats = {}
for r in results:
    v = r["variant"]
    if v not in variant_stats:
        variant_stats[v] = {"total": 0, "success": 0}
    variant_stats[v]["total"] += 1
    if r["collapsed"]:
        variant_stats[v]["success"] += 1

for v, stats in variant_stats.items():
    rate = stats["success"] / stats["total"] * 100
    print(f"Variant {v}: {rate:.1f}% success ({stats['success']}/{stats['total']})")
