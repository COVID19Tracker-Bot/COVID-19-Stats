import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global invites
        invites = {}
        for guild in self.bot.guilds:
            try:
                invites[guild.id] = await guild.invites()
            except discord.errors.Forbidden as exception:
                continue

    def code2inv(self, list, code):
        for invite in list:
            if invite.code == code:
                return invite

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global invites
        try:
            if not member.bot:
                old_inv = invites[member.guild.id]
                new_inv = await member.guild.invites()
                for invite in old_inv:
                    if invite.uses < int(self.code2inv(new_inv, invite.code).uses):
                        print(f"Member {member.name} Joined")
                        print(f"Invite Code: {invite.code}")
                        print(f"Inviter: {invite.inviter}")
                        invites[member.guild.id] = new_inv
                        return
        except discord.errors.Forbidden as exception:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        global invites
        try:
            invites[member.guild.id] = await member.guild.invites()
        except discord.errors.Forbidden as exception:
            pass

def setup(bot):
    bot.add_cog(Invite(bot))