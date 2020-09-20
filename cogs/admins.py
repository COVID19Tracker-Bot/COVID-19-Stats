## Module for server admin-related commands.

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import hashlib
from hashlib import sha256

class Admins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['changeprefix'])
    async def cprefix(self, ctx, arg1):
        hash = bytes(str(ctx.guild.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        if not await has_permissions(manage_guild=True).predicate(ctx):
            raise MissingPermissions(["manage_guild"])
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(hex_dig)] = str(arg1)
        with open('prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f'''My prefix is now `{str(arg1)}`! Please remember it.''')
    @cprefix.error
    async def cprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have permission to do that.")

def setup(bot):
    bot.add_cog(Admins(bot))
