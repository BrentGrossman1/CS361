
# import dependencies

## helpers.py dependencies
- from pathlib import Path
- from textadv.engine import Game
- from textadv.output import BufferOutput
- from textadv.world_loader import build_world, load_world

## test_commands.py dependencies
- import copy
- import tempfile
- import unittest
- from pathlib import Path
- from textadv.model import INVENTORY
- from textadv.world_loader import WorldError, build_world
- from helpers import TINY_WORLD, run, tiny_game

## test_parser.py dependencies
- import unittest
- from textadv.parser import Command, parse

## test_walkthrough.py dependencies
- import unittest
- from helpers import real_game, run

## commands.py dependencies
- from __future__ import annotations
- from collections.abc import Callable
- from dataclasses import dataclass
- from typing import TYPE_CHECKING
- from .conditions import check_all
- from .model import INVENTORY, Item, in_loc, room_loc
- from .output import join_list
- from .parser import CANONICAL_DIRECTIONS, Command
- from .save import SaveError, load_game, save_game, save_path
- from .engine import Game

## conditions.py dependencies
- from __future__ import annotations
- from typing import TYPE_CHECKING
- from .model import INVENTORY, Condition, Effect, room_loc
- from .engine import Game

## engine.py dependecies
- from __future__ import annotations
- from collections.abc import Callable
- from pathlib import Path
- from . import commands
- from .conditions import apply_all, check_all
- from .model import INVENTORY, Extra, GameState, Item, World, in_loc, room_loc
- from .output import Output, join_list
- from .parser import Command, parse

## model.py dependencies
- from __future__ import annotations
- from dataclasses import asdict, dataclass, field, fields

## output.py dependencies
- from __future__ import annotations
- import shutil
- import textwrap
- from collections.abc import Callable

## parser.py dependecies
- from __future__ import annotations
- import re
- from dataclasses import dataclass
- from typing import TYPE_CHECKING
- from .model import Item

## save.py dependencies
- from __future__ import annotations
- import json
- import re
- from pathlib import Path
- from .model import GameState, World

## world_loader.py dependencies
- from __future__ import annotations
- import json
- from pathlib import Path
- from . import conditions
- from .model import (INVENTORY, Event, Exit, Extra, Item, Room, Trigger, World, in_loc, room_loc,)
- from .parser import CANONICAL_DIRECTIONS

## main.py dependencies
- import argparse
- import sys
- from pathlib import Path
- import readline
- from textadv.engine import Game
- from textadv.world_loader import WorldError, load_world

# class dependencies

## model.py
### is-a relationships
- none

### has-a relationships
- Room has-a Exit (a dict of them, in `exits`)
- Room has-a Extra (a list of them, in `extras`)
- Item has-a Extra (a list of them, in `extras`)
- World has-a Room (a dict of them, in `rooms`)
- World has-a Item (a dict of them, in `items`)
- World has-a Trigger (a list of them, in `triggers`)
- World has-a Event (a list of them, in `events`)

### uses
- World's `new_state()` method creates and returns a GameState

## output.py
### is-a relationships
- BufferOutput is-a Output (inherits from it)

### has-a relationships
- none

## parser.py
### is-a relationships
- none

### has-a relationships
- Command has-a Item (two of them, in `item` and `item2`; the engine fills these in after parsing)

## commands.py
### is-a relationships
- none

### has-a relationships
- VerbSpec has-a handler function (in `fn`), not another class

### uses
- every command handler takes a Game and a Command, and reads/changes `game.state`
- the `verb()` decorator creates a VerbSpec for each command and stores it in `VERBS`

## conditions.py
### is-a relationships
- none (no classes in this file)

### uses
- the condition and effect functions take a Game and read/change `game.state`

## engine.py
### is-a relationships
- none

### has-a relationships
- Game has-a World (in `world`)
- Game has-a GameState (in `state`)
- Game has-a Output (in `out`)
- Game has-a Item (in `last_item`, what "it" refers to)

### uses
- Game uses Command (from `parse()`) and VerbSpec (looked up in `commands.VERBS`)

## save.py
### is-a relationships
- SaveError is-a Exception

### uses
- `save_game()` and `load_game()` use World and GameState

## world_loader.py
### is-a relationships
- WorldError is-a Exception

### has-a relationships
- _Builder has-a Item (a dict of them, in `items`)
- _Builder has-a Room (a dict of them, in `rooms`)

### uses
- _Builder creates the World, plus every Room, Exit, Extra, Item, Trigger and Event in it

## tests
### is-a relationships
- CommandTests is-a unittest.TestCase
- WorldValidationTests is-a unittest.TestCase
- ParserTests is-a unittest.TestCase
- WalkthroughTests is-a unittest.TestCase

# data dependencies

## world.json / World
The game's map and story: rooms, items, triggers and events.  Loaded once at startup and never changed during play.
- `data/world.json`: the raw data on disk
- world_loader.py: reads world.json and builds the World object from it
- main.py and tests/helpers.py: give world_loader the path to world.json
- engine.py: reads the World for room descriptions, items, triggers and events
- commands.py: reads it through `game.world`
- save.py: stores the world's title in save files

## GameState
Everything that changes as you play: current room, where each item is, open containers, flags, score, turns, win/lose.
- model.py: `World.new_state()` creates the starting GameState
- engine.py: changes the room, turns, visited rooms, fired triggers/events, and game over
- commands.py: changes item locations (take, drop, put) and open/closed (open, close)
- conditions.py: checks it for conditions, and changes it for effects (flags, score, items, moving the player)
- save.py: writes it to a JSON save file and reads it back

## Command and verb tables
Lookup tables that turn what the player types into an action.
- parser.py: `DIRECTIONS`, `ABBREVIATIONS`, `VERB_PHRASES`, etc. are used by `parse()`
- commands.py: `VERBS` and `ALIASES` are filled in by the `verb()` decorator
- engine.py: looks up each command in `VERBS` and `ALIASES`
- world_loader.py and commands.py: use `CANONICAL_DIRECTIONS` to check directions

## Condition and effect tables
- conditions.py: `CONDITIONS` and `EFFECTS` map each condition or effect name to the code that runs it
- world_loader.py: uses them to check that world.json only uses real conditions and effects
- engine.py: runs them through `check_all()` and `apply_all()` (room extras, triggers, events)
- commands.py: runs `check_all()` to see if an exit is blocked