import pygame
import numpy as np
import random

"""1: sand
   0: air
  -1: stone
   2: water"""

COLORS = {
     0: (20, 20, 30),     # air/void
     2: (17, 17, 132),    # water
}

SAND_PALETTE = [
    (255, 214, 0),    # vivid yellow
    (255, 140, 0),    # bright orange
    (255, 45, 85),    # hot red-pink
    (255, 0, 200),    # magenta
    (150, 50, 255),   # electric purple
    (30, 144, 255),   # bright blue
    (0, 230, 230),    # cyan
    (0, 230, 118),    # neon green
]
LAYER_SIZE = 12       # how many grains are poured before the colour changes

# Stone look
STONE_TOP = (120, 110, 165)        # gradient colour at the top of the screen
STONE_BOTTOM = (55, 50, 90)        # gradient colour at the bottom of the screen
STONE_HIGHLIGHT = (185, 175, 225)  # light edge where stone meets air above
STONE_SHADOW = (28, 24, 48)        # dark edge where stone meets air below/sides

n = 45
CELL = 22   # 45 * 22 = 990px

grid = np.zeros((n, n))
shade = np.zeros((n, n), dtype=int)   # which palette colour each sand grain has
grid[n-1] = -1  # stone floor

# fixed random variation per cell so the stone looks textured
stone_noise = np.random.RandomState(7).randint(-14, 15, (n, n))

# water cells that already spread sideways this step (so they don't move twice)
spread_done = set()


def build_structures():
    # funnel near the top
    for i in range(7):
        grid[8 + i][5 + i] = -1
        grid[8 + i][19 - i] = -1

    # floating ledges
    grid[22, 3:14] = -1
    grid[27, 16:26] = -1
    grid[16, 27:37] = -1

    # basin on the bottom left
    grid[37:44, 4] = -1
    grid[37:44, 15] = -1

    # arch in the middle
    grid[34:44, 19] = -1
    grid[34:44, 25] = -1
    grid[33, 18:27] = -1

    # stepped pyramid on the bottom right
    for step in range(7):
        grid[n - 2 - step, 30 + step:42 - step] = -1


def spread(x, y):
    left_open  = (x - 1 >= 0) and (grid[y][x - 1] == 0)
    right_open = (x + 1 < n)  and (grid[y][x + 1] == 0)
    if left_open and right_open:
        dx = random.choice([-1, 1])
    elif left_open:
        dx = -1
    elif right_open:
        dx = 1
    else:
        return
    # actually MOVE the water (old version copied it and left the original behind)
    grid[y][x] = 0
    grid[y][x + dx] = 2
    spread_done.add((x + dx, y))


def check_down(x, y):
    if y + 1 >= n:
        return "stone"
    val = grid[y + 1][x]
    if val == 0:
        return "air"
    elif val == -1:
        return "stone"
    elif val == 1:
        return "sand"
    elif val == 2:
        return "water"


def is_grid_full(grid):
    return not np.any(grid == 0)   # True if there are zero air cells left


def move_down(x, y):
    # for sand -
    if grid[y][x] == 1:
        grid[y][x] = 0
        grid[y + 1][x] = 1
        shade[y + 1][x] = shade[y][x]
    # for water -
    if grid[y][x] == 2:
        grid[y][x] = 0
        grid[y + 1][x] = 2


def sink_through_water(x, y):
    # sand moves down into water's spot and water moves up into sand's old spot
    grid[y][x] = 2
    grid[y + 1][x] = 1
    shade[y + 1][x] = shade[y][x]


def move_left(x, y):
    # for sand -
    if grid[y][x] == 1:
        grid[y][x] = 0
        grid[y + 1][x - 1] = 1
        shade[y + 1][x - 1] = shade[y][x]
    # for water -
    if grid[y][x] == 2:
        grid[y][x] = 0
        grid[y + 1][x - 1] = 2


def move_right(x, y):
    # for sand -
    if grid[y][x] == 1:
        grid[y][x] = 0
        grid[y + 1][x + 1] = 1
        shade[y + 1][x + 1] = shade[y][x]
    # for water -
    if grid[y][x] == 2:
        grid[y][x] = 0
        grid[y + 1][x + 1] = 2


def move_sideways(x, y):
    # for sand -
    if grid[y][x] == 1:
        if y + 1 >= n:
            return  # already at bottom row so nowhere to go sideways-down to

        left_open  = (x - 1 >= 0) and (grid[y + 1][x - 1] == 0)
        right_open = (x + 1 < n)  and (grid[y + 1][x + 1] == 0)

        if left_open and right_open:
            if random.choice([1, 2]) == 1:
                move_left(x, y)
            else:
                move_right(x, y)
        elif right_open:
            move_right(x, y)
        elif left_open:
            move_left(x, y)
        # else: blocked both sides so stays put

    # for water -
    if grid[y][x] == 2:
        if y + 1 >= n:
            return  # already at bottom row so nowhere to go sideways-down to

        left_open  = (x - 1 >= 0) and (grid[y + 1][x - 1] == 0)
        right_open = (x + 1 < n)  and (grid[y + 1][x + 1] == 0)

        if left_open and right_open:
            if random.choice([1, 2]) == 1:
                move_left(x, y)
            else:
                move_right(x, y)
        elif right_open:
            move_right(x, y)
        elif left_open:
            move_left(x, y)
        else:  # water spreads horizontally
            spread(x, y)


def step(grid):
    """bottom→top guarantees each grain moves at most once per step() call."""
    spread_done.clear()
    for y in range(n - 2, -1, -1):
        for x in range(n):
            if (x, y) in spread_done:
                continue  # this water already spread sideways this step
            if grid[y][x] in (1, 2):
                cell_below = check_down(x, y)
                if cell_below == "air":
                    move_down(x, y)
                elif cell_below == "water" and grid[y][x] == 1:  # ONLY sand sinks
                    sink_through_water(x, y)
                elif cell_below in ("sand", "stone", "water"):  # Water hits water and spreads
                    move_sideways(x, y)
    return grid


def is_stone(x, y):
    if x < 0 or x >= n or y < 0 or y >= n:
        return True
    return grid[y][x] == -1


def draw_stone(screen, grid):
    ys, xs = np.where(grid == -1)
    for y, x in zip(ys, xs):
        # vertical gradient + per-cell texture
        t = y / (n - 1)
        base = [
            int(STONE_TOP[i] + (STONE_BOTTOM[i] - STONE_TOP[i]) * t) + stone_noise[y][x]
            for i in range(3)
        ]
        base = tuple(max(0, min(255, c)) for c in base)

        px, py = x * CELL, y * CELL
        pygame.draw.rect(screen, base, (px, py, CELL, CELL))

        # light edge on top where the stone meets air
        if not is_stone(x, y - 1):
            pygame.draw.rect(screen, STONE_HIGHLIGHT, (px, py, CELL, 3))
        # dark edge underneath where the stone meets air
        if not is_stone(x, y + 1):
            pygame.draw.rect(screen, STONE_SHADOW, (px, py + CELL - 3, CELL, 3))
        # dark thin edges on the sides
        if not is_stone(x - 1, y):
            pygame.draw.rect(screen, STONE_SHADOW, (px, py, 2, CELL))
        if not is_stone(x + 1, y):
            pygame.draw.rect(screen, STONE_SHADOW, (px + CELL - 2, py, 2, CELL))


def draw_grid(screen, grid):
    for val, color in COLORS.items():
        ys, xs = np.where(grid == val)
        for y, x in zip(ys, xs):
            pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

    draw_stone(screen, grid)

    ys, xs = np.where(grid == 1)
    for y, x in zip(ys, xs):
        color = SAND_PALETTE[shade[y][x] % len(SAND_PALETTE)]
        pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))


build_structures()

pygame.init()
screen = pygame.display.set_mode((n * CELL, n * CELL))
clock = pygame.time.Clock()

current_material = 1  # 0=erase, 1=sand, 2=water, 3=stone
grains_poured = 0

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_0:
                current_material = 0
            elif e.key == pygame.K_1:
                current_material = 1
            elif e.key == pygame.K_2:
                current_material = 2
            elif e.key == pygame.K_3:
                current_material = 3

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        gx, gy = mx // CELL, my // CELL
        if 0 <= gx < n and 0 <= gy < n:
            if current_material == 0:
                grid[gy][gx] = 0
            elif grid[gy][gx] == 0:
                if current_material == 1:
                    grid[gy][gx] = 1
                    shade[gy][gx] = (grains_poured // LAYER_SIZE) % len(SAND_PALETTE)
                    grains_poured += 1
                elif current_material == 2:
                    grid[gy][gx] = 2
                elif current_material == 3:
                    grid[gy][gx] = -1

    if is_grid_full(grid):
        running = False

    grid = step(grid)

    screen.fill((0, 0, 0))
    draw_grid(screen, grid)
    pygame.display.flip()
    clock.tick(12)

pygame.quit()
