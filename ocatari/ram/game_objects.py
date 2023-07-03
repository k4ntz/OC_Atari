class GameObject:
    """
    The Parent Class of every detected object in the Atari games (RAM Extraction mode)

    :ivar category: The Category of class name of the game object (e.g. Player, Ball).
    :type category: str
    :ivar x: The x positional coordinate on the image (on the horizontal axis).
    :type x: int
    :ivar y: The y positional coordinate on the image (on the vertical axis).
    :type y: int
    """
    GET_COLOR = False
    GET_WH = False
    _xy = None

    def __init__(self):
        self.rgb = (0, 0, 0)
        self._xy = (0, 0)
        self.wh = (0, 0)
        self._prev_xy = None
        self._orientation = 0
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
        """
        The width/horizontal size of the object (in pixels).

        :type: int
        """
        return self.wh[0]

    @w.setter
    def w(self, w):
        self.wh = w, self.h

    @property
    def h(self):
        """
        The height/vertical size of the object (in pixels).

        :type: int
        """
        return self.wh[1]
    
    @h.setter
    def h(self, h):
        self.wh = self.w, h

    @property
    def xy(self):
        """
        Both (x, y) positional coordinates in a tuple. 

        :type: (int, int)
        """
        return self._xy

    @xy.setter
    def xy(self, xy):
        # self._prev_xy = self._xy
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
        if self._prev_xy:
            return self._xy[0] - self._prev_xy[0]
        else:
            return 0

    @property
    def dy(self):
        """
        The pixel movement correponding to: current_y - previous_y.

        :type: int
        """
        if self._prev_xy:
            return self._xy[1] - self._prev_xy[1]
        else:
            return 0

    @property
    def xywh(self):
        """
        The (x, y, w, h) positional and width coordinates.

        :type: (int, int, int, int)
        """
        return self._xy[0], self._xy[1], self.wh[0], self.wh[1]

    @classmethod
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
        """
        The orientation of the object (if available), game specific.
        """
        return self._orientation

    @orientation.setter
    def orientation(self, o):
        self._orientation = o

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




class ScoreObject(GameObject):
    """
    This class represents the score of the player (or sometimes Enemy).

    :ivar value: The value of the score:
    :type value: int
    """
    def __init__(self):
        super().__init__()
        self.value = 0