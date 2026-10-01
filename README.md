# Brainrot Idle

An idle clicker game for the TI-84 Evo, written in Python. You farm AURA,
buy upgrades, and watch your aura climb.

## Put it on your calculator

1. Connect the calculator with a USB-C cable.
2. Send `brainrot.py` to it with TI Connect Evo.
3. On the calculator, open the Python app and run `brainrot`.

## Controls

| Key        | Action                                                  |
|------------|---------------------------------------------------------|
| UP / DOWN  | Pick a row (the list scrolls)                           |
| ENTER      | Turn auto farm on/off (top row), or buy the selected upgrade |
| CLEAR      | Press twice to quit                                     |

Auto farm farms 5 times per second while it is on, and each farm gives
`1 + (aura per second / 3)`. Each upgrade costs 15%
more every time you buy it.

| Upgrade              |      Start cost | Aura per second |
|----------------------|----------------:|----------------:|
| MEWING               |              15 |               1 |
| RIZZ                 |             100 |               5 |
| FANUM TAX            |             600 |              20 |
| SIGMA                |           3,000 |             100 |
| SKIBIDI              |          20,000 |             500 |
| OHIO                 |         150,000 |           3,000 |
| TUNG TUNG TUNG SAHUR |       1,000,000 |          15,000 |
| TRALALERO TRALALA    |       8,000,000 |          90,000 |
| BOMBARDIRO CROCODILO |      60,000,000 |         500,000 |
| BALLERINA CAPPUCCINA |     500,000,000 |       3,000,000 |
| BRR BRR PATAPIM      |   4,000,000,000 |      20,000,000 |
| CAPPUCCINO ASSASSINO |  30,000,000,000 |     120,000,000 |
| JASON VO             | 250,000,000,000 |     800,000,000 |

## Saving

Progress saves every second, and again when you quit, into a calculator
list named `AURA`. Next time you run the game it picks up where you left off.
To start over, delete the `AURA` list in the calculator's memory manager.

The save is `[aura, owned of each upgrade in table order]`. New upgrades are
added at the end of the list, so older, shorter saves still load.

## TI-84 Evo notes

These behaviors were confirmed on real hardware by the
[ti84evoChess](https://github.com/gcmvanloon/ti84evoChess) project:

- `ti_system.get_key(0)` key codes used here: UP 25, DOWN 34, CLEAR 45,
  ENTER 105.
- `draw_text` draws 18 px higher than shapes at the same y.
- There is no double buffering (`use_buffer()` is unsupported), so the game
  redraws only the parts of the screen that change.

On a real TI-84 Evo, holding ENTER farmed only once: `get_key(0)` reports a
key once per press, not while it is held. That is why farming is a toggle.

Python can't write files on the Evo, so the save uses
`ti_system.store_list` / `recall_list`. Published
[Evo Python sandbox research](https://www.cemetech.net/forum/viewtopic.php?p=317962)
found list names can be up to 5 letters, hold numbers only, and at most 100 items.
