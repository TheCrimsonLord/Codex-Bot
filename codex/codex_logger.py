import logging
from colorama import init, Fore, Style

init()

colours = {
    "TRACE": f"{Fore.WHITE}{Style.DIM}",
    "DEBUG": f"{Fore.LIGHTWHITE_EX}",
    "INFO": "",
    "WARNING": f"{Fore.YELLOW}{Style.BRIGHT}",
    "ERROR": f"{Fore.LIGHTRED_EX}{Style.BRIGHT}",
    "CRITICAL": f"{Fore.RED}{Style.BRIGHT}",
}
colours2 = {
    "TRACE": f"{Fore.WHITE}{Style.DIM}",
    "DEBUG": Fore.LIGHTWHITE_EX,
    "INFO": Fore.BLUE,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.LIGHTRED_EX,
    "CRITICAL": Fore.RED,
}
styles = {
    "TRACE": f"{Fore.WHITE}{Style.DIM}",
    "DEBUG": f"{Fore.LIGHTWHITE_EX}",
    "INFO": "",
    "WARNING": "",
    "ERROR": "",
    "CRITICAL": Style.BRIGHT,
}
names = {
    "codex": Fore.BLUE,
    "discord.client": Fore.GREEN,
    "discord.gateway": Fore.MAGENTA,
    "discord.ext.commands.core": Fore.YELLOW,
    "discord.http": Fore.RED
}


class CodexLogger(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> None:
        name = record.name
        level = record.levelno  # noqa F841
        level_name = record.levelname
        if name == "codex":
            split = record.msg.split(":")
            if len(split) == 1:
                sub = None
                message = split[0]
            else:
                sub = split[0]
                message = ":".join(split[1:])
        else:
            message = record.msg
            sub = None

        message %= record.args

        print(f"{colours2[level_name]}{styles[level_name]}{level_name:>8}{Style.RESET_ALL}"
              f" "
              f"{Style.BRIGHT}{names[name]}{name}{Style.RESET_ALL} " +
              (f"» {Style.BRIGHT}{Fore.LIGHTBLUE_EX}{sub}{Style.RESET_ALL} " if sub else '') +
              f"» "
              f"{colours[level_name]}{message}{Style.RESET_ALL}")
