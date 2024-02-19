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
client = discord.Client(intents=intents)
gid = 942894317087887360
bot = discord.Bot()


with open('config.json') as config_file:
    config = json.load(config_file)
client = OpenAI(api_key=config.get('apikey'))


def db():
    dbclient = MongoClient(config.get('uri'), server_api=ServerApi('1'))
    try:
        dbclient.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    db = dbclient['bigdata']
    setup_discord_collection(db)
    discord_collection = db['discord']

class CreateChannelModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # this is how i added the prompting/stuff
        self.add_item(InputText(label="Prompt"))
        self.add_item(InputText(label="Type (GPT3, GPT3.5, GPT4)"))

    async def callback(self, interaction: discord.Interaction):
        prompt = self.children[0].value
        gpt_type = self.children[1].value
        guild = interaction.guild

        if guild:
            description = f"{prompt} - {gpt_type}"
            new_channel = await guild.create_text_channel(name=prompt, topic=description)
            # still need to validate the type

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        response_message = completion.choices[0].message
        description = f"{prompt} - {response_message}"
        new_channel = await guild.create_text_channel(name=prompt, topic=description)
        # this is sending the response to the channel
        await new_channel.send(f"OpenAI response: {response_message}")
        await interaction.response.send_message(f'Channel "{new_channel.name}" created.', ephemeral=True)

@bot.slash_command(description="Create a new channel")
async def create_channel(ctx):
    modal = CreateChannelModal(title="Create New Channel")
    await ctx.send_modal(modal)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    db()

bot.run(config.get('token'))