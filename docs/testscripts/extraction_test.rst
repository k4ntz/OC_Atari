Extraction test
===============

The `test_game.py` script provide visual qualitative evaluations of the selected method.
It will run the game for some steps, then plot a frame with squares at the bouding boxes of the extracted objects.

The parameters are:

 * ``-g`` GAME, ``--game`` GAME : game to evaluate (e.g. 'Pong')
 * ``-p`` PATH, ``--path`` PATH : the path to a potential DQN agents' model 
 * ``-i`` INTERVAL, ``--interval`` INTERVAL : The frame interval (default 10)
 * ``-m`` {vision,revised}, ``--mode`` {vision,revised} : The extraction mode
 * ``-hud``, ``--hud`` : If true, also detects objects from the HUD

We provide hereafter an example on the Pong game using the vision method.

|vision_em|

.. |vision_em| image:: ../_static/vision_em.png
  :width: 300
  :alt: A picture of the vision extraction method on Pong.
