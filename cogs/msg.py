## Module for the message listener.

import discord
from discord.ext import commands
import hashlib
from hashlib import sha256
import json
import difflib

class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ## Mention for prefix
        if self.bot.user in message.mentions:
            hash = bytes(str(message.guild.id), 'ascii')
            hash_object = hashlib.sha256(hash)
            hex_dig = hash_object.hexdigest()
            with open('prefix.json', 'r') as f:
                prefixes = json.load(f)
            try:
                await message.channel.send(f'My prefix is: `{str(prefixes[str(hex_dig)])}`')
            except KeyError:
                prefixes[str(hex_dig)] = 'c!'
                with open('prefix.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
                with open('prefix.json', 'r') as f:
                    prefixes = json.load(f)
                await message.channel.send(f'My prefix is: `{str(prefixes[str(hex_dig)])}`')
        ## Invalid command detection
        hash = bytes(str(message.guild.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
        try:
            if message.content.startswith(str(prefixes[str(hex_dig)])):
                ctx = await self.bot.get_context(message)
                if ctx.valid:
                    pass
                else:
                    global commands
                    commands = [
                        'cprefix',
                        'ping',
                        'help',
                        'c19hkd'
                        'c19hkcd',
                        'c19hklist',
                        'c19hkclist',
                        'invite',
                        'source'
                    ]
                    content = message.content.replace(f'{str(prefixes[str(hex_dig)])}', '')
                    await ctx.send(f'This is an invalid command! Did you mean `{str(prefixes[str(hex_dig)])}{str(difflib.get_close_matches(content, commands, n=1)[0])}`?\nUse `{str(prefixes[str(hex_dig)])}help` for a list of commands.')
        except KeyError:
            prefixes[str(hex_dig)] = 'c!'
            with open('prefix.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
            with open('prefix.json', 'r') as f:
                prefixes = json.load(f)
            print(f'Set prefix for guild id {message.guild.id} (hashed object: {hex_dig}) to "{str(prefixes[str(hex_dig)])}')

def setup(bot):
    bot.add_cog(MessageHandler(bot))