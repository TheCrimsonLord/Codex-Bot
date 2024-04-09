import logging
from datetime import datetime
import platform
from typing import List

import discord
from discord.ext import commands, tasks

import os
import psutil
import codex


class CodexBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super(CodexBot, self).__init__(*args, **kwargs)
        self.startup_time = datetime.now()
        self.cog_groups = {}
        self.is_restarting = False
        self.logger = logging.getLogger("codex")
        self.version = "0.0.1a"
        self.ping: int = 0
        self.avg_ping: int = 0
        self.mem: int = 0
        self.max_mem: int = 0
        self.ping_run: List[int] = [0]
        for logger in [
            "codex",
            "discord.client",
            "discord.gateway",
            "discord.http",
            "discord.ext.commands.core"
        ]:
            logging.getLogger(logger).setLevel(logging.DEBUG if logger == "codex" else logging.CRITICAL)
            logging.getLogger(logger).addHandler(codex.CodexLogger())

    @tasks.loop(seconds=2)
    async def resource_loop(self):
        self.mem = psutil.Process(os.getpid()).memory_info().rss // 1000000
        self.max_mem = max(self.mem, self.max_mem)
        self.ping = round(self.latency * 1000)
        self.ping_run.append(self.ping)
        if len(self.ping_run) > 30 * 60:
            del self.ping_run[0]
        self.avg_ping = round(sum(self.ping_run) / len(self.ping_run))

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"Ash fail at creating me."),
            status=discord.Status.do_not_disturb)
        self.resource_loop.start()

    async def on_message(self, message: discord.Message):
        ctx: codex.CodexContext = await self.get_context(message, cls=codex.CodexContext)
        await self.invoke(ctx)

    async def load_cogs(self):
        self.logger.info("Attempting to load cogs")
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await self.load_cogs()
        self.logger.info(f"Running Discord {discord.__version__}, Python {platform.python_version()}")
        await self.login(os.getenv("TOKEN"))
        self.logger.info("Token loaded")
        self.logger.info(f"Codex v{self.version} online!")
        await self.connect()
