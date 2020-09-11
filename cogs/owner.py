## Module for bot owner-only commands.

import discord
from discord.ext import commands
import hashlib
from hashlib import sha256
import traceback
import json
import os
import traceback
import io
import sys

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='get_guild')
    async def getguildcommand(self, ctx, arg1):
        owner = os.environ.get("OWNER")
        hash = bytes(str(ctx.message.author.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        hash = bytes(str(owner), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig2 = hash_object.hexdigest()
        if str(hex_dig) == str(hex_dig2):
            guild = self.bot.get_guild(int(arg1))
            if guild != None:
                await ctx.send(f'Guild name: {str(guild.name)}\nGuild owner: {str(guild.owner)}')
            else:
                await ctx.send('Invalid guild ID!')
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

    @commands.command(name='changepresence')
    async def cp(self, ctx, type, arg1, *, arg2 = None):
        owner = os.environ.get("OWNER")
        hash = bytes(str(ctx.message.author.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        hash = bytes(str(owner), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig2 = hash_object.hexdigest()
        if str(hex_dig) == str(hex_dig2):
            try:
                if type == 'playing':
                    if arg2 == None:
                        await self.bot.change_presence(activity=discord.Game(name=str(arg1)))
                    else:
                        await self.bot.change_presence(activity=discord.Game(name=f'{str(arg1)} {str(arg2)}'))
                elif type == 'listening':
                    if arg2 == None:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=str(arg1)))
                    else:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{str(arg1)} {str(arg2)}'))
                elif type == 'watching':
                    if arg2 == None:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(arg1)))
                    else:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{str(arg1)} {str(arg2)}'))
                elif type == 'streaming':
                    if arg2 != None:
                        await self.bot.change_presence(activity=discord.Streaming(name=arg2, url=arg1))
                    else:
                        await self.ctx.send('`arg2` is required for type streaming!')
            except:
                x = traceback.format_exc()
                await ctx.send(f'An error has occured!\n```\n{str(x)}\n```')

    def chunks(s, n):
        """Produce `n`-character chunks from `s`."""
        for start in range(0, len(s), n):
            yield s[start:start+n]

    @commands.command()
    ## Shows the contents of the prefix.json file, for bot owner only.
    async def prefixjson(self, ctx):
        owner = os.environ.get("OWNER")
        hash = bytes(str(ctx.message.author.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        hash = bytes(str(owner), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig2 = hash_object.hexdigest()
        if str(hex_dig) == str(hex_dig2):
            with open('prefix.json', 'r') as f:
                prefixes = json.load(f)
                prefix = json.dumps(prefixes)
            try:
                for chunk in chunks(prefix, 1000):
                    await ctx.send(f'```\n{chunk}\n```')
            except TypeError:
                await ctx.send(f'```\n{prefix}\n```')
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

    @commands.command()
    async def cprefixsu(self, ctx, arg1, arg2 = None):
        owner = os.environ.get("OWNER")
        hash = bytes(str(ctx.message.author.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        hash = bytes(str(owner), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig2 = hash_object.hexdigest()
        hash = bytes(str(ctx.guild.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig3 = hash_object.hexdigest()
        if str(hex_dig) == str(hex_dig2):
            if arg2 != None:
                with open('prefix.json', 'r') as f:
                    prefixes = json.load(f)
                prefixes[str(arg1)] = str(arg2)
                with open('prefix.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
                with open('prefix.json', 'r') as f:
                    prefixes = json.load(f)
                    prefix = prefixes[str(hex_dig3)]
                await ctx.send(f'''`prefixes[{str(arg1)}]` is now `{str(arg2)}`. Verify using `{prefix}prefixjson`.''')
            elif arg2 == None:
                with open('prefix.json', 'r') as f:
                    prefixes = json.load(f)
                prefixes.pop(str(arg1))
                with open('prefix.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
                with open('prefix.json', 'r') as f:
                    prefixes = json.load(f)
                    prefix = prefixes[str(hex_dig3)]
                await ctx.send(f'''`prefixes[{str(arg1)}]` has been removed. Verify using `{prefix}prefixjson`.''')
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")
    @cprefixsu.error
    async def cprefixsu_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing Required Argument!")

    @commands.command(name='hash')
    async def hashcommand(self, ctx, *, arg1):
        owner = os.environ.get("OWNER")
        hash = bytes(str(ctx.message.author.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        hash = bytes(str(owner), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig2 = hash_object.hexdigest()
        if str(hex_dig) == str(hex_dig2):
            hash = bytes(str(arg1), 'ascii')
            hash_object = hashlib.sha256(hash)
            hex_dig = hash_object.hexdigest()
            await ctx.send(hex_dig)

    @commands.command(name='exec')
    async def exec_command(self, ctx, *, arg1):
        owner = os.environ.get("OWNER")
        hash = bytes(str(ctx.message.author.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        hash = bytes(str(owner), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig2 = hash_object.hexdigest()
        if str(hex_dig) == str(hex_dig2):
            arg1 = arg1[6:-4]
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            try:
                exec(arg1)
                output = new_stdout.getvalue()
                sys.stdout = old_stdout
            except:
                x = traceback.format_exc()
                embed=discord.Embed(title=f'Execute Failed!', color=0xff0000)
                embed.set_author(name="COVID-19 Tracker")
                embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
                embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
                await ctx.send(embed = embed)
            else:
                embed=discord.Embed(title=f'Execute Success!', color=0x00ff00)
                embed.set_author(name="COVID-19 Tracker")
                embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
                embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
                await ctx.send(embed = embed)
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

    @commands.command(name='eval')
    async def eval_command(self, ctx, *, arg1):
        ## Put the user IDs of the users you want to whitelist in the list "list". Leave "whitelist" blank!
        ## Alternatively, hash all the user IDs you want to whitelist with SHA256 then put them in "whitelist".
        list = ['438298127225847810', '571590388461076480', '459260229490704394']
        whitelist = []
        if not whitelist and list:
            for i in list:
                hash = bytes(str(i), 'ascii')
                hash_object = hashlib.sha256(hash)
                hex_dig = hash_object.hexdigest()
                whitelist.append(hex_dig)
        elif not whitelist and not list:
            raise NameError('You must fill in at least one of the lists!')
        hash = bytes(str(ctx.message.author.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        if str(hex_dig) in whitelist:
            try:
                evaled = eval(arg1)
            except:
                x = traceback.format_exc()
                embed=discord.Embed(title=f'Evaluate Failed!', color=0xff0000)
                embed.set_author(name="COVID-19 Tracker")
                embed.add_field(name="Code", value=f'```\n{str(arg1)}\n```', inline=False)
                embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
                await ctx.send(embed = embed)
            else:
                embed=discord.Embed(title=f'Evaluate Success!', color=0x00ff00)
                embed.set_author(name="COVID-19 Tracker")
                embed.add_field(name="Code", value=f'```\n{str(arg1)}\n```', inline=False)
                embed.add_field(name="Output", value=f'```\n{str(evaled)}\n```', inline=False)
                await ctx.send(embed = embed)
        else:
            await ctx.send("Sorry, but you don't have permission to do that.")

def setup(bot):
    bot.add_cog(Owner(bot))