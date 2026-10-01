# Brainrot Idle for the TI-84 Evo.
# UP/DOWN pick a row, ENTER farms aura or buys, CLEAR twice quits.

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

NAMES = ["MEWING", "RIZZ", "FANUM TAX", "SIGMA", "SKIBIDI", "OHIO"]
RATES = [1, 5, 20, 100, 500, 3000]
HYPE = ["SHEESH", "NO CAP", "GOATED", "BASED", "HUGE W", "LOCKED IN", "SIGMA MOVE"]

# Rows: row 0 farms aura, rows 1-6 buy upgrades.
ROW_TOP = 44
ROW_H = 23
ROWS = 7

aura = 0
rate = 0
owned = [0, 0, 0, 0, 0, 0]
costs = [15, 100, 600, 3000, 20000, 150000]
sel = 0


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


def draw_header():
    ti_draw.set_color(255, 255, 255)
    ti_draw.fill_rect(0, 0, 320, 20)
    ti_draw.set_color(120, 0, 200)
    text(4, 2, "AURA " + fmt(aura))
    ti_draw.set_color(0, 0, 0)
    text_right(316, 2, "+" + fmt(rate) + "/S")


def draw_msg(s):
    ti_draw.set_color(255, 255, 255)
    ti_draw.fill_rect(0, 20, 320, 21)
    ti_draw.set_color(200, 0, 0)
    text((320 - len(s) * 10 + 2) // 2, 22, s)


def draw_row(r):
    y = ROW_TOP + r * ROW_H
    if r == sel:
        ti_draw.set_color(255, 220, 0)
    else:
        ti_draw.set_color(255, 255, 255)
    ti_draw.fill_rect(0, y, 320, ROW_H)
    ti_draw.set_color(0, 0, 0)
    if r == 0:
        text(8, y + 4, "FARM AURA")
        text_right(312, y + 4, "+" + fmt(1 + rate // 10))
    else:
        text(8, y + 4, NAMES[r - 1] + " x" + str(owned[r - 1]))
        text_right(312, y + 4, fmt(costs[r - 1]))


ti_draw.clear()
draw_header()
draw_msg("ENTER TO FARM AURA")
ti_draw.set_color(0, 0, 0)
ti_draw.draw_line(0, 42, 319, 42)
for r in range(ROWS):
    draw_row(r)

prev = 0
quitting = False
next_tick = time.monotonic() + 1
while True:
    if time.monotonic() >= next_tick:
        next_tick += 1
        aura += rate
        draw_header()

    # get_key(0) reports the key held right now, so act only on a new press.
    k = read_key()
    if k and k != prev:
        if k == KEY_CLEAR:
            if quitting:
                break
            quitting = True
            draw_msg("CLEAR AGAIN TO QUIT")
        else:
            if quitting:
                quitting = False
                draw_msg("")
            if k == KEY_UP or k == KEY_DOWN:
                old = sel
                sel = (sel + (1 if k == KEY_DOWN else -1)) % ROWS
                draw_row(old)
                draw_row(sel)
            elif k == KEY_ENTER and sel == 0:
                aura += 1 + rate // 10
                draw_header()
            elif k == KEY_ENTER:
                i = sel - 1
                if aura < costs[i]:
                    draw_msg("BRO IS BROKE")
                else:
                    aura -= costs[i]
                    owned[i] += 1
                    rate += RATES[i]
                    costs[i] = costs[i] * 115 // 100
                    draw_header()
                    draw_row(0)
                    draw_row(sel)
                    draw_msg(random.choice(HYPE))
    prev = k

ti_draw.clear()
