
# BOTH
for game in Assault Asterix Atlantis Berzerk Bowling Boxing Breakout Carnival Freeway Kangaroo MsPacman Pong Seaquest Skiing SpaceInvaders Tennis
do
    python3 generate_dataset.py -g $game
done

# VISION ONLY
for game in Alien Asteroids BeamRider ChopperCommand DemonAttack FishingDerby Frostbite MontezumaRevenge Qbert Riverraid RoadRunner
# for game in Breakout Pong
do
    python3 generate_dataset_vision.py -g $game
done
