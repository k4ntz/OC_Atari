Comparison test
===============

The `test_game_both.py` script provide visual qualitative evaluations of both extraction methods.
It will run the game for some steps, then plot both frames (of each extraction mode) with squares at the bouding boxes of the extracted objects.

The parameters are:

 * ``-g`` GAME, ``--game`` GAME : game to evaluate (e.g. 'Pong')
 * ``-p`` PATH, ``--path`` PATH : the path to a potential DQN agents' model 
 * ``-i`` INTERVAL, ``--interval`` INTERVAL : The frame interval (default 10)
 * ``-hud``, ``--hud`` : If true, also detects objects from the HUD

We provide hereafter an example on the MsPacman game.

|comparison|

.. |comparison| image:: ../_static/comparison.png
  :width: 600
  :alt: A picture of the vision extraction method on Pong.
