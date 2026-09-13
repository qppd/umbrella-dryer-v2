"""
Smart Umbrella Dryer - Rev 4 representative 3D model generator.

Produces 6 dimensioned PNG views (mm) into this folder:
  exploded-view.png, front-view.png, side-view.png, top-view.png,
  front-right-view.png, front-left-view.png

Usage:  python generate_models.py        (requires matplotlib + numpy)

NOTE: dimensions are REPRESENTATIVE (the capstone paper fixes none).
Edit the CONSTANTS below to match the real chamber, re-run, PNGs update.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ------------------------- CONSTANTS (mm) -------------------------
CH_W, CH_D, CH_H = 2200.0, 800.0, 1300.0   # chamber internal W(x) D(y) H(z) - REAL chamber box
WALL = 20.0
PLATE_T = 6.0                                # 6061 aluminum motor plate
PITCH = 700.0                                # station spacing along X (real: 3-station row)
MOTOR_L, MOTOR_W, MOTOR_H = 115.0, 40.0, 36.0
SHAFT_DIA, SHAFT_LEN = 8.0, 300.0
COUP_L = 25.0
KP08 = (42.0, 22.0, 34.0)                    # bracket approx
CANOPY_D, CANOPY_DEPTH = 650.0, 200.0        # umbrella HALF-OPEN projected (fully open is 950-1000)
TRAY = (500.0, 400.0, 60.0)
HEATER = (200.0, 100.0, 100.0)
FAN_D = 120.0
CLEARANCE = 50.0                             # min canopy tip clearance

Z0 = 0.0                                     # chamber floor
PLATE_Z = CH_H - PLATE_T                     # plate bottom
ST_X = [-PITCH, 0.0, PITCH]

# ------------------------- helpers -------------------------
def box(cx, cy, cz, sx, sy, sz):
    x0, x1 = cx - sx/2, cx + sx/2
    y0, y1 = cy - sy/2, cy + sy/2
    z0, z1 = cz - sz/2, cz + sz/2
    v = np.array([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],
                  [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]])
    f = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]
    return v, f

def cone(cx, cy, z_apex, z_rim, dia):
    n = 24
    th = np.linspace(0, 2*np.pi, n+1)
    r = dia/2
    verts, faces = [], []
    apex = [cx, cy, z_apex]
    for i in range(n):
        a0, a1 = th[i], th[i+1]
        p0 = [cx + r*np.cos(a0), cy + r*np.sin(a0), z_rim]
        p1 = [cx + r*np.cos(a1), cy + r*np.sin(a1), z_rim]
        base = len(verts)
        verts += [apex, p0, p1]
        faces.append([base, base+1, base+2])
    return np.array(verts), faces

def add(ax, verts, faces, color, alpha=1.0, ec='k', lw=0.4):
    pc = Poly3DCollection(verts[list(faces)] if isinstance(faces, list) else verts[faces],
                          facecolor=color, edgecolor=ec, linewidth=lw, alpha=alpha)
    ax.add_collection3d(pc)
    return pc

def draw_system(ax, explode=False):
    ez = 0.0
    def off(z):  # explode: push parts apart vertically by band
        return (0, 0, z * ez) if explode else (0, 0, 0)
    if explode:
        ez = 0.55

    # chamber walls (transparent shell)
    for (cx, cy, cz, sx, sy, sz) in [
        (0, -CH_D/2-WALL/2, CH_H/2, CH_W+2*WALL, WALL, CH_H+2*WALL),      # front wall
        (0,  CH_D/2+WALL/2, CH_H/2, CH_W+2*WALL, WALL, CH_H+2*WALL),      # back wall
        (-CH_W/2-WALL/2, 0, CH_H/2, WALL, CH_D, CH_H+2*WALL),             # left
        ( CH_W/2+WALL/2, 0, CH_H/2, WALL, CH_D, CH_H+2*WALL),             # right
        (0, 0, -WALL/2 + 30, CH_W, CH_D, WALL),                           # floor (sloped in reality)
    ]:
        dx, dy, dz = off(cz * 0.15)
        v, f = box(cx+dx, cy+dy, cz+dz, sx, sy, sz)
        add(ax, v, f, '#d9d9d9', alpha=0.12, ec='#999999', lw=0.6)

    # floor slope wedge hint + drain + tray
    dx, dy, dz = off(Z0 * 0.15)
    v, f = box(0, CH_D/2 - 60, 40+dz, 220, 60, 80)          # drain corner block hint
    add(ax, v, f, '#bbbbbb', alpha=0.35, ec='k')
    v, f = box(0, 0, -WALL - TRAY[2]/2 + (dz if explode else 0) - (120 if explode else 0),
               TRAY[0], TRAY[1], TRAY[2])
    add(ax, v, f, '#e8d44d', alpha=0.9)                      # drip tray

    # motor plate
    dx, dy, dz = off(CH_H)
    v, f = box(0, 0, CH_H + PLATE_T/2 + dz, CH_W + 2*WALL, CH_D + 2*WALL, PLATE_T)
    add(ax, v, f, '#7fbf7f', alpha=0.95)                     # 6061 plate

    # per-station hardware
    for i, sx_ in enumerate(ST_X):
        dzm = off(CH_H + 100)[2]
        v, f = box(sx_, 0, CH_H + PLATE_T + MOTOR_H/2 + dzm, MOTOR_L, MOTOR_W, MOTOR_H)
        add(ax, v, f, '#4f81bd')                             # worm motor
        # motor shaft + coupling
        v, f = box(sx_, 0, PLATE_Z - 8, SHAFT_DIA, SHAFT_DIA, 16)
        add(ax, v, f, '#888888')
        zc = PLATE_Z - 8 - COUP_L/2 + off(700)[2]
        v, f = box(sx_, 0, zc, 16, 16, COUP_L)
        add(ax, v, f, '#9467bd')                             # 8x8 coupling
        # main shaft 300
        zs_top = zc - COUP_L/2
        v, f = box(sx_, 0, zs_top - SHAFT_LEN/2, SHAFT_DIA, SHAFT_DIA, SHAFT_LEN)
        add(ax, v, f, '#666666')
        zs_bot = zs_top - SHAFT_LEN
        # KP08 x2
        for zb in (zs_top - 10, zs_bot + 10):
            v, f = box(sx_, -KP08[1]/2 - 8, zb + off(300)[2] if explode else zb,
                       KP08[0], KP08[1], KP08[2])
            add(ax, v, f, '#c49a6c', alpha=0.95)
        # holder crossbar
        v, f = box(sx_, 0, zs_bot - 6 + (off(150)[2] if explode else 0), 130, 20, 6)
        add(ax, v, f, '#333333')
        # canopy cone
        dzc = off(-150)[2] if explode else 0
        v, f = cone(sx_, 0, zs_bot - 12 + dzc, zs_bot - 12 - CANOPY_DEPTH + dzc, CANOPY_D)
        add(ax, v, f, '#e07b39', alpha=0.75)

    # heater (left wall, low) + fan (right wall, low)
    v, f = box(-CH_W/2 + HEATER[2]/2 + 5, 0, 150, HEATER[2], HEATER[0], HEATER[1])
    add(ax, v, f, '#c0392b', alpha=0.9)
    v, f = cone(CH_W/2 - 30, 0, 150 + FAN_D/2, 150 - FAN_D/2, FAN_D)
    add(ax, v, f, '#3fa7d6', alpha=0.9)

def dims_2d(ax, lines, color='#b00000'):
    """lines: list of (p1, p2, label, offset) in data coords."""
    for p1, p2, label, toff in lines:
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=color, lw=1.2)
        for a, b in ((p1, p2),):
            d = np.array(b) - np.array(a); d = d / (np.linalg.norm(d) + 1e-9)
            for end in (a, b):
                s = np.array(end) - d * 28
                ax.plot([end[0], s[0]], [end[1], s[1]], [end[2], s[2]], color=color, lw=1.2)
        ax.text((p1[0]+p2[0])/2 + toff[0], (p1[1]+p2[1])/2 + toff[1],
                (p1[2]+p2[2])/2 + toff[2], label, color=color, fontsize=9,
                ha='center', fontweight='bold')

def new_ax(title):
    fig = plt.figure(figsize=(12.5, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_proj_type('ortho')
    ax.set_box_aspect((CH_W + 300, CH_D + 300, CH_H + 420))
    ax.set_xlim(-(CH_W/2 + 150), CH_W/2 + 150)
    ax.set_ylim(-(CH_D/2 + 150), CH_D/2 + 150)
    ax.set_zlim(-260, CH_H + 260)
    ax.set_axis_off()
    ax.set_title(title + "\n(representative dimensions, mm - see model/README.md)", fontsize=12)
    return fig, ax

def save(fig, name):
    fig.savefig(name, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("wrote", name)

def view(name, elev, azim, title, explode=False, dimlines=(), notes=""):
    fig, ax = new_ax(title)
    draw_system(ax, explode=explode)
    ax.view_init(elev=elev, azim=azim)
    dims_2d(ax, dimlines)
    if notes:
        ax.text2D(0.01, 0.02, notes, transform=ax.transAxes, fontsize=8.5,
                  va='bottom', family='monospace',
                  bbox=dict(boxstyle='round', fc='#f7f7f7', ec='#999999'))
    save(fig, name)

# ------------------------- generate all views -------------------------
W2, H2 = CH_W/2, CH_H/2

# 1. exploded
fig, ax = new_ax("Exploded view - Smart Umbrella Dryer (Rev 4)")
draw_system(ax, explode=True)
ax.view_init(elev=16, azim=-58)
labels = [
    (0, 0, CH_H + PLATE_T + MOTOR_H + 55, "3x worm gear motor 115x40x36, 60 kg-cm, 16 RPM"),
    (0, 0, CH_H + PLATE_T/2 + 25, "motor plate 6061, 6 mm"),
    (ST_X[1], 0, PLATE_Z - 60, "8x8 coupling + 8 mm shaft x 300 + 2x KP08 per station"),
    (ST_X[1], 0, PLATE_Z - SHAFT_LEN - 60, "umbrella holder (fabricated)"),
    (ST_X[1], 0, PLATE_Z - SHAFT_LEN - CANOPY_DEPTH - 40, "umbrella half-open, projected dia 650 (fully open 950-1000)"),
    (-CH_W/2 + 130, 0, 150, "PTC heater 100 W 12 V (left wall, low)"),
    (CH_W/2 - 130, 0, 150, "120 mm circulation fan (right wall, low)"),
    (0, -CH_D/2 - 60, -160, "drip tray 500x400x60 (drain tube to corner)"),
]
for x, y, z, t in labels:
    ax.text(x, y, z, t, fontsize=8.5, ha='center',
            bbox=dict(boxstyle='round', fc='white', ec='#777777', alpha=0.85))
save(fig, "exploded-view.png")

# 2. front view (looking -Y)
view("front-view.png", 0, -90, "Front view",
    dimlines=[
        ((-W2, 0, -120), (W2, 0, -120), "2200 chamber W", (0, 0, -45)),
        ((-W2-70, 0, 0), (-W2-70, 0, CH_H), "1300 H", (0, 0, 0)),
        ((ST_X[0], 0, CH_H + PLATE_T + MOTOR_H + 95), (ST_X[1], 0, CH_H + PLATE_T + MOTOR_H + 95), "700 pitch", (0, 0, 35)),
        ((ST_X[1]-325, 0, 640), (ST_X[1]+325, 0, 640), "canopy 650 dia half-open", (0, 0, -40)),
        ((ST_X[1], 0, PLATE_Z - 40), (ST_X[1], 0, PLATE_Z - 40 - SHAFT_LEN), "shaft 300, dia 8", (95, 0, 0)),
    ],
    notes="front view (-Y)\nplate t=6 | coupling 8x8\nmin canopy clearance 50")

# 3. side view (looking -X)
view("side-view.png", 0, 0, "Side view",
    dimlines=[
        ((0, -CH_D/2, -120), (0, CH_D/2, -120), "800 D", (0, 0, -45)),
        ((0, -CH_D/2-70, 0), (0, -CH_D/2-70, CH_H), "1300 H", (0, 0, 0)),
        ((0, 0, 150), (0, 0, 150), "", (0, 0, 0)),
    ],
    notes="side view (-X)\nfloor slope 3-5 deg to drain corner\ndrain tube dia 8 | tray 500x400x60\nheater 200x100 left wall | fan dia 120 right wall\nDHT22 mid-chamber | DS18B20 in heater stream")

# 4. top view
view("top-view.png", 90, -90, "Top view (plan)",
    dimlines=[
        ((-W2, -CH_D/2, CH_H + 160), (W2, -CH_D/2, CH_H + 160), "1400 W", (0, 0, 45)),
        ((W2 + 70, -CH_D/2, CH_H + 60), (W2 + 70, CH_D/2, CH_H + 60), "800 D", (60, 0, 0)),
        ((ST_X[0], -60, CH_H + 60), (ST_X[1], -60, CH_H + 60), "700", (0, -80, 0)),
    ],
    notes="top view\nstations on X axis, pitch 700\ncanopy dia 650 half-open, dashed = swing envelope\nplate outline dashed")

# 5-6. front-right / front-left
view("front-right-view.png", 14, -55, "Front-right view",
    notes="axonometric\nkey dims: chamber 2200x800x1300 (real box)\npitch 700 | canopy dia 650 half-open\nshaft 8x300 | plate 6 mm\nall mm")
view("front-left-view.png", 14, -125, "Front-left view",
    notes="axonometric\nkey dims: chamber 2200x800x1300 (real box)\npitch 700 | canopy dia 650 half-open\nshaft 8x300 | plate 6 mm\nall mm")

print("done - 6 views written")
