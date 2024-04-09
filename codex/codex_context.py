import asyncio
import datetime
import random
from typing import List, Tuple, Union, Any, Callable, Iterable, Optional, Sequence

import discord
from discord import app_commands, Embed, File, GuildSticker, StickerItem, AllowedMentions, Message, MessageReference, \
    PartialMessage
from discord.ext import commands
from discord.ui import View

import codex


async def notify_user(user, message):
    if user is not None:
        channel = user.dm_channel
        if channel is None:
            channel = await user.create_dm()
        await channel.send(message)


vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)


def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω´・)', '(´・ω・`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format(
                'Y' if v.isupper() else 'y', v))

    return text


def _wrap_user(user: discord.abc.User):
    return f"**{user}** "


class CodexContext(commands.Context):
    INFO = 0
    ERROR = 1
    OK = 2

    @property
    def clean_prefix(self):
        return self.prefix

    async def trash_reaction(self, message: discord.Message):
        if len(message.embeds) == 0:
            return

        def check(_reaction: discord.Reaction, _user: Union[discord.User, discord.Member]):
            return all([
                _user.id == self.author.id or _user.guild_permissions.manage_messages,
                _reaction.message.id == message.id,
                str(_reaction) == "🗑️"
            ])

        await message.add_reaction("🗑️")
        await asyncio.sleep(0.5)
        try:
            _, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.clear_reactions()
        else:
            await message.delete()

    async def send_info(self, message: str, *, user: discord.abc.User = None,
                        title: str = None, trash: bool = False, ping: bool = False):
        if not user:
            user = self.author
        msg = await self.send(
            user.mention if ping else None,
            embed=discord.Embed(
                title=title,
                description=f"{_wrap_user(user) if user else ''}{message}",
                colour=await self.get_color(self.INFO)
            ))
        if trash:
            await self.trash_reaction(msg)
        else:
            return msg

    async def send_ok(self, message: str, *, user: discord.abc.User = None,
                      title: str = None, trash: bool = False, ping: bool = False):
        if not user:
            user = self.author
        msg = await self.send(
            user.mention if ping else None,
            embed=discord.Embed(
                title=title,
                description=f"{_wrap_user(user) if user else ''}{message}",
                colour=await self.get_color(self.OK)
            ))
        if trash:
            await self.trash_reaction(msg)
        else:
            return msg

    async def send_error(self, message: str, *, user: discord.abc.User = None,
                         title: str = None, trash: bool = False, ping: bool = False):
        if not user:
            user = self.author
        msg = await self.send(
            user.mention if ping else None,
            embed=discord.Embed(
                title=title,
                description=f"{_wrap_user(user) if user else ''}{message}",
                colour=await self.get_color(self.ERROR)
            ))
        if trash:
            await self.trash_reaction(msg)
        else:
            return msg

    async def pages(self, lst: List[Any], n: int,
                    title: str, *, fmt: str = "%s",
                    thumbnails: List[str] = None, sep: str = "\n", color=None) \
            -> List[discord.Embed]:
        # noinspection GrazieInspection
        """
            Paginates a list into embeds to use with :class:disputils.BotEmbedPaginator
            :param lst: the list to paginate
            :param n: the number of elements per page
            :param title: the title of the embed
            :param fmt: a % string used to format the resulting page
            :param sep: the string to join the list elements with
            :param thumbnails: thumbnail
            :param color: color
            :return: a list of embeds
            """
        l: List[List[str]] = self.group_list([str(i) for i in lst], n)
        pgs = [sep.join(page) for page in l]
        if not thumbnails:
            return [
                discord.Embed(
                    title=f"{title} - {i + 1}/{len(pgs)}",
                    description=fmt % pg,
                    color=color,
                ) for i, pg in enumerate(pgs)
            ]
        else:
            return [
                discord.Embed(
                    title=f"{title} - {i + 1}/{len(pgs)}",
                    description=fmt % pg,
                    color=color,
                ).set_thumbnail(url=thumbnails[i]) for i, pg in enumerate(pgs)
            ]

    @staticmethod
    def group_list(lst: List[Any], n: int) -> List[List[Any]]:
        """
        Splits a list into sub-lists of n
        :param lst: the list
        :param n: the subgroup size
        :return: The list of lists
        """
        return [lst[i * n:(i + 1) * n] for i in range((len(lst) + n - 1) // n)]

    @staticmethod
    def numbered(lst: Iterable[Any], num_start=0) -> List[str]:
        """
        Returns a numbered version of a list
        """
        return [f"**{i + num_start}.** {a}" for i, a in enumerate(lst)]

    async def get_color(self, typ: int):
        if not self.guild:
            return discord.Color([0x0000ff, 0xff0000, 0x00cc00][typ])
        if typ == 0:
            return discord.Color(0x0000ff)
        if typ == 1:
            return discord.Color(0xaa0000)
        if typ == 2:
            return discord.Color(0x00aa00)
            # (await self.bot.db.guild_setting(self.guild.id)).ok_color
        raise ValueError

    async def input(self, typ: type, cancel_str: str = "cancel", ch: Callable = None, err=None, check_author=True,
                    return_author=False, del_error=60, del_response=False, timeout=60.0):
        def check(m):
            return ((m.author == self.author and m.channel == self.channel) or not check_author) and not m.author.bot

        while True:
            try:
                inp: discord.Message = await self.bot.wait_for('message', check=check, timeout=timeout)
                if del_response:
                    await inp.delete()
                if inp.content.lower() == cancel_str.lower():
                    return (None, None) if return_author else None
                res = typ(inp.content.lower())
                if ch:
                    if not ch(res):
                        raise ValueError
                return (res, inp.author) if return_author else res
            except ValueError:
                await self.send(err or "That's not a valid response, try again" +
                                ("" if not cancel_str else f" or type `{cancel_str}` to quit"),
                                delete_after=del_error)
                continue
            except asyncio.TimeoutError:
                await self.send("You took too long to respond ): Try to start over", delete_after=del_error)
                return (None, None) if return_author else None

    async def embed(self,
                    author: Optional[str] = None,
                    thumbnail: Optional[str] = None,
                    title: Optional[Any] = None,
                    title_url: Optional[Any] = None,
                    description: Optional[str] = None,
                    clr: Optional[discord.Color] = None,
                    image: Optional[str] = None,
                    fields: List[Tuple[str, str]] = None,
                    not_inline: List[int] = None,
                    timestamp: Optional[datetime.datetime] = None,
                    footer: Optional[str] = None):
        embed = discord.Embed(title=title, url=title_url,
                              description=description,
                              color=clr or discord.Color.random())
        embed.set_footer(text=footer)
        embed.set_image(url=image)
        embed.timestamp = timestamp
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if author:
            embed.set_author(name=author)
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None")
        await self.send(embed=embed)
