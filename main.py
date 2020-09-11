import discord
from discord.ext import commands
import hashlib
from hashlib import sha256
import json
import os

## Define your TOKEN environment variable for the bot to work!
token = os.environ.get("TOKEN")
## Define your OWNER environment variable for the bot to work and to recognize the bot owner!
owner = os.environ.get("OWNER")

def get_prefix(bot, message):
    hash = bytes(str(message.guild.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(hex_dig)]
        prefix = prefixes[str(hex_dig)]
    ## Prefix not found
    except KeyError:
        prefixes[str(hex_dig)] = 'c!'
        return prefixes[str(hex_dig)]
        prefix = prefixes[str(hex_dig)]

bot = commands.Bot(command_prefix=get_prefix)
## Removes the help command in order for custom help command to work
bot.remove_command('help')

for i in os.listdir('./cogs'):
    if i.endswith('.py'):
        bot.load_extension(f'cogs.{i[:-3]}')
print('Extensions loaded!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}. Bot is ready.'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="mentions for prefix"))
    print('Bot status changed!')

@bot.command()
async def extload(ctx, cog):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    hash = bytes(str(owner), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig2 = hash_object.hexdigest()
    if hex_dig == hex_dig2:
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def extunload(ctx, cog):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    hash = bytes(str(owner), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig2 = hash_object.hexdigest()
    if hex_dig == hex_dig2:
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded extension `{cog}`!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command()
async def extlist(ctx):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    hash = bytes(str(owner), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig2 = hash_object.hexdigest()
    if hex_dig == hex_dig2:
        exts = []
        for i in os.listdir('./cogs'):
            if i.endswith('.py'):
                exts.append(i[:-3])
        message = ''
        for j in exts:
            message += f'''`{j}`\n'''
        await ctx.send(message)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

bot.run(token)
