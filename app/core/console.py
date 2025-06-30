import colorama
import traceback

colorama.init(autoreset=True)

class Colors(object):
    NATIVE  = colorama.Style.RESET_ALL
    RED     = colorama.Fore.RED
    GREEN   = colorama.Fore.GREEN
    YELLOW  = colorama.Fore.YELLOW
    BLUE    = colorama.Fore.BLUE
    MAGENTA = colorama.Fore.MAGENTA

class Console:
    """
    Class that wraps console messages for uniformity.
    """

    @staticmethod
    def raw(message: str, color: str = Colors.NATIVE, end: str = "\n") -> None:
        """
        Writes a message to the console with no prefix. Also allows for no
        new line after print if the end argument is set to ''.

        Useful for input prompts or partial lines.
        """
        print(f"{color}{message}{Colors.NATIVE}", end=end)

    @staticmethod
    def write(message: str) -> None:
        """
        Displays a standard message to the console.
        """
        Console.__write(message=message, prefix="[+]", color=Colors.GREEN)

    @staticmethod
    def info(message: str) -> None:
        """
        Displays an information message to the console.
        """
        Console.__write(message=message, prefix="[*]", color=Colors.BLUE)

    @staticmethod
    def warn(message: str) -> None:
        """
        Displays a warning message to the console.
        """
        Console.__write(message=message, prefix="[-]", color=Colors.YELLOW)

    @staticmethod
    def error(message: str) -> None:
        """
        Displays an error message to the console.
        """
        Console.__write(message=message, prefix="[!]", color=Colors.RED)
    
    @staticmethod
    def exception(message: str) -> None:
        """
        Displays exception text without a prefix.
        """
        message = f"\n{message}"
        Console.__write(message=message, prefix="", color=Colors.RED)

    @staticmethod
    def trace() -> None:
        """
        Displays traceback information.

        Use this only in an except block or the trace information may be inaccurate.
        """
        trace = traceback.format_exc()
        Console.exception(trace)

    @staticmethod
    def debug(message: str) -> None:
        """
        Displays debug messages.
        """
        Console.__write(message=message, prefix="[DEBUG]", color=Colors.MAGENTA)

    @staticmethod
    def __write(message: str, prefix: str = "", color: str = Colors.NATIVE):
        """
        Writes a message to the console in a uniform way.
        """
        output = f"{color}{prefix}{Colors.NATIVE} {message}" if prefix else f"{color}{message}{Colors.NATIVE}"
        print(output)
