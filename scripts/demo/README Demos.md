In order to test a game you should run demo files. Use the respective files for each game or simply creat a new file if you added your own game to the project.
Set `MODE` to either `"vison"` or `"revised"` to run the demo with the respected mode.
Running the file with the argument `-p` and a file path to an AI-Agent, will allow you to let the agent play the game for you.
You can set `HUD` to `True` if you also want the hud to be detected ingame.
Every 50th iteration a plotted image of the game with bounding boxes layed over the objects will be plotted. You can adjust this number by changing the `50` in `if i%50 == 0:` to your desired value.
If you want the demo to run longer/shorter change the `range(<number of iteration>)` from the head of the `for-loop`.


Use the following code to create your own demo file. Specify the game you want to test by replacing the < insert game here > token:
```python
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser

game_name = "< insert game here >"
MODE = "vision"
HUD = False
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in range(1000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 4)
    obs, reward, terminated, truncated, info = env.step(action)

    if i%50 == 0:
        print(env.objects)
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
        plt.imshow(obs)
        plt.show()
    if terminated or truncated:
        observation, info = env.reset()
env.close()

```
