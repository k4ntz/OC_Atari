`find_causative_ram` looks at a specific part of the game image.
It manipulates the Ram in every possible place, and looks for changes in the
Image.

````python
if __name__ == "__main__":
    X = 14
    Y = 186
    WIDTH = 50
    HEIGHT = 15

    candidates = find_causative_ram("Centipede", X, Y, WIDTH, HEIGHT, show_plot=True)
````
The only relevant variables are the X, Y, WIDTH, HEIGHT coordinates of the
relevant part of the image.
as well as the first argument of find_causative_ram() which is the
name of the game


`find_causative_ram_full` looks at the entire image, but only small changes
to the image are noted (see line 53)
This Skript also creates a dump in `dumps/find_causative_ram_full/game_name`
so the user can better comprehend the changes induced with each ram change

the only relevant variables are game and dump_path
