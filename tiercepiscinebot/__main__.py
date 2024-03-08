import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from tiercepiscinebot.db_interaction import Database
from tiercepiscinebot.decorateur import in_channel
from tiercepiscinebot.params import *

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()


DB = Database()


# @client.event
# async def on_message(message: discord.message):
#     if message.author == client.user:
#         return

#     if message.content.startswith("$hello"):
#         await message.channel.send("Hello world!")


# define commands
@tree.command(
    name="add",
    description=ADD_DESCRIPTION,
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def ADD_command(interaction):
    await interaction.response.send_message(DB.add_poulain())


@tree.command(
    name="test",
    description="circulez rien a voir ici",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def ADD_command(interaction):
    await interaction.response.send_message("oui ?")


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print(f"We have logged in as {client.user}")


client.run(os.getenv("TOKEN"))
