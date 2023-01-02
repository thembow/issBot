from funcs import *
from time_funcs import *
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
    if iss is None:
        await ctx.respond(f"Error! Cannot find ISS location")
    #catch errors
    time.sleep(1)
    #limit speed so we dont send too many requests at once
    cI = coordImg(iss[0], iss[1], "2012-07-09", zoom)
    if cI:
    #if date_time was valid
        await ctx.respond(f"The International Space Station is currently flying over [{iss[2]}]({cI})")
        #formatted like [text](link) so it displays the image in the message
        #await ctx.respond(f"The International Space Station is currently flying over [{iss[2]}]({cI})\nError: Entered date-time was invalid, defaulting to 2012-07-09")
        #reuse this later? Not even sure when i made this
@bot.slash_command(name = "astronauts", description = "List with links of all astronauts aboard the ISS")
async def astro(ctx):
    links = astroLookup()
    await ctx.respond(f"There are {len(links)} astronauts abord the ISS")
    linksOut = "\n".join(links)
    #sets up links to be multiline message
    await ctx.respond(linksOut)
@bot.slash_command(name= "gibs", description = "Manually give coordinates to retrieve from NASA gibs")
@option("latitude", description="latitude", required=True)
@option("longitude", description="longitude", required=True)
@option("zoom", description="Set the zoom level 0-8", min_value=0, max_value=8, default=5)
async def gibs(ctx, lat:float, long:float, zoom:int):
    cI = coordImg(lat, long, "2012-07-09", zoom)
    download_image(cI, "current.jpg")
    mostly_black = is_image_mostly_black("current.jpg")
    if mostly_black:
        #if we get a url succesfully
        await ctx.respond(f"Sorry, could not find a valid image at those coordinates.")
    else:
        await ctx.respond(f"[Here]({cI}) is your satellite image taken at {lat}, {long}")
    delete_file("current.jpg")



bot.run(token) # run the bot with the token
