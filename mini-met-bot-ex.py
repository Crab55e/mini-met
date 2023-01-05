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

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
bot_token = "とけん"

guild_id = "842320961033601044"
guild = client.get_guild(guild_id)
kanb_room = client.get_channel(966297997216448512)
me = "ぼく"
brocked_words = open("storage/json/brocked_words.json","r",encoding="utf-8")
brocked_words = json.load(brocked_words)
latest_actioned_brocked_word_id = 0
latest_reactioned_message_id = 0
calling_to_crab_word_list = ["heyかに","heyカニ","heyかにさん","heyカニさん","おいに","かにさん！","カニさん！"]

print(console_prefix,"trying main task")

try:
    # 接続完了時イベント
    @client.event
    async def on_ready():   
        # 変数
        log_channel = client.get_channel(965269631050862622)
        now = datetime.datetime.now()

        # 起動メッセージ
        print(console_prefix,"Mini-met is Ready!")
        print(console_prefix,f"status:\n- at {now.strftime('%Y-%m-%d %H:%M.%S')}\n- discord.py ver: {discord.__version__}")
        on_ready_log_embed = discord.Embed(title=f":white_check_mark: {me} が起動しました",description="ステータス:",color=0x00ff00)
        on_ready_log_embed.add_field(name="一人称: ",value=f"{me}")
        on_ready_log_embed.add_field(name="起動日時: ",value=f"{now.strftime('%Y年 %m月 %d日  %H時%M分 %S秒')}")
        on_ready_log_embed.add_field(name="discord.pyバージョン: ",value=f"{discord.__version__}")
        await log_channel.send(embed=on_ready_log_embed)
        # その他
        await client.change_presence(activity=discord.Game(name=f"{me}が起動したなう"))





    @client.event
    # メッセージ受信時イベント
    async def on_message(m):
        print(console_prefix,"received Message event")
        now = datetime.datetime.now()
        global brocked_words
        global latest_actioned_brocked_word_id
        
        # ワードフィルター
        if (m.author.id != 985254515798327296) and (not m.content.startswith("!sc ")):
            for brocked_word in brocked_words:
                if brocked_word in m.content:
                    print(console_prefix,f"detected brocked word: {brocked_word}")
                    brocked_word_embed = discord.Embed(title="ワードフィルタにかかるメッセージを検知しました",url=f"{m.jump_url}",description=f"チャンネル: <#{m.channel.id}>\nユーザー: <@{m.author.id}>")
                    brocked_word_embed.set_author(icon_url=f"{m.author.avatar.url}",name=f"{m.author}")
                    brocked_word_embed.set_footer(text=f"MId: {m.id} ,ChId: {m.channel.id} ,At: {now.strftime('%Y-%m-%d %H:%M.%S')}")
                    brocked_word_embed.add_field(name="メッセージ",value=f"{m.content}")
                    await client.get_channel(998970821232037991).send(embed=brocked_word_embed)
                    await m.add_reaction("❗")
                    latest_actioned_brocked_word_id = m.id
                    await asyncio.sleep(1)
                    await m.remove_reaction("❗",discord.Object(985254515798327296))
        # bot殻のメッセージを無視
        if m.author.bot:
            return

        # 強制終了 コマンド
        if m.content == 'm! stop':
            await m.channel.send(':octagonal_sign: 5秒後に子metのメインプログラムを停止します')
            print(console_prefix,f"{m.author} issued command: {m.content}")
            sleep(5)
            sys.exit()

        # 呼ばれた気がするときにひょっこり顔を出す
        if "子met" in m.content or "小met" in m.content:
            if m.author.top_role.id == 844359217984700446 or m.author.top_role.id == 1020521550945996900:
                await m.channel.send("お呼びでしょうか？")
            else:
                await m.channel.send("呼んだ？")
            print(console_prefix,f"received message:) {m.content}")


        # 僕にメンションを送る
        if m.content == "heyかに" or m.content == "おいに！" or m.content == "heyかにさん！" or m.content == "heyカニさん！" or m.content == "heyかにさん" or m.content == "heyカニさん" or m.content == "かにさん！" or m.content == "カニさん！":
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            if m.content == "heyかに" or m.content == "heyカニ" or m.content == "heyかにさん" or m.content == "heyカニさん":
                async with m.channel.typing():
                    await asyncio.sleep(1)
                temp_rn = random.randrange(1,2)
                if temp_rn == 1:
                    await m.channel.send("<@776726560929480707> 呼ばれてるよ～")
                    return
                if temp_rn == 2:
                    await m.channel.send("<@776726560929480707> よばれてるよ～～")
                    return
                return
            if m.content == "おいに！":
                await m.channel.send("<@776726560929480707> おい！！！")
                return
            else:
                m.channel.send("<@776726560929480707> おーい")
            print(console_prefix,f"called mention to Crab55e")
    
        # ヘルプ コマンド
        if m.content == "!sc help" or m.content == "!sc ?" or m.content == "!sc ヘルプ" or m.content == "!sc":
            help_embed=discord.Embed()
            help_embed.add_field(name="サーバーのIPなどを確認", value="`!sc status`", inline=False)
            help_embed.add_field(name="サーバーの招待リンクを確認", value="`!sc link`", inline=False)
            help_embed.add_field(name="サーバーのwebサイトを確認", value="`!sc web`", inline=False)
            help_embed.add_field(name="サーバーの参加者を確認", value="`!sc list`(<#845185615678144532>でのみ動作)", inline=False)
            help_embed.add_field(name="サーバーのマップのリンクを確認", value="`!sc map`", inline=False)
            await m.channel.send(embed=help_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")
            
        # ステータス コマンド
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

        # マップ コマンド
        if m.content == "!sc map" or m.content == "!sc マップ" or m.content == "!sc 地図":
            map_embed=discord.Embed(title="[マップ！]", url="https://mets-svr.com/map/", description="地形や建築を眺めることが出来ます\n動作してない場合は <#968529044121464843> で報告してください", color=0x00aff4)
            await m.channel.send(embed=map_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        # webリンク コマンド
        if m.content == "!sc web" or m.content == "!sc webサイト" or m.content == "!sc site" or m.content == "!sc www":
            web_embed=discord.Embed(title="[webサイト]", url="https://mets-svr.com/", description="公式webサイト！、更新しないとなぁ...")
            await m.channel.send(embed=web_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        # 招待リンク コマンド
        if m.content == "!sc link" or m.content == "!sc discord" or m.content == "!sc invite" or m.content == "!sc 招待" or m.content == "!sc リンク":
            link_embed=discord.Embed(title="[Discordリンク]", url="https://discord.mets-svr.com/", description="このサーバーのdiscordのリンクです\n`https://discord.mets-svr.com/`")
            await m.channel.send(embed=link_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        # ワードフィルター コマンド
        if m.content.startswith("!sc bword",0) and m.channel.id == 1011965676962984047:
            print(console_prefix,f"{m.author} issued command: {m.content}")
            # 登録
            if m.content.startswith("!sc bword add ",0):
                target_message = m.content.replace("!sc bword add ","")
                bword_temp_r = open("storage/json/brocked_words.json","r",encoding="utf-8")
                bword_temp_r = json.load(bword_temp_r)
                bword_temp_r.append(target_message)
                bword_temp_r = json.dumps(bword_temp_r)
                bword_temp_w = open("storage/json/brocked_words.json","w",encoding="utf-8")
                bword_temp_w.write(bword_temp_r)
                bword_temp_w.close()

                bword_appended_embed = discord.Embed(title=f"\"{target_message}\" をワードフィルターに追加しました")
                await m.channel.send(embed=bword_appended_embed)
                print(console_prefix,f"Appended {target_message}")
            if m.content.startswith("!sc bword remove",0):
                target_message = m.content.replace("!sc bword remove ","")
                bword_temp_r = open("storage/json/brocked_words.json","r",encoding="utf-8")
                bword_temp_r = json.load(bword_temp_r)
                bword_temp_r.remove(target_message)
                bword_temp_r = json.dumps(bword_temp_r)
                bword_temp_w = open("storage/json/brocked_words.json","w",encoding="utf-8")
                bword_temp_w.write(bword_temp_r)
                bword_temp_w.close()

                bword_removed_embed = discord.Embed(title=f"\"{target_message}\" をワードフィルターから削除しました")
                await m.channel.send(embed=bword_removed_embed)
            if m.content.startswith("!sc bword list",0):
                brocked_words_list = ""
                for a_brocked_word in brocked_words:
                    brocked_words_list = brocked_words_list + f"`{a_brocked_word}`, "
                await m.channel.send(brocked_words_list[:-1])
                print(console_prefix,"Sent brocked word list")

        # リロード コマンド
        if m.content == "!sc reload":
            await m.channel.send("再読み込み中...")
            brocked_words = open("storage/json/brocked_words.json","r",encoding="utf-8")
            brocked_words = json.load(brocked_words)
            await m.channel.send("変数が更新されました")
            print(console_prefix,f"{m.author} issued command: {m.content}")

        # 朝の挨拶
        if m.content == 'おはよう' or m.content == 'おはようございます' or m.content == 'おはようございます！' or m.content == 'おはようございます～' or m.content == 'おはよう！' or m.content == 'おはよう～' or m.content == 'ohayou' or m.content == 'oha' or m.content == 'ohayou!'or m.content == 'おはようです'or m.content == 'おはようです～'or m.content == 'おはようです！'or m.content == 'おはようです！！'or m.content == 'おはようです～～':
            print(console_prefix,f"received morning message: {m.content}, from: {m.author}")
            mrn_pattern = ["おはよう～", "おはようございます！", "おはようございます～"]
            mrn_msg = random.choice(mrn_pattern)
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            if m.author.top_role.id == 844359217984700446 or m.author.top_role.id == 1020521550945996900:
                await m.channel.send("おはようございます。")
            else:
                await m.channel.send(mrn_msg)
            print(console_prefix,f"sent morning message: {mrn_msg}")

        # メンションログ
        if "<@" in m.content and ">" in m.content:
            print(console_prefix,f"received mention message: {m.content}, from: {m.author}")
            mention_embed = discord.Embed(title="mention message log", url=f"https://discord.com/channels/{guild_id}/{m.channel.id}/{m.id}/", description=" ", color=0xffd152)
            mention_embed.add_field(name="content: ", value=f"{m.content}", inline=False)
            await client.get_channel(998970570928554095).send(embed=mention_embed)

        # 返信
        if m.content.endswith("。"):
            if "嫌い" in m.content or "きらい" in m.content or "キライ" in m.content:
                return
            if "しね" in m.content or "死ね" in m.content or "シネ" in m.content:
                return
            async with m.channel.typing():
                await asyncio.sleep(1)
            print(console_prefix,f"received message of endwith \"。\"")
            if m.author.top_role.id == 844359217984700446 or m.author.top_role.id == 1020521550945996900:
                await m.reply(content="ですよね！",mention_author=False)
            else:
                await m.reply(content="だよね！！！",mention_author=False)
        # w
        if m.content.endswith("ねw") or m.content.endswith("ねｗ") or m.content.endswith("なw") or m.content.endswith("なｗ"):
            temp_rn = random.randrange(1,3)
            if temp_rn == 1:
                async with m.channel.typing():
                    await asyncio.sleep(random.uniform(2,4))
                if m.content.endswith("www") or m.content.endswith("ｗｗｗ"):
                    await m.channel.send("wwww")
                    return
                if m.content.endswith("ww") or m.content.endswith("ｗｗ"):
                    await m.channel.send("ww")
                    return
                if m.content.endswith("w") or m.content.endswith("ｗ"):
                    await m.channel.send("w")
                    return

        if m.content == "がんば":
            await asyncio.sleep(1.5)
            async with m.channel.typing():
                await asyncio.sleep(random.randrange(1,2))
            await m.channel.send("がんば")
        
        if "なす" in m.content:
            temp_rn = random.randrange(1,10)
            if temp_rn == 1:
                async with m.channel.typing():
                    await asyncio.sleep(random.randrange(1,2))
                temp_rn = random.randrange(1,50)
                if temp_rn == 1:
                    await m.reply(content="なす？\nhttps://cdn.discordapp.com/attachments/845185615678144532/1060025135735771176/IMG_1150.png",mention_author=False)
                else:
                    await m.reply("なす？\nhttps://media.discordapp.net/attachments/1055151855950372874/1055756068728361010/image.gif",mention_author=False)

        
        if m.content.startswith("<@985254515798327296>"):
            if m.content.startswith("<@985254515798327296> "):
                command = m.content.lstrip("<@985254515798327296> ")
            elif m.content.startswith("<@985254515798327296>"):
                command = m.content.lstrip("<@985254515798327296>")
            print(console_prefix,f"received Mention Command: {command}")
            
            await asyncio.sleep(.2)

            if command == "サイコロ振って":
                async with m.channel.typing():
                    temp_rn = random.randrange(1,6)

                await m.channel.send(f"{temp_rn}!")
            if command == "今のドル円教えて":
                async with m.channel.typing():
                    dolyen_rate = "https://www.gaitameonline.com/rateaj/getrate"
                    dolyen_rate = requests.get(dolyen_rate)
                    dolyen_rate = dolyen_rate.json()
                    dolyen_rate = dolyen_rate["quotes"][20]
                    dolyen_rate_embed = discord.Embed(title=f"{dolyen_rate['currencyPairCode']}",description=f"High: {dolyen_rate['high']}\nLow: {dolyen_rate['low']}")

                await m.channel.send(embed=dolyen_rate_embed)

            if (command.startswith("明日の")) and (command.endswith("の天気教えて")):
                async with m.channel.typing():
                    command = command.lstrip("明日の")
                    command = command.rstrip("の天気教えて")
                    if command.endswith("地方"):
                        command = command.rstrip("地方")
                    if command.endswith("県"):
                        command = command.rstrip("県")
                    if command.endswith("都"):
                        command = command.rstrip("都")
                    if command.endswith("府"):
                        command = command.rstrip("府")
                    match command:
                        case "宗谷": areacode = "011000"
                        case "上川": areacode = "012000"
                        case "留萌": areacode = "012000"
                        case "網走": areacode = "013000"
                        case "北見": areacode = "013000"
                        case "紋別": areacode = "013000"
                        case "十勝": areacode = "014030"
                        case "釧路": areacode = "014100"
                        case "根室": areacode = "014100"
                        case "胆振": areacode = "015000"
                        case "日高": areacode = "015000"
                        case "石狩": areacode = "016000"
                        case "空知": areacode = "016000"
                        case "後志": areacode = "016000"
                        case "渡島": areacode = "017000"
                        case "檜山": areacode = "017000"
                        case "青森": areacode = "020000"
                        case "岩手": areacode = "030000"
                        case "宮城": areacode = "040000"
                        case "秋田": areacode = "050000"
                        case "山形": areacode = "060000"
                        case "福島": areacode = "070000"
                        case "茨城": areacode = "080000"
                        case "栃木": areacode = "090000"
                        case "群馬": areacode = "100000"
                        case "埼玉": areacode = "110000"
                        case "千葉": areacode = "120000"
                        case "東京": areacode = "130000"
                        case "神奈川": areacode = "140000"
                        case "山梨": areacode = "190000"
                        case "長野": areacode = "200000"
                        case "岐阜": areacode = "210000"
                        case "静岡": areacode = "220000"
                        case "愛知": areacode = "230000"
                        case "三重": areacode = "240000"
                        case "新潟": areacode = "150000"
                        case "富山": areacode = "160000"
                        case "石川": areacode = "170000"
                        case "福井": areacode = "180000"
                        case "滋賀": areacode = "250000"
                        case "京都": areacode = "260000"
                        case "大阪": areacode = "270000"
                        case "兵庫": areacode = "280000"
                        case "奈良": areacode = "290000"
                        case "和歌山": areacode = "300000"
                        case "鳥取": areacode = "310000"
                        case "島根": areacode = "320000"
                        case "岡山": areacode = "330000"
                        case "広島": areacode = "340000"
                        case "徳島": areacode = "360000"
                        case "香川": areacode = "370000"
                        case "愛媛": areacode = "380000"
                        case "高知": areacode = "390000"
                        case "山口": areacode = "350000"
                        case "福岡": areacode = "400000"
                        case "佐賀": areacode = "410000"
                        case "長崎": areacode = "420000"
                        case "熊本": areacode = "430000"
                        case "大分": areacode = "440000"
                        case "宮崎": areacode = "450000"
                        case "奄美": areacode = "460040"
                        case "鹿児島": areacode = "460100"
                        case "沖縄本島": areacode = "471000"
                        case "大東島": areacode = "472000"
                        case "宮古島": areacode = "473000"
                        case "八重山": areacode = "474000"
                        case _: areacode = "Not Found"
                    if areacode == "Not Found":
                        await m.channel.send("しらん")
                        return
                    jma_data = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{areacode}.json"
                    jma_data = requests.get(jma_data).json()
                    jma_data = jma_data[0]
                    weather_info_embed_title = discord.Embed(color=0xcccccc,title=f"天気by気象庁",url="https://www.jma.go.jp/jma/",description=f'{jma_data["publishingOffice"]} | {jma_data["reportDatetime"]}')
                    
                    weather_info_embed_weather = discord.Embed(color=0xff8888,title=f"天気",description=f'`{jma_data["timeSeries"][0]["timeDefines"][1]}`')
                    try:
                        for weather in jma_data["timeSeries"][0]["areas"]:
                            weather_info_embed_weather.add_field(inline=False,name=f'エリア: {weather["area"]["name"]}',value=f'**天気**: {weather["weathers"][1].replace("　","")}\n**風**: {weather["winds"][1].replace("　","")}\n**波**: {weather["waves"][1].replace("　","")}')
                    except Exception as e:
                        print(console_prefix,"Exception! It\'s keyerror of \"waves\"?\n",e)
                        for weather in jma_data["timeSeries"][0]["areas"]:
                            weather_info_embed_weather.add_field(inline=False,name=f'エリア: {weather["area"]["name"]}',value=f'**天気**: {weather["weathers"][1].replace("　","")}\n**風**: {weather["winds"][1].replace("　","")}')

                    weather_info_embed_rainluck = discord.Embed(color=0x88ff88,title=f"降水確率",description=f'`{jma_data["timeSeries"][1]["timeDefines"][1]}`')
                    for rainluck in jma_data["timeSeries"][1]["areas"]:
                        weather_info_embed_rainluck.add_field(name=f'エリア: {rainluck["area"]["name"]}',value=f'{rainluck["pops"][1]}%')

                    weather_info_embed_temp = discord.Embed(color=0x8888ff,title=f"気温",description=f'`{jma_data["timeSeries"][1]["timeDefines"][0]}` ～ `{jma_data["timeSeries"][1]["timeDefines"][1]}`')
                    for area in jma_data["timeSeries"][2]["areas"]:
                        weather_info_embed_temp.add_field(name=f'エリア: {area["area"]["name"]}',value=f'最低気温: {area["temps"][0]}\n最高気温: {area["temps"][1]}')
                await m.channel.send(embeds=[weather_info_embed_title,weather_info_embed_weather,weather_info_embed_rainluck,weather_info_embed_temp])
    @client.event
    # ユーザー参加時イベント
    async def on_member_join(member):
        print(console_prefix,f"received member join event: {member.name}")
        member_join_embed = discord.Embed(title="メンバー参加イベント",description=f"<@{member.id}>\"{guild.member_count}人目\"のメンバー。\"{member.joined_at.strftime('%Y年%m月%d日 %H時%M分%S秒')}\"に参加。\"{member.created_at.strftime('%Y年%m月%d日 %H時%M分%S秒')}\"にアカウント作成。")
        member_join_embed.set_author(name=f"{member.name}", url="httpLINK", icon_url="httpICON")




    @client.event
    # 招待リンク作成時イベント
    async def on_invite_create(invite):
        if invite.inviter.bot:
            return
        print(console_prefix,f"received invite create event: {invite}")
        invite_log_embed = discord.Embed(title="Invite create event",url=f"{invite}", description=" ", color=0xffb3e3)
        invite_log_embed.add_field(name="URL: ",value=f"{invite}",inline=False)
        invite_log_embed.add_field(name="Author: ",value=f"<@{invite.inviter.id}>",inline=False)
        invite_log_embed.add_field(name="Attributes: ",value=f"maxAge: {invite.max_age}, maxUses: {invite.max_uses}",inline=False)
        await client.get_channel(998970705527984269).send(embed=invite_log_embed)



    @client.event
    # リアクション追加イベント
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        print(console_prefix,f"received Reaction add event: {user}")
        reaction_add_embed = discord.Embed(title="Reaction add event",url=f"https://discord.com/channels/{guild_id}/{reaction.message.channel.id}/{reaction.message.id}/",description=f"{reaction.emoji} by<@{user.id}> total: {reaction.count}",color=0xffcc44)
        await client.get_channel(998970570928554095).send(embed=reaction_add_embed)
        if reaction.count == 5 and reaction.message.guild.id == int(guild_id):
            global latest_reactioned_message_id
            if reaction.message.id == latest_reactioned_message_id:
                pass
            latest_reactioned_message_id = reaction.message.id
            print(console_prefix,"received 5 reactioned message")
            reactioned_5_embed = discord.Embed(title="話題の話題だ！",url=f"{reaction.message.jump_url}",description=f"{reaction.emoji}by <@{user.id}>")
            reactioned_5_embed.set_author(icon_url=f"{user.avatar.url}",name=f"{user}")
            await kanb_room.send(embed=reactioned_5_embed)
        if (reaction.message.id == latest_actioned_brocked_word_id) and (reaction.emoji == "❗"):
            brocked_word_description_embed = discord.Embed(title="メッセージが記録されています",description=f"該当のメッセージには禁止されたワードが含まれている可能性があるため記録されています",color=0x4444ff)
            await reaction.message.channel.send(embed=brocked_word_description_embed)

    @client.event
    # リアクション削除イベント
    async def on_reaction_remove(reaction, user):
        if user.bot:
            return
        print(console_prefix,f"received Reaction remove event: {user}")
        reaction_remove_embed = discord.Embed(title="Reaction remove event",url=f"https://discord.com/channels/{guild_id}/{reaction.message.channel.id}/{reaction.message.id}/",description=f"{reaction.emoji} by<@{user.id}> total: {reaction.count}",color=0xccff44)
        await client.get_channel(998970570928554095).send(embed=reaction_remove_embed)





    @client.event
    # スレッド作成イベント
    async def on_thread_create(thread):
        print(console_prefix,f"received Thread create event: {thread.name}")
        thread_create_event = discord.Embed(title="Thread create event", url=f"{thread.jump_url}")
        await client.get_channel(998970705527984269).send(embed=thread_create_event)





    @client.event
    # AutoModルール作成イベント
    async def on_automod_rule_create(rule):
        print(console_prefix,f"received AutoMod rule create event: {rule.name}")
        automod_rule_create_embed = discord.Embed(title="AutoMod rule create event",description=f"{rule.name}")
        automod_rule_create_embed.add_field(name="trigger: ",value=f"{rule.trigger}",inline=False)
        automod_rule_create_embed.add_field(name="actions: ",value=f"{rule.actions}",inline=False)
        automod_rule_create_embed.add_field(name="creator: ",value=f"<@{rule.creator_id}>")
        await client.get_channel(998970705527984269).send(embed=automod_rule_create_embed)
    # 接続
    client.run(bot_token)
# エラー(例外)発生時
except Exception as e:
    now = datetime.datetime.now()
    error_log_url = "https://discord.com/api/webhooks/1004379654406275072/aaaaaaaaaaaaaaaaaaaaaaaaaa"
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
