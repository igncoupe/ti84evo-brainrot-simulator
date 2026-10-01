# Brainrot Idle

An idle clicker game for the TI-84 Evo, written in Python. You farm AURA,
buy upgrades, and watch your aura climb.

## Put it on your calculator

1. Connect the calculator with a USB-C cable.
2. Send `brainrot.py` to it with TI Connect Evo.
3. On the calculator, open the Python app and run `brainrot`.

## Controls

| Key        | Action                                       |
|------------|----------------------------------------------|
| UP / DOWN  | Pick a row                                   |
| ENTER      | Farm aura (top row) or buy the selected upgrade |
| CLEAR      | Press twice to quit                          |

Farming gives `1 + (aura per second / 10)` per press. Each upgrade costs 15%
more every time you buy it.

| Upgrade   | Start cost | Aura per second |
|-----------|-----------:|----------------:|
| MEWING    |         15 |               1 |
| RIZZ      |        100 |               5 |
| FANUM TAX |        600 |              20 |
| SIGMA     |       3,000 |             100 |
| SKIBIDI   |      20,000 |             500 |
| OHIO      |     150,000 |           3,000 |

## Saving

Progress saves every second, and again when you quit, into a calculator
list named `AURA`. Next time you run the game it picks up where you left off.
To start over, delete the `AURA` list in the calculator's memory manager.

## TI-84 Evo notes

These behaviors were confirmed on real hardware by the
[ti84evoChess](https://github.com/gcmvanloon/ti84evoChess) project:

- `ti_system.get_key(0)` returns the key held right now. Codes used here:
  UP 25, DOWN 34, CLEAR 45, ENTER 105.
- `draw_text` draws 18 px higher than shapes at the same y.
- There is no double buffering (`use_buffer()` is unsupported), so the game
  redraws only the parts of the screen that change.

Python can't write files on the Evo, so the save uses
`ti_system.store_list` / `recall_list`. Published
[Evo Python sandbox research](https://www.cemetech.net/forum/viewtopic.php?p=317962)
found list names can be up to 5 letters, hold numbers only, and at most 100 items.
