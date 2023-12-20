#!/usr/bin/env python
# -*- coding: utf-8 -*-

from box.box import Box


class ConfigBox(Box):
    """
    Modified box object to add object transforms.

    Allows for build in transforms like:

    cns = ConfigBox(my_bool='yes', my_int='5', my_list='5,4,3,3,2')

    cns.bool('my_bool') # True
    cns.int('my_int') # 5
    cns.list('my_list', mod=lambda x: int(x)) # [5, 4, 3, 3, 2]
    """

    _protected_keys = dir(Box) + ["bool", "int", "float", "list", "getboolean", "getfloat", "getint"]

    def __getattr__(self, item):
        """
        Config file keys are stored in lower case, be a little more
        loosey goosey
        """
        try:
            return super().__getattr__(item)
        except AttributeError:
            return super().__getattr__(item.lower())

    def __dir__(self):
        return super().__dir__() + ["bool", "int", "float", "list", "getboolean", "getfloat", "getint"]

    def bool(self, item, default=None):
        """
        Return value of key as a boolean

        :param item: key of value to transform
        :param default: value to return if item does not exist
        :return: approximated bool of value
        """
        try:
            item = self.__getattr__(item)
        except AttributeError as err:
            if default is not None:
                return default
            raise err

        if isinstance(item, (bool, int)):
            return bool(item)

        if isinstance(item, str) and item.lower() in ("n", "no", "false", "f", "0"):
            return False

        return True if item else False

    def int(self, item, default=None):
        """
        Return value of key as an int

        :param item: key of value to transform
        :param default: value to return if item does not exist
        :return: int of value
        """
        try:
            item = self.__getattr__(item)
        except AttributeError as err:
            if default is not None:
                return default
            raise err
        return int(item)

    def float(self, item, default=None):
        """
        Return value of key as a float

        :param item: key of value to transform
        :param default: value to return if item does not exist
        :return: float of value
        """
        try:
            item = self.__getattr__(item)
        except AttributeError as err:
            if default is not None:
                return default
            raise err
        return float(item)

    def list(self, item, default=None, spliter: str = ",", strip=True, mod=None):
        """
        Return value of key as a list

        :param item: key of value to transform
        :param mod: function to map against list
        :param default: value to return if item does not exist
        :param spliter: character to split str on
        :param strip: clean the list with the `strip`
        :return: list of items
        """
        try:
            item = self.__getattr__(item)
        except AttributeError as err:
            if default is not None:
                return default
            raise err
        if strip:
            item = item.lstrip("[").rstrip("]")
        out = [x.strip() if strip else x for x in item.split(spliter)]
        if mod:
            return list(map(mod, out))
        return out

    # loose configparser compatibility

    def getboolean(self, item, default=None):
        return self.bool(item, default)

    def getint(self, item, default=None):
        return self.int(item, default)

    def getfloat(self, item, default=None):
        return self.float(item, default)

    def __repr__(self):
        return "ConfigBox({0})".format(str(self.to_dict()))

    def copy(self):
        return ConfigBox(super().copy())

    def __copy__(self):
        return ConfigBox(super().copy())
