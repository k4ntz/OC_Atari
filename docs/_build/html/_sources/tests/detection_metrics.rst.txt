Get detection metrics 
=====================

The `get_metrics.py` test script provide visual *quantitive* evaluations of both extraction methods.
It use random, DQN and if available C51 agents, and computes the average and per class:

 * Precision
 * Recall
 * F-score
 * Intersection over Union (IOU)

It will run the game for some steps, and save the different metrics, as well as images for which the IOU threshold is met.

The parameters are:

 * ``-g`` GAME, ``--game`` GAME : game to evaluate (e.g. 'Pong')
 * ``-i`` IOU, ``--iou`` IOU : Minimum iou threshold to trigger image saving (e.g. 0.7)
 * ``-p`` PATH, ``--path`` PATH : the path to a potential DQN agents' model 
 * ``-s`` SEED, ``--seed`` SEED  If provided, set the seed


