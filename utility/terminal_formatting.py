class Formatting:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    NOT_BOLD = "\033[21m"
    DIM = "\033[2m"
    NOT_DIM = "\033[22m"
    ITALIC = "\033[3m"
    NOT_ITALIC = "\033[23m"
    UNDERLINE = "\033[4m"
    NOT_UNDERLINE = "\033[24m"
    BLINK = "\033[5m"
    NOT_BLINK = "\033[25m"
    INVERTED = "\033[7m"
    NOT_INVERTED = "\033[27m"
    STRIKEOUT = "\033[9m"
    NOT_STRIKEOUT = "\033[29m"


class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DEFAULT = "\033[39m"


class BackgroundColor:
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
    DEFAULT = "\033[49m"


class Navigation:
    UP = "\033[1A"
    DOWN = "\033[1B"
    RIGHT = "\033[1C"
    LEFT = "\033[1D"
    SCREEN_BEGINNING = "\033[H"
    LINE_BEGINNING = "\033[1F"


class Clear:
    LINE = "\033[2K"
    SCREEN = "\033[2J"
