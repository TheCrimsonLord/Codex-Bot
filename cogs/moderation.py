from discord.ext import commands
import codex
import discord
import datetime as dt
from discord import app_commands
from datetime import time


class Moderation(commands.Cog):
    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_messages=True)
    @app_commands.checks.cooldown(1, 30)
    @app_commands.command(description="Clear message from a channel | Deletes 5 messages by default")
    async def clear(self, interaction: discord.Interaction, amount: int = 5):
        messages_list = []
        embed = discord.Embed(
            title="Deleting",
            colour=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)
        async for message in interaction.channel.history(limit=amount + 1):
            messages_list.append(message)
            if len(messages_list) > 90:
                await interaction.channel.delete_messages(messages_list)
                messages_list = []
        await interaction.channel.delete_messages(messages_list)


async def setup(bot: codex.CodexBot) -> None:
    await bot.add_cog(Moderation(bot))

