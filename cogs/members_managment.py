import discord
from discord.ext import commands

class Member_Managment(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joind a server.')
        ch = discord.TextChannel(position = 0)
        print(channel_list)
        await ch.send(f'Retard has just joined us. I wish u pleasent dying {member}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server')

        ch = discord.TextChannel(position = 0)
        print(channel_list)
        await ch.send(f'Retard has been just kicked. I hope u will die {member}')

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        '''
        Kicks given member from the server (use @)
        '''
        await member.kick(reason=reason)
        await ctx.send(f'Get the fuck out {member}!', tts=True)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        '''
        Bans given member from the server(use @)
        '''
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')
        mem
    @commands.command()
    async def unban(self, ctx, *, member):
        '''
        Unbans given member (use name#discriminator)
        '''
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                print(user)
                await ctx.send(f'Unbanned {user.mention}. Hello again!')
                return

def setup(client):
    client.add_cog(Member_Managment(client))