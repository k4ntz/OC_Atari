import numpy as np
import cv2
from skimage.morphology import (disk, square)  # noqa
from skimage.morphology import (erosion, dilation, opening, closing, white_tophat, skeletonize)  # noqa
import matplotlib.pyplot as plt
from termcolor import colored


# to be removed
def bbs_extend(labels, key: str, stationary=False):
    labels['bbs'].extend([(*bb, "S" if stationary else "M", key) for bb in labels[key]])


# to be removed
def bb_by_color(labels, obs, color, key, closing_active=True):
    print(colored("\n\n\n PLEASE DON'T USE, USE 'find_objects' instead\n\n\n", "red"))
    labels[key] = find_objects(obs, color, closing_active)
    bbs_extend(labels, key)


def assert_in(observed, target, tol):
    if type(tol) is int:
        tol = (tol, tol)
    return np.all([target[i] + tol[i] > observed[i] > target[i] - tol[i] for i in range(2)])
    # return np.all([target[i] + tol[i] >= observed[i] >= target[i] - tol[i] for i in range(2)])


def iou(bb, gt_bb):
    """
    Intersection over Union
    """
    inner_width = min(bb[1] + bb[3], gt_bb[1] + gt_bb[3]) - max(bb[1], gt_bb[1])
    inner_height = min(bb[0] + bb[2], gt_bb[0] + gt_bb[2]) - max(bb[0], gt_bb[0])
    if inner_width < 0 or inner_height < 0:
        return 0
    # bb_height, bb_width = bb[1] - bb[0], bb[3] - bb[2]
    intersection = inner_height * inner_width
    return intersection / ((bb[3] * bb[2]) + (gt_bb[3] * gt_bb[2]) - intersection)


def mark_point(image_array, x, y, color=(255, 0, 0), size=1, show=False, cross=True):
    """
    marks a point on the image at the (x,y) position and displays it
    """
    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            if (not cross or i == j or i == -j) and x + i >= 0 and x + j >= 0 \
                    and x + i < 160 and y + j < 210:
                image_array[y + j, x + i] = color
    if show:
        plt.imshow(image_array)
        plt.show()


def mark_bb(image_array, bb, color=(255, 0, 0), surround=True):
    """
    marks a bounding box on the image
    """
    x, y, w, h = bb
    if surround:
        if x > 0:
            x, w = bb[0] - 1, bb[2] + 1
        else:
            x, w = bb[0], bb[2]
        if y > 0:
            y, h = bb[1] - 1, bb[3] + 1
        else:
            y, h = bb[1], bb[3]
    bottom = min(209, y + h)
    right = min(159, x + w)
    image_array[y:bottom + 1, x] = color
    image_array[y:bottom + 1, right] = color
    image_array[y, x:right + 1] = color
    image_array[bottom, x:right + 1] = color


def plot_bounding_boxes(obs, bbs, objects_colors):
    for bb in bbs:
        try:
            mark_bb(obs, bb, np.array([cv for cv in objects_colors[bb[5]]]))
        except KeyError as err:
            print(err)
            mark_bb(obs, bb, np.array([255, 255, 255]))


def plot_bounding_boxes_from_info(obs, info):
    colors = info.get("objects_colors", {})
    for name, oinf in info["objects"].items():
        if type(oinf) == tuple:
            _plot_bounding_boxes_from_tuple(obs, name, oinf, colors)

        elif type(oinf) == list:
            for bb in oinf:
                _plot_bounding_boxes_from_tuple(obs, name, bb, colors)

        else:
            print(colored("the return type is not supported", "red"))


def _plot_bounding_boxes_from_tuple(obs, name, tup, colors):
    if len(tup) == 4:
        color = colors.get(name, np.array([0, 0, 0]))
        mark_bb(obs, tup, color)
    elif len(tup) == 7:
        bb = tup[:4]
        color = tup[4:]
        mark_bb(obs, bb, color)
    else:
        print(colored("the return type is not supported", "red"))


def showim(im):
    plt.imshow(im)
    plt.show()


def find_mc_objects(image, colors, closing_active=True, size=None, tol_s=10,
                    position=None, tol_p=2, min_distance=10, closing_dist=3,
                    minx=0, miny=0, maxx=160, maxy=210):
    """
    image: image to detect objects from
    color: fixed color of the object
    size: presupposed size
    tol_s: tolerance on the size
    position: presupposed position
    tol_p: tolerance on the position
    min_distance: minimal distance between two detected objects
    """

    masks = [cv2.inRange(image[miny:maxy, minx:maxx, :],
                         np.array(color), np.array(color)) for color in colors]
    for mask in masks:
        if mask.max() == 0:
            return []

    mask = sum(masks)
    if closing_active:
        closed = closing(mask, square(closing_dist))
        # closed = closing(closed, square(closing_dist))
    else:
        closed = mask
    contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, 1)
    detected = []
    # for contour in contours:
    #     cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x, y = x + minx, y + miny  # compensing cuttoff
        if size:
            if not assert_in((w, h), size, tol_s):
                continue
        if position:
            if not assert_in((x, y), position, tol_p):
                continue
        if min_distance:
            too_close = False
            for det in detected:
                if iou(det, (x, y, w, h)) > 0.05:
                    too_close = True
                    break
            if too_close:
                continue
        # if x < minx or x+w > maxx or y < miny or y+h > maxy:
        #     continue
        # detected.append((y, x, h, w))
        detected.append((x, y, w, h))
    return detected


def find_objects(image, color, closing_active=True, size=None, tol_s=10,
                 position=None, tol_p=2, min_distance=10, closing_dist=3,
                 minx=0, miny=0, maxx=160, maxy=210):
    """
    image: image to detect objects from
    color: fixed color of the object
    size: presupposed size
    tol_s: tolerance on the size
    position: presupposed position
    tol_p: tolerance on the position
    min_distance: minimal distance between two detected objects
    """
    mask = cv2.inRange(image[miny:maxy, minx:maxx, :], np.array(color), np.array(color))
    if closing_active:
        closed = closing(mask, square(closing_dist))
        # closed = closing(closed, square(closing_dist))
    else:
        closed = mask
    contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, 1)
    detected = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x, y = x + minx, y + miny  # compensing cuttoff
        if size:
            if not assert_in((w, h), size, tol_s):
                continue
        if position:
            if not assert_in((x, y), position, tol_p):
                continue
        if min_distance:
            too_close = False
            for det in detected:
                if iou(det, (x, y, w, h)) > 0.05:
                    too_close = True
                    break
            if too_close:
                continue
        # if x < minx or x+w > maxx or y < miny or y+h > maxy:
        #     continue
        # detected.append((y, x, h, w))
        detected.append((x, y, w, h))
    return detected


def make_darker(color, col_precent=0.8):
    """
    return a darker color
    """
    if not color:
        print("No color passed, using default black")
        return [0, 0, 0]
    return [int(col * col_precent) for col in color]
