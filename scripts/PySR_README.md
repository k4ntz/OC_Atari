# PySR regression README

## Installation
You need to install the julia language and [pysr](https://github.com/MilesCranmer/PySR) packages to run the regression tests. To do so:

```bash
pip install pysr
```
<!-- and if on a linux system:
```bash
sudo apt-get install julia
``` -->

To run the regression tests, you need to have the `transitions` directory in the same directory as the `scripts` directory. 
The `transitions` directory should contain *e.g.* the `Pong_data.pkl` file.
To compute the vertical position of the ball (at the ram position `54`) in the Pong game, run the following command:

```bash
python3 scripts/regress_ram_position.py -d transitions/Pong_data.pkl -t 54
```

You should obtain the following output:

```bash
=== FINAL EQUATIONS ===-------
ns[54] = s54
ns[54] = s54 + ss56
ns[54] = (ss56 + s54) + 0.2913
------------------------------
```
These correspond to the different levels of complexity allowed in the regression.

* The first equations shows that the vertical position of the ball (in next states (ns)) is equal to the value of the ram position `54` (in the state). 
* The second equation shows that the vertical position of the ball (in next states (ns)) is equal to the sum of the value of the ram position `54` and the value of the ram position `56` (*ie* its vertical speed, positive or negative). The s for `56` indicates that the ram value is considered as a **signed** integer.
* The other equations are more complex and do not provide a better fit to the data.

Similarly, for the horizontal position of the ball (at the ram position 49) in the Pong game, run the following command:

```bash
python3 scripts/regress_ram_position.py -d transitions/Pong_data.pkl -t 49
```

You could obtain the following output:
```bash
...
=== FINAL EQUATIONS ===---------------------------
ns[49] = s49
ns[49] = s49 - ss58
...
-------------------------------------------------
```
To check the accuracy of the following esuation:
`x49[t+1] = x49[t] - x58[t] (signed)`
use the formulae flag:
```bash
python3 scripts/regress_ram_position.py -d transitions/Pong_data.pkl -f "ns[49] = s[49] - ss[58]"
```
You should obtain the following output:
```bash
Accuracy of regression: 88.2%
```

Indeed once the ball is beyond the player or the enemy, its value does no longer change, which is why the accuracy is not 100%.