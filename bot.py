import asyncio
import discord
import os
import praw
import subreddit_scrapper
from discord.ext import commands
from tinydb import TinyDB, Query, where

# Constants
tracked_subreddit = 'MechMarket'
channel_id = 700110066044633169
client = commands.Bot(command_prefix = '!')
discord_bot_token = os.environ['DISCORD_BOT_TOKEN']

# Tiny DB
db = TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))

# Tiny DB tables
submission_table = db.table('post_table')
keyword_table = db.table('keyword_table')

# Tiny DB queries
submission_query = Query()
keyword_query = Query()

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    scraper = subreddit_scrapper.SubredditScraper()

    await channel.send('I am ready!')

    while True:
        for submission in scraper.get_scraped_submissions(tracked_subreddit, [d['keyword'] for d in keyword_table.all()]):
            if not submission_table.search(submission_query.id == submission.id):
                submission_table.insert({ 'id': submission.id })
                await channel.send(submission.url)

        await asyncio.sleep(60)

@client.command()
async def add_keywords(ctx, *arg):
    for keyword in arg:
        keyword_table.insert({ 'keyword': keyword })
        await ctx.send(f'Sucessfully added {keyword}')

@client.command()
async def get_keywords(ctx):
    await ctx.send([d['keyword'] for d in keyword_table.all()])

@client.command()
async def remove_keyword(ctx, arg):
    keyword_table.remove(where('keyword') == arg)

    await ctx.send(f'Sucessfully removed {arg}')

@client.command()
async def get_now(ctx):
    scraper = subreddit_scrapper.SubredditScraper()

    foundInterest = False

    for submission in scraper.get_scraped_submissions(tracked_subreddit, [d['keyword'] for d in keyword_table.all()]):
        if not submission_table.search(submission_query.id == submission.id):
            foundInterest = True
            submission_table.insert({ 'id': submission.id })
            await ctx.send(submission.url)
    
    if not foundInterest:
        await ctx.send('Nothing of interest to be found')

client.run(discord_bot_token)
