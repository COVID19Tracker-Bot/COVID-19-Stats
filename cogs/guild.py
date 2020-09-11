## Module for guild events.

import discord
from discord.ext import commands
import hashlib
from hashlib import sha256
import json

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        hash = bytes(str(guild.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(hex_dig)] = 'c!'
        with open('prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        print(f'I have been invited to {str(guild.name)}! Owner: {str(guild.owner)}')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        hash = bytes(str(guild.id), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(hex_dig))
        with open('prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        print(f'I have been removed from {str(guild.name)}. Owner: {str(guild.owner)}')

def setup(bot):
    bot.add_cog(Guild(bot))