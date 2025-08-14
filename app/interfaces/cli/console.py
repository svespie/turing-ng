import os
import colorama

colorama.init(autoreset=True)

class Console:
    RESET = colorama.Fore.RESET

    @staticmethod
    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    class Color:
        BLACK = colorama.Fore.BLACK
        RED = colorama.Fore.RED
        GREEN = colorama.Fore.GREEN
        YELLOW = colorama.Fore.YELLOW
        BLUE = colorama.Fore.BLUE
        MAGENTA = colorama.Fore.MAGENTA
        CYAN = colorama.Fore.CYAN
        WHITE = colorama.Fore.WHITE
        GRAY = colorama.Fore.LIGHTBLACK_EX

    class Style:
        BOLD = "\033[1m"
        DIM = "\033[2m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"
        RESET = "\033[22m"

    @staticmethod
    def color_text(text: str, effects: list[str] | tuple[str, ...] = None) -> str:
        if effects:
            return "".join(effects) + text + Console.RESET
        return text

    class Write:
        #TODO: extract common logic

        @staticmethod
        def info(msg: str) -> None:
            print(Console.color_text(msg, Console.Color.CYAN))
            print(f"[{Console.color_text('*', Console.Color.CYAN)}] {Console.color_text(msg, Console.Color.CYAN)}")

        @staticmethod
        def success(msg: str) -> None:
            print(f"[{Console.color_text('+', Console.Color.GREEN)}] {Console.color_text(msg, Console.Color.GREEN)}")

        @staticmethod
        def warn(msg: str) -> None:
            print(f"[{Console.color_text('!', [Console.Color.YELLOW, Console.Style.BOLD])}] {Console.color_text(msg, Console.Color.YELLOW)}")

        @staticmethod
        def error(msg: str) -> None:
            print(f"[{Console.color_text('!', [Console.Color.RED, Console.Style.BOLD])}{Console.Style.RESET}] {Console.color_text(msg, Console.Color.RED)}")

        @staticmethod
        def exception(msg: str) -> None:
            print(f"{Console.color_text(msg, Console.Color.RED)}")

        @staticmethod
        def debug(msg: str) -> None:
            print(f"{Console.color_text('(debug)', [Console.Color.YELLOW])} {Console.color_text(msg, Console.Color.YELLOW)}")