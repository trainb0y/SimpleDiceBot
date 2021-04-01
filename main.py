
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
    try: user_macros = macros[ctx.message.author.id]     # First check if they are using a macro
    except KeyError: user_macros = {}
    if arg in user_macros.keys(): arg = user_macros[arg]


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

@bot.command(aliases=["c"], help="Create a new macro")
async def create(ctx, name, dice):
    try: user_macros = macros[ctx.message.author.id]
    except KeyError: user_macros = {}
    user_macros[name] = dice
    macros[ctx.message.author.id] = user_macros

    embed = discord.Embed(
        color=discord.Color.blue(),
        title=f"{ctx.message.author.name}'s macro {name}",
        description = f"Successfuly created macro {name} for {dice}"
    )
    

    await ctx.send(embed=embed)


@bot.command(aliases=["l"],help="List macros")
async def list(ctx):
    try: 
        user_macros = macros[ctx.message.author.id]
        result = ""
        for name in user_macros:
            result += f"\n{name}: {user_macros[name]}"
    except KeyError: result = "You have no macros! Try !create to create one"
    # If they already had a macro, and then deleted it, this error will not occur
    # Therefore that message will never be given.
    
    
    embed = discord.Embed(
        color=discord.Color.blue(),
        title=f"{ctx.message.author.name}'s macros",
        description = result
    )
    

    await ctx.send(embed=embed)

@bot.command(aliases=["d"],help="Delete a macro")
async def delete(ctx,name):
    try: user_macros = macros[ctx.message.author.id]
    except KeyError: user_macros = {}
    result = user_macros.pop(name,None) # Returns none if no name
    macros[ctx.message.author.id] = user_macros

    if result == None: desc = f'No macro "{name}" found! Do !list to see your macros'
    else: desc = f'Deleted macro "{name}"!'

    embed = discord.Embed(
        color=discord.Color.blue(),
        title=f"{ctx.message.author.name} deleting macro {name}",
        description = desc
    )
    

    await ctx.send(embed=embed)




        


bot.run(DISCORD_TOKEN)