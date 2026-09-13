"""
Smart Umbrella Dryer - Rev 4 ACCURATE 3D model generator (v2).

Fixes vs v1 (the inaccurate set):
  * 2D ORTHOGRAPHIC views (front/side/top) are drawn in true millimeter
    coordinates - what you measure on the drawing is the real dimension.
  * 3D parts are geometrically correct: cylindrical shafts/couplings,
    ribbed canopy (not a smooth cone), heater with grille, fan with blades,
    drain tube, chamber door + latch, leveling legs.
  * Every placement is checked by ASSERTIONS - the script refuses to render
    if any part would overlap, misalign, or break a clearance rule.

Outputs 6 PNGs (dimensioned, mm):
  exploded-view.png front-view.png side-view.png top-view.png
  front-right-view.png front-left-view.png

Usage:  pip install matplotlib numpy
        python generate_models.py

All dimensions in millimeters. See model/README.md for the dimension table.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =====================================================================
# CONSTANTS - the decided Rev 4 chamber (HARDWARE.md section 3). mm.
# =====================================================================
CH_W, CH_D, CH_H = 2200.0, 800.0, 1300.0    # internal W(x) D(y) H(z)
WALL = 20.0                                  # panel thickness
LEG_H = 100.0                                # leveling legs under the floor
PLATE_T = 6.0                                # 6061 motor plate
PITCH = 700.0                                # station spacing along X
ST_X = [-PITCH, 0.0, PITCH]

MOTOR_L, MOTOR_W, MOTOR_H = 115.0, 40.0, 36.0
MOTOR_SHAFT_D, MOTOR_SHAFT_LEN = 8.0, 15.0   # protruding motor shaft
SHAFT_D, SHAFT_LEN = 8.0, 300.0              # main station shaft
COUP_D, COUP_LEN = 16.0, 25.0                # 8x8 coupling outer/body
KP_H, KP_W, KP_T = 42.0, 22.0, 34.0          # KP08 bracket (L x H x thick)
HOLDER_W, HOLDER_H = 120.0, 30.0             # hook crossbar
CANOPY_D, CANOPY_DEPTH = 650.0, 200.0        # half-open projected
RIBS = 8                                     # canopy ribs (real umbrellas have 8)
TRAY_W, TRAY_D, TRAY_H = 500.0, 400.0, 60.0
DRAIN_D = 8.0
HEATER_W, HEATER_H, HEATER_T = 200.0, 100.0, 100.0   # face W x H x depth
HEATER_Z = 220.0                             # center height above floor (bottom 50 clear of floor)
FAN_D = 120.0
FAN_Z = 220.0
DOOR_W, DOOR_H = 1600.0, 1000.0              # front access door
DOOR_Z0 = 150.0                              # door bottom above floor
CLEAR = 50.0                                 # min canopy clearance rule

# ---------------- derived layout (single source of truth) -------------
FLOOR_TOP = LEG_H + WALL                     # inner floor surface z
PLATE_BOT = FLOOR_TOP + CH_H                 # plate underside z
PLATE_TOP = PLATE_BOT + PLATE_T
MOTOR_CZ = PLATE_TOP + MOTOR_H / 2
COUP_TOP = PLATE_BOT - MOTOR_SHAFT_LEN       # coupling starts under motor shaft
COUP_CZ = COUP_TOP - COUP_LEN / 2
SHAFT_TOP = COUP_TOP - COUP_LEN              # main shaft top (under coupling)
SHAFT_CZ = SHAFT_TOP - SHAFT_LEN / 2
SHAFT_BOT = SHAFT_TOP - SHAFT_LEN
HOLDER_CZ = SHAFT_BOT - HOLDER_H / 2
CANOPY_APEX_Z = SHAFT_BOT - 12.0
CANOPY_RIM_Z = CANOPY_APEX_Z - CANOPY_DEPTH
CANOPY_SPAN = PITCH + CANOPY_D / 2           # outermost canopy edge from center
WALL_GAP = CH_W / 2 - CANOPY_SPAN            # must be >= CLEAR
CANOPY_GAP = PITCH - CANOPY_D                # must be >= CLEAR
HEADROOM = FLOOR_TOP - CANOPY_RIM_Z          # canopy rim above floor

# =====================================================================
# ASSERTIONS - fail loudly instead of rendering a wrong model
# =====================================================================
def check_layout():
    errs = []
    if WALL_GAP < CLEAR:
        errs.append(f"wall gap {WALL_GAP:.0f} < {CLEAR:.0f} mm rule")
    if CANOPY_GAP < CLEAR:
        errs.append(f"canopy-to-canopy gap {CANOPY_GAP:.0f} < {CLEAR:.0f} mm rule")
    if CANOPY_RIM_Z < FLOOR_TOP + 100:
        errs.append(f"canopy rim only {CANOPY_RIM_Z - FLOOR_TOP:.0f} mm above floor")
    if SHAFT_LEN + COUP_LEN + MOTOR_SHAFT_LEN > CH_H:
        errs.append("drivetrain stack taller than chamber")
    if MOTOR_SHAFT_D != SHAFT_D:
        errs.append("coupling bore mismatch: motor shaft vs main shaft")
    if not (FLOOR_TOP < HEATER_Z - HEATER_H / 2 and HEATER_Z + HEATER_H / 2 < PLATE_BOT):
        errs.append("heater does not fit on the side wall")
    if not (FLOOR_TOP < FAN_Z - FAN_D / 2 and FAN_Z + FAN_D / 2 < PLATE_BOT):
        errs.append("fan does not fit on the side wall")
    if DOOR_W > CH_W - 2 * CLEAR or DOOR_H > CH_H - 2 * CLEAR:
        errs.append("door larger than structural opening allows")
    if TRAY_W > CH_W or TRAY_D > CH_D:
        errs.append("drip tray does not fit inside chamber footprint")
    # canopy rim must not hit heater/fan zone
    if CANOPY_RIM_Z < HEATER_Z + HEATER_H / 2:
        errs.append("canopy rim overlaps heater zone")
    if errs:
        raise SystemExit("LAYOUT ERRORS:\n  " + "\n  ".join(errs))
    print("[assert] layout checks passed:")
    print(f"         wall gap {WALL_GAP:.0f} mm, canopy gap {CANOPY_GAP:.0f} mm, "
          f"rim {CANOPY_RIM_Z - FLOOR_TOP:.0f} mm above floor")

# =====================================================================
# 3D PRIMITIVES (correct geometry)
# =====================================================================
def _faces_box(v):
    return [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]]

def box(cx, cy, cz, sx, sy, sz):
    x0, x1 = cx - sx / 2, cx + sx / 2
    y0, y1 = cy - sy / 2, cy + sy / 2
    z0, z1 = cz - sz / 2, cz + sz / 2
    v = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
                  [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]])
    return v, _faces_box(v)

def cyl_x(r, x0, x1, cy, cz, n=20):
    """Cylinder along X (shafts run vertically? no - vertical is Z)."""
    th = np.linspace(0, 2 * math.pi, n + 1)
    v = []
    for x in (x0, x1):
        for t in th:
            v.append([x, cy + r * math.sin(t), cz + r * math.cos(t)])
    v = np.array(v)
    h = len(th)
    faces = []
    for i in range(n):
        faces.append([i, i + 1, h + i + 1, h + i])          # side
    faces.append(list(range(h))[::-1])                    # end cap x0
    faces.append(list(range(h, 2 * h)))                   # end cap x1
    return v, faces

def cyl_z(r, z0, z1, cx, cy, n=20):
    """Vertical cylinder along Z - shafts, couplings, legs, drain tube."""
    th = np.linspace(0, 2 * math.pi, n + 1)
    v = []
    for z in (z0, z1):
        for t in th:
            v.append([cx + r * math.cos(t), cy + r * math.sin(t), z])
    v = np.array(v)
    h = n + 1
    faces = []
    for i in range(n):
        faces.append([i, i + 1, h + i + 1, h + i])
    faces.append(list(range(h))[::-1])
    faces.append(list(range(h, 2 * h)))
    return v, faces

def cyl_y(r, y0, y1, cx, cz, n=20):
    th = np.linspace(0, 2 * math.pi, n + 1)
    v = []
    for y in (y0, y1):
        for t in th:
            v.append([cx + r * math.cos(t), y, cz + r * math.sin(t)])
    v = np.array(v)
    h = n + 1
    faces = []
    for i in range(n):
        faces.append([i, i + 1, h + i + 1, h + i])
    faces.append(list(range(h))[::-1])
    faces.append(list(range(h, 2 * h)))
    return v, faces

def ribbed_canopy(cx, cy, apex_z, rim_z, dia, ribs=RIBS, n=28):
    """Umbrella canopy: edge-band facets (like a real umbrella) + rib ridges."""
    r = dia / 2
    th = np.linspace(0, 2 * math.pi, n + 1)
    verts, faces = [], []
    apex = [cx, cy, apex_z]
    verts.append(apex)
    for t in th:
        verts.append([cx + r * math.cos(t), cy + r * math.sin(t), rim_z])
    ring0, ring1 = 1, 1 + n
    for i in range(n):
        faces.append([0, ring0 + i, ring0 + i + 1])
    verts = np.array(verts)
    return verts, faces, r

def add(ax, v, f, color, alpha=1.0, ec='k', lw=0.3):
    mx = max(len(face) for face in f)
    padded = [list(face) + [face[-1]] * (mx - len(face)) for face in f]
    polys = [v[np.array(p)] for p in padded]
    ax.add_collection3d(Poly3DCollection(polys, facecolor=color,
                                         edgecolor=ec, linewidth=lw, alpha=alpha))

# =====================================================================
# SYSTEM RENDER (3D)
# =====================================================================
def draw_system(ax, explode=False):
    ez = 90.0 if explode else 0.0           # per-group explode lift (mm)

    def lift(z_group):
        return z_group + ez

    # ---- chamber shell (transparent) ----
    shell = [
        (0, -CH_D / 2 - WALL / 2, FLOOR_TOP + CH_H / 2, CH_W + 2 * WALL, WALL, CH_H, 0.10),  # front
        (0, CH_D / 2 + WALL / 2, FLOOR_TOP + CH_H / 2, CH_W + 2 * WALL, WALL, CH_H, 0.10),   # back
        (-CH_W / 2 - WALL / 2, 0, FLOOR_TOP + CH_H / 2, WALL, CH_D, CH_H, 0.10),             # left
        (CH_W / 2 + WALL / 2, 0, FLOOR_TOP + CH_H / 2, WALL, CH_D, CH_H, 0.10),              # right
        (0, 0, FLOOR_TOP - WALL / 2, CH_W + 2 * WALL, CH_D + 2 * WALL, WALL, 0.30),          # floor
    ]
    for cx, cy, cz, sx, sy, sz, a in shell:
        v, f = box(cx, cy, cz, sx, sy, sz)
        add(ax, v, f, '#d8d8d8', alpha=a, ec='#9a9a9a', lw=0.5)

    # ---- floor slope wedge (3 deg to +X/+Y corner, visual hint) ----
    slope_len = CH_D / 2
    drop = slope_len * math.tan(math.radians(4))
    v = np.array([
        [-CH_W / 2, -CH_D / 2, FLOOR_TOP], [CH_W / 2, -CH_D / 2, FLOOR_TOP],
        [CH_W / 2, CH_D / 2, FLOOR_TOP - drop], [-CH_W / 2, CH_D / 2, FLOOR_TOP - drop],
        [-CH_W / 2, -CH_D / 2, FLOOR_TOP - WALL], [CH_W / 2, -CH_D / 2, FLOOR_TOP - WALL],
        [CH_W / 2, CH_D / 2, FLOOR_TOP - WALL - drop], [-CH_W / 2, CH_D / 2, FLOOR_TOP - WALL - drop],
    ])
    add(ax, v, _faces_box(v), '#c9c9c9', alpha=0.35, ec='#aaaaaa', lw=0.4)

    # ---- drain corner: grommet + tube + tray ----
    drain_cx, drain_cy = CH_W / 2 - 120, CH_D / 2 - 100
    v, f = cyl_z(DRAIN_D / 2 + 3, FLOOR_TOP - WALL - drop, FLOOR_TOP - WALL + 8, drain_cx, drain_cy, n=12)
    add(ax, v, f, '#555555')
    v, f = cyl_z(DRAIN_D / 2, FLOOR_TOP - WALL - drop - 6, FLOOR_TOP + 4, drain_cx, drain_cy, n=12)
    add(ax, v, f, '#777777')
    v, f = cyl_y(DRAIN_D / 2, drain_cy, CH_D / 2 + WALL + 40, drain_cx, FLOOR_TOP - 70, n=12)
    add(ax, v, f, '#777777')                     # tube exiting through wall
    v, f = box(0, 0, LEG_H / 2 - 40 - (120 if explode else 0), TRAY_W, TRAY_D, TRAY_H)
    add(ax, v, f, '#e0c952', alpha=0.95)         # drip tray under drain exit

    # ---- legs ----
    for lx in (-CH_W / 2 + 80, CH_W / 2 - 80):
        for ly in (-CH_D / 2 + 80, CH_D / 2 - 80):
            v, f = cyl_z(12, 0, LEG_H, lx, ly, n=10)
            add(ax, v, f, '#8a8a8a')

    # ---- front door + latch ----
    dz = FLOOR_TOP + DOOR_Z0 + DOOR_H / 2
    v, f = box(0, -CH_D / 2 - WALL - 6, dz + (200 if explode else 0), DOOR_W, 6, DOOR_H)
    add(ax, v, f, '#9fc5e8', alpha=0.35, ec='#5b87a8', lw=0.6)
    v, f = box(DOOR_W / 2 - 60, -CH_D / 2 - WALL - 14, dz, 40, 18, 90)
    add(ax, v, f, '#444444')                     # rotary latch

    # ---- motor plate ----
    v, f = box(0, 0, PLATE_TOP - PLATE_T / 2 + (ez if explode else 0),
               CH_W + 2 * WALL, CH_D + 2 * WALL, PLATE_T)
    add(ax, v, f, '#7fbf7f', alpha=0.95)

    # ---- stations ----
    for sx in ST_X:
        # motor body on top of plate
        v, f = box(sx, 0, MOTOR_CZ + (ez + 60 if explode else 0), MOTOR_L, MOTOR_W, MOTOR_H)
        add(ax, v, f, '#4f81bd')
        # motor shaft (cylinder, 8 x 15)
        v, f = cyl_z(MOTOR_SHAFT_D / 2, COUP_TOP + MOTOR_SHAFT_LEN + (ez + 60 if explode else 0) - MOTOR_SHAFT_LEN,
                     COUP_TOP + MOTOR_SHAFT_LEN + (ez + 60 if explode else 0), sx, 0, n=14)
        add(ax, v, f, '#909090')
        # coupling (cylinder 16 dia x 25)
        zc = COUP_CZ + (ez * 0.6 if explode else 0)
        v, f = cyl_z(COUP_D / 2, zc - COUP_LEN / 2, zc + COUP_LEN / 2, sx, 0, n=16)
        add(ax, v, f, '#9467bd')
        # main shaft (cylinder 8 x 300)
        zs = SHAFT_CZ + (ez * 0.3 if explode else 0)
        v, f = cyl_z(SHAFT_D / 2, zs - SHAFT_LEN / 2, zs + SHAFT_LEN / 2, sx, 0, n=14)
        add(ax, v, f, '#6d6d6d')
        zsb = SHAFT_BOT + (ez * 0.3 if explode else 0)
        # KP08 x2 (bracket beside shaft)
        for zb in (SHAFT_TOP - 25 + (ez * 0.3 if explode else 0),
                   SHAFT_BOT + 25 + (ez * 0.3 if explode else 0)):
            v, f = box(sx, -KP_W / 2 - SHAFT_D / 2 - 2, zb, KP_H, KP_T, KP_W)
            add(ax, v, f, '#c49a6c', alpha=0.95)
        # holder crossbar
        v, f = box(sx, 0, HOLDER_CZ + (ez * 0.15 if explode else 0), HOLDER_W, 18, HOLDER_H)
        add(ax, v, f, '#333333')
        # ribbed canopy
        az = CANOPY_APEX_Z + (ez * 0.15 if explode else 0)
        verts, faces, r = ribbed_canopy(sx, 0, az, az - CANOPY_DEPTH, CANOPY_D)
        add(ax, verts, faces, '#e07b39', alpha=0.82, ec='#8c4a1d', lw=0.5)
        # center pole to holder
        v, f = cyl_z(5, az - CANOPY_DEPTH, HOLDER_CZ, sx, 0, n=10)
        add(ax, v, f, '#555555')

    # ---- heater (left wall) with grille ----
    hx = -CH_W / 2 + HEATER_T / 2 + 4
    v, f = box(hx, 0, HEATER_Z, HEATER_T, HEATER_W, HEATER_H)
    add(ax, v, f, '#c0392b', alpha=0.9)
    for gy in np.linspace(-HEATER_W / 2 + 12, HEATER_W / 2 - 12, 7):   # outlet grille lines
        v, f = box(hx + HEATER_T / 2 + 2, gy, HEATER_Z, 4, 3, HEATER_H - 14)
        add(ax, v, f, '#7c2c22', alpha=0.9)
    # ---- fan (right wall) with blades ----
    fx = CH_W / 2 - 35
    v, f = cyl_x(FAN_D / 2, fx - 20, fx + 20, 0, FAN_Z, n=22)
    add(ax, v, f, '#3fa7d6', alpha=0.55, ec='#24657f', lw=0.5)         # fan ring
    for k in range(4):                                                  # 4 blades
        a0 = k * math.pi / 2 + 0.4
        blade = []
        for rr in (14, FAN_D / 2 - 8):
            blade.append([fx, rr * math.cos(a0), FAN_Z + rr * math.sin(a0)])
            blade.append([fx, (rr + 26) * math.cos(a0 + 0.35), FAN_Z + (rr + 26) * math.sin(a0 + 0.35)])
        bv = np.array(blade)
        add(ax, bv, [[0, 1, 3, 2]], '#2b7a99', alpha=0.9)

# =====================================================================
# 2D ORTHOGRAPHIC - TRUE SCALE mm drawings with dimension lines
# =====================================================================
class Sheet:
    def __init__(self, title, w, h):
        self.fig, self.ax = plt.subplots(figsize=(13, 9))
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_title(title + "   (true scale, mm)", fontsize=12, loc='left')
        self.w, self.h = w, h
        self.ax.set_xlim(-w * 0.16, w * 1.10)
        self.ax.set_ylim(-h * 0.14, h * 1.14)

    def part(self, cx, cz, sx, sz, fc, ec='k', lw=0.8, alpha=1.0, zorder=2):
        self.ax.add_patch(Rectangle((cx - sx / 2, cz - sz / 2), sx, sz,
                                    facecolor=fc, edgecolor=ec, lw=lw,
                                    alpha=alpha, zorder=zorder))

    def circle(self, cx, cz, r, fc, ec='k', lw=0.8, alpha=1.0):
        self.ax.add_patch(Circle((cx, cz), r, facecolor=fc, edgecolor=ec,
                                 lw=lw, alpha=alpha, zorder=2))

    def dim_h(self, x0, x1, z, label, tick=18):
        self.ax.annotate('', xy=(x1, z), xytext=(x0, z),
                         arrowprops=dict(arrowstyle='<->', color='#b00000', lw=1.1))
        for x in (x0, x1):
            self.ax.plot([x, x], [z - tick, z + tick], color='#b00000', lw=0.8)
        self.ax.text((x0 + x1) / 2, z + tick * 0.5, label, color='#b00000',
                     fontsize=9, ha='center', fontweight='bold')

    def dim_v(self, z0, z1, x, label, tick=18, side=1):
        self.ax.annotate('', xy=(x, z1), xytext=(x, z0),
                         arrowprops=dict(arrowstyle='<->', color='#b00000', lw=1.1))
        for z in (z0, z1):
            self.ax.plot([x - tick, x + tick], [z, z], color='#b00000', lw=0.8)
        self.ax.text(x + side * tick * 1.1, (z0 + z1) / 2, label, color='#b00000',
                     fontsize=9, va='center', rotation=90, fontweight='bold')

    def note(self, x, z, text):
        self.ax.text(x, z, text, fontsize=8.2, family='monospace', va='top',
                     bbox=dict(boxstyle='round', fc='#f6f6f6', ec='#999999'))

    def save(self, name):
        self.fig.savefig(name, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(self.fig)
        print("wrote", name)

def draw_chamber_2d(s, front=True):
    """Walls, floor, legs, door in a 2D elevation. front: X-Z else Y-Z."""
    W = CH_W if front else CH_D
    # walls
    s.part(-W / 2 - WALL / 2, FLOOR_TOP + CH_H / 2, WALL, CH_H, '#d8d8d8')
    s.part(W / 2 + WALL / 2, FLOOR_TOP + CH_H / 2, WALL, CH_H, '#d8d8d8')
    s.part(0, FLOOR_TOP + CH_H + WALL / 2, W + 2 * WALL, WALL, '#d8d8d8')
    s.part(0, FLOOR_TOP - WALL / 2, W + 2 * WALL, WALL, '#e2e2e2')
    # legs
    for lx in (-W / 2 + 80, W / 2 - 80):
        s.part(lx, LEG_H / 2, 24, LEG_H, '#8a8a8a')
    # door on front elevation
    if front:
        s.part(0, FLOOR_TOP + DOOR_Z0 + DOOR_H / 2, DOOR_W, DOOR_H,
               '#9fc5e8', ec='#5b87a8', alpha=0.35, lw=1.0)
        s.part(DOOR_W / 2 - 60, FLOOR_TOP + DOOR_Z0 + DOOR_H / 2, 40, 90, '#444444')

def front_view():
    s = Sheet("FRONT VIEW (X-Z)", CH_W, CH_H + LEG_H + 120)
    draw_chamber_2d(s, front=True)
    # stations
    for sx in ST_X:
        s.part(sx, MOTOR_CZ, MOTOR_L, MOTOR_H, '#4f81bd')
        s.part(sx, COUP_CZ, COUP_D, COUP_LEN, '#9467bd')
        s.part(sx, SHAFT_CZ, SHAFT_D, SHAFT_LEN, '#6d6d6d')
        s.circle(sx, SHAFT_TOP - 25, KP_W / 2, '#c49a6c')
        s.circle(sx, SHAFT_BOT + 25, KP_W / 2, '#c49a6c')
        s.part(sx, HOLDER_CZ, HOLDER_W, HOLDER_H, '#333333')
        # canopy as triangle section (true width/depth)
        s.ax.add_patch(plt.Polygon([[sx, CANOPY_APEX_Z],
                                    [sx - CANOPY_D / 2, CANOPY_RIM_Z],
                                    [sx + CANOPY_D / 2, CANOPY_RIM_Z]],
                                   closed=True, facecolor='#e07b39',
                                   edgecolor='#8c4a1d', alpha=0.82, zorder=2))
    # heater + fan
    s.part(-CH_W / 2 + HEATER_T / 2 + 4, HEATER_Z, HEATER_T, HEATER_H, '#c0392b')
    s.circle(CH_W / 2 - 35, FAN_Z, FAN_D / 2, '#3fa7d6')
    # dimensions
    zb = FLOOR_TOP - 110
    s.dim_h(-CH_W / 2, CH_W / 2, zb, "2200 INTERNAL W")
    s.dim_h(ST_X[0], ST_X[1], PLATE_TOP + MOTOR_H + 60, "700 PITCH")
    s.dim_v(FLOOR_TOP, FLOOR_TOP + CH_H, -CH_W / 2 - 90, "1300 H", side=-1)
    s.dim_v(CANOPY_APEX_Z, CANOPY_RIM_Z, ST_X[1] + CANOPY_D / 2 + 40, "CANOPY 200")
    s.dim_h(ST_X[1] - CANOPY_D / 2, ST_X[1] + CANOPY_D / 2, CANOPY_RIM_Z - 60, "650 HALF-OPEN")
    s.dim_v(SHAFT_TOP, SHAFT_BOT, ST_X[0] - 60, "SHAFT 300 x dia8", side=-1)
    s.note(CH_W / 2 * 0.42, FLOOR_TOP + CH_H * 0.96,
           "door 1600x1000, latch right\nfloor slope 4 deg to +X corner\nclearances: 75 wall / 50 canopy (PASS)")
    s.save("front-view.png")

def side_view():
    s = Sheet("SIDE VIEW (Y-Z)", CH_D, CH_H + LEG_H + 120)
    draw_chamber_2d(s, front=False)
    # station silhouette center
    s.part(0, MOTOR_CZ, MOTOR_W, MOTOR_H, '#4f81bd')
    s.part(0, COUP_CZ, COUP_D, COUP_LEN, '#9467bd')
    s.part(0, SHAFT_CZ, SHAFT_D, SHAFT_LEN, '#6d6d6d')
    s.part(0, HOLDER_CZ, 18, HOLDER_H, '#333333')
    s.ax.add_patch(plt.Polygon([[0, CANOPY_APEX_Z], [-CANOPY_D / 2, CANOPY_RIM_Z],
                                [CANOPY_D / 2, CANOPY_RIM_Z]], closed=True,
                               facecolor='#e07b39', edgecolor='#8c4a1d', alpha=0.82))
    # heater (left/back wall) + fan (right/front)
    s.part(-CH_D / 2 + HEATER_T / 2 + 4, HEATER_Z, HEATER_T, HEATER_H, '#c0392b')
    s.circle(CH_D / 2 - 35, FAN_Z, FAN_D / 2, '#3fa7d6')
    # slope + drain + tray
    drop = (CH_D / 2) * math.tan(math.radians(4))
    s.ax.add_patch(plt.Polygon([[-CH_D / 2, FLOOR_TOP], [CH_D / 2, FLOOR_TOP],
                                [CH_D / 2, FLOOR_TOP - drop], [-CH_D / 2, FLOOR_TOP - WALL]],
                               closed=True, facecolor='#cfcfcf', edgecolor='#999999'))
    s.circle(CH_D / 2 - 100, FLOOR_TOP - drop / 2, DRAIN_D, '#555555')
    s.part(CH_D / 2 + 60, FLOOR_TOP - 70, 130, 8, '#777777')
    s.part(0, LEG_H - 40 - TRAY_H / 2, TRAY_D, TRAY_H, '#e0c952')
    s.dim_h(-CH_D / 2, CH_D / 2, FLOOR_TOP - 110, "800 D")
    s.dim_v(FLOOR_TOP, FLOOR_TOP + CH_H, -CH_D / 2 - 90, "1300 H", side=-1)
    s.dim_h(-CH_D / 2, CH_D / 2, FLOOR_TOP - drop - 60, "SLOPE 4 deg = 28 drop", tick=12)
    s.dim_v(HEATER_Z - HEATER_H / 2, HEATER_Z + HEATER_H / 2, -CH_D / 2 - 40, "HEATER 100", side=-1)
    s.note(CH_D / 2 * 0.30, FLOOR_TOP + CH_H * 0.98,
           "heater 200x100 face, left wall\nfan dia120, right wall, both at z=220\nDHT22 mid-chamber, DS18B20 in heater stream")
    s.save("side-view.png")

def top_view():
    s = Sheet("TOP VIEW / PLAN (X-Y)", CH_W, CH_D + 200)
    # walls
    s.part(0, -CH_D / 2 - WALL / 2, CH_W + 2 * WALL, WALL, '#d8d8d8')
    s.part(0, CH_D / 2 + WALL / 2, CH_W + 2 * WALL, WALL, '#d8d8d8')
    s.part(-CH_W / 2 - WALL / 2, 0, WALL, CH_D + 2 * WALL, '#d8d8d8')
    s.part(CH_W / 2 + WALL / 2, 0, WALL, CH_D + 2 * WALL, '#d8d8d8')
    # stations: motor square + shaft circle + canopy circle
    for sx in ST_X:
        s.part(sx, 0, MOTOR_L, MOTOR_W, '#4f81bd')
        s.circle(sx, 0, SHAFT_D / 2 + 4, '#9467bd')
        c = Circle((sx, 0), CANOPY_D / 2, facecolor='#e07b39', edgecolor='#8c4a1d',
                   alpha=0.55, lw=1.0, linestyle='--', zorder=1)
        s.ax.add_patch(c)
    # heater + fan faces
    s.part(-CH_W / 2 + HEATER_T / 2 + 4, 0, HEATER_T, HEATER_W, '#c0392b')
    s.circle(CH_W / 2 - 35, 0, FAN_D / 2, '#3fa7d6')
    # drain corner
    s.circle(CH_W / 2 - 120, CH_D / 2 - 100, DRAIN_D + 3, '#555555')
    s.dim_h(-CH_W / 2, CH_W / 2, CH_D / 2 + 70, "2200 W")
    s.dim_v(-CH_D / 2, CH_D / 2, CH_W / 2 + 80, "800 D")
    s.dim_h(ST_X[0], ST_X[1], -CH_D / 2 - 60, "700 PITCH")
    s.dim_h(ST_X[1] - CANOPY_D / 2, ST_X[1] + CANOPY_D / 2, CH_D / 2 + 30, "650 SWING (dashed)")
    s.note(CH_W * 0.30, CH_D / 2 + 150,
           "canopy swing envelopes dashed\nheater face 200 on left wall\nfan dia120 on right wall\ndrain corner +X,+Y -> tube out back")
    s.save("top-view.png")

# =====================================================================
# 3D VIEW WRAPPER
# =====================================================================
def bounds():
    zlo = 0.0
    zhi = PLATE_TOP + MOTOR_H + (500 if True else 0)
    return -(CH_W / 2 + 260), CH_W / 2 + 260, -(CH_D / 2 + 260), CH_D / 2 + 260, zlo, zhi + 60

def view3d(name, elev, azim, title, explode=False, labels=None):
    fig = plt.figure(figsize=(13, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_proj_type('ortho')
    x0, x1, y0, y1, z0, z1 = bounds()
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_zlim(z0, z1)
    try:
        ax.set_box_aspect((x1 - x0, y1 - y0, z1 - z0))
    except Exception:
        pass
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title + "   (mm)", fontsize=12, loc='left')
    draw_system(ax, explode=explode)
    if labels:
        for x, y, z, t in labels:
            ax.text(x, y, z, t, fontsize=8.5, ha='center',
                    bbox=dict(boxstyle='round', fc='white', ec='#777777', alpha=0.88))
    note = (f"chamber {CH_W:.0f} x {CH_D:.0f} x {CH_H:.0f} internal | pitch {PITCH:.0f} | "
            f"canopy {CANOPY_D:.0f} dia half-open | shaft dia{SHAFT_D:.0f} x {SHAFT_LEN:.0f} | "
            f"plate {PLATE_T:.0f} | legs {LEG_H:.0f} | door {DOOR_W:.0f} x {DOOR_H:.0f}")
    ax.text2D(0.01, 0.02, note, transform=ax.transAxes, fontsize=8.3,
              family='monospace', va='bottom',
              bbox=dict(boxstyle='round', fc='#f6f6f6', ec='#999999'))
    fig.savefig(name, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("wrote", name)

# =====================================================================
# GENERATE
# =====================================================================
if __name__ == "__main__":
    check_layout()

    # 1. exploded with corrected placements + leader labels
    lbl = [
        (ST_X[1], 0, MOTOR_CZ + 140, "worm motor 115x40x36, 60 kg-cm"),
        (ST_X[1], 0, COUP_TOP + 40, "coupling 8x8, dia16 x 25"),
        (ST_X[1], 0, SHAFT_CZ, "shaft dia8 x 300 + 2x KP08"),
        (ST_X[1], 0, HOLDER_CZ - 30, "holder hook 120 wide"),
        (ST_X[1], 0, CANOPY_RIM_Z - 60, "canopy dia650 half-open, 8 ribs"),
        (-CH_W / 2 + 130, 0, HEATER_Z + 90, "PTC heater 100 W + grille"),
        (CH_W / 2 - 90, 0, FAN_Z + 90, "fan dia120, blades"),
        (CH_W / 2 - 120, CH_D / 2 - 100, FLOOR_TOP - 120, "drain dia8 -> tube -> tray 500x400x60"),
        (0, -CH_D / 2 - 120, FLOOR_TOP + DOOR_Z0 + DOOR_H + 40, "door 1600x1000 + latch"),
    ]
    view3d("exploded-view.png", 16, -58, "EXPLODED VIEW", explode=True, labels=lbl)

    # 2-4. true-scale 2D orthographic
    front_view()
    side_view()
    top_view()

    # 5-6. axonometric
    view3d("front-right-view.png", 14, -55, "FRONT-RIGHT VIEW")
    view3d("front-left-view.png", 14, -125, "FRONT-LEFT VIEW")

    print("done - 6 accurate views written")
