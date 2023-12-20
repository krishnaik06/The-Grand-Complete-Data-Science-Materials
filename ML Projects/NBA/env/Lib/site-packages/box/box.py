#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2022 - Chris Griffith - MIT License
"""
Improved dictionary access through dot notation with additional tools.
"""
import copy
import re
import warnings
from keyword import iskeyword
from os import PathLike
from typing import Any, Dict, Generator, List, Tuple, Union, Type

try:
    from typing import Callable, Iterable, Mapping
except ImportError:
    from collections.abc import Callable, Iterable, Mapping

import box
from box.converters import (
    BOX_PARAMETERS,
    _from_json,
    _from_msgpack,
    _from_toml,
    _from_yaml,
    _to_json,
    _to_msgpack,
    _to_toml,
    _to_yaml,
    msgpack_available,
    toml_available,
    yaml_available,
)
from box.exceptions import BoxError, BoxKeyError, BoxTypeError, BoxValueError, BoxWarning

__all__ = ["Box"]

_first_cap_re = re.compile("(.)([A-Z][a-z]+)")
_all_cap_re = re.compile("([a-z0-9])([A-Z])")
_list_pos_re = re.compile(r"\[(\d+)\]")

# a sentinel object for indicating no default, in order to allow users
# to pass `None` as a valid default value
NO_DEFAULT = object()


def _exception_cause(e):
    """
    Unwrap BoxKeyError and BoxValueError errors to their cause.

    Use with `raise ... from _exception_cause(err)` to avoid deeply nested stacktraces, but keep the
    context.
    """
    return e.__cause__ if isinstance(e, (BoxKeyError, BoxValueError)) else e


def _camel_killer(attr):
    """
    CamelKiller, qu'est-ce que c'est?

    Taken from http://stackoverflow.com/a/1176023/3244542
    """
    attr = str(attr)

    s1 = _first_cap_re.sub(r"\1_\2", attr)
    s2 = _all_cap_re.sub(r"\1_\2", s1)
    return re.sub(" *_+", "_", s2.lower())


def _recursive_tuples(iterable, box_class, recreate_tuples=False, **kwargs):
    out_list = []
    for i in iterable:
        if isinstance(i, dict):
            out_list.append(box_class(i, **kwargs))
        elif isinstance(i, list) or (recreate_tuples and isinstance(i, tuple)):
            out_list.append(_recursive_tuples(i, box_class, recreate_tuples, **kwargs))
        else:
            out_list.append(i)
    return tuple(out_list)


def _parse_box_dots(bx, item, setting=False):
    for idx, char in enumerate(item):
        if char == "[":
            return item[:idx], item[idx:]
        elif char == ".":
            if item[:idx] in bx:
                return item[:idx], item[idx + 1 :]
    if setting and "." in item:
        return item.split(".", 1)
    raise BoxError("Could not split box dots properly")


def _get_dot_paths(bx, current=""):
    """A generator of all the end node keys in a box in box_dots format"""

    def handle_dicts(sub_bx, paths=""):
        for key, value in sub_bx.items():
            yield f"{paths}.{key}" if paths else key
            if isinstance(value, dict):
                yield from handle_dicts(value, f"{paths}.{key}" if paths else key)
            elif isinstance(value, list):
                yield from handle_lists(value, f"{paths}.{key}" if paths else key)

    def handle_lists(bx_list, paths=""):
        for i, value in enumerate(bx_list):
            yield f"{paths}[{i}]"
            if isinstance(value, list):
                yield from handle_lists(value, f"{paths}[{i}]")
            if isinstance(value, dict):
                yield from handle_dicts(value, f"{paths}[{i}]")

    yield from handle_dicts(bx, current)


def _get_box_config():
    return {
        # Internal use only
        "__created": False,
        "__safe_keys": {},
    }


class Box(dict):
    """
    Improved dictionary access through dot notation with additional tools.

    :param default_box: Similar to defaultdict, return a default value
    :param default_box_attr: Specify the default replacement.
        WARNING: If this is not the default 'Box', it will not be recursive
    :param default_box_none_transform: When using default_box, treat keys with none values as absent. True by default
    :param default_box_create_on_get: On lookup of a key that doesn't exist, create it if missing
    :param frozen_box: After creation, the box cannot be modified
    :param camel_killer_box: Convert CamelCase to snake_case
    :param conversion_box: Check for near matching keys as attributes
    :param modify_tuples_box: Recreate incoming tuples with dicts into Boxes
    :param box_safe_prefix: Conversion box prefix for unsafe attributes
    :param box_duplicates: "ignore", "error" or "warn" when duplicates exists in a conversion_box
    :param box_intact_types: tuple of types to ignore converting
    :param box_recast: cast certain keys to a specified type
    :param box_dots: access nested Boxes by period separated keys in string
    :param box_class: change what type of class sub-boxes will be created as
    """

    _box_config: Dict[str, Any]

    _protected_keys = [
        "to_dict",
        "to_json",
        "to_yaml",
        "from_yaml",
        "from_json",
        "from_toml",
        "to_toml",
        "merge_update",
    ] + [attr for attr in dir({}) if not attr.startswith("_")]

    def __new__(
        cls,
        *args: Any,
        default_box: bool = False,
        default_box_attr: Any = NO_DEFAULT,
        default_box_none_transform: bool = True,
        default_box_create_on_get: bool = True,
        frozen_box: bool = False,
        camel_killer_box: bool = False,
        conversion_box: bool = True,
        modify_tuples_box: bool = False,
        box_safe_prefix: str = "x",
        box_duplicates: str = "ignore",
        box_intact_types: Union[Tuple, List] = (),
        box_recast: Dict = None,
        box_dots: bool = False,
        box_class: Union[Dict, Type["Box"]] = None,
        **kwargs: Any,
    ):
        """
        Due to the way pickling works in python 3, we need to make sure
        the box config is created as early as possible.
        """
        obj = super().__new__(cls, *args, **kwargs)
        obj._box_config = _get_box_config()
        obj._box_config.update(
            {
                "default_box": default_box,
                "default_box_attr": cls.__class__ if default_box_attr is NO_DEFAULT else default_box_attr,
                "default_box_none_transform": default_box_none_transform,
                "default_box_create_on_get": default_box_create_on_get,
                "conversion_box": conversion_box,
                "box_safe_prefix": box_safe_prefix,
                "frozen_box": frozen_box,
                "camel_killer_box": camel_killer_box,
                "modify_tuples_box": modify_tuples_box,
                "box_duplicates": box_duplicates,
                "box_intact_types": tuple(box_intact_types),
                "box_recast": box_recast,
                "box_dots": box_dots,
                "box_class": box_class if box_class is not None else Box,
            }
        )
        return obj

    def __init__(
        self,
        *args: Any,
        default_box: bool = False,
        default_box_attr: Any = NO_DEFAULT,
        default_box_none_transform: bool = True,
        default_box_create_on_get: bool = True,
        frozen_box: bool = False,
        camel_killer_box: bool = False,
        conversion_box: bool = True,
        modify_tuples_box: bool = False,
        box_safe_prefix: str = "x",
        box_duplicates: str = "ignore",
        box_intact_types: Union[Tuple, List] = (),
        box_recast: Dict = None,
        box_dots: bool = False,
        box_class: Union[Dict, Type["Box"]] = None,
        **kwargs: Any,
    ):
        super().__init__()
        self._box_config = _get_box_config()
        self._box_config.update(
            {
                "default_box": default_box,
                "default_box_attr": self.__class__ if default_box_attr is NO_DEFAULT else default_box_attr,
                "default_box_none_transform": default_box_none_transform,
                "default_box_create_on_get": default_box_create_on_get,
                "conversion_box": conversion_box,
                "box_safe_prefix": box_safe_prefix,
                "frozen_box": frozen_box,
                "camel_killer_box": camel_killer_box,
                "modify_tuples_box": modify_tuples_box,
                "box_duplicates": box_duplicates,
                "box_intact_types": tuple(box_intact_types),
                "box_recast": box_recast,
                "box_dots": box_dots,
                "box_class": box_class if box_class is not None else self.__class__,
            }
        )
        if not self._box_config["conversion_box"] and self._box_config["box_duplicates"] != "ignore":
            raise BoxError("box_duplicates are only for conversion_boxes")
        if len(args) == 1:
            if isinstance(args[0], str):
                raise BoxValueError("Cannot extrapolate Box from string")
            if isinstance(args[0], Mapping):
                for k, v in args[0].items():
                    if v is args[0]:
                        v = self
                    if v is None and self._box_config["default_box"] and self._box_config["default_box_none_transform"]:
                        continue
                    self.__setitem__(k, v)
            elif isinstance(args[0], Iterable):
                for k, v in args[0]:
                    self.__setitem__(k, v)
            else:
                raise BoxValueError("First argument must be mapping or iterable")
        elif args:
            raise BoxTypeError(f"Box expected at most 1 argument, got {len(args)}")

        for k, v in kwargs.items():
            if args and isinstance(args[0], Mapping) and v is args[0]:
                v = self
            self.__setitem__(k, v)

        self._box_config["__created"] = True

    def __add__(self, other: Mapping[Any, Any]):
        if not isinstance(other, dict):
            raise BoxTypeError("Box can only merge two boxes or a box and a dictionary.")
        new_box = self.copy()
        new_box.merge_update(other)
        return new_box

    def __radd__(self, other: Mapping[Any, Any]):
        if not isinstance(other, dict):
            raise BoxTypeError("Box can only merge two boxes or a box and a dictionary.")
        new_box = self.copy()
        new_box.merge_update(other)
        return new_box

    def __iadd__(self, other: Mapping[Any, Any]):
        if not isinstance(other, dict):
            raise BoxTypeError("Box can only merge two boxes or a box and a dictionary.")
        self.merge_update(other)
        return self

    def __or__(self, other: Mapping[Any, Any]):
        if not isinstance(other, dict):
            raise BoxTypeError("Box can only merge two boxes or a box and a dictionary.")
        new_box = self.copy()
        new_box.update(other)
        return new_box

    def __ror__(self, other: Mapping[Any, Any]):
        if not isinstance(other, dict):
            raise BoxTypeError("Box can only merge two boxes or a box and a dictionary.")
        new_box = self.copy()
        new_box.update(other)
        return new_box

    def __ior__(self, other: Mapping[Any, Any]):
        if not isinstance(other, dict):
            raise BoxTypeError("Box can only merge two boxes or a box and a dictionary.")
        self.update(other)
        return self

    def __sub__(self, other: Mapping[Any, Any]):
        frozen = self._box_config["frozen_box"]
        config = self.__box_config()
        config["frozen_box"] = False
        output = self._box_config["box_class"](**config)
        if not isinstance(other, dict):
            raise BoxError("Box can only compare two boxes or a box and a dictionary.")
        if not isinstance(other, Box):
            other = self._box_config["box_class"](other, **config)
        for item in self:
            if item not in other:
                output[item] = self[item]
            elif isinstance(self.get(item), Box) and isinstance(other.get(item), Box):
                output[item] = self[item] - other[item]
                if not output[item]:
                    del output[item]
        output._box_config["frozen_box"] = frozen
        return output

    def __hash__(self):
        if self._box_config["frozen_box"]:
            hashing = 54321
            for item in self.items():
                hashing ^= hash(item)
            return hashing
        raise BoxTypeError('unhashable type: "Box"')

    def __dir__(self):
        items = set(super().__dir__())
        # Only show items accessible by dot notation
        for key in self.keys():
            key = str(key)
            if key.isidentifier() and not iskeyword(key):
                items.add(key)

        for key in self.keys():
            if key not in items:
                if self._box_config["conversion_box"]:
                    key = self._safe_attr(key)
                    if key:
                        items.add(key)

        return list(items)

    def __contains__(self, item):
        in_me = super().__contains__(item)
        if not self._box_config["box_dots"] or not isinstance(item, str):
            return in_me
        if in_me:
            return True
        if "." not in item:
            return False
        try:
            first_item, children = _parse_box_dots(self, item)
        except BoxError:
            return False
        else:
            return children in self[first_item]

    def keys(self, dotted: Union[bool] = False):
        if not dotted:
            return super().keys()

        if not self._box_config["box_dots"]:
            raise BoxError("Cannot return dotted keys as this Box does not have `box_dots` enabled")

        keys = set()
        for key, value in self.items():
            added = False
            if isinstance(key, str):
                if isinstance(value, Box):
                    for sub_key in value.keys(dotted=True):
                        keys.add(f"{key}.{sub_key}")
                        added = True
                elif isinstance(value, box.BoxList):
                    for pos in value._dotted_helper():
                        keys.add(f"{key}{pos}")
                        added = True
                if not added:
                    keys.add(key)
        return sorted(keys, key=lambda x: str(x))

    def items(self, dotted: Union[bool] = False):
        if not dotted:
            return super().items()

        if not self._box_config["box_dots"]:
            raise BoxError("Cannot return dotted keys as this Box does not have `box_dots` enabled")

        return [(k, self[k]) for k in self.keys(dotted=True)]

    def get(self, key, default=NO_DEFAULT):
        if key not in self:
            if default is NO_DEFAULT:
                if self._box_config["default_box"] and self._box_config["default_box_none_transform"]:
                    return self.__get_default(key)
                else:
                    return None
            if isinstance(default, dict) and not isinstance(default, Box):
                return Box(default)
            if isinstance(default, list) and not isinstance(default, box.BoxList):
                return box.BoxList(default)
            return default
        return self[key]

    def copy(self) -> "Box":
        return Box(super().copy(), **self.__box_config())

    def __copy__(self) -> "Box":
        return Box(super().copy(), **self.__box_config())

    def __deepcopy__(self, memodict=None) -> "Box":
        frozen = self._box_config["frozen_box"]
        config = self.__box_config()
        config["frozen_box"] = False
        out = self._box_config["box_class"](**config)
        memodict = memodict or {}
        memodict[id(self)] = out
        for k, v in self.items():
            out[copy.deepcopy(k, memodict)] = copy.deepcopy(v, memodict)
        out._box_config["frozen_box"] = frozen
        return out

    def __setstate__(self, state):
        self._box_config = state["_box_config"]
        self.__dict__.update(state)

    def __get_default(self, item, attr=False):
        default_value = self._box_config["default_box_attr"]
        if default_value in (self._box_config["box_class"], dict):
            value = self._box_config["box_class"](**self.__box_config())
        elif isinstance(default_value, dict):
            value = self._box_config["box_class"](**self.__box_config(), **default_value)
        elif isinstance(default_value, list):
            value = box.BoxList(**self.__box_config())
        elif isinstance(default_value, Callable):
            value = default_value()
        elif hasattr(default_value, "copy"):
            value = default_value.copy()
        else:
            value = default_value
        if self._box_config["default_box_create_on_get"]:
            if not attr or not (item.startswith("_") and item.endswith("_")):
                super().__setitem__(item, value)
        return value

    def __box_config(self) -> Dict:
        out = {}
        for k, v in self._box_config.copy().items():
            if not k.startswith("__"):
                out[k] = v
        return out

    def __recast(self, item, value):
        if self._box_config["box_recast"] and item in self._box_config["box_recast"]:
            recast = self._box_config["box_recast"][item]
            try:
                if isinstance(recast, type) and issubclass(recast, (Box, box.BoxList)):
                    return recast(value, **self.__box_config())
                else:
                    return recast(value)
            except ValueError as err:
                raise BoxValueError(f"Cannot convert {value} to {recast}") from _exception_cause(err)
        return value

    def __convert_and_store(self, item, value):
        if self._box_config["conversion_box"]:
            safe_key = self._safe_attr(item)
            self._box_config["__safe_keys"][safe_key] = item
        if isinstance(value, (int, float, str, bytes, bytearray, bool, complex, set, frozenset)):
            return super().__setitem__(item, value)
        # If the value has already been converted or should not be converted, return it as-is
        if self._box_config["box_intact_types"] and isinstance(value, self._box_config["box_intact_types"]):
            return super().__setitem__(item, value)
        # This is the magic sauce that makes sub dictionaries into new box objects
        if isinstance(value, dict):
            # We always re-create even if it was already a Box object to pass down configurations correctly
            value = self._box_config["box_class"](value, **self.__box_config())
        elif isinstance(value, list) and not isinstance(value, box.BoxList):
            if self._box_config["frozen_box"]:
                value = _recursive_tuples(
                    value, recreate_tuples=self._box_config["modify_tuples_box"], **self.__box_config()
                )
            else:
                value = box.BoxList(value, **self.__box_config())
        elif isinstance(value, box.BoxList):
            value.box_options.update(self.__box_config())
        elif self._box_config["modify_tuples_box"] and isinstance(value, tuple):
            value = _recursive_tuples(value, recreate_tuples=True, **self.__box_config())
        super().__setitem__(item, value)

    def __getitem__(self, item, _ignore_default=False):
        try:
            return super().__getitem__(item)
        except KeyError as err:
            if item == "_box_config":
                cause = _exception_cause(err)
                raise BoxKeyError("_box_config should only exist as an attribute and is never defaulted") from cause
            if self._box_config["box_dots"] and isinstance(item, str) and ("." in item or "[" in item):
                try:
                    first_item, children = _parse_box_dots(self, item)
                except BoxError:
                    if self._box_config["default_box"] and not _ignore_default:
                        return self.__get_default(item)
                    raise BoxKeyError(str(item)) from _exception_cause(err)
                if first_item in self.keys():
                    if hasattr(self[first_item], "__getitem__"):
                        return self[first_item][children]
            if self._box_config["camel_killer_box"] and isinstance(item, str):
                converted = _camel_killer(item)
                if converted in self.keys():
                    return super().__getitem__(converted)
            if self._box_config["default_box"] and not _ignore_default:
                return self.__get_default(item)
            raise BoxKeyError(str(err)) from _exception_cause(err)
        except TypeError as err:
            if isinstance(item, slice):
                new_box = self._box_config["box_class"](**self.__box_config())
                for x in list(super().keys())[item.start : item.stop : item.step]:
                    new_box[x] = self[x]
                return new_box
            raise BoxTypeError(str(err)) from _exception_cause(err)

    def __getattr__(self, item):
        try:
            try:
                value = self.__getitem__(item, _ignore_default=True)
            except KeyError:
                value = object.__getattribute__(self, item)
        except AttributeError as err:
            if item == "__getstate__":
                raise BoxKeyError(item) from _exception_cause(err)
            if item == "_box_config":
                raise BoxError("_box_config key must exist") from _exception_cause(err)
            if self._box_config["conversion_box"]:
                safe_key = self._safe_attr(item)
                if safe_key in self._box_config["__safe_keys"]:
                    return self.__getitem__(self._box_config["__safe_keys"][safe_key])
            if self._box_config["default_box"]:
                if item.startswith("_") and item.endswith("_"):
                    raise BoxKeyError(f"{item}: Does not exist and internal methods are never defaulted")
                return self.__get_default(item, attr=True)
            raise BoxKeyError(str(err)) from _exception_cause(err)
        return value

    def __setitem__(self, key, value):
        if key != "_box_config" and self._box_config["frozen_box"] and self._box_config["__created"]:
            raise BoxError("Box is frozen")
        if self._box_config["box_dots"] and isinstance(key, str) and ("." in key or "[" in key):
            first_item, children = _parse_box_dots(self, key, setting=True)
            if first_item in self.keys():
                if hasattr(self[first_item], "__setitem__"):
                    return self[first_item].__setitem__(children, value)
        value = self.__recast(key, value)
        if key not in self.keys() and self._box_config["camel_killer_box"]:
            if self._box_config["camel_killer_box"] and isinstance(key, str):
                key = _camel_killer(key)
        if self._box_config["conversion_box"] and self._box_config["box_duplicates"] != "ignore":
            self._conversion_checks(key)
        self.__convert_and_store(key, value)

    def __setattr__(self, key, value):
        if key == "_box_config":
            return object.__setattr__(self, key, value)
        if self._box_config["frozen_box"] and self._box_config["__created"]:
            raise BoxError("Box is frozen")
        if key in self._protected_keys:
            raise BoxKeyError(f'Key name "{key}" is protected')

        safe_key = self._safe_attr(key)
        if safe_key in self._box_config["__safe_keys"]:
            key = self._box_config["__safe_keys"][safe_key]
        self.__setitem__(key, value)

    def __delitem__(self, key):
        if self._box_config["frozen_box"]:
            raise BoxError("Box is frozen")
        if (
            key not in self.keys()
            and self._box_config["box_dots"]
            and isinstance(key, str)
            and ("." in key or "[" in key)
        ):
            try:
                first_item, children = _parse_box_dots(self, key)
            except BoxError:
                raise BoxKeyError(str(key)) from None
            if hasattr(self[first_item], "__delitem__"):
                return self[first_item].__delitem__(children)
        if key not in self.keys() and self._box_config["camel_killer_box"]:
            if self._box_config["camel_killer_box"] and isinstance(key, str):
                for each_key in self:
                    if _camel_killer(key) == each_key:
                        key = each_key
                        break
        try:
            super().__delitem__(key)
        except KeyError as err:
            raise BoxKeyError(str(err)) from _exception_cause(err)

    def __delattr__(self, item):
        if self._box_config["frozen_box"]:
            raise BoxError("Box is frozen")
        if item == "_box_config":
            raise BoxError('"_box_config" is protected')
        if item in self._protected_keys:
            raise BoxKeyError(f'Key name "{item}" is protected')
        try:
            self.__delitem__(item)
        except KeyError as err:
            if self._box_config["conversion_box"]:
                safe_key = self._safe_attr(item)
                if safe_key in self._box_config["__safe_keys"]:
                    self.__delitem__(self._box_config["__safe_keys"][safe_key])
                    del self._box_config["__safe_keys"][safe_key]
                    return
            raise BoxKeyError(str(err)) from _exception_cause(err)

    def pop(self, key, *args):
        if self._box_config["frozen_box"]:
            raise BoxError("Box is frozen")

        if args:
            if len(args) != 1:
                raise BoxError('pop() takes only one optional argument "default"')
            try:
                item = self[key]
            except KeyError:
                return args[0]
            else:
                del self[key]
                return item
        try:
            item = self[key]
        except KeyError:
            raise BoxKeyError(f"{key}") from None
        else:
            del self[key]
            return item

    def clear(self):
        if self._box_config["frozen_box"]:
            raise BoxError("Box is frozen")
        super().clear()
        self._box_config["__safe_keys"].clear()

    def popitem(self):
        if self._box_config["frozen_box"]:
            raise BoxError("Box is frozen")
        try:
            key = next(self.__iter__())
        except StopIteration:
            raise BoxKeyError("Empty box") from None
        return key, self.pop(key)

    def __repr__(self) -> str:
        return f"Box({self})"

    def __str__(self) -> str:
        return str(self.to_dict())

    def __iter__(self) -> Generator:
        for key in self.keys():
            yield key

    def __reversed__(self) -> Generator:
        for key in reversed(list(self.keys())):
            yield key

    def to_dict(self) -> Dict:
        """
        Turn the Box and sub Boxes back into a native python dictionary.

        :return: python dictionary of this Box
        """
        out_dict = dict(self)
        for k, v in out_dict.items():
            if v is self:
                out_dict[k] = out_dict
            elif isinstance(v, Box):
                out_dict[k] = v.to_dict()
            elif isinstance(v, box.BoxList):
                out_dict[k] = v.to_list()
        return out_dict

    def update(self, *args, **kwargs):
        if self._box_config["frozen_box"]:
            raise BoxError("Box is frozen")
        if (len(args) + int(bool(kwargs))) > 1:
            raise BoxTypeError(f"update expected at most 1 argument, got {len(args) + int(bool(kwargs))}")
        single_arg = next(iter(args), None)
        if single_arg:
            if hasattr(single_arg, "keys"):
                for k in single_arg:
                    self.__convert_and_store(k, single_arg[k])
            else:
                for k, v in single_arg:
                    self.__convert_and_store(k, v)
        for k in kwargs:
            self.__convert_and_store(k, kwargs[k])

    def merge_update(self, *args, **kwargs):
        merge_type = None
        if "box_merge_lists" in kwargs:
            merge_type = kwargs.pop("box_merge_lists")

        def convert_and_set(k, v):
            intact_type = self._box_config["box_intact_types"] and isinstance(v, self._box_config["box_intact_types"])
            if isinstance(v, dict) and not intact_type:
                # Box objects must be created in case they are already
                # in the `converted` box_config set
                v = self._box_config["box_class"](v, **self.__box_config())
                if k in self and isinstance(self[k], dict):
                    self[k].merge_update(v)
                    return
            if isinstance(v, list) and not intact_type:
                v = box.BoxList(v, **self.__box_config())
                if merge_type == "extend" and k in self and isinstance(self[k], list):
                    self[k].extend(v)
                    return
                if merge_type == "unique" and k in self and isinstance(self[k], list):
                    for item in v:
                        if item not in self[k]:
                            self[k].append(item)
                    return
            self.__setitem__(k, v)

        if (len(args) + int(bool(kwargs))) > 1:
            raise BoxTypeError(f"merge_update expected at most 1 argument, got {len(args) + int(bool(kwargs))}")
        single_arg = next(iter(args), None)
        if single_arg:
            if hasattr(single_arg, "keys"):
                for k in single_arg:
                    convert_and_set(k, single_arg[k])
            else:
                for k, v in single_arg:
                    convert_and_set(k, v)

        for key in kwargs:
            convert_and_set(key, kwargs[key])

    def setdefault(self, item, default=None):
        if item in self:
            return self[item]

        if self._box_config["box_dots"]:
            if item in _get_dot_paths(self):
                return self[item]

        if isinstance(default, dict):
            default = self._box_config["box_class"](default, **self.__box_config())
        if isinstance(default, list):
            default = box.BoxList(default, **self.__box_config())
        self[item] = default
        return self[item]

    def _safe_attr(self, attr):
        """Convert a key into something that is accessible as an attribute"""
        if isinstance(attr, str):
            # By assuming most people are using string first we get substantial speed ups
            if attr.isidentifier() and not iskeyword(attr):
                return attr

        if isinstance(attr, tuple):
            attr = "_".join([str(x) for x in attr])

        attr = attr.decode("utf-8", "ignore") if isinstance(attr, bytes) else str(attr)
        if self.__box_config()["camel_killer_box"]:
            attr = _camel_killer(attr)

        if attr.isidentifier() and not iskeyword(attr):
            return attr

        if sum(1 for character in attr if character.isidentifier() and not iskeyword(character)) == 0:
            attr = f'{self.__box_config()["box_safe_prefix"]}{attr}'
            if attr.isidentifier() and not iskeyword(attr):
                return attr

        out = []
        last_safe = 0
        for i, character in enumerate(attr):
            if f"x{character}".isidentifier():
                last_safe = i
                out.append(character)
            elif not out:
                continue
            else:
                if last_safe == i - 1:
                    out.append("_")

        out = "".join(out)[: last_safe + 1]

        try:
            int(out[0])
        except (ValueError, IndexError):
            pass
        else:
            out = f'{self.__box_config()["box_safe_prefix"]}{out}'

        if iskeyword(out):
            out = f'{self.__box_config()["box_safe_prefix"]}{out}'

        return out

    def _conversion_checks(self, item):
        """
        Internal use for checking if a duplicate safe attribute already exists

        :param item: Item to see if a dup exists
        """
        safe_item = self._safe_attr(item)

        if safe_item in self._box_config["__safe_keys"]:
            dups = [f"{item}({safe_item})", f'{self._box_config["__safe_keys"][safe_item]}({safe_item})']
            if self._box_config["box_duplicates"].startswith("warn"):
                warnings.warn(f"Duplicate conversion attributes exist: {dups}", BoxWarning)
            else:
                raise BoxError(f"Duplicate conversion attributes exist: {dups}")

    def to_json(
        self, filename: Union[str, PathLike] = None, encoding: str = "utf-8", errors: str = "strict", **json_kwargs
    ):
        """
        Transform the Box object into a JSON string.

        :param filename: If provided will save to file
        :param encoding: File encoding
        :param errors: How to handle encoding errors
        :param json_kwargs: additional arguments to pass to json.dump(s)
        :return: string of JSON (if no filename provided)
        """
        return _to_json(self.to_dict(), filename=filename, encoding=encoding, errors=errors, **json_kwargs)

    @classmethod
    def from_json(
        cls,
        json_string: str = None,
        filename: Union[str, PathLike] = None,
        encoding: str = "utf-8",
        errors: str = "strict",
        **kwargs,
    ) -> "Box":
        """
        Transform a json object string into a Box object. If the incoming
        json is a list, you must use BoxList.from_json.

        :param json_string: string to pass to `json.loads`
        :param filename: filename to open and pass to `json.load`
        :param encoding: File encoding
        :param errors: How to handle encoding errors
        :param kwargs: parameters to pass to `Box()` or `json.loads`
        :return: Box object from json data
        """
        box_args = {}
        for arg in kwargs.copy():
            if arg in BOX_PARAMETERS:
                box_args[arg] = kwargs.pop(arg)

        data = _from_json(json_string, filename=filename, encoding=encoding, errors=errors, **kwargs)

        if not isinstance(data, dict):
            raise BoxError(f"json data not returned as a dictionary, but rather a {type(data).__name__}")
        return cls(data, **box_args)

    if yaml_available:

        def to_yaml(
            self,
            filename: Union[str, PathLike] = None,
            default_flow_style: bool = False,
            encoding: str = "utf-8",
            errors: str = "strict",
            **yaml_kwargs,
        ):
            """
            Transform the Box object into a YAML string.

            :param filename:  If provided will save to file
            :param default_flow_style: False will recursively dump dicts
            :param encoding: File encoding
            :param errors: How to handle encoding errors
            :param yaml_kwargs: additional arguments to pass to yaml.dump
            :return: string of YAML (if no filename provided)
            """
            return _to_yaml(
                self.to_dict(),
                filename=filename,
                default_flow_style=default_flow_style,
                encoding=encoding,
                errors=errors,
                **yaml_kwargs,
            )

        @classmethod
        def from_yaml(
            cls,
            yaml_string: str = None,
            filename: Union[str, PathLike] = None,
            encoding: str = "utf-8",
            errors: str = "strict",
            **kwargs,
        ) -> "Box":
            """
            Transform a yaml object string into a Box object. By default will use SafeLoader.

            :param yaml_string: string to pass to `yaml.load`
            :param filename: filename to open and pass to `yaml.load`
            :param encoding: File encoding
            :param errors: How to handle encoding errors
            :param kwargs: parameters to pass to `Box()` or `yaml.load`
            :return: Box object from yaml data
            """
            box_args = {}
            for arg in kwargs.copy():
                if arg in BOX_PARAMETERS:
                    box_args[arg] = kwargs.pop(arg)

            data = _from_yaml(yaml_string=yaml_string, filename=filename, encoding=encoding, errors=errors, **kwargs)
            if not data:
                return cls(**box_args)
            if not isinstance(data, dict):
                raise BoxError(f"yaml data not returned as a dictionary but rather a {type(data).__name__}")
            return cls(data, **box_args)

    else:

        def to_yaml(
            self,
            filename: Union[str, PathLike] = None,
            default_flow_style: bool = False,
            encoding: str = "utf-8",
            errors: str = "strict",
            **yaml_kwargs,
        ):
            raise BoxError('yaml is unavailable on this system, please install the "ruamel.yaml" or "PyYAML" package')

        @classmethod
        def from_yaml(
            cls,
            yaml_string: str = None,
            filename: Union[str, PathLike] = None,
            encoding: str = "utf-8",
            errors: str = "strict",
            **kwargs,
        ) -> "Box":
            raise BoxError('yaml is unavailable on this system, please install the "ruamel.yaml" or "PyYAML" package')

    if toml_available:

        def to_toml(self, filename: Union[str, PathLike] = None, encoding: str = "utf-8", errors: str = "strict"):
            """
            Transform the Box object into a toml string.

            :param filename: File to write toml object too
            :param encoding: File encoding
            :param errors: How to handle encoding errors
            :return: string of TOML (if no filename provided)
            """
            return _to_toml(self.to_dict(), filename=filename, encoding=encoding, errors=errors)

        @classmethod
        def from_toml(
            cls,
            toml_string: str = None,
            filename: Union[str, PathLike] = None,
            encoding: str = "utf-8",
            errors: str = "strict",
            **kwargs,
        ) -> "Box":
            """
            Transforms a toml string or file into a Box object

            :param toml_string: string to pass to `toml.load`
            :param filename: filename to open and pass to `toml.load`
            :param encoding: File encoding
            :param errors: How to handle encoding errors
            :param kwargs: parameters to pass to `Box()`
            :return: Box object
            """
            box_args = {}
            for arg in kwargs.copy():
                if arg in BOX_PARAMETERS:
                    box_args[arg] = kwargs.pop(arg)

            data = _from_toml(toml_string=toml_string, filename=filename, encoding=encoding, errors=errors)
            return cls(data, **box_args)

    else:

        def to_toml(self, filename: Union[str, PathLike] = None, encoding: str = "utf-8", errors: str = "strict"):
            raise BoxError('toml is unavailable on this system, please install the "toml" package')

        @classmethod
        def from_toml(
            cls,
            toml_string: str = None,
            filename: Union[str, PathLike] = None,
            encoding: str = "utf-8",
            errors: str = "strict",
            **kwargs,
        ) -> "Box":
            raise BoxError('toml is unavailable on this system, please install the "toml" package')

    if msgpack_available:

        def to_msgpack(self, filename: Union[str, PathLike] = None, **kwargs):
            """
            Transform the Box object into a msgpack string.

            :param filename: File to write msgpack object too
            :param kwargs: parameters to pass to `msgpack.pack`
            :return: bytes of msgpack (if no filename provided)
            """
            return _to_msgpack(self.to_dict(), filename=filename, **kwargs)

        @classmethod
        def from_msgpack(
            cls,
            msgpack_bytes: bytes = None,
            filename: Union[str, PathLike] = None,
            **kwargs,
        ) -> "Box":
            """
            Transforms msgpack bytes or file into a Box object

            :param msgpack_bytes: string to pass to `msgpack.unpackb`
            :param filename: filename to open and pass to `msgpack.unpack`
            :param kwargs: parameters to pass to `Box()`
            :return: Box object
            """
            box_args = {}
            for arg in kwargs.copy():
                if arg in BOX_PARAMETERS:
                    box_args[arg] = kwargs.pop(arg)

            data = _from_msgpack(msgpack_bytes=msgpack_bytes, filename=filename, **kwargs)
            if not isinstance(data, dict):
                raise BoxError(f"msgpack data not returned as a dictionary but rather a {type(data).__name__}")
            return cls(data, **box_args)

    else:

        def to_msgpack(self, filename: Union[str, PathLike] = None, **kwargs):
            raise BoxError('msgpack is unavailable on this system, please install the "msgpack" package')

        @classmethod
        def from_msgpack(
            cls,
            msgpack_bytes: bytes = None,
            filename: Union[str, PathLike] = None,
            encoding: str = "utf-8",
            errors: str = "strict",
            **kwargs,
        ) -> "Box":
            raise BoxError('msgpack is unavailable on this system, please install the "msgpack" package')
