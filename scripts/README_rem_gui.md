
# Command-Line Arguments

### General Arguments
- **`-g` / `--game`**: Specify the game to be run (default: `Pong`).
- **`-m` / `--mode`**: Set the extraction mode. Options are:
  - `ram`: Use RAM-based extraction.
  - `vision`: Use vision-based extraction.
  Default is `ram`.

### Rendering Options
- **`-nr` / `--no_render`**: Specify a list of RAM cells to exclude from rendering (e.g., `-nr 1 2 3`).
- **`-nra` / `--no_render_all`**: Disable rendering for all RAM cells.

### Gameplay Options
- **`-hu` / `--human`**: Enable human control to play the game.
- **`-sf` / `--switch_frame`**: Apply modifications to the game after the specified frame threshold (default: `0`).

### Saving and Loading
- **`-p` / `--picture`**: Take a screenshot after the specified number of steps (default: `0`).
- **`-a` / `--agent`**: Path to a trained agent to be loaded (default: empty).
- **`-ls` / `--load_state`**: Path to a saved state to be loaded (default: `None`).

---

### Example Usage
1. Run the game `Pong` in RAM mode:
   ```bash
   python rem_gui.py -g Pong -m ram

---

# Key Bindings Manual for `rem_gui.py`

## General Controls
- **`P`**: Pause/Resume the game.
- **`F`**: Toggle frame-by-frame mode. In this mode, the game advances one frame at a time.
- **`N`**: Advance to the next frame (only works in frame-by-frame mode).
- **`B`**: Go back to the previous frame (if saved frames are available).
- **`R`**: Reset the game environment.
- **`C`**: Clone the current game state and save it as a `.pkl` file.
- **`M`**: Save and display the current game screen as an image.
- **`O`**: Print the current game objects to the console.

## RAM Cell Interaction
- **Mouse Left Click**: Select a RAM cell or find causative RAM for a pixel if clicked on the game screen.
- **Mouse Right Click**: Toggle whether a RAM cell is rendered or hidden.
- **Mouse Middle Click**: Toggle whether a RAM cell is highlighted in red.
- **Mouse Wheel Up**: Increment the value of the RAM cell under the mouse pointer.
- **Mouse Wheel Down**: Decrement the value of the RAM cell under the mouse pointer.

## Editing RAM Cell Values
- **`0-9` (Number Keys)**: Enter digits to modify the value of the selected RAM cell.
- **`Backspace`**: Remove the last entered digit for the selected RAM cell.
- **`Enter`/`Keypad Enter`**: Confirm and set the new value for the selected RAM cell.
- **`Escape`**: Deselect the currently active RAM cell.

## Game Interaction
- **Arrow Keys or Custom Key Bindings**: Perform in-game actions based on the `keys2actions` mapping.
