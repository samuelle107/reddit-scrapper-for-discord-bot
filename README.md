# reddit-scrapper-for-discord-bot
## Introduction
This discord bot was purely made so that I can get updates on items of interest on /r/MechMarket.

This bot utilizes discord.py to make a discord bot, PRAW for reddit scraping, and TinyDB to store posts.

## Setup
1. Clone this repository
2. Run `pip3 install asyncio discord.py praw tinydb`
3. Replace all instances of os.enviorn[] with the corresponding key (From Discord and Reddit)
4. Change the subreddit to your subreddit of choice
5. Add your Discord channel id (The channel where the bot will live on the Discord server)
6. Run `python3 subreddit-scrapper`

## Bot Commands
- !add_keywords (arg1, arg2, ...)
  - Add keywords to the bot to know which posts to look for
- !remove_keyword (arg)
  - Remove keyword from the bot
- !get_keywords
  - Get all the keywords that the bot is searching for
