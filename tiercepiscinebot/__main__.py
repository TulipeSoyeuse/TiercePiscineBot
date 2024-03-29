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
    description="list tout les poulains actuels",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def LIST_command(interaction):
    await interaction.response.defer()
    res = DB.list()
    print(res)
    await interaction.followup.send(res)


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


@tree.command(
    name="display",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def display_command(interaction):
    await interaction.response.send_message(DB.display())


@tree.command(
    name="delete",
    description="supprime ton poulain",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def delete_command(interaction, poulain_intra: str):
    DB.delete_poulain(poulain_intra)
    await interaction.response.send_message("poulain deleted")


@tree.command(
    name="score",
    description="classement",
    guild=discord.Object(id=os.getenv("GUILD_ID")),
)
async def score_command(interaction):
    print("\n\n")
    DB.set_score()
    await interaction.response.send_message(DB.get_score())


@tasks.loop(hours=1)
async def update_score_exe():
    print("updating_exercices...")
    DB.update_scoring()
    print("\n", pd.read_sql_query("SELECT * FROM exercice", DB.con).to_markdown())
    print("\n", pd.read_sql_query("SELECT * FROM poulains", DB.con).to_markdown())
    print("score updated")


# launch
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print(f"logged in as {client.user}")
    if not update_score_exe.is_running():
        update_score_exe.start()


client.run(os.getenv("TOKEN"))
