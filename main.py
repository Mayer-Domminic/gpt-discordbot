import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import discord

# proprietaries
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


with open('config.json') as config_file:
    config = json.load(config_file)

def db():
    dbclient = MongoClient(config.get('uri'), server_api=ServerApi('1'))
    try:
        dbclient.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    db = dbclient['bigdata']
    discord_collection = db['discord']

gid = 942894317087887360


bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[gid])
async def hello(ctx):
    await ctx.respond("Hello!")

bot.run(config.get('token'))