# initial variables
console_prefix = "[MM.Lvl]"

# libraries
print(console_prefix,"Loading...")
from datetime import datetime as dt
from time import sleep
import psutil
import asyncio
import discord
import json


def load():
    global return_var
    try:
        global intents
        global client
        global bot_token
        global datas
        global mini_met
        global console_prefix

    # main variables

        console_prefix = "[MM.Lvl]"
        intents = discord.Intents.all()
        client = discord.Client(intents=intents)
        bot_token = "DISABLED FOR ARCHIVE"

        datas = open("storage/json/leveling/main.json","r",encoding="utf-8")
        datas = json.load(datas)
        mini_met = client.get_user(985254515798327296)
        return_var = "No Error"
        return return_var
    except Exception as error:
        print(console_prefix,f"Exceptioned at Reload: {error}")
        return_var = error
        return return_var
load()

print(console_prefix,"trying main task")
try:
    # 起動時イベント
    @client.event
    async def on_ready():
        now = dt.now()
        log_channel = client.get_channel(965269631050862622)
        memory_usage = psutil.virtual_memory()

        on_ready_log_embed = discord.Embed(title=f":white_check_mark: 子metのレベリング機能が起動しました",description="ステータス:",color=0x00ff00)
        on_ready_log_embed.add_field(name="起動日時",value=f"{now.strftime('%Y年 %m月 %d日  %H時%M分 %S秒')}")
        on_ready_log_embed.add_field(name="メモリ使用率",value=f"{memory_usage.percent}%")
        await log_channel.send(embed=on_ready_log_embed)
        await client.change_presence(activity=discord.Game(name=f"レベリング機能が起動したなう"))
        print(console_prefix,"Leveling Feature is READY!!!")

    @client.event
    async def on_message(m):
        if m.content.startswith("!sc lfeat"):
            print(console_prefix,f"{m.author} issued command: \"{m.content}\"")
        
            if m.content == "!sc lfeat reload":
                await m.channel.send(embed=discord.Embed().set_author(icon_url="https://cdn.discordapp.com/embed/avatars/2.png",name="再読み込み中..."))
                print(console_prefix,"Reloading...")
                load()
                print(console_prefix,"Successfully reloaded.")
                reload_embed = discord.Embed(description=f"Return: {return_var}")
                reload_embed.set_author(icon_url="https://cdn.discordapp.com/embed/avatars/2.png",name="再読み込みが完了しました")
                await m.channel.send(embed=reload_embed)
                pass
        pass

    client.run(bot_token)
except Exception as e:
    print(console_prefix,f"EXCEPTION!!!: {e}")
    sleep(100)