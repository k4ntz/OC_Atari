from argparse import ArgumentParser
import json
import timeit
from ocatari.core import OCAtari
import os


parser = ArgumentParser()

parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-ram", "--ram", action="store_true",
                    help="Use the RAM version")

opts = parser.parse_args()

nb_actions = OCAtari(f'{opts.game}-ram-v4').nb_actions - 1

setp = "from ocatari.core import OCAtari\nimport random\n"
if opts.ram:
    setp += f'env = OCAtari("{opts.game}-ram-v4", "ram", obs_mode=None, hud=True)\n'
else:
    setp += f'env = OCAtari("{opts.game}-v4", "vision", obs_mode=None, hud=True)\n'
setp += "obs, infos = env.reset()"

pgtest = "env.step(random.randint(0, nb_actions))"


times = timeit.repeat(number=10**4, stmt=pgtest, setup=setp,
                      globals={'nb_actions': nb_actions}, repeat=5)

print(times)

method = "ram" if opts.ram else "vision"

savefile = "speedtests.json"
if os.path.exists(savefile):
    with open(savefile, "r") as fp:
        results = json.load(fp)
else:
    results = {}

if not opts.game in results:
    results[opts.game] = {}
results[opts.game][method] = times
with open(savefile, 'w') as fp:
    json.dump(results, fp, indent=4, sort_keys=True)
print(f"{savefile} updated")
