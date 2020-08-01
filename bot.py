import asyncio
import datetime
import discord
import logging
import os
import praw
import psycopg2
from db_helper import insert, remove, query_all, does_exist
from discord.ext import commands
from dotenv import load_dotenv
from subreddit_scrapper import get_scraped_submissions

logging.getLogger().setLevel(logging.INFO)

# Get .env keys
load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = 701619618950807665

# Initialize the bot
client = commands.Bot(command_prefix='!')

# Discord functions
@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    logging.info(f'{str(datetime.datetime.now())}: Bot is ready')

    while True:
        logging.info(f'{str(datetime.datetime.now())}: Checking for new submissions: ')

        con = psycopg2.connect(DATABASE_URL, sslmode='require')

        all_subreddits = '+'.join([d[1] for d in query_all(con, 'subreddit')])
        all_keywords = [d[1] for d in query_all(con, 'keyword')]
        all_forbidden_words = [d[1] for d in query_all(con, 'forbidden_word')]

        logging.info(f'{str(datetime.datetime.now())}: Subreddits: {all_subreddits}')
        logging.info(f'{str(datetime.datetime.now())}: Keywords: {all_keywords}')
        logging.info(f'{str(datetime.datetime.now())}: Forbidden Words: {all_forbidden_words}')
        logging.info(f'{str(datetime.datetime.now())}: Begin scraping')
        
        submissions = get_scraped_submissions(all_subreddits, all_keywords, all_forbidden_words)

        for submission in submissions:
            submission_does_exist = does_exist(con, 'submission', 'id', submission.id)

            if not submission_does_exist:
                logging.info(f'{str(datetime.datetime.now())}: Found new submission: {submission.title[:100]}')
                insert(con, 'submission', ['id', 'title'], [submission.id, submission.title[:100].replace("'", "")])
                await channel.send(f'```{submission.title}```\n @everyone \n\n{submission.url}')

        logging.info(f'{str(datetime.datetime.now())}: Finished scraping')

        # # Close the connection and sleep for 1 minute
        con.close()
        await asyncio.sleep(60)

def add_to_table(table_name, columns, values):
    logging.info(f'{str(datetime.datetime.now())}: Adding {table_name}: {values}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    for value in values:
        insert(con, table_name, columns, [value])
    con.close()

def get_from_table(table_name):
    logging.info(f'{str(datetime.datetime.now())}: Getting {table_name}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    result = query_all(con, table_name)
    con.close()
    
    return [d[1] for d in result]

def remove_from_table(table_name, column, value):
    logging.info(f'{str(datetime.datetime.now())}: Removing {value} from {table_name}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    remove(con, table_name, column, value)
    con.close()

@client.command()
async def add_keyword(ctx, *arg):
    keyword = ' '.join(arg)
    add_to_table('keyword', ['keyword'], [keyword])
    await ctx.send(f'Successfully added: {keyword}')

@client.command()
async def add_subreddit(ctx, *arg):
    subreddit = ' '.join(arg)
    add_to_table('subreddit', ['subreddit'], [subreddit])
    await ctx.send(f'Sucessfully added: {subreddit}')

@client.command()
async def add_forbidden_word(ctx, *arg):
    forbidden_word = ' '.join(arg)
    add_to_table('forbidden_word', ['forbidden_word'], [forbidden_word])
    await ctx.send(f'Sucessfully added: {forbidden_word}')

@client.command()
async def get_keywords(ctx):
    result = get_from_table('keyword')
    await ctx.send(f'The keywords are: {result}')

@client.command()
async def get_subreddits(ctx):
    result = get_from_table('subreddit')
    await ctx.send(f'The subreddits are: {result}')

@client.command()
async def get_forbidden_words(ctx):
    result = get_from_table('forbidden_word')
    await ctx.send(f'The forbidden words are: {result}')

@client.command()
async def remove_keyword(ctx, *arg):
    keyword = ' '.join(arg)
    remove_from_table('keyword', 'keyword', keyword)
    await ctx.send(f'Removed: {keyword}')

client.run(DISCORD_BOT_TOKEN)
