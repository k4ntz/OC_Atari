# Generally
If you run the file 'ReverseEngineeringHelper', the environment will be set up and 
will loop threw an amount of steps while giving back valuable information based 
on the given actions.<br>
'ReverseEngineeringHelper' is a tool to provide useful access to the games of atari
for reverse engineering purposes!

## Variables
I divided the variables in 6 blocks. Each fulfills a different purpose. 
1. the basics:
    - This file enables the usage of gym with or without the OCAtari wrapper! 
    - Printing out environment info can be useful => printEnvInfo

2. a few standard gym variables:
   - The game and render mode as well as the reset seed or fps of the gym environment

3. the OCAtari modes:
   - There are the modes raw, ram, vision, test and HUD. 

4. actions that will be performed each step. 
   - You can play the game, define an action sequence or let it run randomly.

5. Gaining valuable information for reversed engineering purposes and others
6. Global variables => DO NOT CHANGE

## How to use gym with a certain game
1. set useOCAtari to False
2. set game_name to your game
3. set playGame to False unless you want to play a game in which case it will take a few more steps
4. set actionSequence to NONE

## How to play a game
1. Get the list of inputs for the game and assign it to the INPUTS variable <br>
(atari game controls are quite the same, so this step might not be necessary, but better take a look)
2. Bind actions to keys
3. set playGame to True
4. set showImage to True
5. run the file
side notes: 
- setting the render_mode to "rgb_array" is advised while playing the game because of fps drops
- render_mode "human" is good for comparison reasons
- slowDownPlot in block 5 might slow down the game, set it to a low value

## How to get the list of inputs for the game
1. set useOCAtari to False
2. set game_name to your game
3. set playGame to False
4. set showInputs to True
5. run the file and read the output on the command line (a list of Strings is what you are searching for)

## How to bind actions to a key
There is key_map that maps the keys to a given basic operation.
A basic operation is directly related to an action name or part of an action name.<br>
For example: you map 'w' to 'UP' and 'd' to 'RIGHT' <br>
- That means, that in case you press w, the action 'UP' will occur and in case of 'd' 'RIGHT'. 
- If you press 'w' and 'd' at the same time and there is an action name
   'UPRIGHT' or 'RIGHTUP' in INPUTS, then that action will occur.<br>
- Note: The plot may have functionalities that use hotkeys. All of your keys will work
as described here, but these hotkeys might be overwritten. If you want to keep these hotkeys,
avoid mapping the keys to an action.

## What can I do while the game runs?
- play (pressing the keys you bound actions to, when none of these keys is pressed, the default_action will occur)
- freeze the game (pressing tab) and look at the current frame
- close the program (pressing escape)
- use ipdb (pressing i)

## ipdb interrupts but the plot doesn't react
- Don't use ipdb.set_trace directly, press i instead or use ipdb_interrupt(0)
- Unfortunately, the plot and the run are on the same thread, that's why the plotting
functionalities only work as long as the program is not interrupted (by a debugger). 
- But you can gain access by typing in plt.pause(x) in ipdb. This will activate the 
functions for x seconds.
- If you know in advance, that you want to have access to the frame before interrupting 
with ipdb, then set ipdb_delay to your wished delay. 

## What is an action sequence?
- An action sequence is a list of Strings that describe actions that the environment will do repeatedly.
- Let's say you set actionSequence to ['RIGHT', 'FIRE', 'LEFT'], then the actions will
be ['RIGHT', 'FIRE', 'LEFT', 'RIGHT', 'FIRE', 'LEFT', 'RIGHT',...]
- It only activates if playGame is False.
- If no action sequence is defined, then the environment will do random actions instead.

## What is valuable information and how can I get it?
- the possible inputs => showInputs
- the action of the current environment step => showActions
- RAM at the current frame => showRAM
- image (plot) of the game => showImage
- the rgb array => printRGB
- normal game => render_mode='human'
### RAM manipulation
- You can set the ram, if manipulateRAM is True. The RAM will be set at the index to a value.
- If the value is negative, then the ram value will instead be increased by 1 with every step of the environment
- The value will always be between 0 and 255, which is made certain by the modulo operator
- The change of the ram and the following step will influence the ram at other points. 
You can get these changes by setting showDelta to True
- 

### What else?
- slowDownPlot can be set to a value, which will act like plt.pause(slowDownPlot) for every step of the environment
- everything that will be displayed is at runtime

