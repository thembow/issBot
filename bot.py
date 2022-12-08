from funcs import *
import discord
from discord import option
import os
from dotenv import load_dotenv
import time
import sys

load_dotenv()
token = os.getenv('TOKEN')
if not token:
    print('ERROR: Discord Token is missing in .env')
    sys.exit(-1)
#env handling
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "iss", description = "See where the Internation Space Station is!")
@option("zoom", description="Set the zoom level 0-8", min_value=0, max_value=8, default=5)
async def iss(ctx, zoom:int):
    iss = issLookup()
    if (iss == "null"):
        #catch errors
        await ctx.respond(f"Error! Cannot find ISS location")
    else:
        cI = coordImg(iss[0], iss[1], zoom)
        time.sleep(1)
        #limit speed so we dont send too many requests at once
        await ctx.respond(f"The International Space Station is currently flying over [{iss[2]}]({cI})")
@bot.slash_command(name = "astronauts", description = "List with links of all astronauts aboard the ISS")
async def astro(ctx):
    links = astroLookup()
    await ctx.respond(f"There are {len(links)} astronauts abord the ISS")
    linksOut = "\n".join(links)
    #sets up links to be multiline message
    await ctx.respond(linksOut)


bot.run(token) # run the bot with the token
