import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from settings import OWNER


def is_owner():
    def predicate(ctx):
        return ctx.author.id == OWNER
    return commands.check(predicate)

print(OWNER)