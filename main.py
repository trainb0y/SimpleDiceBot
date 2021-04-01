
import random, os, json
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

macros = {} # discord uuid: [macroname:roll]

bot = commands.Bot(command_prefix="!")

@bot.command(help="Save all new macros")
async def save(ctx):
    for macro in macros:
        pass 

@bot.command(aliases=["r"], help="Roll dice")
async def roll(ctx, arg):
    dice_roll = arg # Keep a copy of the original roll, for later

    dice = [arg.split("d")[0]]
    arg = arg.split("d")[1] # Arg is the 12+3 in 2d12+3

    if "+" in arg: # If there are any modifiers, split them off
        dice.append(int(arg.split("+")[0]))
        dice.append(int(arg.split("+")[1]))
    elif "-" in arg: # If there are any modifiers, split them off
        dice.append(int(arg.split("-")[0]))
        dice.append(-int(arg.split("-")[1]))

    else: dice.append(arg)

    # now we should have a list of [num,type,mod]
    print(dice)
    dice = [int(i) for i in dice]
    # now its full of integers
    total = 0
    for i in range(dice[0]):
        total += random.randint(1,dice[1])

    try: total += dice[2] # add the modifier
    except IndexError: pass # there might not always be a mod
    
    embed = discord.Embed(
        color=discord.Color.blue(),
        title=f"{ctx.message.author.name}'s roll of {dice_roll}",
        description = total
    )
    

    await ctx.send(embed=embed)


bot.run(DISCORD_TOKEN)