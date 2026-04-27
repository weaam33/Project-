
import time, sys
import pygame
from collections import deque

# ═══════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════

W, H       = 1400, 820
FPS        = 60
SIDEBAR_W  = 220
RIGHT_W    = 280
MAP_W      = W - SIDEBAR_W - RIGHT_W

BG         = ( 8, 11, 18)
PANEL      = (13, 17, 28)
PANEL2     = (17, 22, 36)
BORDER     = (25, 38, 62)
ACCENT     = ( 0,212,255)
ACCENT2    = (255, 77,105)
SUCCESS    = ( 0,230,118)
WARN       = (255,214,  0)
ORANGE     = (255,109,  0)
PURPLE     = (179,136,255)
TEXT       = (200,214,230)
DIM        = ( 74, 90,114)
WHITE      = (255,255,255)
OCEAN      = ( 10, 30, 65)
MAP_BORDER = (138,112, 64)
LOST_COL   = (220, 40, 50)

PALETTE = [
    (232, 75, 65),   # 0  Red
    ( 55,224, 90),   # 1  Green
    (255,214, 45),   # 2  Yellow
    (179,136,255),   # 3  Purple
    (  0,212,255),   # 4  Cyan
    (255,109,  0),   # 5  Orange
]
COLOR_NAMES = ["Red", "Green", "Yellow", "Purple", "Cyan", "Orange"]

COUNTRY_POLYS = {
    "Morocco":        [(-5.9,35.9),(-1.7,35.8),(-1.1,34.9),(-1.7,34.0),(-2.2,32.0),(-3.0,30.9),(-3.0,29.5),(-8.7,27.7),(-8.7,28.7),(-13.2,27.7),(-13.2,28.0),(-8.0,31.7),(-5.9,33.9)],
    "Algeria":        [(-1.7,35.8),(8.6,37.2),(8.6,36.9),(9.5,37.4),(9.5,33.0),(8.0,32.5),(5.0,31.6),(3.0,31.8),(1.2,31.1),(9.5,31.1),(9.5,22.5),(-3.2,22.5),(-3.2,19.0),(-5.5,19.0),(-5.5,21.3),(-8.7,27.7),(-3.0,29.5),(-3.0,30.9),(-2.2,32.0),(-1.7,34.0),(-1.1,34.9)],
    "Tunisia":        [(8.6,37.2),(10.6,37.5),(11.5,33.1),(10.0,30.5),(9.5,33.0),(8.6,36.9)],
    "Libya":          [(9.5,37.4),(10.6,37.5),(11.5,33.1),(13.0,32.9),(20.0,31.9),(25.0,31.6),(25.0,22.5),(15.2,22.5),(9.5,22.5),(9.5,31.1),(10.0,30.5)],
    "Egypt":          [(25.0,22.5),(36.9,22.0),(34.8,29.5),(34.2,31.2),(32.3,31.1),(31.5,30.0),(29.2,30.9),(25.0,31.6)],
    "Western Sahara": [(-13.2,27.7),(-8.7,27.7),(-5.5,21.3),(-5.5,19.0),(-17.0,20.8),(-17.0,21.3),(-13.0,22.9)],
    "Mauritania":     [(-17.0,20.8),(-5.5,19.0),(-5.5,15.5),(-12.3,14.7),(-16.5,16.1),(-16.9,20.1)],
    "Mali":           [(-5.5,19.0),(-3.2,19.0),(-3.2,22.5),(1.2,22.5),(1.2,15.0),(2.0,15.3),(4.2,19.1),(4.2,16.0),(2.5,11.5),(-0.5,11.1),(-3.3,11.9),(-5.5,10.3),(-5.5,15.5)],
    "Niger":          [(9.5,22.5),(15.2,22.5),(14.4,15.5),(13.6,13.3),(13.0,13.5),(12.4,13.1),(11.4,13.5),(7.5,13.7),(5.0,13.5),(4.2,16.0),(4.2,19.1),(2.0,15.3),(1.2,15.0),(1.2,22.5)],
    "Chad":           [(15.2,22.5),(25.0,22.5),(24.0,19.5),(24.0,10.0),(22.0,10.0),(20.5,9.0),(18.5,9.0),(16.0,7.5),(15.5,11.0),(14.0,13.0),(13.6,13.3),(14.4,15.5)],
    "Sudan":          [(25.0,22.5),(36.9,22.0),(37.0,18.0),(36.5,14.5),(34.0,11.0),(32.0,11.5),(29.5,10.0),(27.5,10.5),(25.5,10.5),(24.0,10.0),(24.0,19.5)],
    "South Sudan":    [(24.0,10.0),(25.5,10.5),(27.5,10.5),(29.5,10.0),(32.0,11.5),(34.0,11.0),(33.0,9.5),(33.5,8.5),(36.0,6.0),(36.0,4.5),(35.3,5.0),(34.1,0.4),(29.7,-1.0),(28.0,1.5),(27.0,3.5),(25.0,5.0),(23.5,7.5),(22.5,6.5),(20.5,9.0),(22.0,10.0)],
    "Eritrea":        [(36.9,22.0),(43.1,12.7),(42.0,10.9),(40.0,12.4),(38.5,15.0),(37.0,18.0)],
    "Djibouti":       [(43.1,12.7),(43.5,11.5),(42.3,11.0),(42.0,10.9)],
    "Ethiopia":       [(37.0,18.0),(38.5,15.0),(40.0,12.4),(42.0,10.9),(43.5,11.5),(44.0,11.0),(44.5,10.0),(42.7,6.7),(39.8,3.5),(34.1,0.4),(33.9,4.0),(35.3,5.0),(36.0,4.5),(36.0,6.0),(33.5,8.5),(33.0,9.5),(34.0,11.0),(36.5,14.5)],
    "Somalia":        [(43.5,11.5),(43.1,12.7),(50.0,11.5),(51.4,10.0),(44.0,11.0),(44.5,10.0),(42.7,6.7),(41.5,1.7),(41.0,-1.7),(41.8,-1.7),(49.0,11.0)],
    "Uganda":         [(34.1,0.4),(33.9,4.0),(31.5,4.0),(30.0,2.0),(29.7,-1.0)],
    "Kenya":          [(34.1,0.4),(29.7,-1.0),(34.0,-3.0),(37.5,-4.5),(40.5,-2.0),(41.0,-1.7),(41.5,1.7),(40.0,4.5),(38.5,3.5),(36.0,4.5),(35.3,5.0)],
    "Nigeria":        [(2.5,11.5),(2.5,12.5),(7.5,13.7),(5.0,13.5),(13.0,13.5),(14.0,13.0),(12.0,8.0),(8.5,4.5),(5.0,4.3),(3.9,6.5),(3.9,9.0),(3.9,12.4),(1.7,11.0),(0.5,11.0),(-0.5,11.1)],
    "Cameroon":       [(14.0,13.0),(15.5,11.0),(16.0,7.5),(15.0,4.5),(14.5,2.2),(13.3,2.2),(12.0,2.8),(11.0,2.2),(9.8,3.7),(9.0,3.9),(8.5,4.5),(12.0,8.0),(14.0,13.0)],
}

ADJACENCY = {
    "Morocco":        ["Algeria","Western Sahara"],
    "Algeria":        ["Morocco","Tunisia","Libya","Niger","Mali","Mauritania","Western Sahara"],
    "Tunisia":        ["Algeria","Libya"],
    "Libya":          ["Tunisia","Algeria","Niger","Chad","Sudan","Egypt"],
    "Egypt":          ["Libya","Sudan"],
    "Western Sahara": ["Morocco","Algeria","Mauritania"],
    "Mauritania":     ["Western Sahara","Algeria","Mali"],
    "Mali":           ["Algeria","Mauritania","Niger"],
    "Niger":          ["Algeria","Libya","Chad","Nigeria","Mali"],
    "Chad":           ["Libya","Niger","Nigeria","Cameroon","Sudan","South Sudan"],
    "Sudan":          ["Egypt","Libya","Chad","South Sudan","Ethiopia","Eritrea"],
    "South Sudan":    ["Sudan","Chad","Ethiopia","Uganda"],
    "Eritrea":        ["Sudan","Ethiopia","Djibouti"],
    "Djibouti":       ["Eritrea","Ethiopia","Somalia"],
    "Ethiopia":       ["Eritrea","Djibouti","Somalia","Kenya","South Sudan","Sudan"],
    "Somalia":        ["Djibouti","Ethiopia","Kenya"],
    "Uganda":         ["South Sudan","Kenya"],
    "Kenya":          ["Ethiopia","Somalia","Uganda"],
    "Nigeria":        ["Niger","Chad","Cameroon"],
    "Cameroon":       ["Nigeria","Chad"],
}

COUNTRY_NAMES = list(COUNTRY_POLYS.keys())

LON_MIN, LON_MAX = -18.0, 52.0
LAT_MIN, LAT_MAX =  -5.0, 38.5

ABBREV = {
    "Western Sahara": "W.Sahara",
    "South Sudan":    "S.Sudan",
    "Mauritania":     "Maurit.",
    "Cameroon":       "Camroon",
    "Djibouti":       "Djib.",
}


# ═══════════════════════════════════════════════════════════════════
#  MAP UTILS
# ═══════════════════════════════════════════════════════════════════

MAP_RECT = pygame.Rect(SIDEBAR_W, 0, MAP_W, H)


def project(lon, lat):
    x = MAP_RECT.x + (lon - LON_MIN) / (LON_MAX - LON_MIN) * MAP_RECT.width
    y = MAP_RECT.y + MAP_RECT.height - (lat - LAT_MIN) / (LAT_MAX - LAT_MIN) * MAP_RECT.height
    return int(x), int(y)


def build_screen_polys():
    return {
        name: [project(lon, lat) for lon, lat in pts]
        for name, pts in COUNTRY_POLYS.items()
    }


def centroid(pts):
    return (
        int(sum(p[0] for p in pts) / len(pts)),
        int(sum(p[1] for p in pts) / len(pts)),
    )


def point_in_poly(px, py, pts):
    n = len(pts)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi):
            inside = not inside
        j = i
    return inside


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def lighten(col, amt=40):
    return tuple(min(255, c + amt) for c in col)


def rr(surf, col, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, col, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)


def label_box(surf, font, text, col, x, y):
    t = font.render(text, True, col)
    surf.blit(t, (x, y))
    return t.get_width()


# ═══════════════════════════════════════════════════════════════════
#  ALGORITHMS  (CSP Solver)
# ═══════════════════════════════════════════════════════════════════

class CSPSolver:
    """Constraint Satisfaction Problem solver for map colouring."""

    def __init__(self, regions, adj, nc):
        self.regions = regions
        self.adj     = adj
        self.nc      = nc
        self.steps   = []
        self.use_mrv = True
        self.use_lcv = False
        self.live_domains = {}

    def neighbors(self, r):
        return self.adj.get(r, [])

    def consistent(self, r, color, assignment):
        return all(assignment.get(nb) != color for nb in self.neighbors(r))

    def select_var(self, assignment, domains):
        unassigned = [r for r in self.regions if r not in assignment]
        if self.use_mrv:
            min_domain = min(len(domains[r]) for r in unassigned)
            unassigned = [r for r in unassigned if len(domains[r]) == min_domain]
        return unassigned[0]

    def order_values(self, r, assignment, domains):
        if self.use_lcv:
            return sorted(
                domains[r],
                key=lambda c: sum(
                    1 for nb in self.neighbors(r)
                    if nb not in assignment and c in domains.get(nb, [])
                )
            )
        return list(domains[r])

    def ac3(self, domains):
        queue = deque(
            (r, nb)
            for r  in self.regions
            for nb in self.neighbors(r)
        )
        domains = {k: list(v) for k, v in domains.items()}
        while queue:
            xi, xj = queue.popleft()
            if self._revise(domains, xi, xj):
                if not domains[xi]:
                    return False, domains
                for xk in self.neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True, domains

    def _revise(self, domains, xi, xj):
        revised = False
        for c in list(domains[xi]):
            has_support = any(cj != c for cj in domains[xj])
            if not has_support:
                domains[xi].remove(c)
                self.steps.append(({}, xi, f"ac3_prune:{c}"))
                revised = True
        return revised

    def _forward_check(self, r, color, domains):
        nd = {k: list(v) for k, v in domains.items()}
        for nb in self.neighbors(r):
            if color in nd[nb]:
                nd[nb].remove(color)
                self.steps.append(({}, nb, "domain_update"))
                if not nd[nb]:
                    return False, nd
        return True, nd

    def _bt(self, assignment, domains, alg):
        if len(assignment) == len(self.regions):
            self.steps.append((dict(assignment), None, "done"))
            return assignment

        r = self.select_var(assignment, domains)

        for color in self.order_values(r, assignment, domains):
            if self.consistent(r, color, assignment):
                assignment[r] = color
                self.steps.append((dict(assignment), r, "assign"))

                ok = True
                nd = {k: list(v) for k, v in domains.items()}

                if alg == "Forward Checking":
                    ok, nd = self._forward_check(r, color, nd)
                elif alg == "AC3":
                    ok, nd = self._forward_check(r, color, nd)
                    if ok:
                        ok, nd = self.ac3(nd)

                self.live_domains = {k: list(v) for k, v in nd.items()}

                if ok:
                    result = self._bt(assignment, nd, alg)
                    if result is not None:
                        return result

                self.steps.append((dict(assignment), r, "backtrack"))
                del assignment[r]

        return None

    def solve(self, algorithm="Backtracking"):
        self.steps = []
        domains = {r: list(range(self.nc)) for r in self.regions}
        self.live_domains = {k: list(v) for k, v in domains.items()}

        if algorithm == "AC3":
            ok, domains = self.ac3(domains)
            self.live_domains = {k: list(v) for k, v in domains.items()}
            if not ok:
                self.steps.append(({}, None, "done"))
                return None
            if all(len(domains[r]) == 1 for r in self.regions):
                asgn = {r: domains[r][0] for r in self.regions}
                self.steps.append((asgn, None, "done"))
                return asgn
            return self._bt({}, domains, "AC3")

        return self._bt({}, domains, algorithm)


# ═══════════════════════════════════════════════════════════════════
#  UI  (draw functions)
# ═══════════════════════════════════════════════════════════════════

def draw_map(app, surf):
    pygame.draw.rect(surf, OCEAN, MAP_RECT)

    for lat in range(-5, 39, 5):
        y = app.map_project(0, lat)[1]
        if MAP_RECT.top <= y <= MAP_RECT.bottom:
            pygame.draw.line(surf, (15, 45, 85), (MAP_RECT.left, y), (MAP_RECT.right, y))
    for lon in range(-20, 55, 10):
        x = app.map_project(lon, 0)[0]
        if MAP_RECT.left <= x <= MAP_RECT.right:
            pygame.draw.line(surf, (15, 45, 85), (x, MAP_RECT.top), (x, MAP_RECT.bottom))

    for name in COUNTRY_NAMES:
        poly = app.screen_polys.get(name)
        if not poly or len(poly) < 3:
            continue
        cidx = app.assignment.get(name)
        base = PALETTE[cidx] if cidx is not None else (30, 46, 72)
        if name in app.conflicts:
            base = LOST_COL
        if name in app.flash:
            fc, ft = app.flash[name]
            base = lerp(base, fc, ft / 25 * 0.55)
            app.flash[name][1] -= 1
            if app.flash[name][1] <= 0:
                del app.flash[name]
        if name == app.hovered:
            base = lighten(base, 40)
        if name == app.ai_hl:
            base = lighten(base, 55)
        if app.manual_mode and name == app.selected_country:
            base = lighten(base, 70)
        pygame.draw.polygon(surf, base, poly)
        bc = (240, 220, 160) if name == app.hovered else MAP_BORDER
        bw = 2               if name == app.hovered else 1
        pygame.draw.polygon(surf, bc, poly, bw)

    for name in COUNTRY_NAMES:
        if name not in app.centroids:
            continue
        cx, cy = app.centroids[name]
        if not MAP_RECT.collidepoint(cx, cy):
            continue
        lbl = ABBREV.get(name, name)
        fg  = WHITE if app.assignment.get(name) is not None else DIM
        shd = app.f_map.render(lbl, True, (0, 0, 0))
        txt = app.f_map.render(lbl, True, fg)
        surf.blit(shd, shd.get_rect(center=(cx + 1, cy + 1)))
        surf.blit(txt, txt.get_rect(center=(cx, cy)))

    if app.solved or app.won:
        ov = pygame.Surface((MAP_RECT.width, MAP_RECT.height), pygame.SRCALPHA)
        ov.fill((0, 200, 80, 30))
        surf.blit(ov, MAP_RECT.topleft)
        f_big = pygame.font.SysFont("consolas", 72, bold=True)
        cx2, cy2 = MAP_RECT.centerx, MAP_RECT.centery
        ws = f_big.render("YOU WIN!", True, (0, 0, 0))
        wt = f_big.render("YOU WIN!", True, SUCCESS)
        surf.blit(ws, ws.get_rect(center=(cx2 + 3, cy2 + 3)))
        surf.blit(wt, wt.get_rect(center=(cx2, cy2)))

    if app.lost:
        ov = pygame.Surface((MAP_RECT.width, MAP_RECT.height), pygame.SRCALPHA)
        ov.fill((180, 0, 0, 60))
        surf.blit(ov, MAP_RECT.topleft)
        f_big = pygame.font.SysFont("consolas", 72, bold=True)
        cx2, cy2 = MAP_RECT.centerx, MAP_RECT.centery
        ls = f_big.render("YOU LOST!", True, (0, 0, 0))
        lt = f_big.render("YOU LOST!", True, LOST_COL)
        surf.blit(ls, ls.get_rect(center=(cx2 + 3, cy2 + 3)))
        surf.blit(lt, lt.get_rect(center=(cx2, cy2)))
        sub  = pygame.font.SysFont("consolas", 22).render(
            "Two adjacent countries have the same color!", True, (255, 140, 140))
        hint = pygame.font.SysFont("consolas", 16).render(
            "Press R or click Reset to try again", True, DIM)
        surf.blit(sub,  sub.get_rect(center=(cx2, cy2 + 56)))
        surf.blit(hint, hint.get_rect(center=(cx2, cy2 + 86)))

    if app.manual_mode and app.selected_country and not app.lost and not app.won:
        _draw_color_picker(app, surf)


def _draw_color_picker(app, surf):
    app.color_picker_rects = {}
    cx, cy = app.centroids.get(
        app.selected_country, (MAP_RECT.centerx, MAP_RECT.centery))
    sw = app.num_colors * 36 + 20
    sh = 64
    px = max(MAP_RECT.x + 4, min(cx - sw // 2, MAP_RECT.right - sw - 4))
    py = cy - sh - 10
    if py < MAP_RECT.y + 4:
        py = cy + 20
    box = pygame.Rect(px, py, sw, sh)
    pygame.draw.rect(surf, (20, 28, 46), box, border_radius=8)
    pygame.draw.rect(surf, ACCENT,       box, 2, border_radius=8)
    f   = pygame.font.SysFont("consolas", 11, bold=True)
    nt  = f.render(f"Color: {app.selected_country[:14]}", True, WHITE)
    surf.blit(nt, nt.get_rect(centerx=box.centerx, y=box.y + 6))
    for i in range(app.num_colors):
        bx = px + 10 + i * 36
        by = py + 26
        r  = pygame.Rect(bx, by, 30, 30)
        app.color_picker_rects[i] = r
        pygame.draw.circle(surf, PALETTE[i], r.center, 14)
        if app.assignment.get(app.selected_country) == i:
            pygame.draw.circle(surf, WHITE, r.center, 14, 3)
        else:
            pygame.draw.circle(surf, (0, 0, 0), r.center, 14, 1)


def draw_left(app, surf):
    mx, my = pygame.mouse.get_pos()
    app.left_btns = {}

    panel = pygame.Rect(0, 0, SIDEBAR_W, H)
    pygame.draw.rect(surf, PANEL, panel)
    pygame.draw.line(surf, BORDER, (SIDEBAR_W, 0), (SIDEBAR_W, H), 1)

    top = pygame.Rect(0, 0, SIDEBAR_W, 40)
    pygame.draw.rect(surf, (10, 14, 24), top)
    pygame.draw.line(surf, BORDER, (0, 40), (SIDEBAR_W, 40))
    logo1 = app.f_lg.render("MAP",   True, ACCENT)
    logo2 = app.f_lg.render("COLOR", True, WHITE)
    logo3 = app.f_lg.render(" CSP",  True, ACCENT2)
    surf.blit(logo1, (10, 12))
    surf.blit(logo2, (10 + logo1.get_width(), 12))
    surf.blit(logo3, (10 + logo1.get_width() + logo2.get_width(), 12))
    y = 52

    def sec(label):
        nonlocal y
        t = app.f_xs.render(label, True, DIM)
        surf.blit(t, (12, y))
        y += t.get_height() + 4

    # Algorithm selector
    sec("ALGORITHM")
    for alg in ["Backtracking", "Forward Checking", "AC3"]:
        r      = pygame.Rect(10, y, SIDEBAR_W - 20, 28)
        hov    = r.collidepoint(mx, my)
        active = app.algo == alg
        bg = ACCENT       if active else ((35, 55, 88) if hov else PANEL2)
        tc = (10, 14, 24) if active else (WHITE        if hov else DIM)
        rr(surf, bg, r, 4, 1, ACCENT if active else BORDER)
        t = app.f_md.render(alg, True, tc)
        surf.blit(t, (r.x + 8, r.y + (r.height - t.get_height()) // 2))
        app.left_btns[f"algo:{alg}"] = r
        y += 32
    y += 6

    # Heuristic checkboxes
    sec("HEURISTICS")
    heurs = [("MRV", "mrv", app.use_mrv), ("LCV", "lcv", app.use_lcv)]
    for hlbl, hkey, hval in heurs:
        r   = pygame.Rect(10, y, SIDEBAR_W - 20, 24)
        hov = r.collidepoint(mx, my)
        rr(surf, (25, 38, 62) if hov else PANEL2, r, 4, 1, BORDER)
        cb = pygame.Rect(r.x + 6, r.y + 6, 12, 12)
        if hval:
            pygame.draw.rect(surf, ACCENT, cb, border_radius=3)
            ck = app.f_xs.render("v", True, (0, 0, 0))
            surf.blit(ck, ck.get_rect(center=cb.center))
        else:
            pygame.draw.rect(surf, BORDER, cb, 1, border_radius=3)
        ht = app.f_md.render(hlbl, True, TEXT if hval else DIM)
        surf.blit(ht, (r.x + 24, r.y + (r.height - ht.get_height()) // 2))
        app.left_btns[f"heur:{hkey}"] = r
        y += 28
    y += 6

    # Speed slider
    sec("VISUALIZATION SPEED")
    tx, ty, tw = 12, y, SIDEBAR_W - 24
    pygame.draw.rect(surf, BORDER, pygame.Rect(tx, ty + 5, tw, 4), border_radius=2)
    frac = (app.speed - 1) / 29
    pygame.draw.rect(surf, ACCENT, pygame.Rect(tx, ty + 5, int(tw * frac), 4), border_radius=2)
    knob_x = tx + int(tw * frac)
    pygame.draw.circle(surf, ACCENT, (knob_x, ty + 7), 6)
    pygame.draw.circle(surf, WHITE,  (knob_x, ty + 7), 4)
    app.left_btns["speed_track"] = pygame.Rect(tx, ty, tw, 14)
    sl = app.f_xs.render(f"{int(app.speed)} steps/s", True, DIM)
    surf.blit(sl, (SIDEBAR_W // 2 - sl.get_width() // 2, ty + 14))
    y += 32
    y += 6

    # Number of colours
    sec("NUMBER OF COLORS")
    for i, nc in enumerate([3, 4, 5, 6]):
        bw2 = (SIDEBAR_W - 20 - 18) // 4
        r   = pygame.Rect(10 + i * (bw2 + 6), y, bw2, 26)
        active = app.num_colors == nc
        hov    = r.collidepoint(mx, my)
        bg = ACCENT       if active else (PANEL2 if not hov else (35, 55, 88))
        tc = (10, 14, 24) if active else (WHITE  if hov     else DIM)
        rr(surf, bg, r, 4, 1, ACCENT if active else BORDER)
        nt = app.f_md.render(str(nc), True, tc)
        surf.blit(nt, nt.get_rect(center=r.center))
        app.left_btns[f"nc:{nc}"] = r
    y += 32
    y += 10

    # SOLVE button
    sr  = pygame.Rect(10, y, SIDEBAR_W - 20, 36)
    hov = sr.collidepoint(mx, my)
    rr(surf, lighten(ACCENT, 30) if hov else ACCENT, sr, 6)
    st = app.f_lg.render("▶  SOLVE", True, (0, 0, 0))
    surf.blit(st, st.get_rect(center=sr.center))
    app.left_btns["solve"] = sr
    y += 44

    # RESET button
    rr2 = pygame.Rect(10, y, SIDEBAR_W - 20, 30)
    hov = rr2.collidepoint(mx, my)
    rr(surf, (25, 38, 62) if hov else PANEL2, rr2, 6, 1, ACCENT2 if hov else BORDER)
    rt = app.f_md.render("↺  Reset", True, ACCENT2 if hov else DIM)
    surf.blit(rt, rt.get_rect(center=rr2.center))
    app.left_btns["reset"] = rr2
    y += 40
    y += 6

    # Manual play toggle
    mr  = pygame.Rect(10, y, SIDEBAR_W - 20, 28)
    hov = mr.collidepoint(mx, my)
    mbg = PURPLE if app.manual_mode else (PANEL2 if not hov else (35, 55, 88))
    mtc = (10, 14, 24) if app.manual_mode else (WHITE if hov else DIM)
    rr(surf, mbg, mr, 6, 1, PURPLE if app.manual_mode else BORDER)
    lbl = "Manual  ON" if app.manual_mode else "Manual Play"
    ml  = app.f_md.render(lbl, True, mtc)
    surf.blit(ml, ml.get_rect(center=mr.center))
    app.left_btns["manual"] = mr
    y += 36
    y += 6

    # Colour legend
    sec("COLOR LEGEND")
    for i in range(app.num_colors):
        pygame.draw.circle(surf, PALETTE[i], (20, y + 7), 6)
        ct = app.f_sm.render(COLOR_NAMES[i], True, DIM)
        surf.blit(ct, (32, y + 1))
        y += 18


def draw_right(app, surf):
    mx, my = pygame.mouse.get_pos()
    app.right_btns = {}
    rx = SIDEBAR_W + MAP_W

    panel = pygame.Rect(rx, 0, RIGHT_W, H)
    pygame.draw.rect(surf, PANEL, panel)
    pygame.draw.line(surf, BORDER, (rx, 0), (rx, H), 1)

    top = pygame.Rect(rx, 0, RIGHT_W, 40)
    pygame.draw.rect(surf, (10, 14, 24), top)
    pygame.draw.line(surf, BORDER, (rx, 40), (rx + RIGHT_W, 40))
    sub = f"N&E Africa · 20 Regions · {app.num_colors} Colors"
    st  = app.f_sm.render(sub, True, DIM)
    surf.blit(st, (rx + RIGHT_W // 2 - st.get_width() // 2, 13))
    y = 52

    def sec(label):
        nonlocal y
        t = app.f_xs.render(label, True, DIM)
        surf.blit(t, (rx + 10, y))
        y += t.get_height() + 5

    # Stats grid
    sw2   = (RIGHT_W - 30) // 2
    stats = [
        ("STEPS",      str(app.stats["steps"]),      ACCENT),
        ("BACKTRACKS", str(app.stats["backtracks"]), ACCENT2),
        ("PRUNED",     str(app.stats["pruned"]),     WARN),
        ("MS",         str(app.stats["ms"]),         PURPLE),
    ]
    for i, (k, v, vc) in enumerate(stats):
        col  = i % 2
        row2 = i // 2
        bx   = rx + 10 + col * (sw2 + 10)
        by   = y + row2 * 64
        box  = pygame.Rect(bx, by, sw2, 56)
        rr(surf, PANEL2, box, 6, 1, BORDER)
        vt = pygame.font.SysFont("consolas", 24, bold=True).render(v, True, vc)
        kt = app.f_xs.render(k, True, DIM)
        surf.blit(vt, vt.get_rect(centerx=box.centerx, y=box.y + 8))
        surf.blit(kt, kt.get_rect(centerx=box.centerx, y=box.y + 36))
    y += 138

    # Progress bar
    sec("PROGRESS")
    assigned = len(app.assignment)
    total    = len(COUNTRY_NAMES)
    pygame.draw.rect(surf, BORDER, pygame.Rect(rx + 10, y, RIGHT_W - 20, 5), border_radius=3)
    fw = int((RIGHT_W - 20) * (assigned / total))
    if fw > 0:
        pygame.draw.rect(surf, ACCENT, pygame.Rect(rx + 10, y, fw, 5), border_radius=3)
    y += 9
    pt = app.f_xs.render(f"{assigned} / {total} assigned", True, DIM)
    surf.blit(pt, (rx + 10, y))
    y += 16

    if app.ai_steps:
        prog = app.ai_idx / max(len(app.ai_steps), 1)
        pygame.draw.rect(surf, BORDER, pygame.Rect(rx + 10, y, RIGHT_W - 20, 3), border_radius=2)
        fw2 = int((RIGHT_W - 20) * prog)
        if fw2 > 0:
            pygame.draw.rect(surf, PURPLE, pygame.Rect(rx + 10, y, fw2, 3), border_radius=2)
        y += 7
        at = app.f_xs.render(
            f"{app.ai_idx}/{len(app.ai_steps)} steps  Speed:{app.speed:.0f}/s [<>]", True, DIM)
        surf.blit(at, (rx + 10, y))
        y += 14

    if app.ai_status:
        sc = (SUCCESS if "done"      in app.ai_status else
              ACCENT2 if "backtrack" in app.ai_status else
              WARN    if "ac3"       in app.ai_status else
              ORANGE  if "cutoff"    in app.ai_status else ACCENT)
        st2 = app.f_sm.render(f"* {app.ai_status.upper()}", True, sc)
        surf.blit(st2, (rx + 10, y))
        y += 16

    y += 4
    pygame.draw.line(surf, BORDER, (rx + 6, y), (rx + RIGHT_W - 6, y))
    y += 8

    # Domain sizes
    sec("DOMAIN SIZES")
    show_names = COUNTRY_NAMES[:10]
    for name in show_names:
        abbr = (name[:4]).upper()
        at   = app.f_xs.render(abbr, True, DIM)
        surf.blit(at, (rx + 10, y))
        current_domain = app.live_domains.get(name, list(range(app.num_colors)))
        for ci in range(app.num_colors):
            dx = rx + 52 + ci * 13
            if ci in current_domain:
                pygame.draw.circle(surf, PALETTE[ci], (dx, y + 5), 5)
            else:
                pygame.draw.circle(surf, (30, 40, 60), (dx, y + 5), 5)
                pygame.draw.line(surf, (80, 80, 80), (dx - 3, y + 2), (dx + 3, y + 8), 1)
                pygame.draw.line(surf, (80, 80, 80), (dx + 3, y + 2), (dx - 3, y + 8), 1)
        y += 13
    y += 4
    pygame.draw.line(surf, BORDER, (rx + 6, y), (rx + RIGHT_W - 6, y))
    y += 8

    # Step log
    sec("STEP LOG")
    log_area = pygame.Rect(rx + 6, y, RIGHT_W - 12, H - y - 8)
    pygame.draw.rect(surf, (10, 14, 22), log_area, border_radius=4)
    pygame.draw.rect(surf, BORDER,       log_area, 1, border_radius=4)
    ly = y + 4
    for text, col in app.log:
        if ly + 12 > H - 10:
            break
        pygame.draw.rect(surf, col, pygame.Rect(rx + 8, ly, 2, 10), border_radius=1)
        lt = app.f_xs.render(text[:34], True, col)
        surf.blit(lt, (rx + 14, ly))
        ly += 13


def draw_topbar(app, surf):
    pygame.draw.line(surf, BORDER, (SIDEBAR_W, 0), (SIDEBAR_W + MAP_W, 0))
    sub = f"North & East Africa  ·  20 Regions  ·  {app.num_colors} Colors"
    st  = app.f_sm.render(sub, True, DIM)
    surf.blit(st, (SIDEBAR_W + MAP_W // 2 - st.get_width() // 2, 14))


# ═══════════════════════════════════════════════════════════════════
#  APP  (main class + game loop)
# ═══════════════════════════════════════════════════════════════════

class App:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("MapColor CSP  —  North & East Africa")
        self.clock  = pygame.time.Clock()

        self.f_title = pygame.font.SysFont("consolas", 15, bold=True)
        self.f_lg    = pygame.font.SysFont("consolas", 13, bold=True)
        self.f_md    = pygame.font.SysFont("consolas", 12)
        self.f_sm    = pygame.font.SysFont("consolas", 11)
        self.f_xs    = pygame.font.SysFont("consolas", 10)
        self.f_map   = pygame.font.SysFont("consolas",  9)

        self.screen_polys = build_screen_polys()
        self.centroids    = {n: centroid(p) for n, p in self.screen_polys.items()}

        self.algo       = "Backtracking"
        self.num_colors = 4
        self.use_mrv    = True
        self.use_lcv    = False
        self.speed      = 8.0

        self.left_btns  = {}
        self.right_btns = {}

        self._init_state()

    def _init_state(self):
        self.assignment   = {}
        self.conflicts    = set()
        self.solved       = False
        self.live_domains = {r: list(range(self.num_colors)) for r in COUNTRY_NAMES}

        self.ai_steps   = []
        self.ai_idx     = 0
        self.ai_running = False
        self.ai_timer   = 0.0
        self.ai_hl      = None
        self.ai_status  = ""

        self.flash   = {}
        self.hovered = None
        self.log     = []
        self.stats   = dict(steps=0, backtracks=0, pruned=0, ms=0)

        self.manual_mode      = getattr(self, "manual_mode", False)
        self.selected_country = None
        self.lost             = False
        self.won              = False
        self.color_picker_rects = {}

    def reset(self):
        self._init_state()
        self.live_domains = {r: list(range(self.num_colors)) for r in COUNTRY_NAMES}

    def map_project(self, lon, lat):
        return project(lon, lat)

    # ── AI solve ─────────────────────────────────────────────────────────────

    def start_solve(self):
        self.reset()
        t0     = time.time()
        solver = CSPSolver(COUNTRY_NAMES, ADJACENCY, self.num_colors)
        solver.use_mrv = self.use_mrv
        solver.use_lcv = self.use_lcv
        solver.solve(self.algo)
        self.stats["ms"] = int((time.time() - t0) * 1000)
        self.ai_steps    = solver.steps
        self.ai_idx      = 0
        self.ai_running  = True
        self.ai_timer    = 0.0
        self.live_domains = {r: list(range(self.num_colors)) for r in COUNTRY_NAMES}
        h = []
        if self.use_mrv: h.append("MRV")
        if self.use_lcv: h.append("LCV")
        self.add_log(f"Algorithm: {self.algo}", DIM)
        self.add_log(f"Heuristics: {'+'.join(h) or 'None'}", DIM)

    # ── AI playback ──────────────────────────────────────────────────────────

    def ai_step_once(self):
        if self.ai_idx >= len(self.ai_steps):
            self.ai_running = False
            self.check_conflicts()
            return

        asgn, reg, status = self.ai_steps[self.ai_idx]
        self.assignment   = dict(asgn)
        self.ai_hl        = reg
        self.stats["steps"] += 1

        if status.startswith("ac3_prune"):
            pruned_color = int(status.split(":")[1])
            self.stats["pruned"] += 1
            self.ai_status = f"AC3 pruned {reg}"
            if reg:
                if reg in self.live_domains and pruned_color in self.live_domains[reg]:
                    self.live_domains[reg].remove(pruned_color)
                self.flash[reg] = [(255, 200, 50), 14]
            self.add_log(f"AC3 prune: {reg} col={pruned_color}", WARN)

        elif status == "domain_update":
            if reg:
                self._recompute_live_domain(reg, asgn)
            self.ai_status = "fc_update"

        elif status == "cutoff":
            self.ai_status = "cutoff"
            self.add_log(f"Cutoff depth={len(asgn)}", ORANGE)

        elif status == "backtrack" and reg:
            self.stats["backtracks"] += 1
            self.ai_status = "backtrack"
            self.flash[reg] = [(255, 60, 60), 22]
            self._recompute_live_domain(reg, asgn)
            self.add_log(f"Backtrack: {reg}", ACCENT2)

        elif status == "assign" and reg:
            self.ai_status = "assign"
            self.flash[reg] = [SUCCESS, 18]
            cidx = asgn[reg]
            self.live_domains[reg] = [cidx]
            self.add_log(f"Assign {reg} = {COLOR_NAMES[cidx]}", SUCCESS)

        elif status == "done":
            self.ai_status  = "done"
            self.ai_running = False
            self.check_conflicts()
            self.add_log("Solution found! No conflicts.", ACCENT)
            return

        else:
            self.ai_status = status

        self.ai_idx += 1
        if self.ai_idx >= len(self.ai_steps):
            self.ai_running = False
            self.check_conflicts()

    def _recompute_live_domain(self, region, assignment):
        used_by_neighbors = {
            assignment[nb]
            for nb in ADJACENCY.get(region, [])
            if nb in assignment
        }
        self.live_domains[region] = [
            c for c in range(self.num_colors)
            if c not in used_by_neighbors
        ]

    def ai_tick(self, dt):
        if not self.ai_running:
            return
        self.ai_timer += dt
        interval = 1.0 / max(self.speed, 0.5)
        while self.ai_timer >= interval and self.ai_running:
            self.ai_step_once()
            self.ai_timer -= interval

    # ── conflict / solution checking ─────────────────────────────────────────

    def check_conflicts(self):
        self.conflicts = set()
        for c, nbs in ADJACENCY.items():
            if c in self.assignment:
                for nb in nbs:
                    if nb in self.assignment and self.assignment[nb] == self.assignment[c]:
                        self.conflicts.add(c)
                        self.conflicts.add(nb)
        if len(self.assignment) == len(COUNTRY_NAMES) and not self.conflicts:
            self.solved = True

    # ── manual play ──────────────────────────────────────────────────────────

    def manual_assign(self, country, color_idx):
        self.assignment[country] = color_idx
        self.flash[country] = [PALETTE[color_idx], 20]
        for nb in ADJACENCY.get(country, []):
            if nb in self.assignment and self.assignment[nb] == color_idx:
                self.conflicts.add(country)
                self.conflicts.add(nb)
                self.lost = True
        if not self.lost and len(self.assignment) == len(COUNTRY_NAMES):
            self.check_conflicts()
            if not self.conflicts:
                self.won = True

    # ── logging ──────────────────────────────────────────────────────────────

    def add_log(self, text, col):
        self.log.insert(0, (text, col))
        if len(self.log) > 60:
            self.log.pop()

    # ── event handling ───────────────────────────────────────────────────────

    def handle_click(self, pos):
        mx, my = pos

        # Color picker (manual mode popup)
        if self.manual_mode and self.selected_country and not self.lost and not self.won:
            for ci, r in self.color_picker_rects.items():
                if r.collidepoint(mx, my):
                    self.manual_assign(self.selected_country, ci)
                    self.selected_country = None
                    return

        # Left sidebar buttons
        for key, rect in self.left_btns.items():
            if rect.collidepoint(mx, my):
                if key.startswith("algo:"):
                    self.algo = key.split(":")[1]
                elif key.startswith("heur:"):
                    h = key.split(":")[1]
                    if   h == "mrv": self.use_mrv = not self.use_mrv
                    elif h == "lcv": self.use_lcv = not self.use_lcv
                elif key.startswith("nc:"):
                    self.num_colors = int(key.split(":")[1])
                    self.live_domains = {r: list(range(self.num_colors)) for r in COUNTRY_NAMES}
                elif key == "solve":
                    if not self.manual_mode:
                        self.start_solve()
                elif key == "reset":
                    self.reset()
                elif key == "manual":
                    self.manual_mode = not self.manual_mode
                    self.reset()
                return

        # Map click in manual mode → select country
        if self.manual_mode and MAP_RECT.collidepoint(mx, my) and not self.lost and not self.won:
            clicked = None
            for name in ["Djibouti", "Uganda"]:
                if name in self.screen_polys and point_in_poly(mx, my, self.screen_polys[name]):
                    clicked = name
                    break
            if not clicked:
                for name in COUNTRY_NAMES:
                    if name in self.screen_polys and point_in_poly(mx, my, self.screen_polys[name]):
                        clicked = name
                        break
            self.selected_country = clicked

    def handle_speed_drag(self, mx):
        if "speed_track" in self.left_btns:
            tr   = self.left_btns["speed_track"]
            frac = max(0.0, min(1.0, (mx - tr.x) / tr.width))
            self.speed = 1 + frac * 29

    # ── main loop ────────────────────────────────────────────────────────────

    def run(self):
        dragging_speed = False

        while True:
            dt     = self.clock.tick(FPS) / 1000.0
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:  self.speed = min(30, self.speed + 1)
                    if event.key == pygame.K_LEFT:   self.speed = max(1,  self.speed - 1)
                    if event.key == pygame.K_r:      self.reset()
                    if event.key == pygame.K_ESCAPE: self.selected_country = None
                    if event.key == pygame.K_SPACE and not self.manual_mode:
                        if not self.ai_running and self.ai_steps:
                            self.ai_step_once()
                        elif not self.ai_steps:
                            self.start_solve()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ("speed_track" in self.left_btns and
                            self.left_btns["speed_track"].collidepoint(mx, my)):
                        dragging_speed = True
                        self.handle_speed_drag(mx)
                    else:
                        self.handle_click((mx, my))

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging_speed = False

                if event.type == pygame.MOUSEMOTION and dragging_speed:
                    self.handle_speed_drag(mx)

            # Hover detection
            self.hovered = None
            if MAP_RECT.collidepoint(mx, my):
                for name in ["Djibouti", "Uganda"]:
                    if name in self.screen_polys and point_in_poly(mx, my, self.screen_polys[name]):
                        self.hovered = name
                        break
                if not self.hovered:
                    for name in COUNTRY_NAMES:
                        if name in self.screen_polys and point_in_poly(mx, my, self.screen_polys[name]):
                            self.hovered = name
                            break

            self.ai_tick(dt)

            self.screen.fill(BG)
            draw_map(self, self.screen)
            draw_left(self, self.screen)
            draw_right(self, self.screen)
            draw_topbar(self, self.screen)

            pygame.display.flip()


# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    App().run()
