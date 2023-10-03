import sys

class Logger():
    def __init__(self):
        self.level = 2

    def out(self, prompt, color, *args, **kargs):
        if kargs.get("same_line", False):
            start = "\x1b[2K"
            end = ""
        else:
            start = ""
            end = "\n"

        msg = "".join([start,
          ANSI.BOLD,
          (color if color is not None else ""),
          prompt,
          ANSI.NOT_BOLD,
          " ".join(str(arg) for arg in args),
          ANSI.RESET,
          end])
        sys.stderr.write(msg)
        sys.stderr.flush()


    def info(self, *args, **kargs):
        if self.level < 2: return
        self.out(PROMPTS.INFO, None, *args, **kargs)

    def warning(self, *args, **kargs):
        if self.level < 1: return
        self.out(PROMPTS.WARNING, ANSI.YELLOW, *args, **kargs)

    def error(self, *args, **kargs):
        self.out(PROMPTS.ERROR, ANSI.RED, *args, **kargs)

    def success(self, *args, **kargs):
        if self.level < 2: return
        self.out(PROMPTS.SUCCESS, ANSI.GREEN, *args, **kargs)

    def debug(self, *args, **kargs):
        if self.level < 3: return
        self.out(PROMPTS.INFO, ANSI.CYAN, *args, **kargs)

class ANSI():
    RED = "\x1b[38;5;1m"
    GREEN = "\x1b[38;5;2m"
    BLUE = "\x1b[38;5;4m"
    YELLOW = "\x1b[38;5;3m"
    MAGENTA = "\x1b[38;5;5m"
    CYAN = "\x1b[38;5;6m"
    BOLD = "\x1b[1m"
    NOT_BOLD = "\x1b[22m"
    RESET = "\x1b[0m"

class PROMPTS():
    SUCCESS = "✓ "
    ERROR = "𐄂 "
    WARNING = "! "
    INFO = "> "

logger = Logger()

if not sys.stderr.isatty() or not sys.stdout.isatty():
    ANSI.RED = ""
    ANSI.GREEN = ""
    ANSI.BLUE = ""
    ANSI.YELLOW = ""
    ANSI.MAGENTA = ""
    ANSI.CYAN = ""
    ANSI.BOLD = ""
    ANSI.NOT_BOLD = ""
    ANSI.RESET = ""