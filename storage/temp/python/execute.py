import discord

intents = discord.Intents.all()
client = discord.Client(intents=intents)
BOT_TOKEN = "OTg1MjU0NTE1Nzk4MzI3Mjk2.GDKTEo.b9fwsBeZFwDWvSl33S2aE_ap7KmQ6vTe63T3_I"
@client.event
async def on_ready():
    await print(client.get_guild(842320961033601044).get_channel(1074249452187033682).fetch_message(client.get_guild(842320961033601044).get_channel(1074249452187033682).get_partial_message(1091643677807489084)).embeds[0].to_dict())
    exit()
client.run(BOT_TOKEN)