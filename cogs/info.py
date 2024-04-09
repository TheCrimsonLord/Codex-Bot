from discord.ext import commands, tasks

import codex
from typing import Union, List
from datetime import datetime
import discord
from discord import app_commands

from libs import conversions
from libs.conversions import dhms_notation


class Info(commands.Cog):
    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @app_commands.command(description="Shows Codex's latency to discord")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Pong! Bot Latency is ~{round(self.bot.latency * 1000)}ms",
            colour=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows info on the current server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild: discord.Guild = interaction.guild
        created = guild.created_at.strftime("%c")
        voice_channels = len(guild.voice_channels)
        text_channels = len(guild.text_channels)
        roles = len(guild.roles) - 1
        statuses = {
            "dnd": 0,
            "idle": 0,
            "online": 0,
            "bot": 0,
            "offline": 0
        }
        member: discord.Member
        for member in guild.members:
            if member.bot:
                statuses["bot"] += 1
            else:
                statuses[str(member.status)] += 1
        embed = discord.Embed(
            title=f"Info for {guild}",
            colour=discord.Color.random()
        )
        fields = [
            ("ID", guild.id),
            ("Created at", created),
            ("Owner", guild.owner.display_name),
            ("Channels", f"{voice_channels} Voice, {text_channels} Text"),
            ("System Channel", (guild.system_channel.mention if guild.system_channel else "None")),
            ("Members", guild.member_count),
            ("Roles", roles),
            ("Features", "\n".join(guild.features) if guild.features else "None"),
            ("Breakdown", f":green_circle: {statuses['online']} online\n"
                          f":yellow_circle: {statuses['idle']} idle\n"
                          f":red_circle: {statuses['dnd']} dnd\n"
                          f":white_circle: {statuses['offline']} offline\n"
                          f":robot: {statuses['bot']} bots\n")
        ]
        not_inline: List[int] = []
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None", inline=n not in not_inline)
        embed.set_thumbnail(url=guild.icon if guild.icon else None)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows info on a user")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        if not member:
            member = interaction.user
        joined_at = member.joined_at.strftime("%c")
        created_at = member.created_at.strftime("%c")
        r: discord.Role
        hoisted_roles = [r for r in member.roles if r.hoist and r.id != interaction.guild.id]
        normal_roles = [r for r in member.roles if not r.hoist and r.id != interaction.guild.id]

        embed = discord.Embed(
            title=f"Info for {member}",
            colour=member.color
        )

        fields = [
            ("ID", member.id),
            ("Joined Server", joined_at),
            ("Joined Discord", created_at),
            (f"Hoisted Roles ({len(hoisted_roles)}) ",
             " ".join([r.mention for r in hoisted_roles[:-6:-1]]) if hoisted_roles
             else "None"),
            (f"Normal Roles ({len(normal_roles)})",
             " ".join([r.mention for r in normal_roles[:-6:-1] if r.id not in
                       [x.id for x in hoisted_roles]]) if len(normal_roles) > 1
             else "None"),
            ("Top Role", member.roles[-1].mention if len(member.roles) > 1 else "None"),
            ("Discord Profile", f"[Profile Picture Link]({member.avatar.url})")
        ]
        not_inline: List[int] = []
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None", inline=n not in not_inline)
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows info on a role")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(
            title=f"Info for {role}",
            colour=role.colour
        )
        fields = [
            ("ID", role.id),
            ("Members", len(role.members)),
            ("Color", f"#{conversions.color_to_hex_string(role.colour)}"),
            ("Hoisted", role.hoist),
            ("Mentionable", role.mentionable),
            ("Position", role.position),
            ("Created at", role.created_at.strftime("%c"))
        ]
        not_inline: List[int] = []
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None", inline=n not in not_inline)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows info on a voice channel")
    async def voiceinfo(self, interaction: discord.Interaction, *, channel: discord.VoiceChannel):
        embed = discord.Embed(
            title=f"Info for {channel}",
            colour=discord.Color.random()
        )
        fields = [
            ("ID", channel.id),
            ("Created at", channel.created_at.strftime("%c")),
            ("Max Users", channel.user_limit or "No Limit"),
            ("Bitrate", f"{channel.bitrate // 1000}kbps"),
        ]
        not_inline: List[int] = []
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None", inline=n not in not_inline)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows info on a text channel")
    async def textinfo(self, interaction: discord.Interaction, channel: discord.TextChannel):
        embed = discord.Embed(
            title=f"Info for {channel}",
            colour=discord.Color.random()
        )
        fields = [
            ("ID", channel.id),
            ("Created at", channel.created_at.strftime("%c")),
            ("Slowmode", f"{channel.slowmode_delay}s" if channel.slowmode_delay else "No Slowmode")
        ]
        not_inline: List[int] = []
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None", inline=n not in not_inline)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        description="Shows bot stats"
    )
    async def stats(self, interaction: discord.Interaction):
        text_channels = 0
        voice_channels = 0
        for channel in self.bot.get_all_channels():
            if isinstance(channel, discord.TextChannel):
                text_channels += 1
            if isinstance(channel, discord.VoiceChannel):
                voice_channels += 1
        embed = discord.Embed(
            colour=discord.Color.random()
        )
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_author(name=f"Codex {self.bot.version}")
        fields = [
            ("Ping", f"{round(self.bot.latency * 1000)} ms\n"
                     f"{self.bot.avg_ping} ms (1h average)"),
            ("Memory",
             f"{self.bot.mem} MB\n{self.bot.max_mem} MB max"),
            ("Shard", f"{self.bot.shard_id or 0}/{self.bot.shard_count}"),
            ("Uptime", dhms_notation(datetime.now() - self.bot.startup_time)),
            ("Presence", f"{len(self.bot.guilds)} Guilds\n"
                         f"{text_channels} Text Channels\n"
                         f"{voice_channels} Voice Channels\n"
                         f"{len(self.bot.users)} Users Cached"),
        ]
        not_inline: List[int] = []
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None", inline=n not in not_inline)
        await interaction.response.send_message(embed=embed)


async def setup(bot: codex.CodexBot) -> None:
    await bot.add_cog(Info(bot))
