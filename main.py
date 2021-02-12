import json

import discord
from discord import Embed

bot = discord.Client()
with open("config.json") as fh:
    config = json.load(fh)


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
    desc = 'This server has ' + str(bot.get_guild(message.guild.id).member_count) + ' members.\n\n'
    await message.guild.fetch_members(limit=None).flatten()
    for r in await message.guild.fetch_roles():
        if r.id in config["list_roles"]:
            desc += '**' + r.name + '**: ' + str(len(r.members)) + '\n'
    infoEmbed.description = desc
    await message.channel.send(embed=infoEmbed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == config["role_command"]:
        return await showroles(message)
    await react(message)

def start():
    print("Starting...")
    bot.run(config["bot_token"], reconnect=True)

start()

