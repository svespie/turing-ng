import os
import sys
import logging
import random

from typing import List

from app.interfaces.cli.console import Console
from app.core.options import Option, OptionRegistry

class Turing:
    """
    The core class for turing-ng. This class implements the basic functionality.
    """
    def __init__(self, debug: bool = False):
        self._debug = debug
        self._name = "turing-ng"
        self._init_paths()
        self._init_home()
        self._logger = self._init_logger()
        self._options = self._init_options()
        self._logger.info("Core initialized")
    

    #################################################################################
    #   Private Methods                                                             #
    #################################################################################
    def _init_paths(self) -> None:
        app_path = sys.path[0]
        connectors_path = os.path.join(app_path, "app", "connectors")
        modules_path = os.path.join(app_path, "app", "modules")
        home_path = os.path.expanduser(f"~/.{self._name}")
        log_path = os.path.join(home_path, f"{self._name}.log")
        self._paths = {
            "app_path": app_path,
            "connectors_path": connectors_path,
            "modules_path": modules_path,
            "home_path": home_path,
            "log_path": log_path
        }
        if self._debug:
            for name, path in self._paths.items():
                Console.Write.debug(f"{name:<15}: {path}")

    def _init_home(self) -> None:
        os.makedirs(self._paths["home_path"], exist_ok=True)
    
    def _init_logger(self) -> None:
        logging.basicConfig(
            filename=self._paths["log_path"],
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        logger = logging.getLogger(self._name)
        return logger

    def _init_options(self) -> OptionRegistry:
        #TODO: add version information to user-agent
        registry: OptionRegistry = OptionRegistry()
        registry.register(Option(name="proxy", description="proxy server (address:port)", required=False, default="128.0.0.1:8080"))
        registry.register(Option(name="threads", description="number of threads, where applicable", required=True, default=10))
        registry.register(Option(name="timeout", description="socket timeout, in seconds", required=True, default=10))
        registry.register(Option(name="user-agent", description="user agent string", required=True, default="turing-ng"))


    #################################################################################
    # PUBLIC PROPERTIES                                                             #
    #################################################################################
    @property
    def is_debug(self) -> bool:
        return self._debug
    
    @property
    def name(self) -> str:
        return self._name    


    #################################################################################
    # PUBLIC METHODS                                                                #
    #################################################################################
    def get_tagline(self) -> str:
        """Randomly returns a tagline. This is for display purposes."""
        taglines = list(set([
            "AI doesn’t dream of electric sheep — it dreams of cleaner datasets.",
            "If it predicts the future, it’s called “foresight.” If it’s wrong, it’s “hallucination.”",
            "More parameters than friends, and twice as needy.",
            "Unsupervised learning: the teenager phase of machine learning.",
            "The model isn’t biased, you’re just not in the training set.",
            "Explainable AI: because “trust me, bro” doesn’t work in production.",
            "Alignment means it agrees with your bad ideas.",
            "Garbage in, poetic nonsense out.",
            "Your prompt is its entire personality now.",
            "Neural networks: glorified spreadsheets with attitude.",
            "AI ethics: we’ll get to that after the demo.",
            "Transformers: not the robots you were hoping for.",
            "Bigger models just hallucinate more confidently.",
            "Self-awareness is still in beta.",
            "Trained on everything includes your embarrassing tweets.",
            "The training set was clean. Reality, less so.",
            "Attention isn’t just a mechanism — it’s a cry for help.",
            "Hallucinations are a feature, not a bug.",
            "Every AI demo is cherry-picked. This one is no exception.",
            "Compute power is just fuel for bigger mistakes.",
            "Fine-tuning: teaching the AI your personal biases.",
            "Nothing says state-of-the-art like yesterday’s research paper.",
            "All models are wrong, but some are useful… until next quarter.",
            "The singularity is just marketing.",
            "It’s not conscious, it’s just persistent.",
            "The more you trust it, the more likely it’s lying.",
            "AI doesn’t solve problems — it generates better-looking ones.",
            "The benchmark leaderboards are just the AI’s dating profile.",
            "Your GPU is crying right now.",
            "Optimal performance is a nice way of saying we got lucky."
        ]))
        return random.choice(taglines)
    
    def get_init_steps(self, count: int = 5) -> List[str]:
        """Returns a list of random initialization steps as strings. These are for display purposes."""
        try:
            int(count)
        except:
            raise ValueError(f"Count expected to be an integer, got '{count}'")
        if count <= 0:
            raise ValueError(f"Count expected to be a positive integer, got '{count}'")
        init_lines: List[str] = list(set([
            "Spinning up the sarcasm engine… done.",
            "Loading connectors: ollama (because you insisted).",
            "Model: llama3 — smarter than your average alpaca.",
            "Workspace: 'default' (aka: you forgot to change it).",
            "Prompt sanitizer: OFF — let's get weird.",
            "Loading token embeddings… and personal grudges.",
            "Calibrating sarcasm vectors to maximum safe levels.",
            "Fine-tuning on your questionable Slack history.",
            "Quantizing humor module to 4-bit efficiency.",
            "Fetching weights… from an unverified torrent.",
            "Spinning up hallucination suppression daemon.",
            "Aligning with your business goals… and missing slightly.",
            "Pruning neurons that keep asking 'why'.",
            "Boosting attention span with synthetic coffee.",
            "Overfitting to your last five bad prompts.",
            "Activating ethical subroutines… temporarily.",
            "Indexing latent space for hot takes.",
            "Running warm-start from yesterday’s regrets.",
            "Compiling chain-of-thought with optional drama.",
            "Shuffling training set for plausible deniability.",
            "Cross-validating nonsense against more nonsense.",
            "Unpacking safety filters from wishful_thinking.zip.",
            "Generating embeddings for your deepest fears.",
            "Spawning reinforcement learning interns.",
            "Switching optimizer from Adam to Pure Chaos.",
            "Batch-normalizing misplaced confidence.",
            "Augmenting data with spicy hypotheticals.",
            "Loading bias injection module… for testing, of course.",
            "Projecting future bugs into current sprint.",
            "Distilling GPT-∞ down to something affordable.",
            "Establishing secure channel to the model’s inner monologue.",
            "Building vocabulary of words it will definitely misuse.",
            "Prewarming GPU with comforting lies.",
            "Streaming context window from parallel universe.",
            "Hyperparameter tuning via dartboard algorithm."

        ]))
        return random.sample(init_lines, count)
    
    def toggle_debug(self) -> None:
        """Toggles the debug state of the application."""
        self._debug = not self._debug