# for game in        
games="Asterix Atlantis Berzerk Bowling Boxing Breakout Carnival Centipede DemonAttack 
    Freeway Hero Kangaroo MsPacman Pong QBert Riverraid Seaquest Skiing SpaceInvaders Tennis"
for game in $games
do
    python3 scripts/get_metrics.py -g $game
done
