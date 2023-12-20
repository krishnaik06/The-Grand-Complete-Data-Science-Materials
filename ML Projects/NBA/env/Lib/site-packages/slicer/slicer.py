""" Public facing layer for slicer.
The little slicer that could.
"""
# TODO: Move Obj and Alias class here.

from .slicer_internal import AtomicSlicer, Alias, Obj, AliasLookup, Tracked, UnifiedDataHandler
from .slicer_internal import reduced_o, resolve_dim, unify_slice


class Slicer:
    """ Provides unified slicing to tensor-like objects. """

    def __init__(self, *args, **kwargs):
        """ Wraps objects in args and provides unified numpy-like slicing.

        Currently supports (with arbitrary nesting):

        - lists and tuples
        - dictionaries
        - numpy arrays
        - pandas dataframes and series
        - pytorch tensors

        Args:
            *args: Unnamed tensor-like objects.
            **kwargs: Named tensor-like objects.

        Examples:

            Basic anonymous slicing:

            >>> from slicer import Slicer as S
            >>> li = [[1, 2, 3], [4, 5, 6]]
            >>> S(li)[:, 0:2].o
            [[1, 2], [4, 5]]
            >>> di = {'x': [1, 2, 3], 'y': [4, 5, 6]}
            >>> S(di)[:, 0:2].o
            {'x': [1, 2], 'y': [4, 5]}

            Basic named slicing:

            >>> import pandas as pd
            >>> import numpy as np
            >>> df = pd.DataFrame({'A': [1, 3], 'B': [2, 4]})
            >>> ar = np.array([[5, 6], [7, 8]])
            >>> sliced = S(first=df, second=ar)[0, :]
            >>> sliced.first
            A    1
            B    2
            Name: 0, dtype: int64
            >>> sliced.second
            array([5, 6])

        """
        self.__class__._init_slicer(self, *args, **kwargs)

    @classmethod
    def from_slicer(cls, *args, **kwargs):
        """ Alternative to SUPER SLICE
        Args:
            *args:
            **kwargs:

        Returns:

        """
        slicer_instance = cls.__new__(cls)
        cls._init_slicer(slicer_instance, *args, **kwargs)
        return slicer_instance

    @classmethod
    def _init_slicer(cls, slicer_instance, *args, **kwargs):
        # NOTE: Protected attributes.
        slicer_instance._max_dim = 0

        # NOTE: Private attributes.
        slicer_instance._anon = []
        slicer_instance._objects = {}
        slicer_instance._aliases = {}
        slicer_instance._alias_lookup = None

        # Go through unnamed objects / aliases
        slicer_instance.__setattr__("o", args)

        # Go through named objects / aliases
        for key, value in kwargs.items():
            slicer_instance.__setattr__(key, value)

        # Generate default aliases only if one object and no aliases exist
        objects_len = len(slicer_instance._objects)
        anon_len = len(slicer_instance._anon)
        aliases_len = len(slicer_instance._aliases)
        if ((objects_len == 1) ^ (anon_len == 1)) and aliases_len == 0:
            obj = None
            for _, t in slicer_instance._iter_tracked():
                obj = t

            generated_aliases = UnifiedDataHandler.default_alias(obj.o)
            for generated_alias in generated_aliases:
                slicer_instance.__setattr__(generated_alias._name, generated_alias)

    def __getitem__(self, item):
        index_tup = unify_slice(item, self._max_dim, self._alias_lookup)
        new_args = []
        new_kwargs = {}
        for name, tracked in self._iter_tracked(include_aliases=True):
            if len(tracked.dim) == 0:  # No slice on empty dim
                new_tracked = tracked
            else:
                index_slicer = AtomicSlicer(index_tup, max_dim=1)
                slicer_index = index_slicer[tracked.dim]
                sliced_o = tracked[slicer_index]
                sliced_dim = resolve_dim(index_tup, tracked.dim)

                new_tracked = tracked.__class__(sliced_o, sliced_dim)
                new_tracked._name = tracked._name

            if name == "o":
                new_args.append(new_tracked)
            else:
                new_kwargs[name] = new_tracked

        return self.__class__.from_slicer(*new_args, **new_kwargs)

    def __getattr__(self, item):
        """ Override default getattr to return tracked attribute.

        Args:
            item: Name of tracked attribute.
        Returns:
            Corresponding object.
        """
        if item.startswith("_"):
            return super(Slicer, self).__getattr__(item)

        if item == "o":
            return reduced_o(self._anon)
        else:
            tracked = self._objects.get(item, None)
            if tracked is None:
                tracked = self._aliases.get(item, None)

            if tracked is None:
                raise AttributeError(f"Attribute '{item}' does not exist.")

            return tracked.o

    def __setattr__(self, key, value):
        """ Override default setattr to sync tracking of slicer.

        Args:
            key: Name of tracked attribute.
            value: Either an Obj, Alias or Python Object.
        """
        if key.startswith("_"):
            return super(Slicer, self).__setattr__(key, value)

        # Grab previous objects if they exist:
        old_obj = self._objects.get(key, None)
        old_alias = self._aliases.get(key, None)

        # For existing attributes, honor Alias status and dimension unless specified otherwise
        if getattr(self, key, None) is not None and key != "o":
            if not isinstance(value, Tracked):
                if old_obj:
                    value = Obj(value, dim=old_obj.dim)
                elif old_alias:
                    value = Alias(value, dim=old_alias.dim)

        if isinstance(value, Alias):
            value._name = key
            self._aliases[key] = value
            
            if old_obj: # If object previously existed as an object, clean up all references.
                del self._objects[key]

            # Build lookup (for perf)
            if self._alias_lookup is None:
                self._alias_lookup = AliasLookup(self._aliases)
            else:
                if old_alias:
                    self._alias_lookup.delete(old_alias)
                self._alias_lookup.update(value)
        else:
            if key == "o":
                tracked = [Obj(x) if not isinstance(x, Obj) else x for x in value]
                self._anon = tracked
                for t in tracked:
                    self._update_max_dim(t)

                os = reduced_o(self._anon)
                super(Slicer, self).__setattr__(key, os)
            else:
                if old_alias: # If object previously existed as an alias, clean up all references.
                    self._alias_lookup.delete(old_alias) 
                    del self._aliases[key]
                
                value = Obj(value) if not isinstance(value, Obj) else value
                value._name = key
                self._objects[key] = value
                self._update_max_dim(value)
                super(Slicer, self).__setattr__(key, value.o)

    def __delattr__(self, item):
        """ Override default delattr to remove tracked attribute.

        Args:
            item: Name of tracked attribute to delete.
        """
        if item.startswith("_"):
            return super(Slicer, self).__delattr__(item)

        # Sync private attributes that help track
        self._objects.pop(item, None)
        self._aliases.pop(item, None)
        if item == "o":
            self._anon.clear()

        # Recompute max_dim
        self._recompute_max_dim()

        # Recompute alias lookup
        # NOTE: This doesn't use diff-style deletes, but we don't care (not a perf target).
        self._alias_lookup = AliasLookup(self._aliases)

        # TODO: Mutate and check interactively what it does
        super(Slicer, self).__delattr__(item)

    def __repr__(self):
        """ Override default repr for human readability.

        Returns:
            String to display.
        """
        orig = self.__dict__
        di = {}
        for key, value in orig.items():
            if not key.startswith("_"):
                di[key] = value
        return f"{self.__class__.__name__}({str(di)})"

    def _update_max_dim(self, tracked):
        self._max_dim = max(self._max_dim, max(tracked.dim, default=-1) + 1)

    def _iter_tracked(self, include_aliases=False):
        for tracked in self._anon:
            yield "o", tracked
        for name, tracked in self._objects.items():
            yield name, tracked
        if include_aliases:
            for name, tracked in self._aliases.items():
                yield name, tracked

    def _recompute_max_dim(self):
        self._max_dim = max(
            [max(o.dim, default=-1) + 1 for _, o in self._iter_tracked()], default=0
        )
