# import
print("|")
print("| I M P O R T I N G   L I B R A R I E S . . . ")
print("|")
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

print("|")
print("| I M P O R T E D   L I B R A R I E S.")
print("|")

# え～っと、なんかその、変数
client = discord.Client()
guild_id = "842320961033601044"
guild = client.get_guild(guild_id)
ModeFlag = 0
TOKEN = "OTg1MjU0NTE1Nzk4MzI3Mjk2.GNXk0u.bn_xjXdd-7Df2yk9Sis1--pk83lQUniqxaQSZM"
mes = ["俺","僕","私","私"]
me = random.choice(mes)

print("|")
print("| T R Y I N G   M A I N   T A S K ")
print("|")

try:
    # 起動時イベント
    @client.event
    async def on_ready():   
        # 変数
        logChannel = client.get_channel(965269631050862622)
        now = datetime.datetime.now()

        # 起動メッセージ等
        print("|")
        print("| M I N I - M E T   I S   R E A D Y")
        print("|")
        print("| S T A T U S :")
        print(f"| M E : {me}")
        print(f"| T I M E : {now.month}/{now.day} {now.hour}:{now.min}.{now.second}")
        await logChannel.send(":white_check_mark:  起動しました")
        await logChannel.send("ステータス :")
        await logChannel.send(f"- 一人称 : {me}")
        await logChannel.send(f"- 起動日時 : {now.month}月 {now.day}日 {now.hour}時 {now.minute}分 {now.second}秒")
        # その他
        await client.change_presence(activity=discord.Game(name=f"{me}はmetさんの子です。誰が何と言おうとmetさんの子"))
    #---------------------------ここまで最適化済み

    @client.event
    async def on_message(m):
        global ModeFlag
        rrn = random.randrange(1, 256)  
        print("|")
        print("| R E C E I V E D   M E S S A G E")
        print("|")

        if m.author.bot:
            print("|")
            print("| F R O M   B O T ")
            print("|")
            return
        if m.content == 'm! stop':
            await m.channel.send('- 停止します -')
            print("|")
            print(f"| I S S U E D   C O M M A N D : \"{m.content}\"")
            print("|")
            sleep(5)
            sys.exit()

        if "子met" in m.content or "小met" in m.content:
            await m.channel.send("呼んだ？")
            print("|")
            print("| \"met\" I N   M E S S A G E   C O N T E N T")
            print("|")

        if m.content == "heyかに" or m.content == "おいに！" or m.content == "heyかにさん！" or m.content == "heyカニさん！" or m.content == "heyかにさん" or m.content == "heyカニさん" or m.content == "かにさん！" or m.content == "カニさん！":
            await m.channel.send("<@776726560929480707>おい！！！！")
            print("|")
            print("| C A L L E D   F O R   C R A B")
            print("|")

        if m.content == "!sc help" or m.content == "!sc ?" or m.content == "!sc ヘルプ" or m.content == "!sc":
            help_embed=discord.Embed()
            help_embed.add_field(name="サーバーのIPなどを確認", value="`!sc status`", inline=False)
            help_embed.add_field(name="サーバーの招待リンクを確認", value="`!sc link`", inline=False)
            help_embed.add_field(name="サーバーのwebサイトを確認", value="`!sc web`", inline=False)
            help_embed.add_field(name="サーバーの参加者を確認", value="`!sc list`(<#845185615678144532>でのみ動作)", inline=False)
            help_embed.add_field(name="サーバーのマップのリンクを確認", value="`!sc map`", inline=False)
            await m.channel.send(embed=help_embed)
            print("|")
            print(f"| I S S U E D   C O M M A N D : \"{m.content}\"")
            print("|")
            
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
            print("|")
            print(f"| I S S U E D   C O M M A N D : \"{m.content}\"")
            print("|")

        if m.content == "!sc map" or m.content == "!sc マップ" or m.content == "!sc 地図":
            map_embed=discord.Embed(title="[マップ！]", url="https://mets-svr.com/map/", description="地形や建築を眺めることが出来ます\n動作してない場合は <#968529044121464843> で報告してください", color=0x00aff4)
            await m.channel.send(embed=map_embed)
            print("|")
            print(f"| I S S U E D   C O M M A N D : \"{m.content}\"")
            print("|")

        if m.content == "!sc web" or m.content == "!sc webサイト" or m.content == "!sc site" or m.content == "!sc www":
            web_embed=discord.Embed(title="[webサイト]", url="https://mets-svr.com/", description="公式webサイト！、更新しないとなぁ...")
            await m.channel.send(embed=web_embed)
            print("|")
            print(f"| I S S U E D   C O M M A N D : \"{m.content}\"")
            print("|")

        if m.content == "!sc link" or m.content == "!sc discord" or m.content == "!sc invite" or m.content == "!sc 招待" or m.content == "!sc リンク":
            link_embed=discord.Embed(title="[Discordリンク]", url="https://discord.mets-svr.com/", description="このサーバーのdiscordのリンクです...")
            await m.channel.send(embed=link_embed)
            print("|")
            print(f"| I S S U E D   C O M M A N D : \"{m.content}\"")
            print("|")

        if m.content == "!sc dakuhore" or m.content == "!sc だくほれ":
            dakuhore_embed=discord.Embed(title="[だくほれ]", url="https://mets-svr.com/dakuhore/", description="カルロスさん。彼氏。かわさん。MEE6。世界史の先生。[詳しく](http://mets-svr.com/だくほれ/)")
            await m.channel.send(embed=dakuhore_embed)
            print("|")
            print(f"| I S S U E D   C O M M A N D : \"{m.content}\"")
            print("|")

        if m.content == 'おはよう' or m.content == 'おはようございます' or m.content == 'おはようございます！' or m.content == 'おはようございます～' or m.content == 'おはよう！' or m.content == 'おはよう～' or m.content == 'ohayou' or m.content == 'oha' or m.content == 'ohayou!'or m.content == 'おはようです'or m.content == 'おはようです～'or m.content == 'おはようです！'or m.content == 'おはようです！！'or m.content == 'おはようです～～':
            mrn_pattern = ["おはよう～", "おはようございます！", "おはようございます～"]
            mrn_msg = random.choice(mrn_pattern)
            sleep(random.uniform(1, 5))
            print("|")
            print(f"| S E N D E D   M E S S A G E : \"{mrn_msg}\"")
            print("|")
            await m.channel.send(mrn_msg)

        if "<@" in m.content and ">" in m.content:
            print("|")
            print("| R E C E I V E   M E N T I O N   I N   M E S S A G E:",m.content)
            print("|")
            mention_embed = discord.Embed(title="mention message log", url=f"https://discord.com/channels/{guild_id}/{m.channel.id}/{m.id}/", description="jump to message", color=0xffd152)
            mention_embed.add_field(name="content: ", value=f"{m.content}", inline=False)
            await client.get_channel(998970570928554095).send(embed=mention_embed)

        if rrn == 4:
            await m.channel.send("https://cdn.discordapp.com/attachments/845185615678144532/1009466980929114193/saved.png")
            print("|")
            print("| S E N D E D   M E S S A G E : \"保存済みって話する？\"")
            print("|")
#        if rrn == 3:
#            await m.channel.send("https://cdn.discordapp.com/attachments/842320961033601047/1007215551761883198/767118D2-8E86-43A5-88C3-59F99769544C.jpg")
#            print("|\n| sended message \"貴方頭脳未使用思考...\"\n|")

        if rrn == 2:
            await m.channel.send("Kuruuu2525XD最強")
            print("|")
            print("| S E N D E D   M E S S A G E : \"Kuruuu2525XD最強\"")
            print("|")

        if rrn == 1:
            await m.channel.send("(意味深)")
            print("|")
            print("| S E N D E D   M E S S A G E : \"(意味深)\"")
            print("|")

    client.run(TOKEN)
except Exception as e:
    now = datetime.datetime.now()
    ErrorLog_URL = "https://discord.com/api/webhooks/1004379654406275072/JlIh2V8CyTfwV3nv_WL5qDIltE_D72hKMmvNlicontOINdlYEoIiJrsmYowqF1M34DtE"
    ErrorLog_Content = {
        "username": "game8自動宣伝",
        "avatar_url": "https://discord.com/assets/7c8f476123d28d103efe381543274c25.png",
        "embeds": [{
            "author": {
                    "name": "| error",
                    "icon_url": "https://cdn.discordapp.com/attachments/804239123895681028/990103681330475048/149.png"
            },
            "title": "子metが落ちるくらいのエラーが...",
            "description": f"ERROR :\n{e}",
            "color": 2105893,
            "footer": {
                "text": f"TIME : {now.month}/{now.day}/ {now.hour}:{now.minute}.{now.second}"
            }
        }]
    }
    requests.post(ErrorLog_URL,json.dumps(ErrorLog_Content),headers={"Content-Type":"application/json"})
    print("|")
    print(f"| E X C E P T I O N : {e}")
    print("|")
    sleep(30)
