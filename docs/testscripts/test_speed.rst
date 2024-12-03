Speed test
==========

This `test_speed.py` script test the speed of both methods:

 * Vision extraction, by default
 * RAM extraction, using the `-ram` argument

.. code-block:: python

    env.step(random.randint(0, nb_actions))

it will save the result into the `speedtest.json` file, and you can use `plot_speed_results.py` to visualize the results.