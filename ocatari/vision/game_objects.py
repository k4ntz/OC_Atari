from typing import Tuple


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
        return f"{self.__class__.__name__} at ({self._xy[0]}, {self._xy[1]}), {self.wh}"
    
    @property
    def _nsrepr(self):
        if not self._visible:
            return [0, 0]
        return [self.x, self.y]
    
    @property
    def _ns_meaning(self):
        """NeuroSymbolic Meaning"""
        return [
            'POSITION',
        ]

    @property
    def _ns_types(self):
        return [Tuple[int, int]] 

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

    @property
    def properties(self):
        """
        All the properties of the object in a list.

        :return: The properties of the object.
        :rtype: list
        """
        ignore = ["properties", "GET_COLOR", "GET_WH", "xy", "wh", "prev_xy", "h_coords", "xywh"]
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
        return "\033[34m" + "NaO" + "\033[39m" # blue color