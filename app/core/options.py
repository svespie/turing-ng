from __future__ import annotations

import copy

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence


class OptionError(Exception):
    pass

class OptionNotFound(OptionError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Option '{name}' not found")
        self.name = name

@dataclass
class Option:
    """Option record."""
    name: str
    description: str
    required: bool = False
    value: Optional[Any] = None
    default: Optional[Any] = None

    def __post_init__(self) -> None:
        self.name = self.name.upper()

    def __repr__(self) -> str:
        return (f"Option(name={self.name!r}, desc={self.description!r}, "
                f"val={self.value!r}, default={self.default!r}, req={self.required!r})")


class OptionRegistry:
    """Option registry to manage Option records."""
    def __init__(self) -> None:
        self._options: Dict[str, Option] = {}

    def register(self, option: Option, overwrite: bool = True) -> None:
        """Registers the provided option."""
        key = option.name.upper()
        if not overwrite and key in self._options:
            return
        self._options[key] = copy.deepcopy(option)

    def set(self, name: str, value: Any) -> None:
        """Sets the value of the named option."""
        key = name.upper()
        option = self._require(key)
        option.value = value

    def unset(self, name: str) -> None:
        """Unsets the value of the named option."""
        key = name.upper()
        option = self._require(key)
        option.value = None

    def get(self, name: str) -> Any:
        """Retrieves the *explicit* value for the named option (may be None)."""
        key = name.upper()
        option = self._require(key)
        return copy.deepcopy(option.value)

    def get_option(self, name: str) -> Option:
        """Retrieves the named option object."""
        key = name.upper()
        option = self._require(key)
        return copy.deepcopy(option)

    def get_options(self) -> List[Option]:
        """Retrieves a list of option objects."""
        return [copy.deepcopy(opt) for opt in self._options.values()]

    def get_effective(self, name: str) -> Any:
        """Convenience: returns value if set, else default (does not change get())."""
        opt = self._require(name.upper())
        return copy.deepcopy(opt.value if opt.value is not None else opt.default)

    def to_dict(self) -> Dict[str, Any]:
        """For printing/export."""
        out: Dict[str, Any] = {}
        for k, opt in self._options.items():
            out[k] = opt.value
        return copy.deepcopy(out)

    def missing_required(self) -> List[str]:
        """
        Returns names of required options that currently have no *explicit* value.
        (Does not consider defaults; adjust if you want defaults to satisfy required.)
        """
        #TODO: review this
        missing: List[str] = []
        for name, opt in self._options.items():
            if opt.required and opt.value is None:
                missing.append(name)
        return missing

    def __contains__(self, name: str) -> bool:
        return name.upper() in self._options

    def has(self, name: str) -> bool:
        return name.upper() in self

    def _require(self, key: str) -> Option:
        try:
            return self._options[key]
        except KeyError as ex:
            raise OptionNotFound(key) from ex