# Reddit Scraper for Discord Bot
## Introduction
I started getting into making custom mechanical keyboards lately, but parts are usually not available or sold out fast. I made this bot so that I can get alerted about new parts, group buys, or interest checks. I made it so that it is modular and can be applied to different subreddits(s). The bot will look for recent posts in the specific subreddits and search for posts that contain a set of keywords.

## Things to do
- Make an application on [Heroku](heroku.com) with a Postgres Database
- Make an application using dev tools on [Discord](discord.com)
- Add a bot
- Go to [Reddit's dev preferences](https://www.reddit.com/prefs/apps) and make an application


## Setup
1. Clone this repository
2. Run `pip3 install requirements.txt`
3. Replace all instances of os.enviorn[] with the corresponding key (From Discord, Heroku, and Reddit)
4. Add your Discord channel id (The channel where the bot will live on the Discord server)
5. Run `python3 bot.py`

## Bot Commands
- !add_keywords arg1, arg2, ...
  - Add keywords to the bot to know which posts to look for
- !remove_keyword arg
  - Remove keyword from the bot
- !get_keywords
  - Get all the keywords that the bot is searching for
- !add_subreddits arg1, arg2
  - Add subreddits to track
- !get_subreddits
  - Get all the subreddits that are being tracked
