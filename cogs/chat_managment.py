import discord
from discord.ext import commands


class Chat_Managment(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clear(self, ctx, amount=5):
        """
		Clears given amount of chat logs
		"""
        await ctx.channel.purge(limit=amount)  # usuwa wiadomosci

    @commands.command()
    async def ping(self, ctx):
        '''
		Shows the server's delay
		'''
        await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


def setup(client):
    client.add_cog(Chat_Managment(client))
