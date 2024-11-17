import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()
import asyncio
from discord import app_commands
bot = commands.Bot(command_prefix=">",intents=discord.Intents.all())

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    for cmd in synced:
        print(cmd.name,end=" ")
    print('\n')
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member:discord.Member):
    if member.guild.id != 1260815515044286494:
        return
    welcome = bot.get_channel(1260819993356931154)
    rule = bot.get_channel(1260815515044286497)
    
    await welcome.send(f'''{member.mention}
歡迎加入附中資訊社團社群
可以到{rule.mention}查看規則以及選擇身分組
--------------------------------''')

@bot.command()
async def rl(ctx):
    try:
        await bot.reload_extension('cogs.hsnu')
        await bot.tree.sync()
        await ctx.send(f'reloaded')
    except Exception as e:
        await ctx.send(e)

@bot.command()
async def say(ctx,content):
    try:
        await ctx.channel.purge(limit=1)
        await ctx.send("".join(content))
    except Exception as e:
        await ctx.send(e)

async def load_ext():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename}")

    for filename in os.listdir("./rpg"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"eco.{filename[:-3]}")
            print(f"Loaded {filename}")
    
async def main():
    discord.utils.setup_logging()
    await load_ext()
    await bot.start(os.getenv("token"))

asyncio.run(main())