.. OCAtari documentation master file, created by
   sphinx-quickstart on Fri Jun  9 20:50:33 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
Welcome to OCAtari's documentation!
===================================

.. highlight:: python


.. container:: twocol

   .. container:: leftside

      OCAtari is a wrapper around the Atari environments available in gymnasium. 
      It automatically extracts the objects that exists in the state, 
      either via looking up their attribute in the RAM (fast), or using vision processing methods. 
      OC_Atari environments allow for object centric Reinforcement Learning.

   .. container:: rightside

      |kangpic| 

.. |kangpic| image:: _static/kangaroo.png
  :width: 200
  :alt: A picture of the kangaroo Atari game with bouding boxes around objects, and a list of all detected objects.


Cite our work
=============
If you are using OCAtari for your scientific publications, please cite us:

.. code:: bibtex
   
   @inproceedings{Delfosse2023OCAtariOA,
      title={OCAtari: Object-Centric Atari 2600 Reinforcement Learning Environments},
      author={Quentin Delfosse and Jannis Bluml and Bjarne Gregori and Sebastian Sztwiertnia and Kristian Kersting},
      year={2023}
   }


Requirements
============
This project depends on:

- gymnasium
- numpy
- termcolor (if you want colored Warning error and messages)
- cv2 and torch (if you want to use an automatic wrapper that provides 4x84x84 observations (as used by DQN and many deep algorithms))

Download and install:
You can download from the
`Github <https://github.com/k4ntz/OC_Atari>`_ repository or:

::

    pip install ocatari


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: API:

   ocatari/core.rst
   ocatari/game_objects.rst
   ocatari/ram.rst
   ocatari/vision.rst

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Scripts:
   :glob:

   scripts/*

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Tests:
   :glob:

   tests/*



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
