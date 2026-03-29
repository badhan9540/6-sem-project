import numpy as np
import tensorflow as tf
import pathlib

base = pathlib.Path(r"C:\Users\pkarn\OneDrive\Desktop\project workload pattern")
thr = float(np.load(str(base / "threshold.npy")))
print(f"Threshold: {thr:.8f}")

all_weights = np.load(str(base / "model_weights_np.npy"), allow_pickle=True)
print(f"Weight arrays: {len(all_weights)}")
for i, w in enumerate(all_weights):
    print(f"  [{i}] shapes: {[x.shape for x in w]}")

# Rebuild architecture
inp = tf.keras.Input(shape=(9,))
x = tf.keras.layers.Dense(64, activation="relu")(inp)
x = tf.keras.layers.Dense(32, activation="relu")(x)
x = tf.keras.layers.Dense(16, activation="relu")(x)
x = tf.keras.layers.Dense(8,  activation="relu")(x)
x = tf.keras.layers.Dense(16, activation="relu")(x)
x = tf.keras.layers.Dense(32, activation="relu")(x)
x = tf.keras.layers.Dense(64, activation="relu")(x)
out = tf.keras.layers.Dense(9, activation="sigmoid")(x)
model = tf.keras.Model(inp, out)

# Set weights — only layers that have weights
wi = 0
for layer in model.layers:
    w = layer.get_weights()
    if len(w) > 0 and wi < len(all_weights):
        while wi < len(all_weights) and len(all_weights[wi]) == 0:
            wi += 1  # skip empty arrays
        if wi < len(all_weights) and len(all_weights[wi]) > 0:
            try:
                layer.set_weights(all_weights[wi])
                print(f"Set layer {layer.name} weights [{wi}]")
                wi += 1
            except Exception as e:
                print(f"Skip layer {layer.name}: {e}")
                wi += 1

print(f"\n✅ Model loaded!")

# Test scenarios
scenarios = {
    "BEST  (8hr, light, very active)": [8.5/12, 7/10, 0.8,  0.533, 0.6,   5/16,  0,     0.6,  0.375],
    "GOOD  (7hr, normal, a little)":   [7/12,   6/10, 0.45, 0.533, 0.3,   8/16,  0.075, 0.35, 0.375],
    "MID   (6hr, normal, barely)":     [6/12,   5/10, 0.2,  0.533, 0.15,  8/16,  0.188, 0.15, 0.375],
    "BAD   (5hr, heavy, no breaks)":   [5/12,   3/10, 0.15, 0.667, 0.1,   11/16, 0.188, 0,    0.5  ],
    "WORST (4hr, overwhelm, nothing)": [3.5/12, 2/10, 0.05, 0.833, 0.025, 14/16, 0.5,   0,    0.625],
}

print(f"\n{'Scenario':<40} {'Score':>12}  Label")
print("-"*60)
for name, vals in scenarios.items():
    X = np.array([[min(v,1.0) for v in vals]])
    rec = model.predict(X, verbose=0)
    score = float(np.mean((X-rec)**2))
    if score < 0.000496:   label = "Balanced"
    elif score < 0.001388: label = "Moderate"
    else:                  label = "Overloaded"
    print(f"{name:<40} {score:>12.8f}  {label}")

input("\nPress Enter...")
