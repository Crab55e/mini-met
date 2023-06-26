console_prefix = "[MM.ML]"

print(console_prefix,"Loading...")

import discord
import datetime
import json


intents = discord.Intents.all()
client = discord.Client(intents=intents)
with open("env.json","r") as f:
    ENV = json.loads(f.read())
bot_token = ENV["bot_token"]


try:
    @client.event
    async def on_ready():
        # 変数
        log_channel = client.get_channel(965269631050862622)
        now = datetime.datetime.now()

        # 起動メッセージ
        print(console_prefix,"Message Listenor is Ready!")
        print(console_prefix,f"status:\n- at {now.strftime('%Y-%m-%d %H:%M.%S')}\n- discord.py ver: {discord.__version__}")
        on_ready_log_embed = discord.Embed(title=f":white_check_mark: Message Listenorが起動しました",description="ステータス:",color=0x00ff00)
        on_ready_log_embed.add_field(name="起動日時: ",value=f"{now.strftime('%Y-%m-%d %H:%M.%S')}")
        on_ready_log_embed.add_field(name="discord.pyバージョン: ",value=f"{discord.__version__}")
        await log_channel.send(embed=on_ready_log_embed)

    @client.event
    # メッセージ受信時イベント
    async def on_message(m):
        if (m.author.bot) or (len(m.content) <= 5) or (m.content.startswith("http")) or (m.content.startswith("/")):
            print("Return..")
            return
        # Crab55e
        if (m.author.id == 776726560929480707):
            file_raw = open("storage/txt/ai-databases/crab55e.txt","a",encoding="utf-8")
            file_raw.write(f"\n{m.clean_content}")
            file_raw.close()
            print(console_prefix,f"Writed \"{m.clean_content}\" by @{m.author}")
        # Aru_Fox
        if (m.author.id == 953573832042623036):
            file_raw = open("storage/txt/ai-databases/aru_fox.txt","a",encoding="utf-8")
            file_raw.write(f"\n{m.clean_content}")
            file_raw.close()
            print(console_prefix,f"Writed \"{m.clean_content}\" by @{m.author}")
        # Buta_taicho
        if (m.author.id == 796350579286867988):
            file_raw = open("storage/txt/ai-databases/buta_taicho.txt","a",encoding="utf-8")
            file_raw.write(f"\n{m.clean_content}")
            file_raw.close()
            print(console_prefix,f"Writed \"{m.clean_content}\" by @{m.author}")
        # kae_maru
        if (m.author.id == 940522481079451708):
            file_raw = open("storage/txt/ai-databases/kae_maru.txt","a",encoding="utf-8")
            file_raw.write(f"\n{m.clean_content}")
            file_raw.close()
            print(console_prefix,f"Writed \"{m.clean_content}\" by @{m.author}")
        # mikansugiko
        if (m.author.id == 815468582736625664):
            file_raw = open("storage/txt/ai-databases/mikansugiko.txt","a",encoding="utf-8")
            file_raw.write(f"\n{m.clean_content}")
            file_raw.close()
            print(console_prefix,f"Writed \"{m.clean_content}\" by @{m.author}")
        # 2benpitsu
        if (m.author.id == 945878551805165608):
            file_raw = open("storage/txt/ai-databases/2benpitsu.txt","a",encoding="utf-8")
            file_raw.write(f"\n{m.clean_content}")
            file_raw.close()
            print(console_prefix,f"Writed \"{m.clean_content}\" by @{m.author}")
        # hyocei
        if (m.author.id == 797738135592370197):
            file_raw = open("storage/txt/ai-databases/hyocei.txt","a",encoding="utf-8")
            file_raw.write(f"\n{m.clean_content}")
            file_raw.close()
            print(console_prefix,f"Writed \"{m.clean_content}\" by @{m.author}")
    client.run(bot_token)
# エラー(例外)発生時
except Exception as e:
    print(console_prefix,f"EXCEPTION!!!: {e}")
    