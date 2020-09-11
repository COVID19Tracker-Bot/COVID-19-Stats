## Module for miscellaneous commands.

import discord
from discord.ext import commands
import hashlib
from hashlib import sha256
import json

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['sourcecode'])
    async def source(self, ctx):
        await ctx.send('https://github.com/COVID19Tracker-Bot/COVID-19-Stats')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':ping_pong: Pong! The latency is **{round(bot.latency * 1000)}ms**.')

    @commands.command()
    async def pong(self, ctx):
        await ctx.send(f':ping_pong: Ping! The latency is **{round(bot.latency * 1000)}ms**.')

    @commands.command()
    async def help(self, ctx):
        hash = bytes(str(ctx.guild.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
            prefix = prefixes[str(hex_dig)]
        await ctx.send(f'''**COVID-19 Hong Kong Stats Discord Bot - Help**

`{str(prefix)}ping`
Returns the bot's latency in milliseconds.

`{str(prefix)}c19hkd [DD/MM/YYYY (optional)]`
Sends data regarding Hong Kong's COVID-19 status as of a date. If no date is inserted, the bot will return data as of yesterday.

`{str(prefix)}c19hkcd [caseno]`
Sends data regarding a COVID-19 case in Hong Kong, given the case number.
Note that [caseno] is **required**.

`{str(prefix)}c19hklist [dataType] [operator/ sortType] [val1] [val2]`
Returns a list regarding multiple days of Hong Kong's COVID-19 status, given the parameters.
See images below for details.
Note: this command does not show properly for some clients.

`{str(prefix)}c19hkclist [dataType] [operator/ sortType] [val1] [val2]`
Returns a list regarding multiple Hong Kong's COVID-19 cases, given the parameters.
See images below for details.
Note: this command does not show properly for some clients.

`{str(prefix)}cprefix [newprefix]`
Changes the bot's prefix to the one the user specifies. Requires the user to have the **Manage Server** permission.

`{str(prefix)}invite`
Sends the invite link for the bot.

`{str(prefix)}source`
Sends the source code for the bot.

`{str(prefix)}help`
This command.

https://i.imgur.com/qnpcx83.png
https://i.imgur.com/mfccw5P.png''')

    @commands.command()
    async def invite(self, ctx):
        await ctx.send('https://discord.com/oauth2/authorize?client_id=744841070621360169&scope=bot&permissions=19456')

def setup(bot):
    bot.add_cog(Misc(bot))