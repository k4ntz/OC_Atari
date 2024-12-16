class GameObject:
    """
    The Parent Class of every detected object in the Atari games (Vision Processing mode)
    """
    GET_COLOR = False
    GET_WH = False

    def __init__(self, x, y, w, h, *args):
        self.rgb = (0, 0, 0)
        self._xy = x, y
        self.wh = w, h
        self._prev_xy = (0, 0)
        self.hud = False
        self._visible = True

    def __repr__(self):
        return f"{self.__class__.__name__} at ({self.x}, {self.y}), {self.wh}"

    @property
    def _nsrepr(self):
        if not self._visible:
            return [0, 0]
        return [self.x, self.y]

    @property
    def _ns_meaning(self):
        """NeuroSymbolic Meaning"""
        return "x, y"

    @property
    def _nslen(self):
        return len(self._nsrepr)

    @property
    def category(self):
        """
        The Category of class name of the game object (e.g. Player, Ball, ...).

        :type: str
        """
        return self.__class__.__name__

    @property
    def x(self):
        """
        The x positional coordinate on the image (on the horizontal axis).

        :type: int
        """
        return self._xy[0]

    @x.setter
    def x(self, value):
        self._xy = (value, self.y)

    @property
    def y(self):
        """
        The y positional coordinate on the image (on the vertical axis).

        :type: int
        """
        return self._xy[1]

    @y.setter
    def y(self, value):
        self._xy = (self.x, value)

    @property
    def w(self):
        """
        The width/horizontal size of the object (in pixels).

        :type: int
        """
        return self.wh[0]

    @w.setter
    def w(self, value):
        self.wh = (value, self.h)

    @property
    def h(self):
        """
        The height/vertical size of the object (in pixels).

        :type: int
        """
        return self.wh[1]

    @h.setter
    def h(self, value):
        self.wh = (self.w, value)

    @property
    def xy(self):
        """
        Both (x, y) positional coordinates in a tuple.

        :type: (int, int)
        """
        return self._xy

    @xy.setter
    def xy(self, xy):
        self._xy = xy

    # returns 2 lists with current and past coords
    @property
    def h_coords(self):
        """
        History of coordinates, i.e. current (x, y) and previous (x, y) position.

        :type: [(int, int), (int, int)]
        """
        return [self._xy, self._prev_xy]

    @property
    def dx(self):
        """
        The pixel movement correponding to: current_x - previous_x.

        :type: int
        """
        return self._xy[0] - self._prev_xy[0]

    @property
    def dy(self):
        """
        The pixel movement correponding to: current_y - previous_y.

        :type: int
        """
        return self._xy[1] - self._prev_xy[1]

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, v):
        self._visible = v

    def __bool__(self):
        return self._visible

    @property
    def xywh(self):
        """
        The (x, y, w, h) positional and width coordinates.

        :type: (int, int, int, int)
        """
        return self._xy[0], self._xy[1], self.wh[0], self.wh[1]

    @xywh.setter
    def xywh(self, xywh):
        self._xy = xywh[0], xywh[1]
        self.wh = xywh[2], xywh[3]

    def _save_prev(self):
        self._prev_xy = self._xy

    @property
    def center(self):
        """
        The center of the bounding box of the object.

        :type: (int, int)
        """
        return self._xy[0] + self.wh[0]/2, self._xy[1] + self.wh[1]/2

    def is_on_top(self, other):
        """
        Returns ``True`` if this and another gameobject overlap.

        :return: True if objects overlap
        :rtype: bool
        """
        return (other.x <= self.x <= other.x + other.w) and \
            (other.y <= self.y <= other.y + other.h)

    def manathan_distance(self, other):
        """
        Returns the manathan distance between the center of both objects.

        :return: Manathan distance (in pixel)
        :rtype: int
        """
        c0, c1 = self.center, other.center
        return abs(c0[0] - c1[0]) + abs(c0[1] - c1[1])

    def closest_object(self, others):
        """
        Returns the closest object from others, based on manathan distance between the center of both objects.

        :return: (Index, Object) from others
        :rtype: int
        """
        if len(others) == 0:
            return None
        return min(enumerate(others), key=lambda item: self.manathan_distance(item[1]))

    def _is_equivalent(self, other):
        if self.category != other.category:
            return False
        iou_value = self.iou(other)
        return iou_value > 0.8

    def iou(self, other):
        # Calculate the (x, y) coordinates of the intersection rectangle
        x1 = max(self.x, other.x)
        y1 = max(self.y, other.y)
        x2 = min(self.x + self.w, other.x + other.w)
        y2 = min(self.y + self.h, other.y + other.h)

        # Calculate the area of intersection rectangle
        inter_width = max(0, x2 - x1)
        inter_height = max(0, y2 - y1)
        inter_area = inter_width * inter_height

        # Calculate the area of both bounding boxes
        area_self = self.w * self.h
        area_other = other.w * other.h

        # Calculate the union area
        union_area = area_self + area_other - inter_area

        # Calculate IoU
        if union_area == 0:
            return 0  # Prevent division by zero
        return inter_area / union_area

    @property
    def properties(self):
        """
        All the properties of the object in a list.

        :return: The properties of the object.
        :rtype: list
        """
        ignore = ["properties", "GET_COLOR", "GET_WH",
                  "xy", "wh", "prev_xy", "h_coords", "xywh"]
        properties = [prop for prop in self.__dir__()]
        [properties.remove(p) for p in ignore if p in properties]
        return [prop for prop in properties
                if not prop.startswith("_") and
                not callable(self.__getattribute__(prop))]


class NoObject(GameObject):
    """
    This class represents a non-existent object. It is used to fill in the gaps when no object is detected.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(0, 0, 0, 0)
        self.nslen = 2

    def _save_prev(self):
        pass

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, NoObject)

    @property
    def _nsrepr(self):
        return [0 for _ in range(self.nslen)]

    def __repr__(self):
        # return "NaO"
        # return "\033[31m" + "NaO" + "\033[39m" # red color
        return "\033[34m" + "NaO" + "\033[39m"  # blue color
