# import
import sys
import discord
import random
import asyncio

from time import sleep
from discord.ext import commands
from email import message


client = discord.Client()
ModeFlag = 0
TOKEN = "TOKEN"

@client.event
async def on_ready():
    channel = client.get_channel(939072967395123232)
    print("-----------------------起動しました")
    await channel.send("- 起動しました -")
    mes = ["俺","僕","私"]
    me = random.choice(mes)
    await client.change_presence(activity=discord.Game(name=f"{me}はmetさんの子です。誰が何と言おうとmetさんの子"))
    print("me is : ",me)


@client.event
async def on_message(message):
    global ModeFlag
    rrn = random.randrange(1, 32)
    print("| ユーザーがメッセージを送信しました")

    if message.author.bot:
        return
        print("| botのメッセージを除外しました")

    if message.content == 'm! stop':
        await message.channel.send('- 停止します -')
        print("--------------------------------------------\"m! stop\"コマンドが使用されました")
        sleep(5)
        sys.exit()

    if message.content == 'おはよう' or message.content == 'おはようございます' or message.content == 'おはようございます！' or message.content == 'おはようございます～' or message.content == 'おはよう！' or message.content == 'おはよう～' or message.content == 'ohayou' or message.content == 'oha' or message.content == 'ohayou!':
        mrn_pattern = ["おはよう～", "おはようございます！", "おはようございます～"]
        mrn_msg = random.choice(mrn_pattern)
        sleep(random.uniform(1, 5))
        print("- メッセージを送信しました:\"", mrn_msg, "\"")
        await message.channel.send(mrn_msg)

    if rrn == 2:
            if message.author.bot:
                return
            await message.channel.send("Kuruuu2525XD最強")
            print("- メッセージを送信しました:\"Kuruuu2525XD最強\"")

    if rrn == 1:
            if message.author.bot:
                return
            await message.channel.send("(意味深)")
            print("- メッセージを送信しました:\"(意味深)\"")

client.run(TOKEN)


sleep(3)
