import numpy as np
import cv2
from skimage.morphology import (disk, square)  # noqa
from skimage.morphology import (erosion, dilation, opening, closing, white_tophat, skeletonize)  # noqa
import matplotlib.pyplot as plt
from termcolor import colored
from collections import Counter


# to be removed
def bbs_extend(labels, key: str, stationary=False):
    labels['bbs'].extend([(*bb, "S" if stationary else "M", key) for bb in labels[key]])


def most_common_color(image, exclude_black=True):
    """
    Returns the most common color in the image.

    :param exclude_black: If True, exclude the black color from the taken into account, defaults to `True`
    :type exclude_black: bool
    """
    a2D = image.reshape(-1, image.shape[-1])
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    if exclude_black:
        return np.unravel_index(np.bincount(a1D)[1:].argmax()+1, col_range) # removing first el
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)


# to be removed
def bb_by_color(labels, obs, color, key, closing_active=True):
    print(colored("\n\n\n PLEASE DON'T USE, USE 'find_objects' instead\n\n\n", "red"))
    labels[key] = find_objects(obs, color, closing_active)
    bbs_extend(labels, key)


def assert_in(observed, expected, tol):
    """
    Asserts if the observed point is equal to the expected one with a given tolerance.
    True if ||observed - expected|| <= tol, with || the maximum over the two dimensions.

    :param observed: The observed value point (e.g. (x,y), (w,h))
    :type observed: (int, int)
    :param expected: The expected value point (also (x,y), (w,h))
    :type expected: (int, int)
    :param tol: A given tolerance.
    :type tol: int or (int, int)
    
    :return: True if points within the tolerance
    :rtype: bool
    """
    if type(tol) is int:
        tol = (tol, tol)
    return np.all([expected[i] + tol[i] >= observed[i] >= expected[i] - tol[i] for i in range(2)])


def iou(bb, gt_bb):
    """
    Computes the intersection over union between two bounding boxes. 
    |iou_image|

    :param bb: The bouding box of the detected object in (x, y, w, h) format
    :type bb: (int, int, int, int)
    :param gt_bb: The ground truth bouding box
    :type gt_bb: (int, int, int, int)
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
    Marks a point on the image at the (x,y) position (inplace)

    :param image_array: The image to mark the point on
    :type image_array: RGB np.array
    :param x: The x coordinate of the point
    :type x: int
    :param y: The y coordinate of the point
    :type y: int
    :param color: The rgb values of the point.
    :type color: (int, int, int)
    :param size: The size of the point
    :type size: int
    :param show: If ``True``, shows the image using matplotlib
    :type show: bool
    :param cross: If ``True``, places a diagonal cross, else place a square
    :type cross: bool
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
    Marks a bounding box on the image.

    :param image_array: The image to mark the point on
    :type image_array: RGB np.array
    :param bb: The bouding box of the detected object in (x, y, w, h) format
    :type bb: (int, int, int, int)
    :param color: The rgb values of the point.
    :type color: (int, int, int)
    :param surround: If ``True``, place the bouding box with an offset of 1 pixel to surround the object
    :type surround: bool
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
    bottom = min(208, y + h)
    right = min(158, x + w)
    try:
        image_array[y:bottom + 1, x] = color
        image_array[y:bottom + 1, right] = color
        image_array[y, x:right + 1] = color
        image_array[bottom, x:right + 1] = color
    except IndexError:
        pass
        # import ipdb; ipdb.set_trace()


def plot_bounding_boxes(obs, bbs, objects_colors):
    for bb in bbs:
        try:
            mark_bb(obs, bb, np.array([cv for cv in objects_colors[bb[5]]]))
        except KeyError as err:
            print(err)
            mark_bb(obs, bb, np.array([255, 255, 255]))


def showim(image):
    """
    Display the given in a matplolib.pyplot plot.

    :param image: The image to mark the point on
    :type image: np.array
    """
    plt.imshow(image)
    plt.show()


def find_mc_objects(image, colors, size=None, tol_s=10, position=None, tol_p=2, 
                    min_distance=10, closing_active=True, closing_dist=3,
                    minx=0, miny=0, maxx=160, maxy=210, all_colors=True):
    """
    Finds the multicolors objects in the image. 
        
    This functions is used to detect object in e.g. Atlantis (depicted bellow). 
    
    |atlantis_image|

    :param image: The image to mark the point on
    :type image: np.array
    :param colors: The colors of the object
    :type colors: list of (int, int, int)
    :param size: presupposed size of the targeted object (to detect)
    :type size: int or (int, int)
    :param tol_s: tolerance on the presupposed size of the targeted object
    :type tol_s: int or (int, int)
    :param size: presupposed size of the targeted object (to detect)
    :type size: int or (int, int)
    :param tol_s: tolerance on the presupposed size of the targeted object
    :type tol_s: int or (int, int)
    :param position: presupposed position of the targeted object (to detect)
    :type position: int or (int, int)
    :param tol_p: tolerance on the presupposed position of the targeted object
    :type tol_p: int or (int, int)
    :param min_distance: tolerance on the presupposed position of the targeted object
    :type min_distance: int
    :param closing_active: If true, gathers in one bounding box the instances that are less than \
    `closing_dist` 
    :type closing_active: bool
    :param closing_dist: The closing distance, for the under which two (or more) instances are merged \
    into one bounding box.
    :type closing_dist: int
    :param minx: minimum x position where the object can be located
    :type minx: int
    :param miny: minimum y position where the object can be located
    :type miny: int
    :param maxx: maximum x position where the object can be located
    :type maxx: int
    :param maxy: maximum y position where the object can be located
    :type maxy: int
    :param all_colors: If ``True``, only return the object if every given color in `colors` is present in the image
    :type all_colors: bool


    :return: a list of tuple boxing boxes
    :rtype: list of (int, int, int, int)
    """
    masks = [cv2.inRange(image[miny:maxy, minx:maxx, :],
                         np.array(color), np.array(color)) for color in colors]
    if all_colors:
        for mask in masks:
            if mask.max() == 0:
                return []
    mask = sum(masks)
    # if mask.max() > 0:
        # showim(mask)
        # import ipdb; ipdb.set_trace()
    # if not all_colors and mask.max():
    #     import ipdb;ipdb.set_trace()
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
        if all_colors:
            all_contained = True
            for k in range(len(masks)):
                contained = False
                for i in range(w):
                    for j in range(h):
                        try:
                            if masks[k][y+j-miny][x+i-minx]:
                                contained = True
                                break
                        except:
                            continue

                    if contained:
                        break
                if not contained:
                    all_contained = False
                    break
            if all_contained:
                detected.append((x, y, w, h))
        else:
            detected.append((x, y, w, h))
    return detected


def color_analysis(image, bbox, exclude=[]):
    """
    Returns a Counter of all the detected colors in the bounding box

    :param image: The image to mark the point on
    :type image: np.array
    :param bb: The bouding box where to perform the color analysis
    :type bb: (int, int, int, int)
    :param exclude: A list of color to exclude
    :type exclude: list of (int, int, int)

    :return: A `collections.Counter <https://docs.python.org/3/library/collections.html#collections.Counter>`_ \
        of the detected colors
    :rtype: list of (int, int, int)
    """
    x, y, w, h = bbox
    subpart = image[y:y+h, x:x+w, :]
    w,h,c = subpart.shape
    subpart = list(map(tuple, subpart.reshape(w*h, c)))
    for excolor in exclude:
        subpart = [el for el in subpart if el != tuple(excolor)]
    return Counter(subpart)


def find_objects(image, color, size=None, tol_s=10,
                 position=None, tol_p=2, min_distance=10,
                 closing_active=True, closing_dist=3,
                 minx=0, miny=0, maxx=160, maxy=210):
    """
    Finds the single colored objects in the image.

    :param image: The image to mark the point on
    :type image: np.array
    :param color: The color of the object
    :type color: list of (int, int, int)
    :param size: presupposed size of the targeted object (to detect)
    :type size: int or (int, int)
    :param tol_s: tolerance on the presupposed size of the targeted object
    :type tol_s: int or (int, int)
    :param size: presupposed size of the targeted object (to detect)
    :type size: int or (int, int)
    :param tol_s: tolerance on the presupposed size of the targeted object
    :type tol_s: int or (int, int)
    :param position: presupposed position of the targeted object (to detect)
    :type position: int or (int, int)
    :param tol_p: tolerance on the presupposed position of the targeted object
    :type tol_p: int or (int, int)
    :param closing_active: If true, gathers in one bounding box the instances that are less than \
    `closing_dist` away.
    :type closing_active: bool
    :param closing_dist: The closing distance, for the under which two (or more) instances are merged \
    into one bounding box.
    :type closing_dist: int
    :param minx: minimum x position where the object can be located
    :type minx: int
    :param miny: minimum y position where the object can be located
    :type miny: int
    :param maxx: maximum x position where the object can be located
    :type maxx: int
    :param maxy: maximum y position where the object can be located
    :type maxy: int

    :return: a list of tuple boxing boxes
    :rtype: list of (int, int, int)
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


def find_rope_segments(image, color, seg_height=(2, 5), minx=0, miny=0, maxx=160, maxy=210):
    """
    Finds the rope segments (max rope width of 1) of a displayed rope.
    
    :param image: The image to mark the point on
    :type image: np.array
    :param color: The color of the object
    :type color: list of (int, int, int)
    :param seg_height: interval in which segments are considered
    :type seg_height: int or (int, int)
    :param minx: minimum x position where the object can be located
    :type minx: int
    :param miny: minimum y position where the object can be located
    :type miny: int
    :param maxx: maximum x position where the object can be located
    :type maxx: int
    :param maxy: maximum y position where the object can be located
    :type maxy: int

    :return: a list of tuple boxing boxes
    :rtype: list of (int, int, int)
    """
    mask = cv2.inRange(image[miny:maxy, minx:maxx, :], np.array(color), np.array(color))
    detected = []
    for j in range(mask.shape[1]):
        col = mask[:,j].astype(bool)
        if col.all() or (~col).all():
            continue
        cur = False
        begin = 0
        for i, el in enumerate(col + [0]):
            if el:
                if not cur: 
                    begin = i
                cur = True
            else:
                if cur:
                    length = i-begin
                    if seg_height[0] <= length <= seg_height[1]:
                        detected.append([minx+j, miny+begin, 1, length])
                cur = False
    return detected


def find_rectangle_objects(image, color, max_size=None, minx=0, miny=0, maxx=160, maxy=210):
    """
    Finds rectangle objects with a given maximum size.
    
    :param image: The image in which the objects are displayed
    :type image: RGB np.array
    :param color: The color of the object
    :type color: list of (int, int, int)
    :param max_size: The maximum size of the objects
    :type max_size: (int, int)
    :type minx: int
    :param miny: minimum y position where the object can be located
    :type miny: int
    :param maxx: maximum x position where the object can be located
    :type maxx: int
    :param maxy: maximum y position where the object can be located
    :type maxy: int

    :return: a list of tuple boxing boxes
    :rtype: list of (int, int, int)
    """
    mask = cv2.inRange(image[miny:maxy, minx:maxx, :], np.array(color), np.array(color))
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    detected = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # smaller particles are detected but smaller than the given size (for cut particles)
        w1, h1 = max_size
        if w <= w1 or h <= h1:
            x, y = x + minx, y + miny  # compensating cutoff
            if not detected.__contains__((x, y, w, h)):
                detected.append((x, y, w, h))
        else:
            detected.extend(_find_rectangles_in_bb(mask.copy(), (x, y, w, h), max_size, minx, miny))
    return detected

def _find_rectangles_in_bb(mask, bb, size, minx, miny):
    bounding_boxes = list()
    (offx,offy) = size
    (x,y,w,h) = bb
    mask = mask[y:y + h, x:x + w]
    # np.array_equal(mask[i + a, j + b], black), when image instead of mask
    black = 0

    row = 0
    for line in mask:
        if row + offy > mask.shape[0]:
            break
        column = 0
        for element in line:
            if column+offx > mask.shape[1]:
                break
            if not element == black:
                # searching
                rect = True
                for a in range(offy):
                    for b in range(offx):
                        try:
                            if mask[row + a, column + b] == black:
                                rect = False
                                break
                        except IndexError:
                            import ipdb; ipdb.set_trace()
                    if not rect:
                        break

                # delete Pixels from mask, if found, to avoid intersections
                if rect:
                    for a in range(offy):
                        for b in range(offx):
                            mask[row + a, column + b] = black
                    bounding_boxes.append((x+minx+column, y+miny+row, offx, offy))
            column += 1
        row += 1

    return bounding_boxes


def find_objects_in_color_range(image, color_min, color_max, size=None, tol_s=10,
                                position=None, tol_p=2, min_distance=10,
                                closing_active=True, closing_dist=3,
                                minx=0, miny=0, maxx=160, maxy=210):
    """
    Finds the single colored objects in the image.

    :param image: image to mark the point on
    :type image: np.array
    :param color_min: lower bound of the color spectrum
    :type color_min: (int, int, int)
    :param color_max: upper bound of the color spectrum
    :type color_max: (int, int, int)
    :param size: presupposed size of the targeted object (to detect)
    :type size: int or (int, int)
    :param tol_s: tolerance on the presupposed size of the targeted object
    :type tol_s: int or (int, int)
    :param size: presupposed size of the targeted object (to detect)
    :type size: int or (int, int)
    :param tol_s: tolerance on the presupposed size of the targeted object
    :type tol_s: int or (int, int)
    :param position: presupposed position of the targeted object (to detect)
    :type position: int or (int, int)
    :param tol_p: tolerance on the presupposed position of the targeted object
    :type tol_p: int or (int, int)
    :param closing_active: If true, gathers in one bounding box the instances that are less than \
    `closing_dist` 
    :type closing_active: bool
    :param closing_dist: The closing distance, for the under which two (or more) instances are merged \
    into one bounding box.
    :type closing_dist: int
    :param minx: minimum x position where the object can be located
    :type minx: int
    :param miny: minimum y position where the object can be located
    :type miny: int
    :param maxx: maximum x position where the object can be located
    :type maxx: int
    :param maxy: maximum y position where the object can be located
    :type maxy: int

    :return: a list of tuple boxing boxes
    :rtype: list of (int, int, int)
    """    
    mask = cv2.inRange(image[miny:maxy, minx:maxx, :], np.array(color_min), np.array(color_max))
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
    Return a darker color.

    :param color: upper bound of the color spectrum
    :type color: (int, int, int)
    :param col_precent: the luminosity reduction coefficient (between 0 and 1)
    :type col_precent: float

    :return: the darker color
    :rtype: (int, int, int)
    """
    if not color:
        print("No color passed, using default black")
        return [0, 0, 0]
    return [int(col * col_precent) for col in color]


def to_rgba(color):
    return np.concatenate([np.array(color)/255, [.7]])
