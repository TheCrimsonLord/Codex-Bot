import logging
from discord.ext import commands
import codex


class Owner(commands.Cog):
    def __init__(self, bot: codex.CodexBot):
        self.bot = bot
        self.logger = logging.getLogger('codex')

    @commands.is_owner()
    @commands.command(brief="Sync slash commands | Owner Only")
    async def sync(self, ctx: codex.CodexContext):
        synced = await self.bot.tree.sync()
        await ctx.send_ok(f"Synced {len(synced)} command(s).")

    @commands.is_owner()
    @commands.command(description="Restart Codex | Owner Only")
    async def restart(self, ctx: codex.CodexContext):
        self.bot.is_restarting = True
        self.bot.restart_response_channel = ctx.channel.id
        await ctx.send_ok(title="Restarting", message="Attempting to restart. See you on the other side!")
        await self.bot.close()

    @commands.is_owner()
    @commands.command(description="Testing command | Owner Only")
    async def test(self, ctx: codex.CodexContext):
        self.logger.info("test")


async def setup(bot: codex.CodexBot) -> None:
    await bot.add_cog(Owner(bot))
