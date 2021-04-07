
import random, os, json
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

try:
    with open("save.json","r") as f:
        str_key_macros = json.load(f)
        # When serialized to JSON, the keys, which are python ints, become strings
        # so something saved as {12345: {macros}} would load as {"12345": {macros}}

        macros = {}   # This fixes that
        for key in str_key_macros:
            macros[int(key)] = str_key_macros[key]

except FileNotFoundError: macros = {}

bot = commands.Bot(command_prefix="!")



@bot.command(help="Save all new macros")
async def save(ctx):
    with open("save.json","w") as f:
        json.dump(macros,f)
    embed = discord.Embed(
        color=discord.Color.blue(),
        title=f"Success!",
        description = "All macros saved!"
    )
    
    await ctx.send(embed=embed)
    
    

@bot.command(aliases=["r"], help="Roll dice")
async def roll(ctx, arg, return_result=False):
    global macros
    try: user_macros = macros[ctx.message.author.id]     # First check if they are using a macro
    except KeyError: user_macros = {}

    #if arg in user_macros.keys(): arg = user_macros[arg]

    # Replace all macros with the dice
    # This enables things like !c str 5
    # and then !r 1d20+str
    # 
    # To prevent str from being used if they want strength, we should order
    # the macro keys from largest to smallest
    macro_keys = list(user_macros.keys())
    macro_keys.sort(key=len) # Sorts from smallest to largest
    macro_keys.reverse() # Reverse order

    for macro in macro_keys:
        if macro in arg:
            arg = arg.replace(macro, str(await roll(ctx,user_macros[macro],return_result=True))) # replace the macro with the number result

    dice_roll = arg # Keep a copy of the original roll, for later
    # If they set a macro to be a plain int, it will raise an error while rolling
    # so:
    print(f"Attempting to roll {arg}")
    try:
        arg = int(arg)
        total = arg
        
    except ValueError: # Invalid int
        if "d" not in arg:
            total = eval(arg)
        else:   
            if arg[0] == "d": # prefix rolls such as d6 with a 1, so d6 becomes 1d6
                arg = "1"+arg 


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
        
    if return_result: return total

    embed = discord.Embed(
        color=discord.Color.blue(),
        title=f"{ctx.message.author.name}'s roll of {dice_roll}",
        description = total
    )
    

    await ctx.send(embed=embed)

@bot.command(aliases=["c"], help="Create a new macro")
async def create(ctx, name, dice):
    global macros
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


@bot.command(aliases=["l","list"],help="List macros")
async def list_macros(ctx):
    global macros
    try: 
        user_macros = macros[ctx.message.author.id]
        if user_macros == {}: raise KeyError # because they can delete the macro and have none, but still have a macro dict.
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
    global macros
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