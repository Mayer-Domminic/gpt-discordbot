import discord
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

with open('config.json') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    dbclient = MongoClient(config.get('uri'), server_api=ServerApi('1'))
    try:
        dbclient.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    db = dbclient['bigdata']
    discord_collection = db['discord']
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(config.get('token'))