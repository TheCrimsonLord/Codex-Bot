from datetime import timedelta
from typing import Union

import discord


def dhms_notation(delta: Union[int, timedelta]):
    if isinstance(delta, int):
        delta = timedelta(seconds=delta)
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{delta.days}d{hours}h{minutes}m{seconds}s"


def dhm_notation(td: timedelta, sep="", full=False):
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    return sep.join([f"{td.days}{'days' if full else 'd'}",
                     f"{hours}{'hours' if full else 'h'}",
                     f"{minutes}{'minutes' if full else 'm'}"])


def color_to_hex_string(color: Union[discord.Color]) -> str:
    return "".join(hex(n)[2:].rjust(2, "0") for n in color.to_rgb())
