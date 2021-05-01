import json
import re

import discord
from discord import Embed

bot = discord.Client()
with open("config.json", encoding='utf-8') as fh:
    config = json.load(fh)
xd_regex = r"xd+"

async def xd_message(message):
    if config.get("enable_xd"):
        if re.search(xd_regex, message.content, re.IGNORECASE):
            await message.channel.send("XDDDDDDDDDD")

async def react(message):
    if str(message.channel.id) in config["mapping"].keys():
        print(f"Reacting with {config['mapping'][str(message.channel.id)]} to {message.id} from {message.author.id}")
        for emoji in config["mapping"][str(message.channel.id)]:
            print(emoji)
            if isinstance(emoji, int):
                await message.add_reaction(bot.get_emoji(emoji))
            else:
                await message.add_reaction(emoji)


async def showroles(message):
    infoEmbed = Embed(title="Roles")
    roles = {}
    async for member in message.guild.fetch_members(limit=None):
        for member_role in member.roles:
            if member_role.id in config["list_roles"]:
                if member_role.name in roles:
                    roles[member_role.name] += 1
                else:
                    roles[member_role.name] = 1
    
    desc = f"This server has {str(bot.get_guild(message.guild.id).member_count)} members.\n\n"
    for key, value in roles.items():
        desc += f"**{key}**: {value}\n"
    
    infoEmbed.description = desc
    await message.channel.send(embed=infoEmbed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == config["role_command"] and message.guild is not None:
        return await showroles(message)
    await react(message)
    await xd_message(message)

def start():
    print("Starting...")
    bot.run(config["bot_token"], reconnect=True)

start()

