from enum import Enum


class Orientation(Enum):  # 16-wind compass directions
    N = 0
    NNE = 1
    NE = 2
    ENE = 3
    E = 4
    ESE = 5
    SE = 6
    SSE = 7
    S = 8
    SSW = 9
    SW = 10
    WSW = 11
    W = 12
    WNW = 13
    NW = 14
    NNW = 15


class GameObject:
    """
    The Parent Class of every detected object in the Atari games (RAM Extraction mode)

    :ivar category: The Category of class name of the game object (e.g. Player, Ball).
    :vartype category: str

    :ivar x: The x positional coordinate on the image (on the horizontal axis).
    :vartype x: int

    :ivar y: The y positional coordinate on the image (on the vertical axis).
    :vartype y: int

    :ivar w: The width/horizontal size of the object (in pixels).
    :vartype w: int
    
    :ivar h: The height/vertical size of the object (in pixels).
    :vartype h: int

    :ivar prev_xy: The positional coordinates x and y of the previous time step in a tuple.
    :vartype prev_xy: (int, int)

    :ivar xy: Both positional coordinates x and y in a tuple. 
    :vartype: (int, int)

    :ivar h_coords: History of coordinates, i.e. current (x, y) and previous (x, y) position.
    :vartype h_coords: [(int, int), (int, int)]

    :ivar dx: The pixel movement corresponding to: current_x - previous_x.
    :vartype dx: int

    :ivar dy: The pixel movement corresponding to: current_y - previous_y.
    :vartype dy: int

    :ivar xywh: The positional and width/height coordinates in a single tuple (x, y, w, h).
    :vartype xywh: (int, int, int, int)

    :ivar orientation: The orientation of the object (if available); game specific.
    :vartype orientation: int

    :ivar center: The center of the bounding box of the object.
    :vartype center: (int, int)

    :ivar hud: True, if part of the Heads Up Display, and thus not interactable.
    :vartype hud: bool
    """

    GET_COLOR = False
    GET_WH = False

    def __init__(self):
        self.rgb = (0, 0, 0)
        self._xy = (0, 0)
        self.wh = (0, 0)
        self._prev_xy = None
        self._orientation = None
        self.hud = False

    def __repr__(self):
        return f"{self.__class__.__name__} at ({self._xy[0]}, {self._xy[1]}), {self.wh}"

    @property
    def category(self):
        return self.__class__.__name__

    @property
    def x(self):
        return self._xy[0]

    @property
    def y(self):
        return self._xy[1]

    @property
    def w(self):
        return self.wh[0]

    @w.setter
    def w(self, w):
        self.wh = int(w), self.h

    @property
    def h(self):
        return self.wh[1]
    
    @h.setter
    def h(self, h):
        self.wh = self.w, int(h)

    @property
    def prev_xy(self):
        if self._prev_xy is not None:
            return self._prev_xy
        else:
            return self._xy

    @prev_xy.setter
    def prev_xy(self, newval):
        self._prev_xy = newval
    
    @property
    def prev_x(self):
        return self.prev_xy[0]
    
    @property
    def prev_y(self):
        return self.prev_xy[1]

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        self._xy = (int(xy[0]), int(xy[1]))

    @x.setter
    def x(self, x):
        self._xy = int(x), self.y

    @y.setter
    def y(self, y):
        self._xy = self.x, int(y)

    # returns 2 lists with current and past coords
    @property
    def h_coords(self):
        return [self._xy, self.prev_xy]

    @property
    def dx(self):
        return self._xy[0] - self.prev_xy[0]

    @property
    def dy(self):
        return self._xy[1] - self.prev_xy[1]

    @property
    def xywh(self):
        return self._xy[0], self._xy[1], self.wh[0], self.wh[1]

    def _save_prev(self):
        self._prev_xy = self._xy

    # @x.setter
    # def x(self, x):

    #     self._xy = x, self.xy[1]
    
    # @y.setter
    # def y(self, y):
    #     self._xy = self.xy[0], y

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, o):
        self._orientation = o

    @property
    def center(self):
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

        :return: True if objects overlap
        :rtype: bool
        """
        c0, c1 = self.center, other.center
        return abs(c0[0] - c1[0]) + abs(c0[1]- c1[1])
    
    def closest_object(self, others):
        """
        Returns the closest object from others, based on manathan distance between the center of both objects.

        :return: (Index, Object) from others
        :rtype: int
        """
        if len(others) == 0:
            return None
        return min(enumerate(others), key=lambda item: self.manathan_distance(item[1]))


class ValueObject(GameObject):
    """
    This class represents a game object that incorporates any notion of a value.
    For example:
    * the score of the player (or sometimes Enemy).
    * the level of useable/deployable resources (oxygen bars, ammunition bars, power gauges, etc.)
    * the clock/timer

    :ivar value: The value of the score.
    :vartype value: int
    """

    def __init__(self):
        super().__init__()
        self._value = 0
        self._prev_value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = None if value is None else int(value)

    @property
    def prev_value(self):
        if self._prev_value is not None:
            return self._prev_value
        else:
            return self._value

    def _save_prev(self):
        super()._save_prev()
        self._prev_value = self._value

    @property
    def value_diff(self):
        return self.value - self.prev_value
