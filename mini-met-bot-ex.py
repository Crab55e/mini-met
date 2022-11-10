# さいしょのへんすう
console_prefix = "[mini-met]"

# import
print(console_prefix,"Importing libraries...")
from discord.ext import commands
from email import message
from time import sleep

import asyncio
import random
import requests
import json
import sys
import discord
import datetime
import psutil

# 変数
print(console_prefix,"setting variables...")
client = discord.Client()
guild_id = "842320961033601044"
guild = client.get_guild(guild_id)
bot_token = "ﾄｹﾝ"
mode_flag = 0
mes = ["俺","僕","私","私"]
me = random.choice(mes)
brocked_words = open("brocked_words.json","r",encoding="utf-8")
brocked_words = json.load(brocked_words)
brocked_word_wait_sec = 15

print(console_prefix,"trying main task")

try:
    # 起動時イベント
    @client.event
    async def on_ready():   
        # 変数
        log_channel = client.get_channel(965269631050862622)
        now = datetime.datetime.now()

        # 起動メッセージ等
        print(console_prefix,"Mini-met is Ready!")
        print(console_prefix,f"status:\n- at {now.strftime('%Y-%m-%d %H:%M.%S')}\n- discord.py ver: {discord.__version__}")
        await log_channel.send(":white_check_mark: 子metのメインプログラムが起動しました")
        await log_channel.send("ステータス : ")
        await log_channel.send(f"- 一人称 : {me}")
        await log_channel.send(f"- 起動日時 : {now.month}月 {now.day}日 {now.hour}時 {now.minute}分 {now.second}秒")
        await log_channel.send(f"discord.py バージョン : {discord.__version__}")
        # その他
        await client.change_presence(activity=discord.Game(name=f"{me}はmetさんの子です。誰が何と言おうとmetさんの子"))

    @client.event
    async def on_message(m):
        global mode_flag
        rrn = random.randrange(1, 256)  
        print(console_prefix,"received message event")

        for brocked_word in brocked_words:
            if brocked_word in m.content:
                print(console_prefix,f"detected brocked word: {brocked_word}")
                print(console_prefix,f"waiting {brocked_word_wait_sec}s...")
                await m.add_reaction("❗")
                await asyncio.sleep(brocked_word_wait_sec)
                print(console_prefix,f"deleting brocked message: {m.content}")
                nsfw_embed = discord.Embed(title="Brocked words", description=" ", color=0xffd152)
                nsfw_embed.add_field(name="user: ", value=f"<@{m.author.id}>", inline=False)
                nsfw_embed.add_field(name="content: ", value=f"{m.content}", inline=False)
                await client.get_channel(998970821232037991).send(embed=nsfw_embed)
                await m.delete()
                print(console_prefix,"deleted")

        if m.author.bot:
            return

        if m.content == 'm! stop':
            await m.channel.send(':octagonal_sign: 5秒後に子metのメインプログラムを停止します')
            print(console_prefix,f"{m.author} issued command: {m.content}")
            sleep(5)
            sys.exit()

        if "子met" in m.content or "小met" in m.content:
            await m.channel.send("呼んだ？")
            print(console_prefix,f"received message:) {m.content}")

        if m.content == "heyかに" or m.content == "おいに！" or m.content == "heyかにさん！" or m.content == "heyカニさん！" or m.content == "heyかにさん" or m.content == "heyカニさん" or m.content == "かにさん！" or m.content == "カニさん！":
            await m.channel.send("<@967372572859695184>おい！！！！")
            print(console_prefix,f"called for Crab55e")

        if m.content == "!sc help" or m.content == "!sc ?" or m.content == "!sc ヘルプ" or m.content == "!sc":
            help_embed=discord.Embed()
            help_embed.add_field(name="サーバーのIPなどを確認", value="`!sc status`", inline=False)
            help_embed.add_field(name="サーバーの招待リンクを確認", value="`!sc link`", inline=False)
            help_embed.add_field(name="サーバーのwebサイトを確認", value="`!sc web`", inline=False)
            help_embed.add_field(name="サーバーの参加者を確認", value="`!sc list`(<#845185615678144532>でのみ動作)", inline=False)
            help_embed.add_field(name="サーバーのマップのリンクを確認", value="`!sc map`", inline=False)
            await m.channel.send(embed=help_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")
            
        if m.content == "!sc status" or m.content == "!sc stats" or m.content == "!sc ステータス":
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory()
            status_embed=discord.Embed(title="サーバーステータス！", description="IPやバージョン等の情報", color=0x6f5134)
            status_embed.add_field(name="Java Edition - IP", value="`pre-mets.feathermc.gg`", inline=False)
            status_embed.add_field(name="Bedrock Edition - IP", value="`hot.ssnetwork.io`", inline=False)
            status_embed.add_field(name="Bedrock Edition - Port", value="`49931`")
            status_embed.add_field(name="CPU Usage",value=f"{cpu_usage}%", inline=False)
            status_embed.add_field(name="Memory Usage",value=f"{memory_usage.percent}%")
            status_embed.set_footer(text="ver:1.19.2, 情報更新: 2022/8/22")
            await m.channel.send(embed=status_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        if m.content == "!sc map" or m.content == "!sc マップ" or m.content == "!sc 地図":
            map_embed=discord.Embed(title="[マップ！]", url="https://mets-svr.com/map/", description="地形や建築を眺めることが出来ます\n動作してない場合は <#968529044121464843> で報告してください", color=0x00aff4)
            await m.channel.send(embed=map_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        if m.content == "!sc web" or m.content == "!sc webサイト" or m.content == "!sc site" or m.content == "!sc www":
            web_embed=discord.Embed(title="[webサイト]", url="https://mets-svr.com/", description="公式webサイト！、更新しないとなぁ...")
            await m.channel.send(embed=web_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        if m.content == "!sc link" or m.content == "!sc discord" or m.content == "!sc invite" or m.content == "!sc 招待" or m.content == "!sc リンク":
            link_embed=discord.Embed(title="[Discordリンク]", url="https://discord.mets-svr.com/", description="このサーバーのdiscordのリンクです...")
            await m.channel.send(embed=link_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        if m.content == "!sc dakuhore" or m.content == "!sc だくほれ":
            dakuhore_embed=discord.Embed(title="[だくほれ]", url="https://mets-svr.com/dakuhore/", description="カルロスさん。彼氏。かわさん。MEE6。世界史の先生。[詳しく](http://mets-svr.com/だくほれ/)")
            await m.channel.send(embed=dakuhore_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        if m.content == 'おはよう' or m.content == 'おはようございます' or m.content == 'おはようございます！' or m.content == 'おはようございます～' or m.content == 'おはよう！' or m.content == 'おはよう～' or m.content == 'ohayou' or m.content == 'oha' or m.content == 'ohayou!'or m.content == 'おはようです'or m.content == 'おはようです～'or m.content == 'おはようです！'or m.content == 'おはようです！！'or m.content == 'おはようです～～':
            print(console_prefix,f"received morning message: {m.content}, from: {m.author}")
            mrn_pattern = ["おはよう～", "おはようございます！", "おはようございます～"]
            mrn_msg = random.choice(mrn_pattern)
            await asyncio.sleep(random.uniform(1,2))
            print(console_prefix,f"sent morning message: {mrn_msg}")
            await m.channel.send(mrn_msg)

        if "<@" in m.content and ">" in m.content:
            print(console_prefix,f"received mention message: {m.content}, from: {m.author}")
            mention_embed = discord.Embed(title="mention message log", url=f"https://discord.com/channels/{guild_id}/{m.channel.id}/{m.id}/", description=" ", color=0xffd152)
            mention_embed.add_field(name="content: ", value=f"{m.content}", inline=False)
            await client.get_channel(998970570928554095).send(embed=mention_embed)

        if rrn == 4:
            await m.channel.send("https://cdn.discordapp.com/attachments/845185615678144532/1009466980929114193/saved.png")
            print(console_prefix,"sent random  message: \"保存済みって話する？\"")

        if rrn == 2:
            await m.channel.send("Kuruuu2525XD最強")
            print(console_prefix,"sent random message: \"Kuruuu2525XD最強\"")

        if rrn == 1:
            await m.channel.send("(意味深)")
            print(console_prefix,"sent random message: \"(意味深)\"")

    client.run(bot_token)
except Exception as e:
    now = datetime.datetime.now()
    ErrorLog_URL = "https://discord.com/api/webhooks/1004379654406275072/JlIh2V8CyTfwV3nv_WL5qDIltE_D72hKMmvNlicontOINdlYEoIiJrsmYowqF1M34DtE"
    ErrorLog_Content = {
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
    requests.post(ErrorLog_URL,json.dumps(ErrorLog_Content),headers={"Content-Type":"application/json"})
    print(console_prefix,f"EXCEPTION!!!: {e}")
    sleep(30)
