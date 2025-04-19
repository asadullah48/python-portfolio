import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None  # Using custom help
)

# Bot events
@bot.event
async def on_ready():
    print(f'✅ Bot online as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Game(name="Type !help"))

# Custom help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        color=discord.Color.blue()
    )
    commands_list = {
        "!hello": "Get a greeting",
        "!info": "Bot information",
        "!help": "This menu"
    }
    for cmd, desc in commands_list.items():
        embed.add_field(name=cmd, value=desc, inline=False)
    await ctx.send(embed=embed)

# Main commands
@bot.command()
async def hello(ctx):
    await ctx.send(f"👋 Hello, {ctx.author.mention}!")

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Bot Info",
        description="Open-source Discord Bot",
        color=discord.Color.green()
    )
    embed.add_field(name="Version", value="2.0.0")
    embed.add_field(name="GitHub", value="https://github.com/asadullah48/Discord-Bot")
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use !help")

# Secure token handling
try:
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
except discord.LoginFailure:
    print("🚨 Invalid token! Check your .env or GitHub Secrets")
except Exception as e:
    print(f"⚠️ Unexpected error: {e}")