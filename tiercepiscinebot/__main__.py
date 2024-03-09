import os
from random import randint

import discord
from discord import app_commands
from dotenv import load_dotenv
from tiercepiscinebot.db_interaction import Database
from tiercepiscinebot.params import *

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()


DB = Database()


# define commands
@tree.command(
    name="add",
    description=ADD_DESCRIPTION,
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def ADD_command(interaction, poulain: str, mentor: str):
    await interaction.response.send_message(DB.add_poulain(poulain, mentor))


@tree.command(
    name="test",
    description="circulez rien a voir ici",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def TEST_command(interaction):
    await interaction.response.send_message("oui ?")


@tree.command(
    name="coucou",
    description="tierce bot te parle tel un veritable chatbot",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def COUCOU_command(interaction):
    await interaction.response.send_message(
        CREEPY_THINGS[randint(0, len(CREEPY_THINGS) - 1)]
    )


@tree.command(
    name="list",
    description="list tout les poulains actuels",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def LIST_command(interaction):
    await interaction.response.send_message(DB.list())


# launch
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print(f"logged in as {client.user}")


client.run(os.getenv("TOKEN"))
