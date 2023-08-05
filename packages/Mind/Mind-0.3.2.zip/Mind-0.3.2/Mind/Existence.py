import pygame
from Mind import Orientation


class Object:
    """Basic object class in object/group model.

    :param groups: groups which object belongs to
    """
    def __init__(self, *groups):
        self.groups = list(groups)
        for gr in self.groups:
            gr.add_object(self)

    def __str__(self):
        return "Object"

    def __repr__(self):
        self.fin = "Object ["
        for gr in self.groups:
            self.fin += str(gr)
            self.fin += ", "
        self.fin = self.fin[:-2] + ("]" if self.groups else "")
        return self.fin

    def add_group(self, gr):
        """Adds groups to object.

        :param gr: group which will object be added to.
        """
        if gr not in self.groups:
            self.groups.append(gr)
            gr.add_object(self)

    def search_groups(self, atr_name, pass_func):
        fin = []
        for gr in self.groups:
            if pass_func(getattr(gr, atr_name)):
                fin.append(gr)
        return fin

    @classmethod
    def __tmx_init__(cls, obj, Map):
        super().__tmx_init__(obj, Map)

    def blit(self):
        super().blit()

    def set_position(self, *arg):
        super().set_position(*arg)

    def move(self, *arg):
        super().move(*arg)


class group(Object):
    """Basic group class in object/group model.

    :param objects: objects which belongs to group
    :param list groups: list of groups group belongs to
    :param bool part: if ``True`` if any object has some function it will belong to group
    """
    def __init__(self, *objects, groups=[], part=False):
        super().__init__(*groups)
        self.objects = list(objects)
        self.part = part
        self.funcs = []
        for f, obj in enumerate(self.objects):
            if self.part or not f:
                for att in dir(obj):
                    if '__call__' in dir(getattr(obj, att)) and att not in\
                      dir(self):
                        self.add_func(att)
            else:
                for p, f in enumerate(list(self.funcs)):
                    if f not in dir(obj):
                        delattr(self, p)
                        del self.funcs[p]
            obj.add_group(self)

    def __str__(self):
        return "Group"

    def __repr__(self):
        self.fin = "Group ["
        for obj in self.objects:
            self.fin += str(obj)
            self.fin += ", "
        self.fin = self.fin[:-2] + ("]" if self.objects else "")
        return self.fin

    def add_func(self, fname):
        """Adds function to group.*
        """
        def f(*args, **kwargs):
            for obj in self.objects:
                getattr(obj, fname)(*args, **kwargs)
        setattr(self, fname, f)
        self.funcs.append(fname)

    def add_object(self, obj):
        """Adds object to group.

        :param obj: object which will be added to group.
        """
        if obj not in self.objects:
            if self.part or not len(self.objects):
                for att in dir(obj):
                    if '__call__' in dir(getattr(obj, att)) and att not in\
                      dir(self):
                        self.add_func(att)
            else:
                for p, f in enumerate(list(self.funcs)):
                    if f not in dir(obj):
                        del self.funcs[p]
            self.objects.append(obj)
            obj.add_group(self)

def join(*dicts):
    """Joins dictionaries.*
    """
    fin = {}
    for d in dicts:
        for key in d:
            fin[key] = d[key]
    return fin


class mov_type:
    """Basic class for all types of game objects.

    :param Map: Map for all objects
    :param picture: picture for all objects
    :param groups: groups for all objects
    :param int width: width for all objects
    :param int height: height for all objects
    :param str name: type name for all objects
    :param dict props: properties for all objects
    :param logic: type's logic
    :type logic: None or instance of :py:class:`Logic`
    """
    def __init__(Type, Map, picture, *groups, width=None, height=None,
          name="", props={}, logic=None):
        Type.Map = Map
        Type.picture = picture
        Type.groups = groups
        Type.type = name
        if width:
            Type.width = width
        if height:
            Type.height = height
        Type.props = props
        Type.logic = logic if logic else Logic([[], [], [], []])
        class ret(Object, Orientation.map_obj):
            def __init__(self, x, y, name, *groups, width=None,
              height=None, props={}, Map=None, picture=None, type_="", logic=None):
                Object.__init__(self, *groups + Type.groups)
                width = width if width else getattr(Type, "width", 0)
                height = height if height else getattr(Type, "height", 0)
                Map = Type.Map if not Map else Map
                type_ = type_ if type_ else Type.type
                if not (width or height) and Map.gid_point:
                    Obj = Orientation.point(x, y, Map.in_map, name,
                      True)
                elif not (width and height) and Map.gid_line:
                    Obj = Orientation.line(q_points(x, y, x + width, y +
                      height, Map.in_map), Map.in_map, name, True)
                else:
                    Obj = Orientation.rect(x, y, width, height, Map.in_map,
                      name, True)
                picture = picture if picture else Type.picture
                Orientation.map_obj.__init__(self, name, type_,
                  join(props, Type.props), picture, Map, Obj)
                self.logic = logic if logic else Type.logic
                for lc in self.logic.lc:
                    lc.bind(self)
                for f in self.logic[0]:
                    f(self)

            @classmethod
            def __tmx_init__(cls, obj, Map):
                super().__tmx_init__(obj, Map)
                return cls(cls.obj.x, cls.obj.y, cls.name,
                  width=cls.width if cls.width else None,
                  height=cls.height if cls.height else None,
                  props=cls.properties, Map=Map, type_=cls.type)

            def blit(self):
                super().blit()
                for f in self.logic[1]:
                    f(self)

            def set_position(self, x, y):
                super().set_position(x, y)
                self.obj.x = x
                self.obj.y = y
                for f in self.logic[2]:
                    f(self)

            def move(self, x, y):
                super().move(x, y)
                self.obj.x = self.x
                self.obj.y = self.y
                for f in self.logic[3]:
                    f(self)
            
        Type.cls = ret

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

    def __tmx_init__(self, obj, Map):
        return self.cls.__tmx_init__(obj, Map)


class Logic:
    """Basic logic class for move type.*
    """
    def __init__(self, lf, lc=[], doc="", name=""):
        self.lf = lf
        self.lc = lc
        self.__doc__ = doc
        self.__name__ = name

    def __getitem__(self, n):
        return self.lf[n]

    def __add__(self, other):
        lc = self.lc + other.lc
        lf = [[], [], [], []]
        for p, l in enumerate(lf):
            l += self.lf[p]
            l += other.lf[p]
        return Logic(lf, lc)


def init_logic(fnc):
    """Decorator for init logic functions.
    """
    ret = [[fnc], [], [], []]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[0] = ret[1] + ret[2] + ret[3]
    return Logic(ret, doc=fnc.__doc__, name=fnc.__name__)


def blit_logic(fnc):
    """Decorator for blit logic functions.
    """
    ret = [[], [fnc], [], []]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[1] = ret[0] + ret[2] + ret[3]
    return Logic(ret, doc=fnc.__doc__, name=fnc.__name__)


def set_pos_logic(fnc):
    """Decorator for set_position logic functions.
    """
    ret = [[], [], [fnc], []]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[2] = ret[0] + ret[1] + ret[3]
    return Logic(ret, doc=fnc.__doc__, name=fnc.__name__)


def move_logic(fnc):
    """Decorator for move logic functions.
    """
    ret = [[], [], [], [fnc]]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[3] = ret[0] + ret[1] + ret[2]
    return Logic(ret, doc=fnc.__doc__, name=fnc.__name__)


class logic_class(Logic):
    """Decorator for logic class.
    """
    def __init__(self, cls):
        self.cls = cls
        self.__doc__ = cls.__doc__
        self.__name__ = cls.__name__
        self.__bases__ = cls.__bases__
        self.lf = []
        self.lc = [self]
        self.lf.append([getattr(self.cls, "__init__", False)] if
          getattr(self.cls, "__init__", False) else [])
        self.lf.append([getattr(self.cls, "blit", False)] if
          getattr(self.cls, "blit", False) else [])
        self.lf.append([getattr(self.cls, "set_position", False)] if
          getattr(self.cls, "set_position", False) else [])
        self.lf.append([getattr(self.cls, "move", False)] if
          getattr(self.cls, "move", False) else [])

    def bind(self, obj):
        """Binds logic class with type's object.*
        """
        for att in dir(self.cls):
            if att[:2] != "__" and att not in ("blit", "set_position",
              "move"):
                setattr(type(obj), att, getattr(self.cls, att))


class logic_obj(Logic):
    """Logic object.*
    """
    def __init__(self, obj):
        self.obj = obj
        self.lf = []
        self.lc = [self]
        self.lf.append([getattr(type(self.obj), "init", False)] if
          getattr(self.obj, "init", False) else [])
        self.lf.append([getattr(type(self.obj), "blit", False)] if
          getattr(self.obj, "blit", False) else [])
        self.lf.append([getattr(type(self.obj), "set_position", False)] if
          getattr(self.obj, "set_position", False) else [])
        self.lf.append([getattr(type(self.obj), "move", False)] if
          getattr(self.obj, "move", False) else [])

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def bind(self, obj):
        """Binds logic object with type's object.*
        """
        for att in dir(self.obj):
            if att[:2] != "__" and att not in ("blit", "set_position",
              "move", "init", "bind"):
                if callable(getattr(self.obj, att)):
                    setattr(type(obj), att, getattr(type(self.obj), att))
                else:
                    setattr(type(obj), att, getattr(self.obj, att))


class logic_object:
    """Decorator for logic object class.
    """
    def __init__(self, cls):
        self.cls = cls
        self.__doc__ = cls.__doc__
        self.__name__ = cls.__name__
        self.__bases__ = cls.__bases__

    def __call__(self, *args, **kwargs):
        return logic_obj(self.cls(*args, **kwargs))


@init_logic
@set_pos_logic
@move_logic
def Subject(self):
    """Subject logic for ``move_type`` logic.
    """
    self.Map.set_camera_pos(self.x, self.y)


@init_logic
def opt_size(self):
    """Optimizes size of object. Size will be picture size.
    """
    self.obj = Orientation.rect(self.x, self.y, self.picture.get_width(), self.picture.get_height(), self.Map.in_map)


@logic_object
class gravity:
    """Basic gravity object logic class.

    :param float g: pixels of acceleration
    :param float jf: jump force
    """
    G = 6.674e-11
    def __init__(self, g, jf=None):
        self.g = g
        self.set_jump_force(jf)

    def init(self):
        self.fy = 0

    def blit(self):
        self.fy += self.g
        self.move(0, self.fy)

    def set_jump_force(self, jf):
        self.default_jf = jf != None
        if self.default_jf:
            self.jf = jf

    def jump(self, jf=None):
        """Player jumps.
        """
        Jf = self.jf if self.default_jf else jf
        self.fy -= Jf


@logic_object
class collider:
    """Basic collision object logic class.

    :param funcs: list functions to execute (1st for player's left, 2nd\
    for player's down ... 5th for any collision)
    :type funcs: list of function or None
    :param str cl_types: names of colliding types
    """
    def __init__(self, funcs, *cl_types):
        self.cl_types = cl_types
        self.cl_objects = []
        self.funcs = funcs
        self.first = True

    def blit(self):
        if self.first:
            for Type in self.cl_types:
                objs = self.Map.clone_obj(Type, "type")
                if type(objs) == list:
                    self.cl_objects += objs
                elif objs:
                    self.cl_objects.append(objs)
            self.first = False

    def move(self):
        for obj in self.cl_objects:
            cld = self.obj.collide(obj.obj)
            Mn = min(filter(lambda x: x, cld)) if any(cld) else None
            if Mn:
                if self.funcs[-1]:
                    self.funcs[-1](self, obj)
                if self.funcs[cld.index(Mn)]:
                    self.funcs[cld.index(Mn)](self, Mn, obj)


@logic_object
class collider2(collider.cls):
    """Basic collision object logic class (simmilar to collider).

    :param str cl_types: names of colliding types
    :param str attr: name of attribute in which are collide functions
    """
    def __init__(self, *cl_types, attr="collide"):
        self.cl_types = cl_types
        self.cl_objects = []
        self.first = True
        self.attr = attr

    def blit(self):
        if self.first:
            for Type in self.cl_types:
                objs = self.Map.clone_obj(Type, "type")
                if type(objs) == list:
                    self.cl_objects += objs
                elif objs:
                    self.cl_objects.append(objs)
            self.funcs = getattr(self, self.attr)
            self.first = False
