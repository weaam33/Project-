"""
North & East Africa Map Coloring — CSP Game
20 Countries: Morocco → Egypt → Horn of Africa → East Africa
Algorithms : Backtracking, Forward Checking
Heuristics : MRV, Degree Heuristic, LCV
Modes      : Manual | AI (step-by-step or auto)
"""

import pygame
import sys
import math

# ═══════════════════════════════════════════════
#  WINDOW & THEME
# ═══════════════════════════════════════════════
W, H = 1280, 800
FPS  = 60

BG        = (10, 13, 20)
PANEL_BG  = (16, 20, 32)
SIDEBAR   = (13, 17, 27)
ACCENT    = (50, 200, 120)
ACCENT2   = (255, 80, 100)
SUCCESS   = (50, 220, 110)
WARN      = (255, 200, 60)
TEXT      = (210, 220, 235)
TEXT_DIM  = (90, 105, 135)
BORDER    = (30, 42, 65)
WHITE     = (255, 255, 255)
MAP_OCEAN = (15, 35, 65)
MAP_BORDER= (180, 160, 100)
LOST_COL  = (220, 40,  50)
PURPLE_BTN= (110, 70, 200)

PALETTE = [
    (220,  75,  65),   # 0 Red
    ( 55, 145, 225),   # 1 Blue
    ( 50, 190,  85),   # 2 Green
    (240, 195,  45),   # 3 Yellow
    (170,  80, 205),   # 4 Purple
    (235, 135,  40),   # 5 Orange
]
COLOR_NAMES = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]

# ═══════════════════════════════════════════════
#  20 COUNTRIES — North & East Africa
#  (lon, lat) polygons
# ═══════════════════════════════════════════════
COUNTRY_POLYS = {
    "Morocco": [
        (-5.9,35.9),(-1.7,35.8),(-1.1,34.9),(-1.7,34.0),(-2.2,32.0),
        (-3.0,30.9),(-3.0,29.5),(-8.7,27.7),(-8.7,28.7),(-13.2,27.7),
        (-13.2,28.0),(-8.0,31.7),(-5.9,33.9)
    ],
    "Algeria": [
        (-1.7,35.8),(8.6,37.2),(8.6,36.9),(9.5,37.4),(9.5,33.0),
        (8.0,32.5),(5.0,31.6),(3.0,31.8),(1.2,31.1),(1.2,22.5),
        (-3.2,22.5),(-3.2,19.0),(-5.5,19.0),(-5.5,21.3),(-8.7,27.7),
        (-3.0,29.5),(-3.0,30.9),(-2.2,32.0),(-1.7,34.0),(-1.1,34.9)
    ],
    "Tunisia": [
        (8.6,37.2),(10.6,37.5),(11.5,33.1),(10.0,30.5),(9.5,33.0),(8.6,36.9)
    ],
    "Libya": [
        (9.5,37.4),(13.6,32.9),(15.2,23.4),(15.2,22.5),(25.0,22.5),
        (25.0,31.6),(20.0,31.9),(13.0,32.9),(11.5,33.1),(10.6,37.5)
    ],
    "Egypt": [
        (25.0,22.5),(36.9,22.0),(34.8,29.5),(34.2,31.2),(32.3,31.1),
        (31.5,30.0),(29.2,30.9),(25.0,31.6)
    ],
    "Western Sahara": [
        (-13.2,27.7),(-8.7,27.7),(-5.5,21.3),(-5.5,19.0),(-17.0,20.8),
        (-17.0,21.3),(-13.0,22.9)
    ],
    "Mauritania": [
        (-17.0,20.8),(-5.5,19.0),(-5.5,15.5),(-12.3,14.7),(-16.5,16.1),
        (-16.9,20.1)
    ],
    "Mali": [
        (-5.5,19.0),(-3.2,19.0),(-3.2,22.5),(1.2,22.5),(1.2,15.0),
        (2.0,15.3),(4.2,19.1),(4.2,16.0),(2.5,11.5),(-0.5,11.1),
        (-3.3,11.9),(-5.5,10.3),(-5.5,15.5)
    ],
    "Niger": [
        (1.2,22.5),(15.2,22.5),(14.4,15.5),(13.6,13.3),(13.0,13.5),
        (12.4,13.1),(11.4,13.5),(7.5,13.7),(5.0,13.5),(4.2,16.0),
        (4.2,19.1),(2.0,15.3),(1.2,15.0)
    ],
    "Chad": [
        (15.2,22.5),(25.0,22.5),(24.0,19.5),(24.0,10.0),(22.0,10.0),
        (20.5,9.0),(18.5,9.0),(16.0,7.5),(15.5,11.0),(14.0,13.0),
        (13.6,13.3),(14.4,15.5)
    ],
    "Sudan": [
        (25.0,22.5),(36.9,22.0),(37.0,18.0),(36.5,14.5),(34.0,11.0),
        (32.0,11.5),(29.5,10.0),(27.5,10.5),(25.5,10.5),(24.0,10.0),
        (24.0,19.5)
    ],
    "South Sudan": [
        (24.0,10.0),(25.5,10.5),(27.5,10.5),(29.5,10.0),(32.0,11.5),
        (34.0,11.0),(33.0,9.5),(33.5,8.5),(36.0,6.0),(36.0,4.5),
        (35.3,5.0),(34.1,0.4),(29.7,-1.0),(28.0,1.5),(27.0,3.5),
        (25.0,5.0),(23.5,7.5),(22.5,6.5),(20.5,9.0),(22.0,10.0)
    ],
    "Eritrea": [
        (36.9,22.0),(43.1,12.7),(42.0,10.9),(40.0,12.4),(38.5,15.0),(37.0,18.0)
    ],
    "Djibouti": [
        (43.1,12.7),(43.5,11.5),(42.3,11.0),(42.0,10.9)
    ],
    "Ethiopia": [
        (37.0,18.0),(38.5,15.0),(40.0,12.4),(42.0,10.9),(43.5,11.5),
        (44.0,11.0),(44.5,10.0),(42.7,6.7),(39.8,3.5),(34.1,0.4),
        (33.9,4.0),(35.3,5.0),(36.0,4.5),(36.0,6.0),(33.5,8.5),
        (33.0,9.5),(34.0,11.0),(36.5,14.5)
    ],
    "Somalia": [
        (43.5,11.5),(43.1,12.7),(50.0,11.5),(51.4,10.0),(44.0,11.0),
        (44.5,10.0),(42.7,6.7),(41.5,1.7),(41.0,-1.7),(41.8,-1.7),(49.0,11.0)
    ],
    "Uganda": [
        (34.1,0.4),(33.9,4.0),(31.5,4.0),(30.0,2.0),(29.7,-1.0)
    ],
    "Kenya": [
        (34.1,0.4),(29.7,-1.0),(34.0,-3.0),(37.5,-4.5),(40.5,-2.0),
        (41.0,-1.7),(41.5,1.7),(40.0,4.5),(38.5,3.5),(36.0,4.5),
        (35.3,5.0)
    ],
    "Nigeria": [
        (2.5,11.5),(2.5,12.5),(7.5,13.7),(5.0,13.5),(13.0,13.5),
        (14.0,13.0),(12.0,8.0),(8.5,4.5),(5.0,4.3),(3.9,6.5),(3.9,9.0),
        (3.9,12.4),(1.7,11.0),(0.5,11.0),(-0.5,11.1)
    ],
    "Cameroon": [
        (14.0,13.0),(15.5,11.0),(16.0,7.5),(15.0,4.5),(14.5,2.2),
        (13.3,2.2),(12.0,2.8),(11.0,2.2),(9.8,3.7),(9.0,3.9),
        (8.5,4.5),(12.0,8.0),(14.0,13.0)
    ],
}

# ═══════════════════════════════════════════════
#  ADJACENCY — 20-country subset
# ═══════════════════════════════════════════════
ADJACENCY = {
    "Morocco":        ["Algeria", "Western Sahara"],
    "Algeria":        ["Morocco", "Tunisia", "Libya", "Niger", "Mali", "Mauritania", "Western Sahara"],
    "Tunisia":        ["Algeria", "Libya"],
    "Libya":          ["Tunisia", "Algeria", "Niger", "Chad", "Sudan", "Egypt"],
    "Egypt":          ["Libya", "Sudan"],
    "Western Sahara": ["Morocco", "Algeria", "Mauritania"],
    "Mauritania":     ["Western Sahara", "Algeria", "Mali"],
    "Mali":           ["Algeria", "Mauritania", "Niger"],
    "Niger":          ["Algeria", "Libya", "Chad", "Nigeria", "Mali"],
    "Chad":           ["Libya", "Niger", "Nigeria", "Cameroon", "Sudan", "South Sudan"],
    "Sudan":          ["Egypt", "Libya", "Chad", "South Sudan", "Ethiopia", "Eritrea"],
    "South Sudan":    ["Sudan", "Chad", "Ethiopia", "Uganda"],
    "Eritrea":        ["Sudan", "Ethiopia", "Djibouti"],
    "Djibouti":       ["Eritrea", "Ethiopia", "Somalia"],
    "Ethiopia":       ["Eritrea", "Djibouti", "Somalia", "Kenya", "South Sudan", "Sudan"],
    "Somalia":        ["Djibouti", "Ethiopia", "Kenya"],
    "Uganda":         ["South Sudan", "Kenya"],
    "Kenya":          ["Ethiopia", "Somalia", "Uganda"],
    "Nigeria":        ["Niger", "Chad", "Cameroon"],
    "Cameroon":       ["Nigeria", "Chad"],
}

COUNTRY_NAMES = list(COUNTRY_POLYS.keys())

# ═══════════════════════════════════════════════
#  PROJECTION  — zoomed to North/East Africa
# ═══════════════════════════════════════════════
LON_MIN, LON_MAX = -18.0, 52.0
LAT_MIN, LAT_MAX =  -5.0, 38.5

MAP_RECT = pygame.Rect(8, 8, 840, H - 16)

def project(lon, lat, rect=None):
    if rect is None: rect = MAP_RECT
    x = rect.x + (lon - LON_MIN) / (LON_MAX - LON_MIN) * rect.width
    y = rect.y + rect.height - (lat - LAT_MIN) / (LAT_MAX - LAT_MIN) * rect.height
    return (int(x), int(y))

def build_screen_polys():
    return {name: [project(lon, lat) for lon, lat in pts]
            for name, pts in COUNTRY_POLYS.items()}

def centroid(pts):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return (int(cx), int(cy))

def point_in_poly(px, py, pts):
    n = len(pts); inside = False
    x, y = px, py; j = n - 1
    for i in range(n):
        xi, yi = pts[i]; xj, yj = pts[j]
        if ((yi > y) != (yj > y)) and (x < (xj-xi)*(y-yi)/(yj-yi+1e-9)+xi):
            inside = not inside
        j = i
    return inside


# ═══════════════════════════════════════════════
#  CSP SOLVER
# ═══════════════════════════════════════════════
class CSPSolver:
    def __init__(self, regions, adjacency, num_colors):
        self.regions = regions
        self.adj     = adjacency
        self.nc      = num_colors
        self.steps   = []
        self.use_mrv    = True
        self.use_lcv    = True
        self.use_degree = False

    def neighbors(self, r):
        return self.adj.get(r, [])

    def consistent(self, r, c, asgn):
        return all(asgn.get(nb) != c for nb in self.neighbors(r))

    def select_var(self, asgn, domains):
        unassigned = [r for r in self.regions if r not in asgn]
        if self.use_mrv:
            min_d = min(len(domains[r]) for r in unassigned)
            candidates = [r for r in unassigned if len(domains[r]) == min_d]
        else:
            candidates = unassigned
        if self.use_degree:
            return max(candidates, key=lambda r: len(self.neighbors(r)))
        return candidates[0]

    def order_values(self, r, asgn, domains):
        def conflicts(c):
            return sum(1 for nb in self.neighbors(r)
                       if nb not in asgn and c in domains.get(nb, []))
        if self.use_lcv:
            return sorted(domains[r], key=conflicts)
        return domains[r]

    def solve(self, algorithm="Backtracking"):
        self.steps = []
        domains = {r: list(range(self.nc)) for r in self.regions}
        return self._bt({}, domains, algorithm)

    def _bt(self, asgn, domains, alg):
        if len(asgn) == len(self.regions):
            self.steps.append((dict(asgn), None, "done"))
            return asgn
        r = self.select_var(asgn, domains)
        for c in self.order_values(r, asgn, domains):
            if self.consistent(r, c, asgn):
                asgn[r] = c
                self.steps.append((dict(asgn), r, "assign"))
                new_d = {k: list(v) for k, v in domains.items()}
                ok = True
                if alg == "Forward Checking":
                    for nb in self.neighbors(r):
                        if nb not in asgn and c in new_d[nb]:
                            new_d[nb].remove(c)
                            if not new_d[nb]:
                                ok = False; break
                if ok:
                    res = self._bt(asgn, new_d, alg)
                    if res is not None:
                        return res
                self.steps.append((dict(asgn), r, "backtrack"))
                del asgn[r]
        return None


# ═══════════════════════════════════════════════
#  UI HELPERS
# ═══════════════════════════════════════════════
def rr(surf, col, rect, r=10, bw=0, bc=None):
    pygame.draw.rect(surf, col, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)

def btn(surf, font, label, rect, hover, active=False, icon=None):
    if active:
        bg = PURPLE_BTN
        tc = WHITE
    elif hover:
        bg = (40, 60, 90)
        tc = WHITE
    else:
        bg = (20, 27, 45)
        tc = TEXT_DIM
    rr(surf, bg, rect, 9, 1, BORDER if not active else (140, 100, 230))
    t = font.render(label, True, tc)
    surf.blit(t, t.get_rect(center=rect.center))

def lerp(a, b, t):
    return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def lighten(col, amt=40):
    return tuple(min(255, c+amt) for c in col)


# ═══════════════════════════════════════════════
#  ICONS (drawn with pygame primitives)
# ═══════════════════════════════════════════════
def draw_icon(surf, kind, cx, cy, size=14, col=WHITE):
    """Draw simple icons for UI buttons."""
    if kind == "step":  # ▷ triangle
        pts = [(cx-size//2, cy-size//2), (cx+size//2, cy), (cx-size//2, cy+size//2)]
        pygame.draw.polygon(surf, col, pts)
        pygame.draw.line(surf, col, (cx-size//2-3, cy-size//2), (cx-size//2-3, cy+size//2), 2)
    elif kind == "play":  # ▶
        pts = [(cx-size//2, cy-size//2), (cx+size//2, cy), (cx-size//2, cy+size//2)]
        pygame.draw.polygon(surf, col, pts)
    elif kind == "pause":  # ⏸
        pygame.draw.rect(surf, col, pygame.Rect(cx-size//2, cy-size//2, size//3, size))
        pygame.draw.rect(surf, col, pygame.Rect(cx+size//6, cy-size//2, size//3, size))
    elif kind == "reset":  # ↺ circle arrow
        pygame.draw.circle(surf, col, (cx, cy), size//2, 2)
        pts2 = [(cx+size//2, cy-size//4), (cx+size//2+4, cy), (cx+size//2-4, cy)]
        pygame.draw.polygon(surf, col, pts2)
    elif kind == "menu":  # ← arrow
        pygame.draw.line(surf, col, (cx+size//2, cy), (cx-size//2, cy), 2)
        pygame.draw.line(surf, col, (cx-size//2, cy), (cx, cy-size//2), 2)
        pygame.draw.line(surf, col, (cx-size//2, cy), (cx, cy+size//2), 2)


# ═══════════════════════════════════════════════
#  MAIN GAME
# ═══════════════════════════════════════════════
class NorthAfricaGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("North & East Africa — CSP Map Coloring")
        self.clock  = pygame.time.Clock()

        # Fonts
        self.fn_xl = pygame.font.SysFont("segoeui", 36, bold=True)
        self.fn_lg = pygame.font.SysFont("segoeui", 26, bold=True)
        self.fn_md = pygame.font.SysFont("segoeui", 18)
        self.fn_sm = pygame.font.SysFont("segoeui", 15)
        self.fn_xs = pygame.font.SysFont("segoeui", 12)

        self.state      = "menu"
        self.mode       = "Manual"
        self.algo       = "Backtracking"
        self.num_colors = 4
        self.use_mrv    = True
        self.use_degree = False
        self.use_lcv    = True

        self.screen_polys = build_screen_polys()
        self.centroids    = {n: centroid(p) for n, p in self.screen_polys.items()}

        self.assignment  = {}
        self.conflicts   = set()
        self.solved      = False
        self.lost        = False
        self.ai_steps    = []
        self.ai_idx      = 0
        self.ai_running  = False
        self.ai_speed    = 8.0
        self.ai_timer    = 0.0
        self.ai_hl       = None
        self.ai_status   = ""
        self.feedback_msg   = ""
        self.feedback_col   = TEXT
        self.feedback_timer = 0
        self.hovered     = None
        self.sel_color   = 0
        self.picker_open = False
        self.picker_tgt  = None
        self.menu_btns   = {}
        self.game_btns   = {}
        self.flash       = {}

    def reset(self):
        self.assignment  = {}
        self.conflicts   = set()
        self.solved      = False
        self.lost        = False
        self.ai_running  = False
        self.ai_steps    = []
        self.ai_idx      = 0
        self.ai_hl       = None
        self.ai_status   = ""
        self.picker_open = False
        self.picker_tgt  = None
        self.flash       = {}
        self.feedback_msg = ""

    # ── Conflict / win check ──
    def check_conflicts(self):
        self.conflicts = set()
        for country, nbs in ADJACENCY.items():
            if country in self.assignment:
                for nb in nbs:
                    if nb in self.assignment and self.assignment[nb] == self.assignment[country]:
                        self.conflicts.add(country)
                        self.conflicts.add(nb)
        if self.conflicts:
            self.lost = True
        if len(self.assignment) == len(COUNTRY_NAMES) and not self.conflicts:
            self.solved = True
            self.feedback_msg   = "✓ All 20 countries colored!"
            self.feedback_col   = SUCCESS
            self.feedback_timer = 400

    def assign_color(self, country, cidx):
        self.assignment[country] = cidx
        self.flash[country] = [lighten(PALETTE[cidx], 60), 20]
        self.check_conflicts()

    def country_at(self, mx, my):
        priority = ["Djibouti", "Uganda"]  # small countries first
        for name in priority:
            if name in self.screen_polys and point_in_poly(mx, my, self.screen_polys[name]):
                return name
        for name in COUNTRY_NAMES:
            if name not in priority and name in self.screen_polys:
                if point_in_poly(mx, my, self.screen_polys[name]):
                    return name
        return None

    def start_ai(self):
        solver = CSPSolver(COUNTRY_NAMES, ADJACENCY, self.num_colors)
        solver.use_mrv    = self.use_mrv
        solver.use_lcv    = self.use_lcv
        solver.use_degree = self.use_degree
        solver.solve(self.algo)
        self.ai_steps   = solver.steps
        self.ai_idx     = 0
        self.ai_running = True
        self.ai_timer   = 0.0

    def ai_step_once(self):
        if self.ai_idx >= len(self.ai_steps):
            self.ai_running = False
            self.check_conflicts()
            return
        asgn, reg, status = self.ai_steps[self.ai_idx]
        self.assignment = dict(asgn)
        self.ai_hl      = reg
        self.ai_status  = status
        if status == "backtrack" and reg:
            self.flash[reg] = [(255, 80, 80), 22]
        elif status == "assign" and reg:
            self.flash[reg] = [SUCCESS, 18]
        self.ai_idx += 1
        if self.ai_idx >= len(self.ai_steps):
            self.ai_running = False
            self.check_conflicts()

    def ai_tick(self, dt):
        if not self.ai_running: return
        self.ai_timer += dt
        interval = 1.0 / max(self.ai_speed, 0.5)
        while self.ai_timer >= interval and self.ai_running:
            self.ai_step_once()
            self.ai_timer -= interval

    # ═══════════════════════════════════════════
    #  DRAW MAP
    # ═══════════════════════════════════════════
    def draw_map(self, surf):
        # Ocean background with subtle gradient feel
        pygame.draw.rect(surf, MAP_OCEAN, MAP_RECT)
        # Very faint grid lines for geographic feel
        for lat in range(-5, 39, 5):
            y = project(0, lat)[1]
            if MAP_RECT.top <= y <= MAP_RECT.bottom:
                pygame.draw.line(surf, (20, 45, 80), (MAP_RECT.left, y), (MAP_RECT.right, y), 1)
        for lon in range(-20, 53, 10):
            x = project(lon, 0)[0]
            if MAP_RECT.left <= x <= MAP_RECT.right:
                pygame.draw.line(surf, (20, 45, 80), (x, MAP_RECT.top), (x, MAP_RECT.bottom), 1)

        mx, my = pygame.mouse.get_pos()
        self.hovered = self.country_at(mx, my) if mx < MAP_RECT.right else None

        for name in COUNTRY_NAMES:
            if name not in self.screen_polys: continue
            poly = self.screen_polys[name]
            if len(poly) < 3: continue

            cidx = self.assignment.get(name)
            base = PALETTE[cidx] if cidx is not None else (38, 52, 78)

            if name in self.conflicts:
                base = LOST_COL

            if name in self.flash:
                fc, ft = self.flash[name]
                t = ft / 25.0
                base = lerp(base, fc, t * 0.55)
                self.flash[name][1] -= 1
                if self.flash[name][1] <= 0:
                    del self.flash[name]

            if name == self.hovered and self.mode == "Manual":
                base = lighten(base, 45)
            if name == self.ai_hl:
                base = lighten(base, 60)

            pygame.draw.polygon(surf, base, poly)
            bc = (240, 220, 170) if name == self.hovered else MAP_BORDER
            bw = 2 if name == self.hovered else 1
            pygame.draw.polygon(surf, bc, poly, bw)

        # Country labels — full names where space allows
        for name in COUNTRY_NAMES:
            if name not in self.centroids: continue
            cx, cy = self.centroids[name]
            if not MAP_RECT.collidepoint(cx, cy): continue
            cidx = self.assignment.get(name)
            fg = WHITE if cidx is not None else TEXT_DIM

            # Abbreviations for small/crowded countries
            abbrev = {
                "Western Sahara": "W.Sahara",
                "South Sudan":    "S.Sudan",
                "Mauritania":     "Maurit.",
                "Cameroon":       "Camroon",
                "Djibouti":       "Djib.",
            }
            label = abbrev.get(name, name)

            lbl = self.fn_xs.render(label, True, fg)
            shd = self.fn_xs.render(label, True, (0, 0, 0))
            surf.blit(shd, shd.get_rect(center=(cx+1, cy+1)))
            surf.blit(lbl,  lbl.get_rect(center=(cx, cy)))

        if self.picker_open and self.picker_tgt:
            self.draw_picker(surf)

        # LOST overlay
        if self.lost:
            ov = pygame.Surface((MAP_RECT.width, MAP_RECT.height), pygame.SRCALPHA)
            ov.fill((180, 30, 30, 55))
            surf.blit(ov, MAP_RECT.topleft)
            t = self.fn_xl.render("You Lost!", True, (255, 60, 60))
            surf.blit(t, t.get_rect(center=MAP_RECT.center))

        # SOLVED overlay
        if self.solved:
            ov = pygame.Surface((MAP_RECT.width, MAP_RECT.height), pygame.SRCALPHA)
            ov.fill((20, 180, 80, 35))
            surf.blit(ov, MAP_RECT.topleft)

    def draw_picker(self, surf):
        cx, cy = self.centroids.get(self.picker_tgt, MAP_RECT.center)
        px = min(cx + 10, MAP_RECT.right - 180)
        py = max(min(cy - 25, H - 65), 10)
        r  = 12
        n  = self.num_colors
        bw = 16 + n * (r*2 + 6) + 8
        box = pygame.Rect(px, py, bw, 50)
        rr(surf, (14, 20, 38), box, 12, 1, BORDER)
        for i in range(n):
            bx = px + 12 + i*(r*2+6) + r
            by = py + 25
            pygame.draw.circle(surf, PALETTE[i], (bx, by), r)
            if i == self.sel_color:
                pygame.draw.circle(surf, WHITE, (bx, by), r+3, 2)
            num = self.fn_xs.render(str(i+1), True, TEXT_DIM)
            surf.blit(num, num.get_rect(center=(bx, by + r + 7)))

    # ═══════════════════════════════════════════
    #  DRAW PANEL (right sidebar)
    # ═══════════════════════════════════════════
    def draw_panel(self, surf):
        PX = MAP_RECT.right + 8
        PW = W - PX - 6
        panel = pygame.Rect(PX, 0, PW, H)
        pygame.draw.rect(surf, SIDEBAR, panel)
        pygame.draw.line(surf, BORDER, (PX, 0), (PX, H), 2)

        mx, my = pygame.mouse.get_pos()
        self.game_btns = {}
        y = 16

        # ── Header ──
        t1 = self.fn_lg.render("CSP Map Coloring", True, ACCENT)
        surf.blit(t1, t1.get_rect(centerx=PX+PW//2, y=y)); y += 28
        t2 = self.fn_xs.render("North & East Africa · 20 Countries", True, TEXT_DIM)
        surf.blit(t2, t2.get_rect(centerx=PX+PW//2, y=y)); y += 20
        pygame.draw.line(surf, BORDER, (PX+10, y), (W-10, y)); y += 10

        def info(label, val, vc=TEXT):
            nonlocal y
            l = self.fn_sm.render(label, True, TEXT_DIM)
            v = self.fn_sm.render(val,   True, vc)
            surf.blit(l, (PX+12, y))
            surf.blit(v, (PX+PW-v.get_width()-12, y))
            y += 20

        info("Mode",     self.mode)
        info("Algorithm", self.algo if self.mode == "AI" else "—", ACCENT)
        info("Colors",   str(self.num_colors))
        assigned = len(self.assignment)
        total    = len(COUNTRY_NAMES)
        info("Progress", f"{assigned}/{total}",
             WARN if assigned < total else SUCCESS)
        info("Conflicts", str(len(self.conflicts)),
             ACCENT2 if self.conflicts else SUCCESS)
        pygame.draw.line(surf, BORDER, (PX+10, y), (W-10, y)); y += 8

        # ── Color palette (Manual) ──
        if self.mode == "Manual":
            cl = self.fn_xs.render("Colors (click or 1–6):", True, TEXT_DIM)
            surf.blit(cl, (PX+12, y)); y += 18
            sp = min(30, (PW-20) // self.num_colors)
            for i in range(self.num_colors):
                cx2 = PX + 12 + i*sp + sp//2
                r2 = 10
                pygame.draw.circle(surf, PALETTE[i], (cx2, y+r2), r2)
                if i == self.sel_color:
                    pygame.draw.circle(surf, WHITE, (cx2, y+r2), r2+3, 2)
                n2 = self.fn_xs.render(str(i+1), True, TEXT_DIM)
                surf.blit(n2, n2.get_rect(center=(cx2, y+r2*2+8)))
            y += 42
            pygame.draw.line(surf, BORDER, (PX+10, y), (W-10, y)); y += 8

        # ── AI info ──
        if self.mode == "AI":
            heur_labels = []
            if self.use_mrv:    heur_labels.append("MRV")
            if self.use_degree: heur_labels.append("Degree")
            if self.use_lcv:    heur_labels.append("LCV")
            hstr = " + ".join(heur_labels) if heur_labels else "None"
            info("Heuristics", hstr, ACCENT)

            sc = SUCCESS if "done" in self.ai_status else \
                 ACCENT2 if "backtrack" in self.ai_status else ACCENT
            if self.ai_status:
                st = self.fn_xs.render(f"● {self.ai_status.capitalize()}", True, sc)
                surf.blit(st, (PX+12, y)); y += 16

            prog = self.ai_idx / max(len(self.ai_steps), 1)
            bar  = pygame.Rect(PX+12, y, PW-24, 6)
            pygame.draw.rect(surf, BORDER, bar, border_radius=3)
            fill = pygame.Rect(PX+12, y, int((PW-24)*prog), 6)
            pygame.draw.rect(surf, ACCENT, fill, border_radius=3)
            y += 10
            sp2 = self.fn_xs.render(f"{self.ai_idx}/{len(self.ai_steps)} steps", True, TEXT_DIM)
            surf.blit(sp2, (PX+12, y)); y += 16
            spd = self.fn_xs.render(f"Speed: {self.ai_speed:.0f}/s  [← →]", True, TEXT_DIM)
            surf.blit(spd, (PX+12, y)); y += 16
            pygame.draw.line(surf, BORDER, (PX+10, y), (W-10, y)); y += 8

        # ── Status ──
        if self.lost:
            t = self.fn_lg.render("You Lost!", True, ACCENT2)
            surf.blit(t, t.get_rect(centerx=PX+PW//2, y=y)); y += 30
            sub = self.fn_xs.render("Adjacent countries share a color!", True, TEXT_DIM)
            surf.blit(sub, sub.get_rect(centerx=PX+PW//2, y=y)); y += 18
            pygame.draw.line(surf, BORDER, (PX+10, y), (W-10, y)); y += 8
        elif self.solved:
            t = self.fn_lg.render("✓  SOLVED!", True, SUCCESS)
            surf.blit(t, t.get_rect(centerx=PX+PW//2, y=y)); y += 28
            pygame.draw.line(surf, BORDER, (PX+10, y), (W-10, y)); y += 8

        if self.feedback_msg and self.feedback_timer > 0:
            fm = self.fn_xs.render(self.feedback_msg, True, self.feedback_col)
            surf.blit(fm, fm.get_rect(centerx=PX+PW//2, y=y)); y += 16
            self.feedback_timer -= 1

        # ── Buttons with icons ──
        by = H - 310
        button_defs = []
        if self.mode == "AI":
            if not self.ai_running and self.ai_steps:
                button_defs.append(("  AI Step", "ai_step", "step"))
            if not self.ai_running:
                button_defs.append(("  Run AI", "run_ai", "play"))
            else:
                button_defs.append(("  Pause", "pause", "pause"))
        button_defs += [("  Reset", "reset", "reset"), ("  Menu", "menu", "menu")]

        for label, key, icon_kind in button_defs:
            r3 = pygame.Rect(PX+14, by, PW-28, 40)
            hov = r3.collidepoint(mx, my)
            self.game_btns[key] = r3
            is_active = key == "ai_step"

            # background
            if is_active:
                bg_c = PURPLE_BTN
            elif hov:
                bg_c = (40, 60, 90)
            else:
                bg_c = (20, 27, 45)
            border_c = (140, 100, 230) if is_active else BORDER
            rr(surf, bg_c, r3, 9, 1, border_c)

            # icon
            ic = WHITE if (hov or is_active) else TEXT_DIM
            draw_icon(surf, icon_kind, PX+14+22, by+20, 10, ic)

            # label
            tc = WHITE if (hov or is_active) else TEXT_DIM
            t3 = self.fn_md.render(label, True, tc)
            surf.blit(t3, t3.get_rect(midleft=(PX+14+36, by+20)))
            by += 48

        # ── Legend ──
        pygame.draw.line(surf, BORDER, (PX+10, H-55), (W-10, H-55))
        l1 = self.fn_xs.render("Click country → pick color", True, TEXT_DIM)
        surf.blit(l1, l1.get_rect(centerx=PX+PW//2, y=H-46))
        l2 = self.fn_xs.render("ESC → menu  |  Space → AI step", True, TEXT_DIM)
        surf.blit(l2, l2.get_rect(centerx=PX+PW//2, y=H-30))

    # ═══════════════════════════════════════════
    #  DRAW MENU
    # ═══════════════════════════════════════════
    def draw_menu(self, surf):
        surf.fill(BG)
        # Subtle dot-grid background
        for gx in range(0, W, 30):
            for gy in range(0, H, 30):
                pygame.draw.circle(surf, (18, 25, 40), (gx, gy), 1)

        mx, my = pygame.mouse.get_pos()
        self.menu_btns = {}

        # Title block
        title_rect = pygame.Rect(W//2 - 340, 22, 680, 80)
        rr(surf, (14, 20, 36), title_rect, 14, 1, BORDER)
        t = self.fn_xl.render("North & East Africa — CSP", True, TEXT)
        surf.blit(t, t.get_rect(centerx=W//2, y=32))
        s = self.fn_sm.render(
            "Backtracking  ·  Forward Checking  ·  MRV  ·  Degree  ·  LCV",
            True, ACCENT)
        surf.blit(s, s.get_rect(centerx=W//2, y=72))

        y = 120
        bw = 210; gap = 14

        def section(label):
            nonlocal y
            l = self.fn_sm.render(label, True, (130, 150, 180))
            surf.blit(l, l.get_rect(centerx=W//2, y=y)); y += 26

        def row(opts, current, group):
            nonlocal y
            total = len(opts)*(bw+gap)-gap
            sx = W//2 - total//2
            for i, opt in enumerate(opts):
                r4 = pygame.Rect(sx+i*(bw+gap), y, bw, 42)
                hov = r4.collidepoint(mx, my)
                active = (opt == current)
                # active = purple style
                if active:
                    bg_c = PURPLE_BTN
                    bc_c = (140, 100, 230)
                    tc = WHITE
                elif hov:
                    bg_c = (40, 60, 90)
                    bc_c = BORDER
                    tc = WHITE
                else:
                    bg_c = (20, 27, 45)
                    bc_c = BORDER
                    tc = TEXT_DIM
                rr(surf, bg_c, r4, 10, 1, bc_c)
                t4 = self.fn_md.render(opt, True, tc)
                surf.blit(t4, t4.get_rect(center=r4.center))
                self.menu_btns[f"{group}:{opt}"] = r4
            y += 60

        section("MODE")
        row(["Manual", "AI"], self.mode, "mode")

        if self.mode == "AI":
            section("ALGORITHM")
            row(["Backtracking", "Forward Checking"], self.algo, "algo")

            section("HEURISTICS")
            heur_list = [
                ("MRV (Min Remaining Values)",    "mrv",    self.use_mrv),
                ("Degree Heuristic",              "degree", self.use_degree),
                ("LCV (Least Constraining Value)","lcv",    self.use_lcv),
            ]
            total_w = 300
            sx3 = W//2 - total_w//2
            for hlabel, hkey, hval in heur_list:
                r5 = pygame.Rect(sx3, y, total_w, 36)
                hov = r5.collidepoint(mx, my)
                cb_bg = (30, 45, 70) if hov else (20, 27, 45)
                rr(surf, cb_bg, r5, 8, 1, BORDER)
                # Checkbox
                cb = pygame.Rect(sx3 + 12, y + 10, 16, 16)
                if hval:
                    pygame.draw.rect(surf, ACCENT, cb, border_radius=4)
                    ck = self.fn_sm.render("✓", True, (10, 13, 20))
                    surf.blit(ck, ck.get_rect(center=cb.center))
                else:
                    pygame.draw.rect(surf, BORDER, cb, 2, border_radius=4)
                hl = self.fn_sm.render(hlabel, True, TEXT if hval else TEXT_DIM)
                surf.blit(hl, (sx3 + 36, y + 9))
                self.menu_btns[f"heur:{hkey}"] = r5
                y += 44

        section("NUMBER OF COLORS")
        row([str(i) for i in range(3, 7)], str(self.num_colors), "colors")

        y += 4
        # Start button
        start = pygame.Rect(W//2-150, y, 300, 52)
        hov   = start.collidepoint(mx, my)
        sc    = (60, 220, 130) if hov else ACCENT
        rr(surf, sc, start, 14, 1, (80, 240, 150) if hov else (40, 160, 90))
        draw_icon(surf, "play", W//2 - 80, y+26, 12, (10, 13, 20))
        sl = self.fn_lg.render("Start Game", True, (10, 13, 20))
        surf.blit(sl, sl.get_rect(midleft=(W//2 - 60, y+26)))
        self.menu_btns["start"] = start
        y += 68

        # Info box
        box = pygame.Rect(W//2-330, y, 660, 72)
        rr(surf, (14, 20, 36), box, 12, 1, BORDER)
        infos = [
            ("Backtracking:",     "Classic recursive search — backtracks on conflict"),
            ("Forward Checking:", "Prunes neighbor domains after each assignment"),
        ]
        iy = y + 12
        for alg, desc in infos:
            a = self.fn_sm.render(alg, True, ACCENT)
            d = self.fn_xs.render(desc, True, TEXT_DIM)
            surf.blit(a, (box.x+18, iy))
            surf.blit(d, (box.x+200, iy + 2))
            iy += 26

        rule = self.fn_xs.render(
            "Rule: Same color on adjacent countries = You Lost!",
            True, ACCENT2)
        surf.blit(rule, rule.get_rect(centerx=W//2, y=y+82))

    # ═══════════════════════════════════════════
    #  MAIN LOOP
    # ═══════════════════════════════════════════
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if self.state == "menu":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for key, rect in self.menu_btns.items():
                            if rect.collidepoint(event.pos):
                                if key.startswith("mode:"):
                                    self.mode = key.split(":")[1]
                                elif key.startswith("algo:"):
                                    self.algo = key.split(":")[1]
                                elif key.startswith("colors:"):
                                    self.num_colors = int(key.split(":")[1])
                                elif key.startswith("heur:"):
                                    h = key.split(":")[1]
                                    if h == "mrv":    self.use_mrv    = not self.use_mrv
                                    elif h == "degree": self.use_degree = not self.use_degree
                                    elif h == "lcv":  self.use_lcv    = not self.use_lcv
                                elif key == "start":
                                    self.reset(); self.state = "game"

                elif self.state == "game":
                    if event.type == pygame.KEYDOWN:
                        for i in range(6):
                            if event.key == pygame.K_1+i and i < self.num_colors:
                                self.sel_color = i
                        if event.key == pygame.K_RIGHT:
                            self.ai_speed = min(30, self.ai_speed+1)
                        if event.key == pygame.K_LEFT:
                            self.ai_speed = max(1, self.ai_speed-1)
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                        if event.key == pygame.K_SPACE and self.mode == "AI":
                            if not self.ai_steps: self.start_ai(); self.ai_running = False
                            self.ai_step_once()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = event.pos
                        consumed = False

                        for key, rect in self.game_btns.items():
                            if rect.collidepoint(mx, my):
                                consumed = True
                                if key == "menu":    self.state = "menu"
                                elif key == "reset": self.reset()
                                elif key == "run_ai":
                                    if not self.ai_steps: self.start_ai()
                                    else: self.ai_running = True
                                elif key == "pause":
                                    self.ai_running = not self.ai_running
                                elif key == "ai_step":
                                    if not self.ai_steps: self.start_ai(); self.ai_running = False
                                    self.ai_step_once()
                                break

                        if not consumed and self.mode == "Manual" and mx < MAP_RECT.right:
                            if self.picker_open and self.picker_tgt:
                                cx2, cy2 = self.centroids.get(self.picker_tgt, (0, 0))
                                px2 = min(cx2+10, MAP_RECT.right-180)
                                py2 = max(min(cy2-25, H-65), 10)
                                picked = False
                                for i in range(self.num_colors):
                                    bx = px2 + 12 + i*(12*2+6) + 12
                                    by = py2 + 25
                                    if math.hypot(mx-bx, my-by) < 14:
                                        self.sel_color = i
                                        self.assign_color(self.picker_tgt, i)
                                        self.picker_open = False
                                        picked = True; break
                                if not picked:
                                    self.picker_open = False
                            else:
                                country = self.country_at(mx, my)
                                if country:
                                    if self.picker_tgt == country and self.picker_open:
                                        self.picker_open = False
                                    else:
                                        self.picker_tgt  = country
                                        self.picker_open = True

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        if self.mode == "Manual":
                            mx, my = event.pos
                            if mx < MAP_RECT.right:
                                c = self.country_at(mx, my)
                                if c: self.assign_color(c, self.sel_color)

            # DRAW
            if self.state == "menu":
                self.draw_menu(self.screen)
            else:
                self.screen.fill(BG)
                self.ai_tick(dt)
                self.draw_map(self.screen)
                self.draw_panel(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    NorthAfricaGame().run()