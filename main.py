import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import discord
from openai import OpenAI
from discord.ui import Modal, InputText, Select
from discord import SelectOption
from discord.ext import commands
from db_validation import setup_discord_collection

# proprietaries
intents = discord.Intents.default()
intents.message_content = True
gid = 942894317087887360
bot = discord.Bot(intents=intents)


with open('config.json') as config_file:
    config = json.load(config_file)
aiclient = OpenAI(api_key=config.get('apikey'))
dbclient = MongoClient(config.get('uri'), server_api=ServerApi('1'))
db = dbclient['discord']
# setup_discord_collection(db)
data = db['discord_collection']

def find_cid():
    return [doc['channel_id'] for doc in data.find({}, {'channel_id': 1})]

def create_item(prompt, pre_prompt, user, type, channel):
    document = {
        "user_id": user,
        "channel_id": channel,
        "gpt_type": type,
        "messages": [pre_prompt, prompt]
    }
    data.insert_one(document)


class CreateChannelModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # this is how i added the prompting/stuff
        self.add_item(InputText(label="Prompt"))
        self.add_item(InputText(label="Pre-prompt"))
        self.add_item(InputText(label="Type (GPT3, GPT3.5, GPT4)"))

    async def callback(self, interaction: discord.Interaction):
        prompt = self.children[0].value
        pre_prompt = self.children[1].value
        gpt_type = self.children[2].value
        guild = interaction.guild
        if len(prompt) > 99:
            prompt = prompt[:99]

        description = f"{prompt} - {gpt_type}"
        new_channel = await guild.create_text_channel(name=prompt, topic=description)
        # TODO still need to validate the type

        #completion = aiclient.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": pre_prompt},{"role": "user", "content": prompt}])
        #response_message = completion.choices[0].message
        description = f"{prompt}, {pre_prompt}, {gpt_type} " #{response_message}
        #await new_channel.send(f"OpenAI response: {response_message}")
        await interaction.response.send_message(f'Channel "{new_channel.name}" created.', ephemeral=True)
        create_item(prompt, pre_prompt, interaction.user.id, gpt_type, new_channel.id)

@bot.slash_command(description="Create a new channel")
async def create_channel(ctx):
    modal = CreateChannelModal(title="Create New Channel")
    await ctx.send_modal(modal)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    channel_id = find_cid()

    if message.author == bot.user:
        return

    # Check if the message channel is in the set of tracked channel IDs
    if message.channel.id in channel_id:
        print(f"Received a message in a tracked channel: {message, message.content}")

bot.run(config.get('token'))