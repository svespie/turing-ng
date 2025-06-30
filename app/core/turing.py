import cmd

from app.core.console import Console

class TuringCore(cmd.Cmd):
    """
    The core class for turing-ng. This class implements the basic functionality.
    """

    def __init__(self, debug: bool =False) -> None:
        _debug: bool = debug
        if _debug:
            Console.debug("Debug mode enabled.")