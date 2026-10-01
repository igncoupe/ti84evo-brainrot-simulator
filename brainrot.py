# Brainrot Idle for the TI-84 Evo.
# UP/DOWN pick a row, ENTER farms aura or buys, CLEAR twice quits.
# Hold ENTER on FARM AURA to farm 5 times per second.
# Progress is saved every second in the calculator list AURA.

import ti_draw
import ti_system
import random
import time

KEY_UP = 25
KEY_DOWN = 34
KEY_CLEAR = 45
KEY_ENTER = 105

# The draw area is 320x210. draw_text puts text 18 px higher than
# shapes drawn at the same y, so text() shifts it down to match.
TEXT_Y_FIX = 18

# Upgrades in price order. Add new ones at the end so old saves still load.
NAMES = [
    "MEWING", "RIZZ", "FANUM TAX", "SIGMA", "SKIBIDI", "OHIO",
    "TUNG TUNG TUNG SAHUR", "TRALALERO TRALALA", "BOMBARDIRO CROCODILO",
    "BALLERINA CAPPUCCINA", "BRR BRR PATAPIM", "CAPPUCCINO ASSASSINO",
    "JASON VO",
]
BASE_COSTS = [
    15, 100, 600, 3000, 20000, 150000,
    1000000, 8000000, 60000000, 500000000, 4000000000, 30000000000,
    250000000000,
]
RATES = [
    1, 5, 20, 100, 500, 3000,
    15000, 90000, 500000, 3000000, 20000000, 120000000,
    800000000,
]
# Color of the tab at the left of each upgrade row.
TABS = [
    (0, 200, 255), (255, 80, 160), (255, 160, 0), (160, 160, 190), (90, 220, 90), (255, 60, 60),
    (200, 140, 80), (60, 140, 255), (130, 170, 80), (255, 150, 200), (60, 190, 110), (170, 100, 60),
    (255, 230, 120),
]
HYPE = ["SHEESH", "NO CAP", "GOATED", "BASED", "HUGE W", "LOCKED IN", "SIGMA MOVE"]

# Theme colors.
BG = (18, 16, 40)
HEADER_BG = (70, 20, 130)
MSG_BG = (32, 28, 64)
ROW_BG = [(26, 24, 52), (36, 32, 70)]
SEL_BG = (255, 205, 40)
GOLD = (255, 210, 60)
WHITE = (240, 240, 255)
CYAN = (80, 220, 255)
DARK = (30, 20, 60)
PINK = (255, 60, 200)
GREEN = (80, 255, 140)
RED = (255, 90, 90)

# Row 0 farms aura, the rest buy upgrades. 7 rows fit, so the list scrolls.
# Rows end at x=315; the scrollbar uses x=316-319.
ROW_TOP = 44
ROW_H = 23
VISIBLE = 7
ROWS = len(NAMES) + 1

# Holding ENTER on FARM AURA farms once per FARM_EVERY seconds.
FARM_EVERY = 0.2

# The save is the list [aura, owned of upgrade 1, owned of upgrade 2, ...].
# List names can be at most 5 letters.
SAVE = "AURA"

# On the first run there is no AURA list yet, so recall_list fails.
try:
    save = ti_system.recall_list(SAVE)
except Exception:
    save = [0]
aura = int(save[0])
# A save made before newer upgrades existed is shorter; those start at 0.
owned = [0] * len(NAMES)
for i in range(len(save) - 1):
    owned[i] = int(save[i + 1])

# Rate and costs follow from what you own.
rate = 0
costs = list(BASE_COSTS)
for i in range(len(NAMES)):
    rate += RATES[i] * owned[i]
    for _ in range(owned[i]):
        costs[i] = costs[i] * 115 // 100
sel = 0
top = 0


def text(x, y, s):
    ti_draw.draw_text(x, y + TEXT_Y_FIX, s)


def text_right(x, y, s):
    # Glyphs are 8 px wide with 2 px between characters.
    text(x - len(s) * 10 + 2, y, s)


def fmt(n):
    # 999 -> "999", 12345 -> "12.3K", 1234567 -> "1.2M"
    if n < 1000:
        return str(n)
    i = 0
    while n >= 1000000 and i < 4:
        n //= 1000
        i += 1
    return str(n // 1000) + "." + str(n % 1000 // 100) + "KMBTQ"[i]


def read_key():
    return int(ti_system.get_key(0))


def save_game():
    ti_system.store_list(SAVE, [aura] + owned)


def color(c):
    ti_draw.set_color(c[0], c[1], c[2])


def box(c, x, y, w, h):
    color(c)
    ti_draw.fill_rect(x, y, w, h)


def draw_header():
    box(HEADER_BG, 0, 0, 320, 20)
    color(GOLD)
    text(4, 2, "AURA " + fmt(aura))
    color(WHITE)
    text_right(316, 2, "+" + fmt(rate) + "/S")


def draw_msg(s, c):
    box(MSG_BG, 0, 20, 320, 22)
    color(c)
    text((320 - len(s) * 10 + 2) // 2, 22, s)


def draw_row(r):
    y = ROW_TOP + (r - top) * ROW_H
    if r == sel:
        box(SEL_BG, 0, y, 316, ROW_H)
    else:
        box(ROW_BG[r % 2], 0, y, 316, ROW_H)
    if r == 0:
        color(DARK if r == sel else GOLD)
        text(8, y + 4, "FARM AURA")
        text_right(312, y + 4, "+" + fmt(1 + rate // 10))
    else:
        box(TABS[r - 1], 0, y, 4, ROW_H)
        color(DARK if r == sel else WHITE)
        text(8, y + 4, NAMES[r - 1] + " x" + str(owned[r - 1]))
        color(DARK if r == sel else CYAN)
        text_right(312, y + 4, fmt(costs[r - 1]))


def draw_rows():
    for r in range(top, top + VISIBLE):
        draw_row(r)
    # Scrollbar: the thumb shows which part of the list is on screen.
    h = VISIBLE * ROW_H
    box(MSG_BG, 316, ROW_TOP, 4, h)
    box(PINK, 317, ROW_TOP + h * top // ROWS, 2, h * VISIBLE // ROWS)


box(BG, 0, 0, 320, 210)
draw_header()
draw_msg("WELCOME BACK" if aura or rate else "HOLD ENTER TO FARM", CYAN)
color(PINK)
ti_draw.draw_line(0, 42, 319, 42)
draw_rows()

prev = 0
quitting = False
next_tick = time.monotonic() + 1
next_farm = 0
while True:
    if time.monotonic() >= next_tick:
        next_tick += 1
        aura += rate
        draw_header()
        save_game()

    # get_key(0) reports the key held right now, so a new press is a key
    # that differs from the last read.
    k = read_key()
    new = k != 0 and k != prev
    prev = k

    if new and k == KEY_CLEAR:
        if quitting:
            break
        quitting = True
        draw_msg("CLEAR AGAIN TO QUIT", RED)
    elif new and quitting:
        quitting = False
        draw_msg("HOLD ENTER TO FARM", CYAN)

    if k == KEY_ENTER and sel == 0:
        if new or time.monotonic() >= next_farm:
            next_farm = time.monotonic() + FARM_EVERY
            aura += 1 + rate // 10
            draw_header()
    elif new and (k == KEY_UP or k == KEY_DOWN):
        old = sel
        old_top = top
        sel = (sel + (1 if k == KEY_DOWN else -1)) % ROWS
        if sel < top:
            top = sel
        elif sel >= top + VISIBLE:
            top = sel - VISIBLE + 1
        if top == old_top:
            draw_row(old)
            draw_row(sel)
        else:
            draw_rows()
    elif new and k == KEY_ENTER:
        i = sel - 1
        if aura < costs[i]:
            draw_msg("BRO IS BROKE", RED)
        else:
            aura -= costs[i]
            owned[i] += 1
            rate += RATES[i]
            costs[i] = costs[i] * 115 // 100
            draw_header()
            draw_row(sel)
            if top == 0:
                draw_row(0)
            draw_msg(random.choice(HYPE), GREEN)

save_game()
ti_draw.clear()
