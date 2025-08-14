import cmd2
import shlex

from cmd2 import Cmd
from cmd2.plugin import PostcommandData
from typing import List

from app.core.turing import Turing
from app.interfaces.cli.console import Console

class TuringShell(cmd2.Cmd):
    """"""
    def __init__(self, turing: Turing) -> None:
        super().__init__(allow_cli_args=False)
        self._help_color = Console.Color.GRAY
        self._init_cmd2()
        self._turing = turing
        

    def _init_cmd2(self) -> None:
        """Initializes cmd2 for custom output requirements."""
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_macro
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_run_script
        del cmd2.Cmd.do_set
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_shortcuts
        self.do_quit = self.do_exit
        self.intro = f"\n{Console.color_text('Type help or ? to list commands.', [self._help_color])}\n"
        self.nohelp = "No help for %s"
        self.do_help.__func__.__doc__ = """Displays this menu."""
        self.do_history.__func__.__doc__ = """Displays command history."""
        self.doc_header = f"Commands (type [help|?]) <command>:"
        self.register_postcmd_hook(self._postcmd_hook)


    #################################################################################
    # cmd2 Overrides                                                                #
    #################################################################################
    # https://cmd2.readthedocs.io/en/2.4.0/api/cmd.html?highlight=default#cmd2.Cmd.default
    def default(self, statement: cmd2.parsing.Statement):
        Console.Write.error(f"Invalid command: {statement.raw}")

    # https://cmd2.readthedocs.io/en/2.4.0/api/cmd.html?highlight=print_topics#cmd2.Cmd.print_topics
    def print_topics(self, header: str, cmds: List[str]|None, cmdlen: int, maxcol: int) -> None:
        if cmds:
            self.stdout.write(f"{header}\n")
            self.stdout.write(f"{'─'*len(header)}\n")
            for cmd in cmds:
                self.stdout.write(f"{cmd.ljust(15)} {getattr(self,'do_'+cmd).__doc__}\n")
            self.stdout.write("\n")

    # https://cmd2.readthedocs.io/en/2.4.0/api/cmd.html?highlight=do_help#cmd2.Cmd.do_help
    def do_help(self, arg: str) -> None:
        """Displays this menu. Use 'help -v' for version or 'help <command>' for details."""
        parts = shlex.split(arg)
        if parts and parts[0] in ("-v", "--version"):
            super().do_help("")
            return
        if parts == ["help"]:
            self.help_help()
            return
        if parts == ["history"]:
            self.help_history()
            return
        if not parts:
            super().do_help("")
            return
        super().do_help(arg)

    def help_help(self) -> None:
        self.poutput("I can only do so much...")

    def help_history(self) -> None:
        self.poutput(self.do_history.__func__.__doc__)


    #################################################################################
    #   Private Methods                                                             #
    #################################################################################
    def _display_banner(self):
        CYAN = Console.Color.CYAN
        WHITE = Console.Color.WHITE
        MAGENTA = Console.Color.MAGENTA
        RESET = Console.RESET
        art = [
            "                         ▗                                         ",
            "                         ▜▘▌▌▛▘▌▛▌▛▌▄▖▛▌▛▌                         ",
            "                         ▐▖▙▌▌ ▌▌▌▙▌  ▌▌▙▌                         ",
            "                                  ▄▌    ▄▌                         ",
        ]
        init_lines: List[str] = self._turing.get_init_steps()
        tagline: str = self._turing.get_tagline()
        INIT_PREFIX = " > "
        content_width = max(
            max(len(s) for s in art),
            max(len(s) for s in init_lines) + len(INIT_PREFIX),
        )
        top_border = f"{CYAN}╔{'═' * content_width}╗{RESET}"
        separator = f"{CYAN}╟{'─' * content_width}╢{RESET}"
        bottom_border = f"{CYAN}╚{'═' * content_width}╝{RESET}"
        print()
        print(top_border)
        for line in art:
            print(f"{CYAN}║{RESET}{CYAN}{line.ljust(content_width)}{RESET}{CYAN}║{RESET}")
        print(separator)
        for line in init_lines:
            print(f"{CYAN}║{MAGENTA}{INIT_PREFIX}{WHITE}{line.ljust(content_width - len(INIT_PREFIX))}{CYAN}║{RESET}")
        print(bottom_border)
        print(MAGENTA + tagline.center(content_width) + RESET)
        print()

    def _set_prompt(self) -> None:
        prompt_core: str = "turing"
        debug_indicator = Console.color_text("(debug) ", [Console.Color.YELLOW]) if self._turing.is_debug else ""
        prompt_root = Console.color_text(f"{prompt_core}", [Console.Color.CYAN])
        prompt_suffix = Console.color_text(">", [Console.Color.CYAN])
        self.prompt = f"{debug_indicator}{prompt_root}{prompt_suffix} "
    
    def _postcmd_hook(self, data: PostcommandData) -> PostcommandData:
        self._set_prompt()
        return data
    
    
    #################################################################################
    # PUBLIC METHODS                                                                #
    #################################################################################
    def start(self) -> None:
        self._display_banner()
        self._set_prompt()
        self.cmdloop()


    #################################################################################
    # COMMAND METHODS                                                               #
    #################################################################################
    def do_exit(self, _) -> None:
        """Exits the shell."""
        return True
    
    def do_banner(self, _) -> None:
        """Displays the banner."""
        self._display_banner()

    def do_debug(self, _) -> None:
        """Toggles debug state."""
        self._turing.toggle_debug()


    #debug             Display information useful for debugging
    #get               Gets the value of a context-specific variable
    #getg              Gets the value of a global variable
    #set               Sets a context-specific variable to a value
    #setg              Sets a global variable to a value
    #threads           View and manipulate background threads
    #unset             Unsets one or more context-specific variables
    #unsetg            Unsets one or more global variables
    #version           Show the framework and console library version numbers