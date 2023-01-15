import os
import discord
from discord.ext import commands
TOKEN = os.environ['TOKEN']

def custom_has_permissions(**perms) -> commands.check:
    async def predicate(ctx):
        # Add the perms to a variable, you can format this any way you'd want
        ctx.command.required_perms = [p.replace('_', ' ').title() for p in perms.keys()]
        # Just use the normal check
        return await commands.has_permissions(**perms).predicate(ctx)

    return commands.check(predicate)

### Bot initialization

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(help_command=None, command_prefix = "gb!", intents=intents)

### Prints the successful message.

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='gb!help'))

### General commands

# Create webhook command
@client.command()
async def webhook(ctx):
  try:
    discord.message.channel.create_webhook(name="Cyndaquil", avatar="cyndaquil.png")
  except:
    pass
  
# Help command
@client.command()
async def help(ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send(f'```\nHelp:\n\nGeneral commands:\n\nPing - Sends "Pong!"\nSay - Repeats a phrase\nSpam - Spams a message - [NUMBER OF TIMES, MESSAGE]\n\nModeration Commands:\n\nBan - Bans a member - (Requires: "Ban Members")\nClear - Purges the channel - (Requires:"Manage Messages")\n```')
  
# Ping! command
@client.command()
async def ping(ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.reply(f"Pong!", mention_author=False)

# Tell the bot to say something
@client.command()
async def say(ctx, arg):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send(arg)

"""
# Spam command
@client.command()
async def spam(ctx, num_spam, spam_msg):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send('3, 2, 1, GO!')
    i = 0
    for i in range(int(num_spam)):
        await ctx.send(spam_msg)
        if i == num_spam:
            break
"""

### Moderation commands

# Ban someone
@custom_has_permissions(ban_members=True)
@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    try:
      await ctx.message.delete()
    except:
      pass
    if reason == None:
        await ctx.send(f"Woah {ctx.author.mention}, make sure you provide a reason!")
    else:
        messageok = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.ban(reason=reason)
        await ctx.reply("Member banned!", mention_author=False)

# Clear channel command
@custom_has_permissions(administrator=True)
@client.command()
async def clear(ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.channel.purge()

client.run(TOKEN)