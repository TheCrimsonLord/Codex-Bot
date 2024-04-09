import os
import sys
import time
import discord
import dotenv

import codex

bot = codex.CodexBot(intents=discord.Intents.all(), fetch_offline_users=True,
                     command_prefix=".", help_command=None)


dotenv.load_dotenv()
bot.run(os.getenv("TOKEN"))

if bot.is_restarting:
    bot.logger.info("Bot is attempting restart")
    bot.logger.info("In 3")
    time.sleep(1)
    bot.logger.info("2")
    time.sleep(1)
    bot.logger.info("1")
    time.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)
