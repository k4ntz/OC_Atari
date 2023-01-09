from matplotlib import pyplot as plt
import sys
# import pathlib
sys.path.insert(0, '../../ocatari') # noqa
from ocatari import core
from ocatari.vision.utils import plot_bounding_boxes_from_info
from ocatari.vision.utils import find_objects, plot_bounding_boxes # noqa

"""
trying to automate the creation of vision
mouse button :      to select the object
keybord button :    to go to next object
"""
rgb_array = []
name = "object0"
index = 0
objects = {}
colors = {}


def on_click(event):
    global index, name

    x, y = event.xdata, event.ydata
    color = rgb_array[int(y)][int(x)]
    print(rgb_array[int(y)][int(x)])

    objects[name] = find_objects(rgb_array, color)
    colors[name] = color.tolist()
    print(objects[name])

    index += 1
    name = name[:-1] + str(index)

def on_key_pressed(event):
    plt.close()
    show_altered_image()


def show_image():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.add_artist(plt.imshow(rgb_array))
    cid = fig.canvas.mpl_connect("button_press_event", on_click)
    cid2 = fig.canvas.mpl_connect("key_press_event", on_key_pressed)
    cid2 = fig.canvas.mpl_connect("close_event", print_colors)
    plt.show()

def show_altered_image():
    info["objects"] = objects
    info["objects_colors"] = colors
    plot_bounding_boxes_from_info(rgb_array, info)
    show_image()

def print_colors(event):
    print(colors)

if __name__ == "__main__":
    env = core.OCAtari("Skiing", mode="vision", render_mode='rgb_array')
    rgb_array, info = env.reset()
    rgb_array = env.render()

    try:
        show_image()
    except:
        print_colors()





