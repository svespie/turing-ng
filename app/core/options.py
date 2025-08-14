import copy

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

Validator = Callable[[Any], Optional[str]]
TypeSpec = Union[type, Tuple[type,...]]

class Option:
    """Option record."""
    def __init__(
        self, 
        name: str, 
        description: str, 
        required: bool = False, 
        value: Optional[Any] = None, 
        default: Optional[Any] = None
    ) -> None:
        self.name: str = name.upper()
        self.description: str = description
        self.required: bool = required
        self.value: Optional[Any] = value
        self.default: Optional[Any] = default

    def __repr__(self) -> str:
        return f"Option(name={self.name!r}, desc={self.default!r} val={self.value!r}, default={self.default!r}, req={self.required!r})"

class OptionRegistry:
    """Option registry to manage Option records."""
    def __init__(self) -> None:
        self._options: Dict[str, Option] = {}

    def register(self, option: Option, overwrite: bool = True) -> None:
        """Registers the provided option."""
        # TODO: consider validation here
        key: str = option.name.upper()
        if not overwrite and key in self._options:
            return
        self._options[key] = copy.deepcopy(option)

    def set(self, name: str, value: Any) -> None:
        """Sets the value of the named option."""
        #TODO: implement value/type/required validation post MVP
        key: str = name.upper()
        option: Option = self._require(key)
        option.value = value
        
    def unset(self, name: str) -> None:
        """Unsets the value of the  named option."""
        key: str = name.upper()
        option: Option = self._require(key)
        option.value = None

    def get(self, name:str) -> Any:
        """Retrieves the value for the named option."""
        key: str = name.upper()
        option: Option = self._require(key)
        return copy.deepcopy(option.value)
    
    def get_option(self, name: str) -> Option:
        """Retrieves the named option object."""
        key: str = name.upper()
        option: Option = self._require(key)
        return copy.deepcopy(option)
    
    def get_options(self) -> List[Option]:
        """Retrieves a list of option objects."""
        return [copy.deepcopy(option) for option in self._options.values()]
    
    def __contains__(self, name: str) -> bool:
        return name.upper() in self._options

    def _require(self, key: str) -> Option:
        if key not in self._options:
            raise KeyError(f"Option '{key}' not found")
        return self._options[key]