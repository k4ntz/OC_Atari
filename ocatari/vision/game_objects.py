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

    def __repr__(self):
        return f"{self.__class__.__name__} at ({self._xy[0]}, {self._xy[1]}), {self.wh}"

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

    @property
    def y(self):
        """
        The y positional coordinate on the image (on the vertical axis).

        :type: int
        """
        return self._xy[1]

    @property
    def w(self):
        """
        The width/horizontal size of the object (in pixels).

        :type: int
        """
        return self.wh[0]

    @property
    def h(self):
        """
        The height/vertical size of the object (in pixels).

        :type: int
        """
        return self.wh[1]


    @property
    def xy(self):
        """
        Both (x, y) positional coordinates in a tuple. 

        :type: (int, int)
        """
        return self._xy

    @xy.setter
    def xy(self, xy):
        self._prev_xy = self._xy
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
    def xywh(self):
        """
        The (x, y, w, h) positional and width coordinates.

        :type: (int, int, int, int)
        """
        return self._xy[0], self._xy[1], self.wh[0], self.wh[1]


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
