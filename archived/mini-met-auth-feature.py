# さいしょのへんすう
console_prefix = "[MM.Auth]"

# import
print(console_prefix,"Loading...")
from time import sleep
from PIL import Image, ImageDraw, ImageFont

import asyncio
import random
import requests
import json
import sys
import discord
import datetime
import shutil
import os

# 変数
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot_token = "DISABLED FOR ARCHIVE"
auth_image_font = ImageFont.truetype("C:/Windows/Fonts/NotoSerifJP-ExtraLight.otf", 100)
auth_image_raw = Image.open("storage/images/auth/raw.png")

try:
    # 接続完了時イベント
    @client.event
    async def on_ready():   
        # 変数
        now = datetime.datetime.now()

        # 起動メッセージ
        print(console_prefix,"Mini-met is Ready!")
        print(console_prefix,f"status:\n- at {now.strftime('%Y-%m-%d %H:%M.%S')}\n- discord.py ver: {discord.__version__}")
        on_ready_log_embed = discord.Embed(title=f":white_check_mark: 認証機能が起動しました",description="ステータス:",color=0x00ff00)
        on_ready_log_embed.add_field(name="起動日時: ",value=f"{now.strftime('%Y年 %m月 %d日  %H時%M分 %S秒')}")
        on_ready_log_embed.add_field(name="discord.pyバージョン: ",value=f"{discord.__version__}")
        await client.get_channel(965269631050862622).send(embed=on_ready_log_embed)
        # その他
        await client.change_presence(activity=discord.Game(name=f"認証機能が起動したなう"))





    @client.event
    # メッセージ受信時イベント
    async def on_message(m):
        print(console_prefix,"get message")
        if m.author.bot:
            return
        if m.content.startswith("!sc get-auth-image "):
            print(console_prefix,"received command:",m.content)
            command = m.content.lstrip("!sc get-auth-image ")
            generated_text = f"{command}"
            shutil.copyfile("storage/images/auth/raw.png","storage/images/auth/temp.png")
            auth_image_temp = Image.open("storage/images/auth/temp.png")
            auth_image_draw = ImageDraw.Draw(auth_image_temp)
            auth_image_draw.text((96,400),generated_text,"#ffffff",font=auth_image_font,align="center")
            auth_image_temp.save("storage/images/auth/generated.png")
            await m.channel.send(file=discord.File("storage/images/auth/generated.png"))
            os.remove("storage/images/auth/generated.png")
            os.remove("storage/images/auth/temp.png")

    @client.event
    # ユーザー参加時イベント
    async def on_member_join(member):
        if member.bot:
            return

    @client.event
    # リアクション追加イベント
    async def on_reaction_add(reaction, user):
        if user.bot:
            return

    @client.event
    # リアクション削除イベント
    async def on_reaction_remove(reaction, user):
        if user.bot:
            return

    # 接続
    client.run(bot_token)
# エラー(例外)発生時
except Exception as e:
    now = datetime.datetime.now()
    error_log_url = "https://discord.com/api/webhooks/1004379654406275072/JlIh2V8CyTfwV3nv_WL5qDIltE_D72hKMmvNlicontOINdlYEoIiJrsmYowqF1M34DtE"
    error_log_content = {
        "username": "mini-met - authentication",
        "avatar_url": "https://discord.com/assets/7c8f476123d28d103efe381543274c25.png",
        "embeds": [{
            "author": {
                    "name": "| error",
                    "icon_url": "https://cdn.discordapp.com/attachments/804239123895681028/990103681330475048/149.png"
            },
            "title": "子metの認証機能がエラーによってダウンしました",
            "description": f"ERROR :\n{e}",
            "color": 2105893,
            "footer": {
                "text": f"at : {now.strftime('%Y-%m-%d %H:%M.%S')}"
            }
        }]
    }
    requests.post(error_log_url,json.dumps(error_log_content),headers={"Content-Type":"application/json"})
    print(console_prefix,f"EXCEPTION!!!: {e}")
    sleep(30)