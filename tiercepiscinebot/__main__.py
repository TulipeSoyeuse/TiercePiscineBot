import os
from random import randint

import discord
import pandas as pd
from discord import app_commands
from discord.ext import tasks
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
    description="liste tout les poulains actuels",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def LIST_command(interaction):
    await interaction.response.send_message(DB.list())


@tree.command(
    name="help",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def HELP_command(interaction):
    await interaction.response.send_message(HELP)


@tree.command(
    name="cleanup",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def cleanup_command(interaction):
    DB.cleanup()
    await interaction.response.send_message("DB clean")


@tasks.loop(hours=1)
async def update_score_exe():
    print("updating_exercices...")
    DB.update_scoring()
    print(pd.read_sql_query("SELECT * FROM exercice", DB.con).to_markdown())
    print("score updated")


# launch
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print(f"logged in as {client.user}")
    update_score_exe.start()


client.run(os.getenv("TOKEN"))
