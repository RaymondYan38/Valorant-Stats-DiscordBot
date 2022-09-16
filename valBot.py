"""Discord bot that scapes information from Tracker.gg

    This module is code for a Dsicord bot that responds to commands
    request by users in Discord channels. The bot uses code from webScrape.py
    to scape information abotu statistics about Valorant from users that have
    registered with Tracker.gg. It tells users to wait while the information is
    being processed and the message is deleted after. Also handles exceptions
    gracefully with error messages telling users what had happened in the error.
"""

import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os
import webScrape
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

intents=discord.Intents.all()

prefix = '$'
bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command('help')

ERROR_PAGE_MESSAGE = "An error has occured: Page could not be found"

ERROR_ELEMENT_MESSAGE = "An error has occured: Content could not be found"

@bot.command()
async def help(message):
    """Sends help message that tells users how to use the bot
    """
    helpMessage = discord.Embed(title="Valorant Bot \nGuide", description="Valorant bot is a discord bot that is built for Valorant players to check their statistics if they have ever logged into tracker.gg. NOTE: Information is taken from Tracker.gg so you MUST be logged in with a public account to use this bot!")
    helpMessage.add_field(name="accuracy", value="To use this command type $accuracy RIOT_ID#TAG ex.$accuracy pipluptiny#boba", inline=False)
    helpMessage.add_field(name="weapon", value="To use this command type $weapon RIOT_ID#TAG ex.$weapon pipluptiny#boba", inline=False)
    helpMessage.add_field(name="maps", value="To use this command type $maps RIOT_ID#TAG ex.$maps pipluptiny#boba", inline=False)
    helpMessage.add_field(name="current", value="To use this command type $current RIOT_ID#TAG ex.$current pipluptiny#boba", inline=False)
    helpMessage.add_field(name="peak", value="To use this command type $peak RIOT_ID#TAG ex.$peak pipluptiny#boba", inline=False)
    helpMessage.add_field(name="agents", value="To use this command type $agents RIOT_ID#TAG ex.$agents pipluptiny#boba", inline=False)
    helpMessage.add_field(name="overview", value="To use this command type $overview RIOT_ID#TAG ex.$overview pipluptiny#boba", inline=False)
    await message.channel.send(embed=helpMessage)

@bot.command()
async def accuracy(message, *, arg):
    """Sends statistics about accuracy
    """
    try:
        await message.channel.send("Please wait...", delete_after=2)
        END_URL = webScrape.createURL(arg)
        driver = webScrape.getDriver()
        accuracy = webScrape.get_accuracy(driver, END_URL)
        accuracy = webScrape.parse_accuracy(accuracy)
        await message.channel.send(accuracy)
    except TimeoutException:
        await message.channel.send(ERROR_PAGE_MESSAGE)
    except (NoSuchElementException, InvalidSelectorException):
        await message.channel.send(ERROR_ELEMENT_MESSAGE)

@bot.command()
async def weapon(message, *, arg):
    """Sends statistics about weapons
    """
    try:
        await message.channel.send("Please wait...", delete_after=2)
        END_URL = webScrape.createURL(arg)
        driver = webScrape.getDriver()
        weapon = webScrape.get_weapons(driver, END_URL)
        weapon = webScrape.parse_top_weapons(weapon)
        await message.channel.send(weapon)
    except TimeoutException:
        await message.channel.send(ERROR_PAGE_MESSAGE)
    except (NoSuchElementException, InvalidSelectorException):
        await message.channel.send(ERROR_ELEMENT_MESSAGE)

@bot.command()
async def maps(message, *, arg):
    """Sends statistics about maps
    """
    try:
        await message.channel.send("Please wait...", delete_after=2)
        END_URL = webScrape.createURL(arg)
        driver = webScrape.getDriver()
        maps = webScrape.get_maps(driver, END_URL)
        maps = webScrape.parse_maps(maps)
        await message.channel.send(maps)
    except TimeoutException:
        await message.channel.send(ERROR_PAGE_MESSAGE)
    except (NoSuchElementException, InvalidSelectorException):
        await message.channel.send(ERROR_ELEMENT_MESSAGE)

@bot.command()
async def current(message, *, arg):
    """Sends statistics about current rank
    """
    try:
        await message.channel.send("Please wait...", delete_after=2)
        END_URL = webScrape.createURL(arg)
        driver = webScrape.getDriver()
        current_rank = webScrape.get_current_rank(driver, END_URL)
        current_rank = webScrape.parse_current_rank(current_rank)
        await message.channel.send(current_rank)
    except TimeoutException:
        await message.channel.send(ERROR_PAGE_MESSAGE)
    except (NoSuchElementException, InvalidSelectorException):
        await message.channel.send(ERROR_ELEMENT_MESSAGE)

@bot.command()
async def peak(message, *, arg):
    """Sends statistics about peak rank
    """
    try:
        await message.channel.send("Please wait...", delete_after=2)
        END_URL = webScrape.createURL(arg)
        driver = webScrape.getDriver()
        peak_rank = webScrape.get_peak_rank(driver, END_URL)
        peak_rank = webScrape.parse_peak_rank(peak_rank)
        await message.channel.send(peak_rank)
    except TimeoutException:
        await message.channel.send(ERROR_PAGE_MESSAGE)
    except (NoSuchElementException, InvalidSelectorException):
        await message.channel.send(ERROR_ELEMENT_MESSAGE)


@bot.command()
async def agents(message, *, arg):
    """Sends statistics about agents
    """
    try:
        await message.channel.send("Please wait...", delete_after=2)
        END_URL = webScrape.createURL(arg)
        driver = webScrape.getDriver()
        agents = webScrape.get_agents(driver, END_URL)
        agents = webScrape.parse_agents(agents)
        await message.channel.send(agents)
    except TimeoutException:
        await message.channel.send(ERROR_PAGE_MESSAGE)
    except (NoSuchElementException, InvalidSelectorException):
        await message.channel.send(ERROR_ELEMENT_MESSAGE)

@bot.command()
async def overview(message, *, arg):
    """Sends overall statistics of players
    """
    try:
        await message.channel.send("Please wait...", delete_after=2)
        END_URL = webScrape.createURL(arg)
        driver = webScrape.getDriver()
        overview = webScrape.get_overview(driver, END_URL)
        overview = webScrape.parse_overview(overview)
        await message.channel.send(overview)
    except TimeoutException:
        await message.channel.send(ERROR_PAGE_MESSAGE)
    except (NoSuchElementException, InvalidSelectorException):
        await message.channel.send(ERROR_ELEMENT_MESSAGE)

bot.run(TOKEN)
