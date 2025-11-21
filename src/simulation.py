# Disclaimer: Vibe Coded
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Circle, Ellipse

# === Physical constants ===
A = 1e-6
a = np.sqrt(A / np.pi)
sigma_dc = 0.3
eps_r = 5000
eps0 = 8.854e-12


def sigma_star(omega, sigma=sigma_dc, eps_r=eps_r):
    return sigma + 1j * omega * eps0 * eps_r


def V_point(I, r, omega, sigma_dc=sigma_dc, eps_r=eps_r):
    sig = sigma_star(omega, sigma_dc, eps_r)
    return I / (4 * np.pi * sig * np.maximum(r, 1e-6))


# === Scene setup ===
Rn = 1.5e-3
N = 400
x = np.linspace(-Rn, Rn, N)
y = np.linspace(-Rn, Rn, N)
X, Y = np.meshgrid(x, y)
mask = (X**2 + Y**2) > Rn**2

total_I_global = 2e-3  # total current (A)
f1, f2 = 20e3, 22e3
w1, w2 = 2 * np.pi * f1, 2 * np.pi * f2

# === Define 3 electrode pairs (angle = position around cuff) ===
pairs = [
    {"angle": 0, "weight": 1.0, "steer": 0.0},
    {"angle": 120, "weight": 1.0, "steer": 0.0},
    {"angle": 240, "weight": 1.0, "steer": 0.0},
]


def normalize_weights(pairs):
    wsum = sum(p["weight"] for p in pairs)
    for p in pairs:
        p["weight"] /= wsum


normalize_weights(pairs)


# === Compute AM envelope ===
def compute_am(pairs):
    AM_list = []
    for p in pairs:
        th = np.deg2rad(p["angle"])
        total_I = total_I_global * p["weight"]
        steer = (p["steer"] + 1) / 2
        I1 = steer * total_I
        I2 = (1 - steer) * total_I

        # Electrode pair opposite around circumference
        e1 = np.array([Rn * np.cos(th), Rn * np.sin(th)])
        e2 = np.array([Rn * np.cos(th + np.pi), Rn * np.sin(th + np.pi)])

        R1 = np.sqrt((X - e1[0]) ** 2 + (Y - e1[1]) ** 2)
        R2 = np.sqrt((X - e2[0]) ** 2 + (Y - e2[1]) ** 2)

        V1 = V_point(I1, R1, w1)
        V2 = V_point(I2, R2, w2)
        A1, A2 = np.abs(V1), np.abs(V2)
        AM_pp = 2 * np.minimum(A1, A2)
        AM_list.append(AM_pp)

    AM_total = np.sum(AM_list, axis=0)
    AM_total[mask] = np.nan
    return AM_total / np.nanmax(AM_total)


# === Initial plot ===
AM = compute_am(pairs)
fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.42)
im = ax.imshow(
    AM, extent=[-Rn * 1e3, Rn * 1e3, -Rn * 1e3, Rn * 1e3], origin="lower", cmap="plasma"
)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title(f"Interferential Field (ΣI = {total_I_global*1e3:.1f} mA)")
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Normalized AM")

# Nerve outline and fake fascicles
ax.add_patch(Circle((0, 0), Rn * 1e3, fill=False, color="white", lw=1.5))
rng = np.random.default_rng(0)
for _ in range(15):
    cx, cy = rng.uniform(-0.6, 0.6, 2) * Rn * 1e3
    w, h = rng.uniform(0.15, 0.35, 2) * Rn * 1e3
    ax.add_patch(
        Ellipse(
            (cx, cy),
            w,
            h,
            angle=rng.uniform(0, 180),
            edgecolor="white",
            facecolor="none",
            lw=0.8,
        )
    )

# === Slider setup: 9 total (3 angle, 3 weight, 3 steer) ===
sliders = []

y_start = 0.30
y_step = 0.08
for i, label in enumerate(["angle", "weight", "steer"]):
    for j, p in enumerate(pairs):
        ypos = y_start - (i * 0.09 + j * 0.025)
        ax_slider = plt.axes([0.15, ypos, 0.65, 0.02])
        if label == "angle":
            s = Slider(ax_slider, f"Pair {j+1} angle (°)", 0, 360, valinit=p["angle"])
        elif label == "weight":
            s = Slider(ax_slider, f"Pair {j+1} weight", 0.1, 2.0, valinit=p["weight"])
        else:
            s = Slider(ax_slider, f"Pair {j+1} steer", -1.0, 1.0, valinit=p["steer"])
        sliders.append(s)


# === Update function ===
def update(val):
    # update parameters from sliders
    for i, p in enumerate(pairs):
        p["angle"] = sliders[i].val  # angles 0–2
        p["weight"] = sliders[3 + i].val  # weights 3–5
        p["steer"] = sliders[6 + i].val  # steers 6–8
    normalize_weights(pairs)
    AM_new = compute_am(pairs)
    im.set_data(AM_new)
    fig.canvas.draw_idle()


for s in sliders:
    s.on_changed(update)

plt.show()
