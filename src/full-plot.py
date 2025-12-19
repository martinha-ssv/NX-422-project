import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Circle

# Optional style
try:
    plt.style.use("custom_dark_bg.mplstyle")
except OSError:
    pass

# === Physical constants ===
sigma_dc = 0.3
eps_r = 5000
eps0 = 8.854e-12

def sigma_star(omega, sigma=sigma_dc, eps_r=eps_r):
    return sigma + 1j * omega * eps0 * eps_r

def V_point(I, r, omega):
    sig = sigma_star(omega)
    return I / (4 * np.pi * sig * np.maximum(r, 1e-6))


# === Frequencies & waveform time ===
f1, f2 = 20e3, 22e3
w1, w2 = 2*np.pi*f1, 2*np.pi*f2

t = np.linspace(0, 2e-3, 2000)
t_env = t
base_current_amp = 2e-3  # 0.002 A max per wave when fully "on"


# === Nerve geometry ===
Rn = 1.5e-3
N = 200
x = np.linspace(-Rn, Rn, N)
y = np.linspace(-Rn, Rn, N)
X, Y = np.meshgrid(x, y)

mask = (X**2 + Y**2) > Rn**2

# Electrode positions
e1 = np.array([Rn, 0.0])   # right
e2 = np.array([-Rn, 0.0])  # left

R1 = np.sqrt((X - e1[0])**2 + (Y - e1[1])**2)
R2 = np.sqrt((X - e2[0])**2 + (Y - e2[1])**2)

total_I_global = 2e-3

def compute_fields(I1, I2):
    """Return raw A1, A2, AM_raw with NO masking (for physics)."""
    V1 = V_point(I1, R1, w1)
    V2 = V_point(I2, R2, w2)

    A1 = np.abs(V1)
    A2 = np.abs(V2)

    A1 = np.where(mask, 0.0, A1)
    A2 = np.where(mask, 0.0, A2)

    AM_raw = 2 * np.minimum(A1, A2)
    AM_raw = np.where(mask, 0.0, AM_raw)

    return A1, A2, AM_raw


# === Normalization for AM map ===
_, _, AM_ref = compute_fields(total_I_global/2, total_I_global/2)
AM_global_max = np.max(AM_ref) + 1e-18


# === Figure setup ===
fig = plt.figure(figsize=(12, 6))
gs = fig.add_gridspec(2, 2, width_ratios=[2,1], height_ratios=[1,1],
                      wspace=0.25, hspace=0.3)

ax_waves = fig.add_subplot(gs[0, 0])
ax_sum   = fig.add_subplot(gs[1, 0])
ax_field_indiv = fig.add_subplot(gs[0, 1])
ax_field_am    = fig.add_subplot(gs[1, 1])

extent_mm = [-Rn*1e3, Rn*1e3, -Rn*1e3, Rn*1e3]


# === LEFT: waveforms ===
line_s1, = ax_waves.plot([], [], label="20 kHz")
line_s2, = ax_waves.plot([], [], label="22 kHz")
ax_waves.set_xlim(t[0], t[-1])
ax_waves.set_ylim(-2.5e-3, 2.5e-3)
ax_waves.legend(loc='upper left', bbox_to_anchor=(1,1))
ax_waves.grid(False)
ax_waves.axis('off')
ax_waves.set_title("Carrier Currents at Point")

line_sum, = ax_sum.plot([], [], label="Sum", alpha=0.5, color='C2')
line_env_up, = ax_sum.plot([], [], label="Envelope", color='white')
line_env_down, = ax_sum.plot([], [], color='white')
ax_sum.set_xlim(t[0], t[-1])
ax_sum.set_ylim(-4e-3, 4e-3)
ax_sum.legend(loc='upper left', bbox_to_anchor=(1,1))
ax_sum.grid(False)
ax_sum.axis('off')
ax_sum.set_title("AM Waveform")


# === RIGHT: initial electrode fields ===
A1_init, A2_init, AM_init = compute_fields(total_I_global/2, total_I_global/2)

A1_norm = A1_init / (np.max(A1_init)+1e-18)
A2_norm = A2_init / (np.max(A2_init)+1e-18)

A1_alpha = np.where(mask, 0.0, A1_norm)
A2_alpha = np.where(mask, 0.0, A2_norm)

rgba1 = np.zeros((N, N, 4))
rgba2 = np.zeros((N, N, 4))
rgba1[...,0] = 1.0   # red tint
rgba2[...,2] = 1.0   # blue tint
rgba1[...,3] = A1_alpha
rgba2[...,3] = A2_alpha

im_e1 = ax_field_indiv.imshow(rgba1, extent=extent_mm, origin="lower")
im_e2 = ax_field_indiv.imshow(rgba2, extent=extent_mm, origin="lower")
ax_field_indiv.add_patch(Circle((0,0), Rn*1e3, fill=False, color="white"))
ax_field_indiv.axis("off")
ax_field_indiv.set_title("Individual Electrode Fields")


# === RIGHT: AM field ===
AM_norm_init = AM_init / (AM_global_max + 1e-18)
AM_norm_init_plot = np.where(mask, np.nan, AM_norm_init)

im_AM = ax_field_am.imshow(
    AM_norm_init_plot, extent=extent_mm, origin="lower", cmap="plasma"
)
ax_field_am.add_patch(Circle((0,0), Rn*1e3, fill=False, color="white"))
ax_field_am.axis("off")
ax_field_am.set_title("AM Envelope")

cbar = fig.colorbar(im_AM, ax=ax_field_am)
cbar.set_label("Normalized AM")


# Moving point
point_indiv, = ax_field_indiv.plot([], [], "wo", ms=5)
point_am,    = ax_field_am.plot([], [], "wo", ms=5)


def xy_to_index(xp, yp):
    ix = np.argmin(np.abs(x - xp))
    iy = np.argmin(np.abs(y - yp))
    return ix, iy


# === Animation ===
n_frames = 240

def init():
    line_s1.set_data([], [])
    line_s2.set_data([], [])
    line_sum.set_data([], [])
    line_env_up.set_data([], [])
    line_env_down.set_data([], [])
    return (
        line_s1, line_s2, line_sum, line_env_up, line_env_down,
        im_e1, im_e2, im_AM,
        point_indiv, point_am
    )

def update(frame):
    # --- 1. Move along diameter: +Rn → -Rn → +Rn ---
    phase = frame / n_frames
    px = Rn * np.cos(2*np.pi*phase)
    py = 0.0

    point_indiv.set_data([px*1e3], [py*1e3])
    point_am.set_data([px*1e3], [py*1e3])

    # --- 2. Fixed steering for fields ---
    I1 = total_I_global * 0.5
    I2 = total_I_global * 0.5

    A1, A2, AM_raw = compute_fields(I1, I2)

    # Electrode visibility boost (gamma)
    gamma = 0.25
    A1_vis = (A1 / (np.max(A1)+1e-18)) ** gamma
    A2_vis = (A2 / (np.max(A2)+1e-18)) ** gamma

    rgba1[...,3] = np.where(mask, 0.0, A1_vis)
    rgba2[...,3] = np.where(mask, 0.0, A2_vis)
    im_e1.set_data(rgba1)
    im_e2.set_data(rgba2)

    # AM field visualization
    AM_norm = AM_raw / (AM_global_max + 1e-18)
    im_AM.set_data(np.where(mask, np.nan, AM_norm))

    # --- 3. Distance-based amplitudes (what you asked for) ---
    # Distances from point to each electrode
    d1 = np.linalg.norm([px - e1[0], py - e1[1]])
    d2 = np.linalg.norm([px - e2[0], py - e2[1]])

    # Normalize distances to [0, 1] over the diameter (max is 2*Rn)
    max_d = 2 * Rn
    d1_norm = np.clip(d1 / max_d, 0.0, 1.0)
    d2_norm = np.clip(d2 / max_d, 0.0, 1.0)

    # Amplitudes: 0.002 * (1 - distance_norm)
    amp1 = base_current_amp * (1.0 - d1_norm)  # electrode 1 side
    amp2 = base_current_amp * (1.0 - d2_norm)  # electrode 2 side

    # --- 4. Waveforms & envelope ---
    s1 = amp1 * np.sin(w1*t)
    s2 = amp2 * np.sin(w2*t)
    s_sum = s1 + s2

    env = np.sqrt(
        amp1**2 + amp2**2 +
        2*amp1*amp2*np.cos(2*np.pi*(f2-f1)*t_env)
    )

    line_s1.set_data(t, s1)
    line_s2.set_data(t, s2)
    line_sum.set_data(t, s_sum)
    line_env_up.set_data(t, env)
    line_env_down.set_data(t, -env)

    return (
        line_s1, line_s2, line_sum, line_env_up, line_env_down,
        im_e1, im_e2, im_AM,
        point_indiv, point_am
    )

anim = FuncAnimation(
    fig, update, frames=n_frames,
    init_func=init, blit=True, interval=50
)

writer = FFMpegWriter(fps=20)
anim.save("ti_amplitude_modulation_nerve.gif", writer=writer, dpi=150)

plt.show()
