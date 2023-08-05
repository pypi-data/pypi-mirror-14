from xml.etree.ElementTree import ElementTree as Tree
import base64 as b64
import zlib
import math
from os import path

import pygame


class MapError(Exception):
    """Exception for points outside the map.*
    """
    def __init__(self, x, y, max_x, max_y):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y

    def __str__(self):
        self.fin = ''
        if self.x > self.max_x:
            self.fin += 'x should be reduced by ' + str(self.x -
              self.max_x)
            if self.y > self.max_y:
                self.fin += ', '
        if self.y > self.max_y:
            self.fin += 'y should be reduced by ' + str(self.y -
              self.max_y)
        return self.fin


class MAP:
    """Basic map class.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []

    def __repr__(self):
        if self.objects:
            self.fin = 'Map ' + str(self.width) + "x" + str(self.height) +\
              ":\n"
            self.count = 1
            for obj in self.objects:
                self.fin += str(self.count) + '. ' + str(obj) + '\n'
                self.count += 1
            return self.fin[:-1]
        else:
            return "Empty Map " + str(self.width) + "x" + str(self.height)\
              + ":"

    def __contains__(self, item):
        self.item = item
        return self.item in self.objects

    def __bool__(self):
        return bool(self.objects)

    def add_obj(self, obj):
        """Function that adds object(point, rect...) to map.
        """
        self.obj = obj
        if type(self.obj) == point:
            if self.obj.x > self.width or self.obj.y > self.height:
                raise MapError(obj.x, obj.y, self.width, self.height)
        self.objects.append(self.obj)

    def at(self, x, y):
        """Return generator of all items in map on x, y coordinates.
        """
        self.x = x
        self.y = y
        for obj in self.objects:
            if type(obj) == point:
                if obj.x == self.x and obj.y == self.y:
                    yield obj
            elif type(obj) == group_of_points:
                self.T = False
                for POINT in obj.at(self.x, self.y):
                    yield POINT
                    self.T = True
                if self.T:
                    yield obj
            elif type(obj) == rect:
                if obj.at(self.x, self.y):
                    yield obj


class point:
    """Basic point class.
    """
    def __init__(self, x, y, Map, description='Unknown', quiet=False):
        self.x = x
        self.y = y
        self.Map = Map
        self.description = description
        if not quiet:
            self.Map.add_obj(self)
        self.name = self.description

    def __str__(self):
        return self.description + ' @ ' + str(self.x) + ', ' + str(self.y)

    __repr__ = __str__

    def distance(self, other):
        """Calculates distance between this and given point.
        """
        self.other = other
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y)
          ** 2)

    def get_xy(self):
        """Returns point's x and y.
        """
        return (self.x, self.y)


class line:
    """Basic line class.
    """
    def __init__(self, points, Map, description='Unknown', quiet=False,
      from_line_seg=False):
        self.points = points
        if from_line_seg:
            self.segment = from_line_seg
        else:
            self.segment = line_seg(self.points, Map, quiet=True,
              from_line=self)
        self.Map = Map
        self.name = self.description = description
        if not quiet:
            self.Map.add_obj(self)
        self.dif = self.x_dif, self.y_dif = self.points[1].x -\
          self.points[0].x, self.points[1].y - self.points[0].y
        self.a = self.y_dif / self.x_dif
        self.b = self.points[0].y - self.a * self.points[0].x
        self.fnc = lambda x: self.a * x + self.b

    def __str__(self):
        return self.description + ' line (' + str(self.points[0]) + ', ' +\
          str(self.points[1]) + ')'

    __repr__ = __str__

    def __contains__(self, other):
        self.other = other
        if type(self.other) == point:
            return self.fnc(self.other.x) == self.other.y
        elif type(self.other) == group_of_points:
            for P in self.other.points:
                if not P in self:
                    return False
            return True
        elif type(self.other) == rect:
            if self.points[0] in self.other or self.points[1] in \
              self.other:
                return True
            self.lines = []
            for p in self.other.points():
                self.lines.append(line((self.points[0], p), self.Map,
                  quiet=True))
            self.angles = []
            for l in self.lines:
                self.angles.append(l.get_f_angle(0) + 360)
            if min(self.angles) <= self.get_f_angle(0) + 360 <=\
              max(self.angles):
                return True
        return False

    def get_angle(self):
        """Returns line smallest angle (0-90).*
        """
        return self.segment.get_angle()

    def get_f_angle(self, p_index):
        """Returns full line angle (0-360).
        """
        return self.segment.get_f_angle(p_index)

    def perpend(self, point, quiet=False):
        """Returns perpendicular that goes through given point.
        """
        self.d = direction(point, (self.get_f_angle(0) + 90) % 360,
          self.Map, quiet=quiet)
        return self.d.line(quiet)

    def collide(self, L):
        """Returns point of intersection of lines.
        """
        self.L = L
        x = -(self.b - self.L.b)/(self.a - self.L.a)
        y = self.fnc(x)
        return (x, y)


class line_seg:
    """Basic line segment class.
    """
    def __init__(self, points, Map, description='Unknown', quiet=False,
          from_line=False):
        self.points = points
        self.Map = Map
        self.description = description
        if not quiet:
            self.Map.add_obj(self)
        self.name = self.description
        self.dif = self.x_dif, self.y_dif = (abs(self.points[0].x -
          self.points[1].x), abs(self.points[0].y - self.points[1].y))
        if self.y_dif == 0:
            self.cof = "horizontal"
        else:
            self.cof = self.x_dif / self.y_dif
        if from_line:
            self.line = from_line
        else:
            self.line = line(self.points, self.Map, quiet=True,
              from_line_seg=self)

    def __len__(self):
        return int(self.points[0].distance(self.points[1]))

    def __str__(self):
        return self.description + ' line segment (' + str(self.points[0]) +\
          ', ' + str(self.points[1]) + ')'

    __repr__ = __str__

    def __contains__(self, other):
        self.other = other
        if type(self.other) == point:
            if self.other in self.points:
                return True
            self.l = line((self.points[0], self.other), Map, quiet=True)
            if self.l.cof == self.cof:
                if self.cof == "horizontal":
                    if self.points[0].y > self.points[1].y:
                        if self.points[0].y > self.other.y >\
                          self.points[1].y:
                            return True
                    else:
                        if self.points[0].y < self.other.y <\
                          self.points[1].y:
                            return True
                else:
                    if (self.points[0].y > self.other.y > self.points[1].y
                      or self.points[0].y < self.other.y <
                      self.points[1].y) and (self.points[0].x >
                      self.other.x > self.points[1].x or self.points[0].x <
                      self.other.x < self.points[1].x):
                        return True
        elif type(self.other) == group_of_points:
            for P in self.other.points:
                if not P in self:
                    return False
            return True
        elif type(self.other) == rect:
            if self.other in self.line:
                if ((self.points[0].x >= self.points[1].x and self.other.x
                  <= self.points[0].x) or (self.points[1].x >
                  self.points[0].x and self.other.x <= self.points[1].x))\
                  and (self.points[0].y >= self.points[1].y and
                  self.other.y <= self.points[0].y) or (self.points[1].y >
                  self.points[0].y and self.other.y <= self.points[1].y):
                    return True
        return False

    def get_angle(self):
        """Returns line smallest angle(0-90).*
        """
        if self.cof == "horizontal":
            return 90.0
        return math.degrees(math.atan(self.x_dif / self.y_dif))

    def get_f_angle(self, p_index):
        """Returns full line angle (0-360).
        """
        self.a = self.get_angle()
        self.x1, self.y1 = self.points[p_index].get_xy()
        self.x2, self.y2 = self.points[not p_index].get_xy()
        if self.x1 > self.x2:
            if self.y1 > self.y2:
                self.a = 180 - self.a
        else:
            if self.y1 > self.y2:
                self.a += 180
            else:
                self.a = 360 - self.a
        self.a %= 360
        return self.a


def q_points(x1, y1, x2, y2, Map):
    """Returns points for line and line_seg.
    """
    p1 = point(x1, y1, Map, quiet=True)
    p2 = point(x2, y2, Map, quiet=True)
    return (p1, p2)


class ray:
    """Basic ray class.
    """
    def __init__(self, start_p, some_p, Map, description='Unknown',
          quiet=False):
        self.start_p = start_p
        self.some_p = some_p
        self.line = line((self.start_p, self.some_p), Map, quiet=True,
          from_line_seg=True)
        self.line_seg = self.line.segment
        self.Map = Map
        if not quiet:
            self.Map.add_obj(self)
        self.description = description
        self.name = self.description
        self.dif = self.x_dif, self.y_dif = (abs(self.start_p.x -
          self.some_p.x), abs(self.start_p.y - self.some_p.y))
        if self.y_dif == 0:
            self.cof = "horizontal"
        else:
            self.cof = self.x_dif / self.y_dif

    def __contains__(self, other):
        self.other = other
        if type(self.other) == point:
            if self.other == self.start_p:
                return True
            self.l = line((self.start_p, self.other), Map, quiet=True)
            if self.l.cof == self.cof:
                if self.cof == "horizontal":
                    if self.start_p.y > self.some_p.y:
                        if self.start_p.y > self.other.y:
                            return True
                    else:
                        if self.start_p.y < self.other.y:
                            return True
                else:
                    if ((self.start_p.y > self.other.y and self.start_p >
                      self.some_p) or (self.start_p.y < self.other.y and
                      self.start_p.y < self.some_p.y)) and ((self.start_p.x
                      > self.other.x and self.start_p > self.some_p) or
                      (self.start_p.x < self.other.x and self.start_p >
                      self.some_p)):
                        return True
        elif type(self.other) == group_of_points:
            for P in self.other.points:
                if not P in self:
                    return False
            return True
        return False


class direction:
    """Basic direction class.
    """
    def __init__(self, point, angle, Map, description='Unknown',
        quiet=False):
        self.angle = angle
        self.rd = math.radians(self.angle)
        self.point = point
        self.description = description
        self.Map = Map
        if not quiet:
            self.Map.add_obj(self)

    def __str__(self):
        return self.description + " direction @" + str(self.point.x) +\
          ", " + str(self.point.y) + "; angle: " + str(self.angle)

    __repr__ = __str__

    def get_pos(self, distance):
        """Gets point of direction with given distance.
        """
        self.distance = distance
        if self.angle == 0:
            return point(self.point.x, self.point.y - self.distance,
              self.Map, quiet=True)
        else:
            self.x = math.sin(self.rd) * self.distance
            self.y = math.cos(self.rd) * self.distance
            return point(self.point.x + self.x, self.point.y - self.y,
              self.Map, quiet=True)

    def move(self, distance):
        """'Moves' directions point.
        """
        self.point.x, self.point.y = self.get_pos(distance).get_xy()

    def set_angle(self, angle):
        """Sets new angle.
        """
        self.angle = angle
        self.rd = math.radians(self.angle)

    def get_angle(self):
        """Returns direction angle.
        """
        return self.angle

    def ch_angle(self, change):
        """Changes angle for given value.
        """
        self.angle += change
        self.rd = math.radians(self.angle)

    def line(self, quiet=False):
        """Returns direction's line.
        """
        return line((self.point, self.get_pos(10)), self.Map,
          self.description, quiet)


class group_of_points:
    """Class for group of points.
    """
    def __init__(self, Map, description='Unknown', *points, quiet=False):
        self.Map = Map
        self.description = description
        self.points = points
        self.counter = 0
        if not quiet:
            self.Map.add_obj(self)
        self.name = self.description

    def __str__(self):
        self.fin = self.description + ' group ['
        for Point in self.points:
            self.fin += str(Point) + '; '
        self.fin = self.fin[:-2] + ']'
        return self.fin

    __repr__ = __str__

    def at(self, x, y):
        """Return generator of all items in group on x, y coordinates.
        """
        self.x = x
        self.y = y
        for Point in self.points:
            if Point.x == self.x and Point.y == self.y:
                yield Point


class rect:
    """Basic map rect class.
    """
    def __init__(self, x, y, width, height, Map, description='Unknown',
          quiet=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Map = Map
        if not quiet:
            self.Map.add_obj(self)
        self.description = description
        self.name = self.description

    def __str__(self):
        return self.description + ' rect ' + str(self.width) + 'X' +\
          str(self.height) + ' @ ' + str(self.x) + ', ' + str(self.y)

    __repr__ = __str__

    def __contains__(self, item):
        self.item = item
        if type(self.item) == point:
            if self.at(self.item.x, self.item.y):
                return True
        elif type(self.item) == group_of_points:
            for p in self.item.points:
                if not p in self:
                    return False
            return True
        elif type(self.item) == rect:
            if self.x <= self.item.x and self.y <= self.item.y and self.x\
              + self.width >= self.item.x + self.item.width and self.y +\
              self.height >= self.item.y + self.item.height:
                return True
            return False
        else:
            raise TypeError("'in <rect>' doesn't support " +
              repr(self.item))

    def at(self, x, y):
        """Test if point is in rect.*
        """
        return self.x + self.width >= x >= self.x and self.y +\
          self.height >= y >= self.y

    def collide(self, other):
        """Tests colliding with given rect.
        """
        self.fin = [0, 0, 0, 0]
        if self.y + self.height > other.y and self.y < other.y +\
          other.height:
            if other.x + other.width > self.x + self.width > other.x:
                self.fin[0] = self.x + self.width - other.x
            if self.x + self.width > other.x + other.width > self.x:
                self.fin[2] = other.x + other.width - self.x
        if self.x + self.width > other.x and self.x < other.x +\
          other.width:
            if other.y + other.height > self.y + self.height > other.y:
                self.fin[1] = self.y + self.height - other.y
            if self.y + self.height > other.y + other.height > self.y:
                self.fin[3] = other.y + other.height - self.y
        return self.fin

    def touch(self, other):
        """Tests touching with other rect.
        """
        self.fin = [False, False, False, False]
        if self.y + self.height > other.y and self.y < other.y +\
          other.height:
            if self.x + self.width == other.x:
                self.fin[0] = True
            if other.x + other.width == self.x:
                self.fin[2] = True
        if self.x + self.width > other.x and self.x < other.x +\
          other.width:
            if self.y + self.height == other.y:
                self.fin[1] = True
            if other.y + other.height == self.y:
                self.fin[3] = True
        return self.fin

    def points(self, quiet=True):
        """Returns rect's points.
        """
        yield point(self.x, self.y, self.Map, quiet=quiet)
        yield point(self.x + self.width, self.y, self.Map, quiet=quiet)
        yield point(self.x, self.y + self.height, self.Map, quiet=quiet)
        yield point(self.x + self.width, self.y + self.height, self.Map,
          quiet=quiet)

    def get_xy(self):
        """Returns rect's coordinates.
        """
        return (self.x, self.y)


class circle:
    """Basic circle class.
    """
    def __init__(self, centre, radius, Map, description='Unknown',
         quiet=False):
        self.centre = centre
        self.x, self.y = self.centre.get_xy()
        self.radius = radius
        self.Map = Map
        if not quiet:
            self.Map.add_obj(self)
        self.description = description

    def __repr__(self):
        return 'circle ' + self.description + ' @' + str(self.x) + ', ' +\
          str(self.y) + '; r=' + str(self.radius)

    __str__ = __repr__

    def __contains__(self, p):
        return self.centre.distance(p) <= self.radius

    def distance(self, l):
        """Returns distance between centre and line.
        """
        self.l = l
        self.p = self.l.collide(self.l.perpend(self.centre))
        return self.centre.distance(self.p)


class element:
    """Basic tilemap element class.*
    """
    def __init__(self, name, props, Map):
        self.name = name

        self.Map = Map

        self.props = props
        self.opts = []
        for prop in dict(self.props):
            self.opts.append(prop)
            if not self.props[prop]:
                del self.props[prop]

    @classmethod
    def __tmx_init__(cls, obj, Map):
        name = ""
        if "name" in obj.attrib:
            name = obj.attrib["name"]
        properties = {}
        if obj.find("properties"):
            for prop in obj.find("properties"):
                properties[prop.attrib["name"]] = prop.attrib["value"]
        if cls.__tmx_init__.__func__ == element.__tmx_init__.__func__:
            return cls(name, properties, Map)
        else:
            cls.name = name
            cls.properties = properties


class layer(element):
    """Basic tilemap layer (Tile Layer) class.*
    """
    def __init__(self, name, props, mapping, Map):
        super().__init__(name, props, Map)
        self.mapping = mapping
        self.Map = Map
        self.screen = self.Map.screen
        self.screen_w, self.screen_h = self.screen.get_size()
        self.tiles = self.Map.images
        self.tile_width, self.tile_height = self.Map.tile_size
        self.x = self.y = 0
        self.d = {}
        for t in self.tiles:
            for x in range(t.size):
                self.d[t.first + x] = (t, x)

    @classmethod
    def __tmx_init__(cls, obj, Map):
        super().__tmx_init__(obj, Map)
        BIN = zlib.decompress(b64.b64decode(obj.find("data").text[4:-3]))
        mapping = [[] for x in range(int(Map.t_height))]
        for p, x in enumerate(BIN):
            if not p % 4:
                mapping[int(p/4/Map.t_width)].append(int(x))
        if cls.__tmx_init__.__func__ == layer.__tmx_init__.__func__:
            return cls(cls.name, cls.properties, mapping, Map)
        else:
            cls.mapping = mapping

    def set_pos(self, x, y):
        """Sets position of layer.*
        """
        self.x = x
        self.y = y

    def get_tiles(self):
        x_s = int(self.x / self.tile_width)
        x_o = self.x % self.tile_width
        x_e = int(x_s + self.screen_w / self.tile_width + bool(x_o))
        y_s = int(self.y / self.tile_height)
        y_o = self.y % self.tile_height
        y_e = int(y_s + self.screen_h / self.tile_height + bool(y_o))
        return (x_s, x_o, x_e, y_s, y_o, y_e)

    def blit(self):
        """Blits layer.*
        """
        pos = self.get_tiles()
        for p_y, y in enumerate(self.mapping[pos[3]:pos[5]]):
            for p_x, x in enumerate(y[pos[0]:pos[2]]):
                if x:
                    self.d[x][0].blit((p_x * self.tile_width - pos[1], p_y *
                      self.tile_height - pos[4]), self.d[x][1])


class Object(element):
    """Basic tilemap object class.*
    """
    def __init__(self, name, Type, props, Map, obj):
        super().__init__(name, props, Map)
        self.type = Type
        self.obj = obj
        self.Map.objects.append(self)
        self.Map.in_map.add_obj(self)

    @classmethod
    def __tmx_init__(cls, obj, Map):
        super().__tmx_init__(obj, Map)
        Type = ""
        x = int(obj.attrib["x"])
        y = int(obj.attrib["y"])
        width = height = 0
        if "type" in obj.attrib:
            Type = obj.attrib["type"]
        if "width" in obj.attrib:
            width = int(obj.attrib["width"])
        if "height" in obj.attrib:
            height = int(obj.attrib["height"])
        if (not (width or height)) and Map.gid_point:
            Obj = point(x, y, Map.in_map, cls.name, True)
        elif (not width and height) and Map.gid_line:
            Obj = line(q_points(x, y, x + width, y + height, Map.in_map),
              Map.in_map, cls.name, True)
        else:
            Obj = rect(x, y, width, height, Map.in_map, cls.name, True)
        if cls.__tmx_init__.__func__ == Object.__tmx_init__.__func__:
            return cls(cls.name, Type, cls.properties, Map, Obj)
        else:
            cls.type = Type
            cls.x, cls.y = x, y
            cls.width, cls.height = width, height
            cls.obj = Obj

    def __str__(self):
        self.fin = "object " + str(self.obj)
        if self.opts:
            self.fin += '; ['
            for opt in self.opts:
                self.fin += str(opt)
                self.fin += ', '
            self.fin = self.fin[:-2]
            self.fin += ']'
        if self.props:
            self.fin += '; {'
            for prop in self.props:
                self.fin += str(prop)
                self.fin += ': '
                self.fin += str(self.props[prop])
                self.fin += ', '
            self.fin = self.fin[:-2]
            self.fin += '}'
        return self.fin

    __repr__ = __str__


class map_obj(Object):
    """Blitable tilemap object class.
    """
    def __init__(self, name, Type, props, picture, Map, obj):
        super().__init__(name, Type, props, Map, obj)
        self.picture = picture
        self.x, self.y = self.obj.get_xy()

    @classmethod
    def __tmx_init__(cls, obj, Map):
        super().__tmx_init__(obj, Map)
        if cls.__tmx_init__.__func__ == map_obj.__tmx_init__.__func__:
            return cls(cls.name, cls.type, cls.properties, None, Map,
              cls.obj)

    def blit(self):
        """Blits object.*
        """
        if self.picture:
            self.Map.screen.blit(self.picture, self.get_blit())

    def get_blit(self):
        """Returns where object should be blitted.*
        """
        return (self.x - self.Map.x, self.y - self.Map.y)

    def set_position(self, x, y):
        """Sets object position.
        """
        self.x = x
        self.y = y

    def move(self, x, y):
        """Moves object.
        """
        self.x += x
        self.y += y


class Subject(map_obj):
    """Basic centre tilemap object class (subclass of :py:class:`map_obj`).
    """
    def __init__(self, name, Type, props, picture, Map, obj):
        super().__init__(name, Type, props, picture, Map, obj)
        self.Map.set_camera_pos(self.x, self.y)

    def set_position(self, x, y):
        """Sets object position.
        """
        super().set_position(x, y)
        self.Map.set_camera_pos(self.x, self.y)

    def move(self, x, y):
        """Moves object.
        """
        super().move(x, y)
        self.Map.set_camera_pos(self.x, self.y)


class objectgroup(element):
    """Basic tilemap objectgroup (Object Layer) class.
    """
    def __init__(self, name, props, objects, Map):
        super().__init__(name, props, Map)
        self.objects = objects

    def __iter__(self):
        for o in self.objects:
            yield o

    @classmethod
    def __tmx_init__(cls, obj, Map):
        super().__tmx_init__(obj, Map)
        objects = []
        for P in obj:
            if P.tag == "object":
                if "type" in P.attrib and P.attrib["type"] in\
                  Map.decode[2]:
                    objects.append(Map.decode[2][P.attrib["type"]].\
                      __tmx_init__(P, Map))
                else:
                    objects.append(Map.default[2].__tmx_init__(P, Map))
        if cls.__tmx_init__.__func__ == objectgroup.__tmx_init__.__func__:
            return cls(cls.name, cls.properties, objects, Map)
        else:
            cls.objects = objects

    def blit(self):
        """Blits all objects in objectgroup.*
        """
        for o in self:
            if "blit" in dir(o) and not getattr(o, "no_blit", False):
                o.blit()


class image:
    """Basic tileset class.*
    """
    def __init__(self, name, tile_x, tile_y, first, screen):
        self.name = name
        self.image = pygame.image.load(name).convert()
        self.tile_size = self.tile_x, self.tile_y = (tile_x, tile_y)
        self.images = []
        self.size = self.x, self.y = self.image.get_size()
        self.xt = self.x // self.tile_x
        self.yt = self.y // self.tile_y
        for y in range(self.yt):
            for x in range(self.xt):
                self.images.append(pygame.Rect(x * tile_x, y * tile_y,
                  tile_x, tile_y))
        self.size = self.xt * self.yt
        self.first = first
        self.screen = screen

    def Index(self, index):
        """Returns firstindex if index is in tileset else 0.*
        """
        return (self.first <= index < self.first + self.size) * self.first

    def blit(self, pos, index):
        """Blits image on index at position pos.*
        """
        self.screen.blit(self.image, pos, self.images[index])


class visual_map:
    """Basic class for game map.

    :param int x: width of map
    :param int y: height of map
    :param bool layers: does map have layers
    :param str path: path to all map images
    :param decode: decoding; first dict is for layers, second for\
    objectgroup and third for object
    :type decode: list of dicts
    :param tuple tilesize: size of each tile (needed only if *layers* are used)
    :param dict images: dictionary containing images paths and their nickname (used in ``write_on``)
    :param list else_: default decoding; first for layer, second for\
    objectgroup, third for object
    :param bool gid_point: if ``True`` object's obj will be point if rect\
    doesn't have width **and** height
    :param bool gid_line: if ``True`` object's obj will be line if rect\
    doesn't have width **or** height
    :param bool size_in_tiles: is ``x`` and ``y`` measured in tiles
    """
    def __init__(self, x, y, layers=True, path="", decode=[{}, {}, {}],
          tilesize=(), images={}, else_=[layer, objectgroup, Object],
          gid_point=True, gid_line=True, size_in_tiles=False):
        self.path = path
        
        self.screen = pygame.display.get_surface()
        if self.screen:
            self.screen_w, self.screen_h = self.screen.get_size()

        self.size = self.width, self.height = self.edge_width, self.edge_height = x, y

        self.x = self.y = self.edge_x = self.edge_y = 0

        self.decode = decode
        self.default = else_

        self.layers = layers
        if self.layers:
            if not tilesize:
                raise ValueError("If layers are ON, tilesize should be defined")
            self.images = []
            self.layers = []
            self.translate = {None: 0}
            self.tile_size = self.tile_width, self.tile_height = tilesize
            if size_in_tiles:
                self.tiles = self.t_width, self.t_height = self.width, self.height
                self.width *= self.tile_width
                self.height *= self.tile_height
                self.size = self.edge_width, self.edge_height = self.width, self.height
            else:
                self.tiles = self.t_width, self.t_height = self.width //\
                  self.tile_width, self.height // self.tile_height
            self.next_id = 1
            for im, nm in images.items():
                self.create_tileset(im, nm)

        self.objects = []
        self.objectgroups = []
        self.in_map = MAP(self.width, self.height)
        self.gid_point = gid_point
        self.gid_line = gid_line

    def set_camera_pos(self, x, y, pos=(50, 50), edge=True):
        """Sets camera position.
        
        :param int x: x position of point
        :param int y: y position of point
        :param tuple pos: point of screen in percentage
        :param bool edge: if ``True`` won't be outside the screen
        """
        self.x = x - self.screen_w * pos[0] / 100
        self.y = y - self.screen_h * pos[1] / 100
        self.edge = edge
        if self.edge:
            self.x = max(self.edge_x, min(self.x, self.edge_width -
              self.screen_w))
            self.y = max(self.edge_y, min(self.y, self.edge_height -
              self.screen_h))
        if self.layers:
            for l in self.layers:
                l.set_pos(self.x, self.y)

    def get_camera_pos(self, pos=(50, 50)):
        """Gets camera position.

        :param tuple pos: point of screen in percentage 
        """
        return (self.x + self.screen_w * pos[0] / 100,
          self.y + self.screen_h * pos[1] / 100)

    def blit(self):
        """Blits map and it’s all objects to the screen.
        """
        if self.layers:
            for l in self.layers:
                l.blit()
        for g in self.objectgroups:
            g.blit()

    def create_objectgroup(self, name, props={}, objects=[], **rest):
        """Creates map's objectgroup.

        :param str name: objectgroup name
        :param dict props: properties of objectgroup
        :param list objects: objects that belong to objectgroup
        :param rest: other objectgroup parameters
        """
        if name in self.decode[1]:
            obj = self.decode[1][name]
        else:
            obj = self.default[1]
        self.objectgroups.append(obj(name, props, objects, Map=self, **rest))

    def load_objectgroup(self, xml_obj):
        """Loads objectgroup from xml element.*

        :param xml_obj: element from which objectgroup is loaded
        """
        if xml_obj.attrib["name"] in self.decode[1]:
            obj = self.decode[1][xml_obj.attrib["name"]]
        else:
            obj = self.default[1]
        self.objectgroups.append(obj.__tmx_init__(xml_obj, self))

    def assign_object(self, objgroup, obj):
        """Assigns object to particular objectgroup.*

        :param str objgroup: name of the objectgroup
        :param obj: object which will be assigned
        """
        for gr in self.objectgroups:
            if gr.name == objgroup:
                gr.objects.append(obj)
                break

    def create_object(self, objgroup, name, Type, props={}, obj=None, **rest):
        """Creates map object and assigns it to particular objectgroup.
        """
        if Type in self.decode[2]:
            o = self.decode[2][Type](name, Type, props, obj, **rest)
        else:
            o = self.default[2][Type](name, Type, props, obj, **rest)
        self.assign_object(objgroup, o)
        return o

    def create_layer(self, name, props={}, **rest):
        """Creates map layer

        :param str name: layer name
        :param dict props: layer properties
        :param rest: other layer parameters
        """
        if name in self.decode[0]:
            obj = self.decode[0][name]
        else:
            obj = self.default[0]      
        self.layers.append(obj(name, props, [[0 for x in
          range(self.t_width)] for y in range(self.t_height)], self, **rest))
        self.layers[-1].set_pos(self.x, self.y)

    def load_layer(self, xml_obj):
        """Loads objectgroup from xml element.*

        :param xml_obj: element from which layer is loaded
        """
        if xml_obj.attrib["name"] in self.decode[0]:
            obj = self.decode[0][xml_obj.attrib["name"]]
        else:
            obj = self.default[0]
        self.layers.append(obj.__tmx_init__(xml_obj, self))

    def create_tileset(self, img, name):
        """Creates map tileset.

        :param str img: path to tileset image
        :param str name: tileset name
        """
        self.images.append(image(path.join(self.path, img),
          self.tile_width, self.tile_height, self.next_id, self.screen))
        self.translate[self.next_id] = name
        self.next_id += self.images[-1].size

    def write_on(self, pos, layer, num, pic=None, mul_pos=False):
        """Changes map layer.
        """
        if not self.layers:
            raise NotImplementedError("Can't use write_on when layers are off!")
        n = num + self.translate[pic]
        for l in self.layers:
            if l.name == layer:
                L = l
                break
        if mul_pos:
            for p in pos:
                L.mapping[p[1]][p[0]] = n
        else:
            L.mapping[pos[1]][pos[0]] = n

    def clone_obj(self, key, key_type="name"):
        """Returns list of all objects with given parameter.

        :param str key: parameter of searching object/s
        :param str key_type: name, group or type; what key means.
        """
        self.final = []
        if key_type in ("group", "objectgroup"):
            for group in self.objectgroups:
                if group.name == key:
                    for obj in group:
                        self.final.append(obj)
        else:
            for obj in self.objects:
                if (obj.name if key_type == "name" else obj.type) == key:
                    self.final.append(obj)
        if len(self.final) > 1:
            return self.final
        elif self.final:
            return self.final[0]
        else:
            return None

    def set_edge(self, width, height):
        """Sets map edge.
        
        :param int width: new map width
        :param int height: new map height
        """
        self.edge_width = width
        self.edge_height = height

    def offset(self, x, y):
        """Sets map offset.
        
        :param int x: starting x of map
        :param int y: starting y of map
        """
        self.edge_x = x
        self.edge_y = y


class tiled_map(visual_map):
    """Basic class for map in Tiled.
    
    :param str name: file name
    :param decode: decoding; first dict is for layers, second for\
    objectgroup and third for object
    :type decode: list of dicts
    :param list else_: default decoding; first for layer, second for\
    objectgroup, third for object
    :param bool gid_point: if ``True`` object's obj will be point if rect\
    doesn't have width **and** height
    :param bool gid_line: if ``True`` object's obj will be line if rect\
    doesn't have width **or** height
    """
    def __init__(self, name, decode=[{}, {}, {}], else_=[layer,
          objectgroup, Object], gid_point=True, gid_line=True):
        self.name = name + '.tmx'
        self.xml = Tree(file=self.name)
        self.out_map = self.xml.getroot()
        super().__init__(int(self.out_map.attrib["width"]),
          int(self.out_map.attrib["height"]), True, path.dirname(self.name),
          decode, (int(self.out_map.attrib["tilewidth"]),
          int(self.out_map.attrib["tileheight"])), {}, else_, gid_point,
          gid_line, True)

        for part in self.out_map:
            if part.tag == "tileset":
                self.create_tileset(part.find("image").attrib["source"],
                  part.attrib["name"])
            elif part.tag == "layer":
                self.load_layer(part)
            elif part.tag == "objectgroup":
                self.load_objectgroup(part)

    def __str__(self):
        return "Tiled m" + str(self.in_map)[1:]

    __repr__ = __str__

    def reset_screen(self):
        """Resets map's screen (should be executed if screen wasn't\
        defined before)
        """
        self.screen = pygame.display.get()
        self.screen_w, self.screen_h = self.screen.get_size()



class moving_map(tiled_map):
    """Subclass of :py:class:`tiled_map` for easier moving.

    :param str name: file name
    :param int x: map centre object x
    :param int y: map centre object y
    :param decode: decoding; first dict is for layers, second for\
    objectgroup and third for object
    :type decode: list of dicts
    :param list else_: default decoding; first for layer, second for\
    objectgroup, third for object
    :param bool gid_point: if ``True`` object's obj will be point if rect\
    doesn't have width **and** height
    :param bool gid_line: if ``True`` object's obj will be line if rect\
    doesn't have width **or** height
    """
    def __init__(self, name, x, y, decode=[{}, {}, {}], else_=[layer,
          objectgroup, Object], gid_point=True, gid_line=True):
        super().__init__(name, decode, else_, gid_point, gid_line)
        self.X = x
        self.Y = y
        self.set_camera_pos(self.X, self.Y)

    def set_position(self, x, y, pos=(50, 50), edge=True):
        """Sets centre object position
        
        :param int x: x position of centre object
        :param int y: y position of centre object
        :param tuple pos: point of screen in percentage
        :param bool edge: if ``True`` won't be outside the screen
        """
        self.X = x
        self.Y = y
        self.set_camera_pos(self.X, self.Y, pos, edge)

    def get_position(self):
        """Returns centre object coordinates.
        
        :returns: centre x and y
        :rtype: tuple
        """
        return (self.X, self.Y)

    def move(self, hor, ver, pos=(50, 50), edge=True):
        """Moves centre object.
        
        :param int hor: horizontal movement (positive for right, negative\
        for left)
        :param int ver: vertical movement (positive for down, negative\
        for up)
        :param tuple pos: point of screen in percentage
        :param bool edge: if ``True`` won't be outside the screen
        """
        self.X += hor
        self.Y += ver
        self.set_camera_pos(self.X, self.Y, pos, edge)
