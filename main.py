import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
from datetime import datetime, date, timedelta
import pytz
import tabulate
from tabulate import tabulate
import pandas as pd
import urllib.request
import json
import sys
import os
import traceback
import difflib
import io
import hashlib
from hashlib import sha256

token = os.environ.get("TOKEN")

def get_prefix(bot, message):
    hash = bytes(str(message.guild.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(hex_dig)]
        prefix = prefixes[str(hex_dig)]
    except KeyError:
        prefixes[str(hex_dig)] = 'c!'
        return prefixes[str(hex_dig)]
        prefix = prefixes[str(hex_dig)]

bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command('help')

@bot.event
async def on_message(message):
    ## Mention for prefix
    if bot.user in message.mentions:
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
            ctx = await bot.get_context(message)
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
                print(content)
                await ctx.send(f'This is an invalid command! Did you mean `{str(prefixes[str(hex_dig)])}{str(difflib.get_close_matches(content, commands, n=1)[0])}`?\nUse `{str(prefixes[str(hex_dig)])}help` for a list of commands.')
    except KeyError:
        prefixes[str(hex_dig)] = 'c!'
        with open('prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
        print(f'Set prefix for guild id {message.guild.id} (hashed object: {hex_dig}) to `{str(prefixes[str(hex_dig)])}`')
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}. Bot is ready.'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="mentions for prefix"))
    print('Bot status changed!')

@bot.event
async def on_guild_join(guild):
    hash = bytes(str(guild.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(hex_dig)] = 'c!'
    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    print(f'I have been invited to {str(guild.name)}! Owner: {str(guild.owner)}')

@bot.event
async def on_guild_remove(guild):
    hash = bytes(str(guild.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(hex_dig))
    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    print(f'I have been removed from {str(guild.name)}. Owner: {str(guild.owner)}')

@bot.command(aliases = ['sourcecode'])
async def source(ctx):
    await ctx.send('https://github.com/COVID19Tracker-Bot/COVID-19-Stats')

@bot.command(name='get_guild')
async def getguildcommand(ctx, arg1):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    if str(hex_dig) == 'c3b59cc104f00d50259f1ff2979d3284cc3123300609a9fb14718da1fdbfccad':
        guild = bot.get_guild(int(arg1))
        if guild != None:
            await ctx.send(f'Guild name: {str(guild.name)}\nGuild owner: {str(guild.owner)}')
        else:
            await ctx.send('Invalid guild ID!')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command(name='hash')
async def hashcommand(ctx, *, arg1):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    if str(hex_dig) == 'c3b59cc104f00d50259f1ff2979d3284cc3123300609a9fb14718da1fdbfccad':
        hash = bytes(str(arg1), 'ascii')
        hash_object = hashlib.sha256(hash)
        hex_dig = hash_object.hexdigest()
        await ctx.send(hex_dig)

@bot.command(name='changepresence')
async def cp(ctx, type, arg1, *, arg2 = None):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    if str(hex_dig) == 'c3b59cc104f00d50259f1ff2979d3284cc3123300609a9fb14718da1fdbfccad':
        try:
            if type == 'playing':
                if arg2 == None:
                    await bot.change_presence(activity=discord.Game(name=str(arg1)))
                else:
                    await bot.change_presence(activity=discord.Game(name=f'{str(arg1)} {str(arg2)}'))
            elif type == 'listening':
                if arg2 == None:
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=str(arg1)))
                else:
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{str(arg1)} {str(arg2)}'))
            elif type == 'watching':
                if arg2 == None:
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(arg1)))
                else:
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{str(arg1)} {str(arg2)}'))
            elif type == 'streaming':
                if arg2 != None:
                    await bot.change_presence(activity=discord.Streaming(name=arg2, url=arg1))
                else:
                    await ctx.send('`arg2` is required for type streaming!')
        except:
            x = traceback.format_exc()
            await ctx.send(f'An error has occured!\n```\n{str(x)}\n```')

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

@bot.command()
async def prefixjson(ctx):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    if str(hex_dig) == 'c3b59cc104f00d50259f1ff2979d3284cc3123300609a9fb14718da1fdbfccad':
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

@bot.command()
async def cprefixsu(ctx, arg1, arg2):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    if str(hex_dig) == 'c3b59cc104f00d50259f1ff2979d3284cc3123300609a9fb14718da1fdbfccad':
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(arg1)] = str(arg2)
        with open('prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        with open('prefix.json', 'r') as f:
            prefixes = json.load(f)
            prefix = prefixes[str(ctx.guild.id)]
        await ctx.send(f'`prefixes[{str(arg1)}]` is now `{str(arg2)}`. Verify using `{prefix}prefixjson`.')
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")
@cprefixsu.error
async def cprefixsu_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing Required Argument!")

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! The latency is **{round(bot.latency * 1000)}ms**.')

@bot.command()
async def pong(ctx):
    await ctx.send(f':ping_pong: Ping! The latency is **{round(bot.latency * 1000)}ms**.')

@bot.command(aliases = ['changeprefix'])
async def cprefix(ctx, arg1):
    if not await has_permissions(manage_guild=True).predicate(ctx):
        raise MissingPermissions(["manage_guild"])
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = str(arg1)
    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'''My prefix is now `{str(arg1)}`! Please remember it.''')
@cprefix.error
async def cprefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Sorry, but you don't have permission to do that.")

@bot.command(name='exec')
async def exec_command(ctx, *, arg1):
    hash = bytes(str(ctx.message.author.id), 'ascii')
    hash_object = hashlib.sha256(hash)
    hex_dig = hash_object.hexdigest()
    if str(hex_dig) == 'c3b59cc104f00d50259f1ff2979d3284cc3123300609a9fb14718da1fdbfccad':
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

@bot.command(name='eval')
async def eval_command(ctx, *, arg1):
    whitelist = ['c3b59cc104f00d50259f1ff2979d3284cc3123300609a9fb14718da1fdbfccad', 'ae7ff309e32c3ebe31578cd895ca68201b86684ae5f5caad5d591bce38cacc6b', 'ec3cc93cc9fed9248bd338d1d6cb481a59697e1a94fcc42b788f14451287f5da']
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

@bot.command()
async def help(ctx):
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

@bot.command()
async def invite(ctx):
    await ctx.send('https://discord.com/oauth2/authorize?client_id=744841070621360169&scope=bot&permissions=19456')

## Processes data from data.gov.hk API 'Latest situation of reported cases of COVID-19 in Hong Kong (English)' only.
@bot.command(aliases = ['COVID-19hklist', 'COVID19hklist', 'covid19hklist', 'covid-19hklist', 'C19hklist', 'COVID-19hkl', 'COVID19hkl', 'covid19hkl', 'covid-19hkl', 'C19hkl', 'c19hkl'])
## arg1: Data type
## arg2: Operator/ Sort
## arg3: Value
## arg4: Value2
async def c19hklist(ctx, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
    ## arg1 Key
    ## aod: As of date 
    ## cc: No. of confirmed cases
    ## dc: No. of death cases
    ## pc: No. of probable cases
    ## dcc: No. of discharge cases
    ## roc: No. of ruled out cases
    ## hfi: No. of cases still hospitalised for investigation
    ## frc: No. of cases fulfulling the reporting criteria
    ## hcc: No. of hospitalised cases in critical condition
    ## All the possible values.
    carg1 = ['aod', 'cc', 'dc', 'pc', 'dcc', 'roc', 'hfi', 'frc', 'hcc']
    carg2 = ['=', '!=', '$', '!$', '%', '!%', '&', '!&', '^', '!^', '<', '<=', '>', '>=', '?']
    carg3 = ['ascending', 'descending']
    sorts = r'sorts%22%3A%5B%5B{dataType}%2C%22{sortType}%22%5D%5D%7D'
    filters = r'filters%22%3A%5B%5B{dataType}%2C%22{opr}%22%2C%5B%22{num}%22%5D%5D%5D%7D'
    ## Massive data defining code
    ## arg1
    if arg1 in carg1:
        if arg1 == 'aod':
            dataType = 1
        elif arg1 == 'cc':
            dataType = 3
        elif arg1 == 'dc':
            dataType = 7
        elif arg1 == 'pc':
            dataType = 9
        elif arg1 == 'dcc':
            dataType = 8
        elif arg1 == 'roc':
            dataType = 4
        elif arg1 == 'hfi':
            dataType = 5
        elif arg1 == 'frc':
            dataType = 6
        elif arg1 == 'hcc':
            dataType = 10
    elif arg1 == None:
        dataType = 3
    else:
        await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
    if arg2 in carg2:
        requestType = 'filters'
        if arg2 == '=':
            opr = 'eq'
        elif arg2 == '!=':
            opr = 'ne'
        elif arg2 == '$' and arg1 == 'aod':
            opr = 'ct'
        elif arg2 == '!$' and arg1 == 'aod':
            opr = 'nct'
        elif arg2 == '%' and arg1 == 'aod':
            opr = 'bw'
        elif arg2 == '!%' and arg1 == 'aod':
            opr = 'nbw' 
        elif arg2 == '&' and arg1 == 'aod':
            opr = 'ew'
        elif arg2 == '!&' and arg1 == 'aod':
            opr = 'new'
        elif arg2 == '^' and arg1 == 'aod':
            opr = 'in'
        elif arg2 == '!^' and arg1 == 'aod':
            opr = 'ni'
        elif arg2 == '<' and arg1 != 'aod':
            opr = 'lt'
        elif arg2 == '<=' and arg1 != 'aod':
            opr = 'le'
        elif arg2 == '>' and arg1 != 'aod':
            opr = 'gt'
        elif arg2 == '>=' and arg1 != 'aod':
            opr = 'ge'
        elif arg2 == '?' and arg1 != 'aod':
            opr = 'bt'
        else:
            await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
        if not arg4:
            if isinstance(arg3, str):
                num = arg3
            elif isinstance(arg3, int):
                num = str(arg3)
            else:
                await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
        else:
            num = r'{num1}%22%2C%22{num2}'
            num = num.replace(r'{num1}', str(arg3))
            num = num.replace(r'{num2}', str(arg4))
    elif arg2 in carg3:
        requestType = 'sorts'
        if arg2 == 'ascending':
            sortType = 'asc'
        elif arg2 == 'descending':
            sortType = 'desc'
    elif arg2 == None and arg3 == None:
        requestType = 'sorts'
        sortType = 'desc'
    else:
        await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
    ## API Website Construction
    if requestType == 'filters':
        filters = filters.replace(r'{dataType}', str(dataType))
        filters = filters.replace(r'{opr}', str(opr))
        filters = filters.replace(r'{num}', str(num))
        data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters)) 
        print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters))
    elif requestType == 'sorts':
        sorts = sorts.replace(r'{dataType}', str(dataType))
        sorts = sorts.replace(r'{sortType}', str(sortType))
        data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts)) 
        print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts))
    data2 = urllib.request.urlopen(data1) ## Stores info from API to var
    for line in data2: ## Code that decodes the API data into json we can use
        data3 = json.loads(line.decode("utf-8")) ## Stores json into var
    with open('api.json', 'w') as f:
        json.dump(data3, f, indent = 4)
        print('Dumped to api.json')
    df = pd.json_normalize(data3)
    number_of_rows = 10
    headers = ["Date", "Time", "Confirmed", "Ruled Out", "In Investigation", "Fulfill Criteria", "Deaths", "Discharged", "Probable", "Critical"]
    for n in range(int(df.shape[0]/number_of_rows)):
        start_row = n * number_of_rows
        end_row = start_row + number_of_rows
        new_df = df.iloc[start_row:end_row]
        message = str(tabulate(new_df, headers=headers, showindex=False))
        await ctx.send(f'```\n{message}\n```')
    if int(df.shape[0]/number_of_rows) < 1:
        start_row = 0
        end_row = 10
        new_df = df.iloc[start_row:end_row]
        message = str(tabulate(new_df, headers=headers, showindex=False))
        await ctx.send(f'```\n{message}\n```') 

@bot.command(aliases = ['COVID-19hkdata', 'covid19hkdata', 'covid19hkd'])
async def c19hkd(ctx, arg1 = None):
    if arg1 == None:
        tz = pytz.timezone('Asia/Hong_Kong')
        yesterday = datetime.now(tz) - timedelta(days=1)
        today1 = str(yesterday.strftime('%d/%m/%Y'))
        today2 = today1.replace('/', '%2F')
    else:
        today1 = arg1
        today2 = today1.replace('/', '%2F')
    api = r'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22eq%22%2C%5B%22{today1}%22%5D%5D%5D%7D'
    api = api.replace('{today1}', str(today2))
    data1 = urllib.request.Request(f"{api}")
    print(f'Requesting data now from: {api}')
    data2 = urllib.request.urlopen(data1)
    for line in data2: ## Code that decodes the API data into json we can use
        data3 = json.loads(line.decode("utf-8")) ## Stores dict into var 
    with open('api.json', 'w') as f:
        json.dump(data3, f, indent = 4)
        print('Dumped to api.json')
    if data3[0]['As of date'] == '':
        data3[0]['As of date'] = 'No data'
    if data3[0]['As of time'] == '':
        data3[0]['As of time'] = 'No data'
    if data3[0]['Number of confirmed cases'] == '':
        data3[0]['Number of confirmed cases'] = 'No data'
    if data3[0]['Number of ruled out cases'] == '':
        data3[0]['Number of ruled out cases'] = 'No data'
    if data3[0]['Number of cases still hospitalised for investigation'] == '':
        data3[0]['Number of cases still hospitalised for investigation'] = 'No data'
    if data3[0]['Number of cases fulfilling the reporting criteria'] == '':
        data3[0]['Number of cases fulfilling the reporting criteria'] = 'No data'
    if data3[0]['Number of death cases'] == '':
        data3[0]['Number of death cases'] = 'No data'
    if data3[0]['Number of discharge cases'] == '':
        data3[0]['Number of discharge cases'] = 'No data'
    if data3[0]['Number of probable cases'] == '':
        data3[0]['Number of probable cases'] = 'No data'
    if data3[0]['Number of hospitalised cases in critical condition'] == '':
        data3[0]['Number of hospitalised cases in critical condition'] = 'No data'
    embed=discord.Embed(title=f'Latest situation of reported cases of COVID-19 in Hong Kong as of {today1}', url="https://www.chp.gov.hk", color=0x223d78)
    embed.set_author(name="DATA.GOV.HK", url="https://data.gov.hk", icon_url="https://i.imgur.com/0gxkNQp.jpg")
    embed.set_thumbnail(url="https://i.imgur.com/9mNLNjQ.png")
    embed.add_field(name="As of date", value=str(data3[0]['As of date']), inline=True)
    embed.add_field(name="As of time", value=str(data3[0]['As of time']), inline=True)
    embed.add_field(name="No. of confirmed cases", value=str(data3[0]['Number of confirmed cases']), inline=True)
    embed.add_field(name="No. of ruled out cases", value=str(data3[0]['Number of ruled out cases']), inline=True)
    embed.add_field(name="No. of cases still hospitalised for investigation", value=str(data3[0]['Number of cases still hospitalised for investigation']), inline=True)
    embed.add_field(name="No. of cases fulfilling the reporting criteria", value=str(data3[0]['Number of cases fulfilling the reporting criteria']), inline=True)
    embed.add_field(name="No. of death cases", value=str(data3[0]['Number of death cases']), inline=True)
    embed.add_field(name="No. of discharge cases", value=str(data3[0]['Number of discharge cases']), inline=True)
    embed.add_field(name="No. of probable cases", value=str(data3[0]['Number of probable cases']), inline=True)
    embed.add_field(name="No. of hospitalised cases in critical condition", value=str(data3[0]['Number of hospitalised cases in critical condition']), inline=True)
    await ctx.send(embed = embed)

## Processes data from data.gov.hk API 'Details of probable/confirmed cases of COVID-19 infection in Hong Kong (English)' only.
@bot.command(aliases = ['COVID-19hkclist', 'COVID19hkclist', 'covid19hkclist', 'covid-19hkclist', 'C19hkclist', 'COVID-19hkcl', 'COVID19hkcl', 'covid19hkcl', 'covid-19hkcl', 'C19hkcl', 'c19hkcl'])
## arg1: Data type
## arg2: Operator/ Sort
## arg3: Value
## arg4: Value2
async def c19hkclist(ctx, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
    ## arg1 Key
    ## cn: Case no.
    ## rp: Report date
    ## doo: Date of onset
    ## g: Gender
    ## a: Age
    ## ha: Name of hospital admitted
    ## hdd: Hospitalised/Discharged/Deceased
    ## hk: HK/Non-HK resident
    ## cc: Case classification
    ## cp: Confirmed/Probable
    ## All the possible values.
    carg1 = ['cn', 'rp', 'doo', 'g', 'a', 'ha', 'hdd', 'hk', 'cc', 'cp']
    carg2 = ['=', '!=', '$', '!$', '%', '!%', '&', '!&', '^', '!^', '<', '<=', '>', '>=', '?']
    carg3 = ['ascending', 'descending']
    sorts = r'sorts%22%3A%5B%5B{dataType}%2C%22{sortType}%22%5D%5D%7D'
    filters = r'filters%22%3A%5B%5B{dataType}%2C%22{opr}%22%2C%5B%22{num}%22%5D%5D%5D%7D'
    ## Massive data defining code
    ## arg1
    if arg1 in carg1:
        if arg1 == 'cn':
            dataType = 1
        elif arg1 == 'rp':
            dataType = 2
        elif arg1 == 'doo':
            dataType = 3
        elif arg1 == 'g':
            dataType = 4
        elif arg1 == 'a':
            dataType = 5
        elif arg1 == 'ha':
            dataType = 6
        elif arg1 == 'hdd':
            dataType = 7
        elif arg1 == 'hk':
            dataType = 8
        elif arg1 == 'cc':
            dataType = 9
        elif arg1 == 'cp':
            dataType = 10
    elif arg1 == None:
        dataType = 1
    else:
        await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
    if arg2 in carg2:
        requestType = 'filters'
        if arg2 == '=':
            opr = 'eq'
        elif arg2 == '!=':
            opr = 'ne'
        elif arg2 == '$' and arg1 != 'a':
            opr = 'ct'
        elif arg2 == '!$' and arg1 != 'a':
            opr = 'nct'
        elif arg2 == '%' and arg1 != 'a':
            opr = 'bw'
        elif arg2 == '!%' and arg1 != 'a':
            opr = 'nbw' 
        elif arg2 == '&' and arg1 != 'a':
            opr = 'ew'
        elif arg2 == '!&' and arg1 != 'a':
            opr = 'new'
        elif arg2 == '^' and arg1 != 'a':
            opr = 'in'
        elif arg2 == '!^' and arg1 != 'a':
            opr = 'ni'
        elif arg2 == '<' and arg1 == 'a':
            opr = 'lt'
        elif arg2 == '<=' and arg1 == 'a':
            opr = 'le'
        elif arg2 == '>' and arg1 == 'a':
            opr = 'gt'
        elif arg2 == '>=' and arg1 == 'a':
            opr = 'ge'
        elif arg2 == '?' and arg1 == 'a':
            opr = 'bt'
        else:
            await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
        if not arg4:
            if isinstance(arg3, str):
                num = arg3
            elif isinstance(arg3, int):
                num = str(arg3)
            else:
                await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
        else:
            num = r'{num1}%22%2C%22{num2}'
            num = num.replace(r'{num1}', str(arg3))
            num = num.replace(r'{num2}', str(arg4))
    elif arg2 in carg3:
        requestType = 'sorts'
        if arg2 == 'ascending':
            sortType = 'asc'
        elif arg2 == 'descending':
            sortType = 'desc'
    elif arg2 == None and arg3 == None:
        requestType = 'sorts'
        sortType = 'desc'
    else:
        await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
    ## API Website Construction
    if requestType == 'filters':
        filters = filters.replace(r'{dataType}', str(dataType))
        filters = filters.replace(r'{opr}', str(opr))
        filters = filters.replace(r'{num}', str(num))
        data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters)) 
        print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters))
    elif requestType == 'sorts':
        sorts = sorts.replace(r'{dataType}', str(dataType))
        sorts = sorts.replace(r'{sortType}', str(sortType))
        data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts)) 
        print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts))
    data2 = urllib.request.urlopen(data1) ## Stores info from API to var 
    for line in data2: ## Code that decodes the API data into json we can use
        data3 = json.loads(line.decode("utf-8")) ## Stores json into var
    for case in data3:
        if case['Case classification*'] == 'Epidemiologically linked with local case':
            case['Case classification*'] = 'lw/ local case'
    for case in data3:
        if case['Case classification*'] == 'Epidemiologically linked with imported case':
            case['Case classification*'] = 'lw/ imported case'
    for case in data3:
        if case['Case classification*'] == 'Epidemiologically linked with possibly local case':
            case['Case classification*'] = 'lw/ p. local case'
    for case in data3:
        if case['Case classification*'] == 'Epidemiologically linked with possibly imported case':
            case['Case classification*'] = 'lw/ p. imported case'
    with open('api.json', 'w') as f:
        json.dump(data3, f, indent = 4)
        print('Dumped to api.json')
    df = pd.json_normalize(data3)
    number_of_rows = 5
    headers = ["Case no.", "Report date", "Date of onset", "Gender", "Age", "Hospital admitted", "Status", "Resident", "Classification", "Case Status"]
    for n in range(int(df.shape[0]/number_of_rows)):
        start_row = n * number_of_rows
        end_row = start_row + number_of_rows
        new_df = df.iloc[start_row:end_row]
        message = str(tabulate(new_df, headers=headers, showindex=False))
        await ctx.send(f'```\n{message}\n```')
    if int(df.shape[0]/number_of_rows) < 1:
        start_row = 0
        end_row = 5
        new_df = df.iloc[start_row:end_row]
        message = str(tabulate(new_df, headers=headers, showindex=False))
        await ctx.send(f'```\n{message}\n```') 

@bot.command(aliases = ['COVID-19hkcdata', 'covid19hkcdata', 'covid19hkcd'])
async def c19hkcd(ctx, arg1 = None):
    if arg1 == None:
        await ctx.send('The value you inputted is probably invalid. Please verify it and try again.')
    else:
        api = r'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22eq%22%2C%5B%22{cn}%22%5D%5D%5D%7D'
        api = api.replace('{cn}', str(arg1))
        data1 = urllib.request.Request(f"{api}")
        print(f'Requesting data now from: {api}')
        data2 = urllib.request.urlopen(data1)
        for line in data2: ## Code that decodes the API data into json we can use
            data3 = json.loads(line.decode("utf-8")) ## Stores dict into var 
        with open('api.json', 'w') as f:
            json.dump(data3, f, indent = 4)
            print('Dumped to api.json')
        if data3[0]['Case no.'] == '':
            data3[0]['Case no.'] = 'No data'
        if data3[0]['Report date'] == '':
            data3[0]['Report date'] = 'No data'
        if data3[0]['Date of onset'] == '':
            data3[0]['Date of onset'] = 'No data'
        if data3[0]['Gender'] == '':
            data3[0]['Gender'] = 'No data'
        if data3[0]['Age'] == '':
            data3[0]['Age'] = 'No data'
        if data3[0]['Name of hospital admitted'] == '':
            data3[0]['Name of hospital admitted'] = 'No data'
        if data3[0]['Hospitalised/Discharged/Deceased'] == '':
            data3[0]['Hospitalised/Discharged/Deceased'] = 'No data'
        if data3[0]['HK/Non-HK resident'] == '':
            data3[0]['HK/Non-HK resident'] = 'No data'
        if data3[0]['Case classification*'] == '':
            data3[0]['Case classification*'] = 'No data'
        if data3[0]['Confirmed/probable'] == '':
            data3[0]['Confirmed/probable'] = 'No data'
        embed=discord.Embed(title=f'Status of Case no. {arg1}', url="https://www.chp.gov.hk", color=0x223d78)
        embed.set_author(name="DATA.GOV.HK", url="https://data.gov.hk", icon_url="https://i.imgur.com/0gxkNQp.jpg")
        embed.set_thumbnail(url="https://i.imgur.com/9mNLNjQ.png")
        embed.add_field(name="Case no.", value=str(data3[0]['Case no.']), inline=True)
        embed.add_field(name="Report date", value=str(data3[0]['Report date']), inline=True)
        embed.add_field(name="Date of onset", value=str(data3[0]['Date of onset']), inline=True)
        embed.add_field(name="Gender", value=str(data3[0]['Gender']), inline=True)
        embed.add_field(name="Age", value=str(data3[0]['Age']), inline=True)
        embed.add_field(name="Name of hospital admitted", value=str(data3[0]['Name of hospital admitted']), inline=True)
        embed.add_field(name="Status", value=str(data3[0]['Hospitalised/Discharged/Deceased']), inline=True)
        embed.add_field(name="Resident", value=str(data3[0]['HK/Non-HK resident']), inline=True)
        embed.add_field(name="Classification", value=str(data3[0]['Case classification*']), inline=True)
        embed.add_field(name="Case status", value=str(data3[0]['Confirmed/probable']), inline=True)
        await ctx.send(embed = embed)

bot.run(token)
