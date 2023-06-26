# さいしょのへんすう
console_prefix = "[mini-met]"

# import
print(console_prefix,"Importing libraries...")
from time import sleep

import requests
import json
import discord
import datetime

# 変数
print(console_prefix,"setting variables...")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
bot_token = "OTg1MjU0NTE1Nzk4MzI3Mjk2.GeD_W-.r7R73X4nWNgXkbtvPvg0hYpa55QHjMpCICA5Xs"

print(console_prefix,"trying main task")

try:
    # 接続完了時イベント
    @client.event
    async def on_ready():   
        # 変数
        log_channel = client.get_channel(965269631050862622)
        now = datetime.datetime.now()
        crab55e = client.get_user(776726560929480707)
        await crab55e.send(content=f"{now}")





    @client.event
    # メッセージ受信時イベント
    async def on_message(m):
        print(console_prefix,"received Message event")
        # bot殻のメッセージを無視
        if m.author.bot:
            return
    # 接続
    client.run(bot_token)
# エラー(例外)発生時
except Exception as e:
    now = datetime.datetime.now()
    error_log_url = "https://discord.com/api/webhooks/1004379654406275072/JlIh2V8CyTfwV3nv_WL5qDIltE_D72hKMmvNlicontOINdlYEoIiJrsmYowqF1M34DtE"
    error_log_content = {
        "username": "mini-met - main",
        "avatar_url": "https://discord.com/assets/7c8f476123d28d103efe381543274c25.png",
        "embeds": [{
            "author": {
                    "name": "| error",
                    "icon_url": "https://cdn.discordapp.com/attachments/804239123895681028/990103681330475048/149.png"
            },
            "title": "子metのメインプログラムがエラーによってダウンしました",
            "description": f"ERROR :\n{e}",
            "color": 2105893,
            "footer": {
                "text": f"at : {now.month}/{now.day}/ {now.hour}:{now.minute}.{now.second}"
            }
        }]
    }
    requests.post(error_log_url,json.dumps(error_log_content),headers={"Content-Type":"application/json"})
    print(console_prefix,f"EXCEPTION!!!: {e}")
    sleep(30)