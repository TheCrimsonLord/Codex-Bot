import random
from typing import Optional

import aiohttp
import discord
import codex
from discord import app_commands
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Ask and you shall receive ")
    async def _8ball(self, interaction: discord.Interaction, question: str):
        responses = ["It is certain",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Maybe?",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        embed = discord.Embed(
            title=random.choice(responses),
            description=question,
            colour=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Clones your friends")
    async def clone(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        embed = discord.Embed(
            title=f"Cloning Processes of {user.display_name} Complete",
            colour=discord.Color.random()
        )
        embed.set_image(
            url=user.avatar
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.checks.cooldown(3, 5)
    @app_commands.command(description="Sends a random death message")
    async def kill(self, interaction: discord.Interaction, user: discord.Member):
        author = interaction.user.display_name
        usr = user.display_name
        if user.name == interaction.user.name:
            embed = discord.Embed(
                title=f"Hey {author}, if you are struggling with suicidal "
                      f"thoughts there's people to help you\n"
                      f"You can call or text 988 toll free completely anonymously",
                colour=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
        elif user.id == 349663496465678338:
            outcome = [
                f"{author} was shot.",
                f"{usr} stabbed {author} in the chest",
                f"{author} dodged the attack",
                f"{author} was run over by a car",
                f"{author} was shot by a tank",
                f"{author} had a heart attack",
                f"{usr} called in a tactical nuke\nto be dropped on {author}",
                f"{author} tried to stab {usr} and\ngot called the cops on themself",
                f"{usr} shot you instead"
            ]
            embed = discord.Embed(
                title=f"{random.choice(outcome)}",
                colour=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
        else:
            outcome = [
                f"{usr} was shot.",
                f"{author} stabbed {usr} in the chest",
                f"{usr} dodged the attack",
                f"{usr} was run over by a car",
                f"{usr} was shot by a tank",
                f"{usr} had a heart attack",
                f"{author} called in a tactical nuke\nto be dropped on {usr}",
                f"{author} tried to stab {usr} and\ngot called the cops on themself",
                f"{usr} shot you instead"
            ]
            embed = discord.Embed(
                title=f"{random.choice(outcome)}",
                colour=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.checks.cooldown(3, 1)
    @app_commands.command(description="Sends a hot post from any subreddit")
    async def meme(self, interaction: discord.Interaction, subreddit: Optional[str]):
        subreddit = subreddit or "memes"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/{subreddit}/hot.json?sort=hot") as r:
                res = await r.json()

        if len(subreddit) > 21:
            embed = discord.Embed(
                title=f"It seems that {subreddit} isn't available right now.",
                colour=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                delete_after=10
            )
        elif res["data"]["dist"] <= 1:
            embed = discord.Embed(
                title=f"It seems that {subreddit} isn't available right now.",
                colour=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                delete_after=10
            )
        elif 'error' in res:
            embed = discord.Embed(
                title=f"It seems that {subreddit} isn't available right now.",
                colour=discord.Color.random()
            )
            await interaction.response.send_message(
                embed=embed,
                delete_after=10
            )
        else:
            dist = res["data"]["dist"]
            data = res["data"]["children"][random.randint(0, (dist - 1))]["data"]
            desc = data["selftext"] or "\n"
            reddit_title = data["title"]
            reddit_link = data["permalink"]
            if data["over_18"]:
                if interaction.channel.is_nsfw():
                    embed = discord.Embed(
                        title=reddit_title, description=desc,
                        url=f"https://reddit.com{reddit_link}",
                        colour=discord.Color.random()
                    )
                    embed.set_footer(
                        text=f"👍{data['ups']} | 💬{data['num_comments']}"
                    )
                    embed.set_image(
                        url=data["url"]
                    )
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"**{interaction.channel}** is not a NSFW channel,\nbut you"
                              f"can still look at it on your own if you want.",
                        url=f"https://reddit.com{reddit_link}",
                        colour=discord.Color.random()
                    )
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title=reddit_title, description=desc,
                    url=f"https://reddit.com{reddit_link}",
                    colour=discord.Color.random()
                )
                embed.set_footer(
                    text=f"👍{data['ups']} | 💬{data['num_comments']}"
                )
                embed.set_image(
                    url=data["url"]
                )
                await interaction.response.send_message(embed=embed)


async def setup(bot: codex.CodexBot) -> None:
    await bot.add_cog(Fun(bot))
