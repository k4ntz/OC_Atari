`TestSkriptNr1` uses Gymnasium to creat a game-environment.
It will print the current RAM state as an array as well as any values that changed since the last iteration.
Use:
```python
    gym.make("insert game name here", render_mode="human/rgb_array")
```

this will set up the environment for the game.
Use:
```python
observation, reward, terminated, truncated, info = env.step(any number  between 0-8)
```

this will let you choose the input given to the environment.

`TestSkriptNr2` uses Gymnasium to creat a game-environment.
This Script lets you set values to a RAM state.
'target_ram_position' determines which RAM-position will be changed
'new_ram_value' determines what value the RAM-position will  be set to.

`TestSkriptNr3` does the same as TestSkriptNr1, but instead of using gymnasium it will call the OCAtari-wrapper.
Use:
```python
env = OCAtari("insert game name here", mode="raw/revised/vision", render_mode="human/rgb_array")
```

to set up the environment.

`TestSkriptNr4` uses the OCAtari-wrapper to create the environment just like `TestSkriptNr3`.
This will print all values within the current RAM-state which lie in a specified range.
`min` sets the floor of the range and `max` the ceiling. Edit the `already_figured_out` variable to include all RAM-states that should not be printed even if they lie in the specified range.

`TestSkriptNr5` is the same as `TestSkriptNr3` but contains a `ipdb.set_trace()` statement which will trigger right after printing the changed RAM values. It also includes 2 `set_ram()` statements. 
___
`TestSkriptNr6`:

we could name this test manually test, as we shall see ahead.
this test makes it easy to set several indices individually. like to iterate through them or their values or both
together in same run, or you just comment the decisive line:
```python
env._env.unwrapped.ale.setRAM(i, value)  # DON'T CHANGE
```
so you don't change any of both. With "don't change" the variables `i` and `value` are meant. do changes in other lines
as for their values to avoid mistakes

the other feature of this test is reading the individual bits of changing values and the bits of difference between
old and new values. like to get them printed in console. you could also read if the difference is positive or negative.

There are much uncommented lines, which are not meant to be deleted. Because you would need to test with any of them,
while e.g. testing specific behavior of some variable(according to your sense).

So at the beginning you have the array `already_figured_out` for indices you know their functionality and don't want to 
test or set them further in this tests file. this array at same time includes two other arrays to keep indices separated
and keep clear view of them.
Right after it come initial values for value and index. after then, you have two lines, for `i` and `index`. regularly 
you rather keep one of them uncommented. so for uncommented `i` you are testing for only one fixed index. on the other hand
if you go with `index`, so you chose to test with changing index. more precisely increasing one and by one.
after them come much uncommented lines for `value`, which are singly the methods/ways, you change the value of some
index. they are not meant to be deleted. Because you would need to test with any of them,
while e.g. testing specific behavior of some variable(according to your sense).
After that comes the part where we jump to the next index. you jump indices which are figured out with
```python
while index in already_figured_out:
    index += 1
```
If you ever wanted to observe value of specific indices, you could get them printed even if there values are not
changing with next two lines:
```python
for k in [6, 38, 54, 83, 88, 89, 120]:  # checking set of specific values
print('ram[' + str(k) + '] =', ram[k])
```

so we called this test manual, because you could begin to test with it from the beginning of your looking for
functionality of indices until having them all. (think about using `find_causative_ram.py` too)
there is a recommended way to work with when having a new game. it is as follows:

1- set index to zero

2- uncomment the line of `i = index`

3- uncomment the line where value increases by 85

4- have jumping to the next index every four rounds (to have time to stop game to read current index)

5- have rendering every round (and from far one `ROUND > 50` if game takes many frames to really begin)

6- have `time.sleep()` uncommented

you would at end have next specific lines:
```python
index = 0

i = index

value = (prevRam[i] + 85) % 256  # 85 = 01010101

if ROUND % 1 == 0:  # how often we increment index
    index += 1
    
if ROUND % 1 == 0 and ROUND > 50:
    env._env.unwrapped.ale.setRAM(i, value)  # DON'T CHANGE

time.sleep(0.1)
``` 

___
`testSkriptNr7` can be used to identify for which attribute each RAM state stands
by setting the RAM values for each RAM position or a user-defined slice of the
RAM positions. After each position ipdb stops the game and the rendered image, so
that you can see which object position exactly changed.

Caution this can crash the game!

```python
env = OCAtari("Assault", mode="raw", render_mode="human")  # set game
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):

    ram_value = 9   # set here the RAM value

    for b in range(0, 126):     # loop through the RAM
        obs, reward, terminated, truncated, info = env.step(random.randint(0, 0))
        print(b - 1)
        env.set_ram(b, ram_value)
        env.render()
        ipdb.set_trace()
```
