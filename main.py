import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

OWNER_ID = 1340615307282219078
secret_role = "Gamer"

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

max_spam = 100


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")

    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")


@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")


# ----------------
# SPAM COMMAND
# ----------------

@bot.command()
async def spam(ctx, amount: int, *, message):
    global max_spam

    if amount > max_spam:
        await ctx.send(f"❌ Max spam is {max_spam}")
        return

    for _ in range(amount):
        await ctx.send(message)
        await asyncio.sleep(0.5)


@bot.command()
async def maxspam(ctx, amount: int):
    global max_spam

    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Only the bot owner can change max spam")
        return

    max_spam = amount
    await ctx.send(f"✅ Max spam changed to {amount}")


# ----------------
# GLOBAL BROADCAST
# ----------------

@bot.command()
async def gb(ctx, *, message):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Only the bot owner can use this command")
        return

    sent = 0

    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(f"📢 **Global Broadcast:** {message}")
                    sent += 1
                    await asyncio.sleep(1)
                    break
                except:
                    pass

    await ctx.send(f"✅ Broadcast sent to {sent} servers.")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
