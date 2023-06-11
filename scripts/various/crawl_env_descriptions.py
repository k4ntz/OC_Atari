import requests
from bs4 import BeautifulSoup
from pathlib import Path
envs = ["Assault", "Asterix", "Atlantis", "Berzerk", "Bowling", 
        "Boxing", "Breakout", "Carnival", "Centipede", "Fishing_Derby", 
        "Freeway", "Frostbite", "Kangaroo", "Montezuma_Revenge", "Ms_Pacman", 
        "Pong", "Qbert", "Riverraid", "Seaquest", "Skiing", "Space_Invaders", "Tennis"]

out_dir = Path("env_descriptions")
out_dir.mkdir(exist_ok=True)
for e in envs:
    target_url = "https://gymnasium.farama.org/environments/atari/" + e.lower()
    html = requests.get(target_url).text
    soup = BeautifulSoup(html, features="html.parser")
    resp = soup.find("section", {"id": "description"})
    out = out_dir / Path(e.replace("_", "") + ".tex")
    if resp:
        if out.exists():
            print(f"{out.name} already exists.")
        else:
            desc = resp.p.get_text()
            with out.open("w") as f:
                f.write(desc)
            print(f"{out.name} written.")
    else:
        print(f"Error with env {e}")