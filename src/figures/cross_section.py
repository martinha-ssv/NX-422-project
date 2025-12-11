import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.text import Text

from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap

eps0 = 8.854e-12


# ----------------------------------------------------------------------------
# Physics
# ----------------------------------------------------------------------------
def sigma_star(omega, sigma_dc, eps_r):
    return sigma_dc + 1j * omega * eps0 * eps_r


def V_point(I, r, omega, sigma_dc, eps_r):
    sig = sigma_star(omega, sigma_dc, eps_r)
    return I / (4 * np.pi * sig * np.maximum(r, 1e-6))


# ----------------------------------------------------------------------------
# Electrode Pair Object
# ----------------------------------------------------------------------------
class ElectrodePair:
    def __init__(self, angle_deg, color_e1, color_e2,
                 weight=1.0, steer=0.0, f1=20e3, f2=22e3, Rn=3e-3, label_e1="E1", label_e2="E2"):

        self.angle = np.deg2rad(angle_deg)
        self.color_e1 = color_e1
        self.color_e2 = color_e2
        self.label_e1 = label_e1
        self.label_e2 = label_e2
        self.weight = weight
        self.steer = steer

        self.w1 = 2 * np.pi * f1
        self.w2 = 2 * np.pi * f2
        self.Rn = Rn

    def currents(self, total_I):
        I_total = total_I * self.weight
        α = (self.steer + 1) / 2
        return α * I_total, (1 - α) * I_total

    def positions(self):
        θ = self.angle
        e1 = np.array([self.Rn * np.cos(θ),         self.Rn * np.sin(θ)])
        e2 = np.array([self.Rn * np.cos(θ + np.pi), self.Rn * np.sin(θ + np.pi)])
        return e1, e2


# ----------------------------------------------------------------------------
# Fast field calculation (vectorized)
# ----------------------------------------------------------------------------
def compute_field(pairs, X, Y, mask, total_I, sigma_dc, eps_r):
    AMs = []

    for p in pairs:
        e1, e2 = p.positions()
        I1, I2 = p.currents(total_I)

        R1 = np.sqrt((X - e1[0])**2 + (Y - e1[1])**2)
        R2 = np.sqrt((X - e2[0])**2 + (Y - e2[1])**2)

        V1 = V_point(I1, R1, p.w1, sigma_dc, eps_r)
        V2 = V_point(I2, R2, p.w2, sigma_dc, eps_r)

        A1, A2 = np.abs(V1), np.abs(V2)
        AMs.append(2 * np.minimum(A1, A2))

    AM = np.sum(AMs, axis=0)
    AM[mask] = np.nan
    return AM / np.nanmax(AM)


# ============================================================================
# FIELD VISUALIZER (the main class)
# ============================================================================
class FieldVisualizer:
    def __init__(self, pairs, Rn=3e-3, N=450,
                 total_I=2e-3, sigma_dc=0.3, eps_r=5000,
                 show_sliders=True, cmap="plasma"):

        self.pairs = pairs
        self.Rn = Rn
        self.total_I = total_I
        self.sigma_dc = sigma_dc
        self.eps_r = eps_r
        self.show_sliders = show_sliders
        self.cmap = cmap

        # ---------------- GRID ----------------
        x = np.linspace(-Rn, Rn, N)
        y = np.linspace(-Rn, Rn, N)
        self.X, self.Y = np.meshgrid(x, y)
        self.mask = (self.X**2 + self.Y**2) > Rn**2

        self.Xmm = self.X * 1e3
        self.Ymm = self.Y * 1e3

        # ---------------- INITIAL FIELD ----------------
        self.AM = compute_field(
            pairs, self.X, self.Y, self.mask,
            total_I, sigma_dc, eps_r
        )

        # ============================================================================
        #   FIGURE LAYOUT: Two panels if sliders, one panel if clean mode
        # ============================================================================
        if show_sliders:
            self.fig, (self.ax_ctrl, self.ax) = plt.subplots(
                1, 2, figsize=(12, 6),
                gridspec_kw={"width_ratios": [1, 2]},
                facecolor="black"
            )
            self.ax_ctrl.set_facecolor("black")
            self.ax_ctrl.axis("off")

        else:
            self.fig, self.ax = plt.subplots(
                figsize=(7, 7), facecolor="black"
            )

        self.ax.set_facecolor("black")
        self.ax.axis("off")
        self.ax.set_aspect("equal")

        # Draw core image + static shapes
        self.draw_field(initial=True)
        self.draw_nerve()
        self.draw_electrodes()

        if show_sliders:
            self.add_sliders()

        plt.show()

    # ============================================================================
    # DRAWING
    # ============================================================================
    def draw_field(self, initial=False):
        cmap = plt.get_cmap(self.cmap)
        rgba = cmap(self.AM)
        rgba[self.mask, 3] = 0

        if initial:
            self.im = self.ax.imshow(
                rgba,
                extent=[self.Xmm.min(), self.Xmm.max(),
                        self.Ymm.min(), self.Ymm.max()],
                origin="lower",
                interpolation="bilinear"
            )
        else:
            self.im.set_data(rgba)

        # prevent cropping
        pad = 1.5
        r = self.Rn * 1e3
        self.ax.set_xlim(-pad*r, pad*r)
        self.ax.set_ylim(-pad*r, pad*r)
        self.ax.set_aspect("equal", "box")

    def draw_nerve(self):
        Rnmm = self.Rn * 1e3
        circ = Circle(
            (0, 0), Rnmm, fill=False,
            zorder=20
        )
        self.ax.add_patch(circ)

    def draw_electrodes(self):
        Rnmm = self.Rn * 1e3
        arc_len = 20
        lw = 18
        dR = 0.5e-3
        dRmm = dR * 1e3

        for p in self.pairs:
            θ = np.rad2deg(p.angle)

            e1 = Arc((0,0), 2*(Rnmm + dRmm), 2*(Rnmm + dRmm),
                     theta1=θ - arc_len/2, theta2=θ + arc_len/2,
                     color=p.color_e1, lw=lw, capstyle="round",
                     zorder=30)
            e2 = Arc((0,0), 2*(Rnmm + dRmm), 2*(Rnmm + dRmm),
                     theta1=θ + 180 - arc_len/2,
                     theta2=θ + 180 + arc_len/2,
                     color=p.color_e2, lw=lw, capstyle="round",
                     zorder=30)

            e1_label = Text((Rnmm + 2*dRmm) * np.cos(np.deg2rad(θ)), (Rnmm + 2*dRmm) * np.sin(np.deg2rad(θ)), p.label_e1, color=p.color_e1, ha='center', va='center')
            e2_label = Text((Rnmm + 2*dRmm) * np.cos(np.deg2rad(θ + 180)), (Rnmm + 2*dRmm) * np.sin(np.deg2rad(θ + 180)), p.label_e2, color=p.color_e2, ha='center', va='center')

            self.ax.add_patch(e1)
            self.ax.add_patch(e2)

            self.ax.add_artist(e1_label)
            self.ax.add_artist(e2_label)

    # ============================================================================
    # SLIDER PANEL
    # ============================================================================
    def add_sliders(self):

        self.sliders = []

        N = len(self.pairs)
        total_rows = 3 * N
        row_height = 1 / (total_rows + 1)

        slider_specs = [
            ("Angle",  lambda p: np.rad2deg(p.angle), 0,   360),
            ("Weight", lambda p: p.weight,            0.1, 3.0),
            ("Steer",  lambda p: p.steer,            -1.0, 1.0),
        ]

        row_index = 0
        for label, getter, vmin, vmax in slider_specs:
            for i, p in enumerate(self.pairs):

                ypos = 1 - (row_index + 1) * row_height

                ax_s = inset_axes(
                    self.ax_ctrl,
                    width="90%", height=f"{row_height*90}%",
                    loc="upper center",
                    bbox_to_anchor=(0.05, ypos, 0.90, row_height),
                    bbox_transform=self.ax_ctrl.transAxes,
                    borderpad=0
                )

                s = Slider(
                    ax=ax_s,
                    label=f"P{i+1} {label}",
                    valmin=vmin, valmax=vmax,
                    valinit=getter(p),
                    color="white",
                )
                s.label.set_color("white")
                s.valtext.set_color("white")

                self.sliders.append((label, i, s))
                row_index += 1

        # assign callback
        for _, _, s in self.sliders:
            s.on_changed(self.update)

    # ============================================================================
    # UPDATE LOGIC (FAST: only field recalculation)
    # ============================================================================
    def update(self, _):
        # update model values
        for label, idx, slider in self.sliders:
            p = self.pairs[idx]
            v = slider.val

            if label == "Angle":
                p.angle = np.deg2rad(v)
            elif label == "Weight":
                p.weight = v
            elif label == "Steer":
                p.steer = v

        # fast recompute
        self.AM = compute_field(
            self.pairs, self.X, self.Y, self.mask,
            self.total_I, self.sigma_dc, self.eps_r
        )

        # update imshow
        self.draw_field(initial=False)
        self.fig.canvas.draw_idle()


# ============================================================================
# Example run
# ============================================================================
pairs = [
    ElectrodePair(0,   "#ff5bc8", "#5bb0ff", steer=0.0, label_e1="E1", label_e2="E2"),
    ElectrodePair(60, "#3f3f3f", "#3f3f3f", steer=-0.0, label_e1="E3", label_e2="E4"),
    ElectrodePair(120, "#3f3f3f", "#3f3f3f", steer=0.0, label_e1="E5", label_e2="E6")
]

viz = FieldVisualizer(pairs, show_sliders=True, cmap='plasma')