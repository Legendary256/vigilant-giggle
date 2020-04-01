import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("Bot is ready")
    await la()


@client.command()
async def l(extension):
    """
    Loads given extension
    """
    client.load_extension(f'cogs.{extension}')


# await ctx.send(f"Loaded {extension}")

@client.command()
async def ul(ctx, extension):
    """
    Unloads given extension
    """
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded {extension}')


@client.command()
async def la():
    '''
    Loads all the extensions
    '''
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await l(filename[:-3])


client.run('Njg4MTUxODk1NDk5MzQxODY0.XmwK_Q.y9z8ictRHRZOFpclFED5NTNNvpU')
