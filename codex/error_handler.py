from discord.ext import commands
import codex


@commands.Cog.listener()
async def on_command_error(ctx: codex.CodexContext, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send_error("This command is restricted to bot\nowner only")


@commands.Cog.listener()
async def on_command_error(ctx: codex.CodexContext, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send_error("This command doesn't exist")


class RoleHierarchyError(commands.CommandError):
    pass


class PermissionFailed(commands.CommandError):
    pass


class NotOwner(commands.CommandError):
    pass
