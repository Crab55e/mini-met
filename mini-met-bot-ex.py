# initial
import ctypes

ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11),0x0007)

def printe(content,mode = None,label = None):
    if label != None and mode == None:
        print(f"\033[092m[MM.{label}] {content}\033[0m")
        return
    if mode != None:
        mode = mode.lower()
        match mode:
            case "error":
                color = "\033[091m"
                mode_text = "Error"
            case "info":
                color = "\033[092m"
                mode_text = "Info"
            case "warn":
                color = "\033[093m"
                mode_text = "Warn"
            case "debug":
                color = "\033[094m"
                mode_text = "Debug"
            case _:
                print("Error on printe()\nmode option is not matched value: ",mode)
    if label != None and mode != None:
        print(f"{color}[MM.{label}.{mode_text}] {content}\033[0m")
        return
    if mode != None and label == None:
        print(f"{color}[MM.{mode_text}] {content}\033[0m")
        return
    print(f"\033[092m[MM] {content}\033[0m")

printe("Loading...")



# libraries
import asyncio
import discord
import json
import os
import psutil
import random
import re
import requests
import shutil
import sys

from datetime import datetime as dt
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from time import sleep



# variables
intents = discord.Intents.all()
client = discord.Client(intents=intents)

global_chat_data = open("storage/json/global_chat.json","r",encoding="utf-8")
global_chat_data = json.load(global_chat_data)
brocked_words = open("storage/json/brocked_words.json","r",encoding="utf-8")
brocked_words = json.load(brocked_words)
strftime_arg = "%Y-%m-%d %H:%M.%S"
already_one_time_executed = False
latest_temp_datas = {
    "actioned_brocked_word_message_id":0,
    "reactioned_message_id":0,
    "received_dm_user_id":796350579286867988
}
last_actioned_times = {
    "dayone_msg": dt.now()
}

admin_ids = [
        776726560929480707,
        967372572859695184,
        632596386772287532,
        661416929168457739,
        796350579286867988,
        775952326493863936,
        628513445964414997,
        839884489424502855,
        964438295440396320,
        895267282413039646,
        527514813799333889,
        891337046239625306
    ]



# constant
BOT_TOKEN = "ﾄｹﾝｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯ"
METS_SERVER_ID = 842320961033601044
MINI_MET_ID = 985254515798327296
AUTH_IMAGE_FONT = ImageFont.truetype("C:/Windows/Fonts/NotoSerifJP-ExtraLight.otf", 100)
AUTH_IMAGE_RAW = Image.open("storage/images/auth/raw.png")
LOG_CHANNEL_IDS = {
    "member_joining_leaving": 998970295350206596,
    "message_events": 998970570928554095,
    "member_events": 998970739879329882,
    "bot_log": 965269631050862622,
    "server_events": 998970705527984269,
    "auto_moderations": 998970821232037991,
    "voice_events": 1015499859945607228
}

# functions
def seconds_to_string(seconds: int = 0, outstr: str = "%wweeks, %ddays %h:%m.%s"):
    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    if seconds >= 604800:
        while seconds >= 604800:
            seconds = seconds - 604800
            weeks = weeks + 1
    if seconds >= 86400:
        while seconds >= 86400:
            seconds = seconds - 86400
            days = days + 1
    if seconds >= 3600:
        while seconds >= 3600:
            seconds = seconds - 3600
            hours = hours + 1
    if seconds >= 60:
        while seconds >= 60:
            seconds = seconds - 60
            minutes = minutes + 1
    result = outstr.replace("%w",str(weeks)).replace("%d",str(days)).replace("%h",str(hours)).replace("%m",str(minutes)).replace("%s",str(seconds))
    return result




class MiniMet(discord.Client):

    async def on_ready(self):
        global already_one_time_executed
        printe(f"{client.user.name} is Ready!!!",label="Event")
        printe(f"at {dt.now().strftime(strftime_arg)}")
        if already_one_time_executed == False:
            await tree.sync()
            already_one_time_executed = True
        await client.change_presence(activity=discord.Game(name=f"/help | mets-svr.com/mini-met | i\'m mini-met!"))

    async def on_message(self, m: discord.Message):
        if m.author.id == MINI_MET_ID:
            return
        global brocked_words
        global latest_temp_datas
        try:
            printe(f"message: \"{m.clean_content}\" by @{m.author}, in #{m.channel.name}",label="Event")
        except AttributeError:
            # On DM Message
            printe(f"message: \"{m.clean_content}\" by @{m.author}, in DMChannel",label="Event")
            if m.content.startswith("!sc"):
                printe(f"catched command in DM: {m.content}",label="DMCmd")

                # ↓ admin only
                for admin_id in admin_ids:
                    if m.author.id != admin_id:
                        printe("Author isn't Admin.",label="DMCmd")
                        return
                printe("Author is admin.",label="Bword")
                if m.content.startswith("!sc bword add "):
                    target_message = m.content.lstrip("!sc bword add ")
                    try:
                        bword_temp_r = open("storage/json/brocked_words.json","r",encoding="utf-8")
                        bword_temp_r = json.load(bword_temp_r)
                        bword_temp_r.append(target_message)
                        bword_temp_r = json.dumps(bword_temp_r)
                        bword_temp_w = open("storage/json/brocked_words.json","w",encoding="utf-8")
                        bword_temp_w.write(bword_temp_r)
                        bword_temp_w.close()
                        bword_appended_embed = discord.Embed(title=f"\"{target_message}\" をワードフィルターに追加しました").set_footer(text="DM Channel Commands")
                        await m.author.send(embed=bword_appended_embed)
                        await client.get_channel(LOG_CHANNEL_IDS["bot_log"]).send(embed=bword_appended_embed)
                    except Exception as e:
                        await client.get_channel(LOG_CHANNEL_IDS["bot_log"]).send(f"Appending blocked word Exception in DMChannel:\n{e}")
                    return

                if m.content.startswith("!sc bword remove "):
                    target_message = m.content.lstrip("!sc bword remove ")
                    try:
                        bword_temp_r = open("storage/json/brocked_words.json","r",encoding="utf-8")
                        bword_temp_r = json.load(bword_temp_r)
                        bword_temp_r.remove(target_message)
                        bword_temp_r = json.dumps(bword_temp_r)
                        bword_temp_w = open("storage/json/brocked_words.json","w",encoding="utf-8")
                        bword_temp_w.write(bword_temp_r)
                        bword_temp_w.close()
                        bword_removed_embed = discord.Embed(title=f"\"{target_message}\" をワードフィルターから削除しました").set_footer(text="DM Channel Commands")
                        await m.author.send(embed=bword_removed_embed)
                        await client.get_channel(LOG_CHANNEL_IDS["bot_log"]).send(embed=bword_removed_embed)
                    except Exception as e:
                        await client.get_channel(LOG_CHANNEL_IDS["bot_log"]).send(f"Removing blocked word Exception in DMChannel:\n{e}")
                    return

                return
            # talker
            if m.author.id != latest_temp_datas["received_dm_user_id"]:
                await client.get_channel(1065610631618764821).send(embed=discord.Embed().set_author(name=f"DMの送信先が{m.author}に変更されました",icon_url=m.author.avatar.url))
            dm_channel_embed = discord.Embed(description=f"{m.content}")
            dm_channel_embed.set_author(name=m.author,icon_url=m.author.avatar.url)
            dm_channel_embed.set_footer(text=f"at: {dt.now().strftime(strftime_arg)}, Connecting ID: {m.author.id}")
            await client.get_channel(1065610631618764821).send(embed=dm_channel_embed)
            latest_temp_datas["received_dm_user_id"] = m.author.id
            return
        if m.author.id != 985254515798327296 and not m.content.startswith("!sc") and m.guild.id == 842320961033601044:
            for brocked_word in brocked_words:
                if brocked_word in m.content:
                    printe(f"Detected brocked word: {m.content}",label="Bword")
                    brocked_word_embed = discord.Embed(title="ワードフィルタにかかるメッセージを検知しました",url=f"{m.jump_url}",description=f"チャンネル: <#{m.channel.id}>\nユーザー: <@{m.author.id}>")
                    brocked_word_embed.set_author(icon_url=f"{m.author.avatar.url}",name=f"{m.author}")
                    brocked_word_embed.set_footer(text=f"MId: {m.id} ,ChId: {m.channel.id} ,At: {dt.now().strftime(strftime_arg)}")
                    brocked_word_embed.add_field(name="メッセージ",value=f"{m.content}")
                    await client.get_channel(LOG_CHANNEL_IDS["auto_moderations"]).send(embed=brocked_word_embed)
                    await m.add_reaction("❗")
                    latest_temp_datas["actioned_brocked_word_message_id"] = m.id
                    await asyncio.sleep(5)
                    await m.remove_reaction("❗",discord.Object(MINI_MET_ID))
        if m.author.bot:
            return

        if m.content.startswith("!sc bword",0) and m.channel.id == 1011965676962984047:
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

            # リロード コマンド
            if m.content == "!sc reload":
                await m.channel.send("再読み込み中...")
                brocked_words = open("storage/json/brocked_words.json","r",encoding="utf-8")
                brocked_words = json.load(brocked_words)
                await m.channel.send("変数が更新されました")

        if re.match("\<\@\d*\>",m.content):
            printe("Received mention message",label="MentionLog")
            mention_embed = discord.Embed(title="mention message log", url=m.jump_url, description=" ", color=0xffd152)
            mention_embed.add_field(name="content: ", value=f"{m.content}", inline=False)
            await client.get_channel(LOG_CHANNEL_IDS["message_events"]).send(embed=mention_embed)

        # メンションコマンド
        if m.content.startswith("<@985254515798327296>"):
            if m.content.startswith("<@985254515798327296> "):
                command = m.content.lstrip("<@985254515798327296> ")
            elif m.content.startswith("<@985254515798327296>"):
                command = m.content.lstrip("<@985254515798327296>")
            printe(f"received Mention Command: {command}",label="MentionCmd")
            await asyncio.sleep(.2)

            if command == "サイコロ振って":
                async with m.channel.typing():
                    temp_rn = random.randrange(1,6)
                await m.channel.send(f"{temp_rn}!")
                return
            elif command == "今のドル円教えて":
                async with m.channel.typing():
                    dolyen_rate = "https://www.gaitameonline.com/rateaj/getrate"
                    dolyen_rate = requests.get(dolyen_rate)
                    dolyen_rate = dolyen_rate.json()
                    dolyen_rate = dolyen_rate["quotes"][20]
                    dolyen_rate_embed = discord.Embed(title=f"{dolyen_rate['currencyPairCode']}",description=f"High: {dolyen_rate['high']}\nLow: {dolyen_rate['low']}")
                await m.channel.send(embed=dolyen_rate_embed)
                return
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
                try:
                    jma_data = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{areacode}.json"
                    jma_data = requests.get(jma_data).json()
                    jma_data = jma_data[0]
                except Exception as e:
                    printe(f"Exception at get weather data: {e}",mode="error")
                    await m.channel.send(embed=discord.Embed(color=0xff0000,title="内部エラーによりデータの取得に失敗しました"))
                    await client.get_channel(965269631050862622).send(content=f"Get Weather Exception:\n{e}")
                    return
                weather_info_embed_title = discord.Embed(color=0xcccccc,title=f"天気by気象庁",url="https://www.jma.go.jp/jma/",description=f'{jma_data["publishingOffice"]} | {jma_data["reportDatetime"]}')

                weather_info_embed_weather = discord.Embed(color=0xff8888,title=f"天気",description=f'`{jma_data["timeSeries"][0]["timeDefines"][1]}`')
                try:
                    for weather in jma_data["timeSeries"][0]["areas"]:
                        weather_info_embed_weather.add_field(inline=False,name=f'エリア: {weather["area"]["name"]}',value=f'**天気**: {weather["weathers"][1].replace("　","")}\n**風**: {weather["winds"][1].replace("　","")}\n**波**: {weather["waves"][1].replace("　","")}')
                except Exception as e:
                    printe(f"Exception! It\'s keyerror of \"waves\"?\n{e}","error")
                    for weather in jma_data["timeSeries"][0]["areas"]:
                        weather_info_embed_weather.add_field(inline=False,name=f'エリア: {weather["area"]["name"]}',value=f'**天気**: {weather["weathers"][1].replace("　","")}\n**風**: {weather["winds"][1].replace("　","")}')

                        weather_info_embed_rainluck = discord.Embed(color=0x88ff88,title=f"降水確率",description=f'`{jma_data["timeSeries"][1]["timeDefines"][1]}`')
                        for rainluck in jma_data["timeSeries"][1]["areas"]:
                            weather_info_embed_rainluck.add_field(name=f'エリア: {rainluck["area"]["name"]}',value=f'{rainluck["pops"][1]}%')

                        weather_info_embed_temp = discord.Embed(color=0x8888ff,title=f"気温",description=f'`{jma_data["timeSeries"][1]["timeDefines"][0]}` ～ `{jma_data["timeSeries"][1]["timeDefines"][1]}`')
                        for area in jma_data["timeSeries"][2]["areas"]:
                            weather_info_embed_temp.add_field(name=f'エリア: {area["area"]["name"]}',value=f'最低気温: {area["temps"][0]}\n最高気温: {area["temps"][1]}')
            await m.channel.send(embeds=[weather_info_embed_title,weather_info_embed_weather,weather_info_embed_rainluck,weather_info_embed_temp])
            return

        if "<@985254515798327296>" in m.content:
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,3))
            await m.channel.send("</help:1063776235156672632>でコマンドのヘルプを表示できるよ")
            return

        if m.channel.id == 1065610631618764821:
            await client.get_user(latest_temp_datas["received_dm_user_id"]).send(m.content)
            return

    ### 生きるこめたん
        if re.match("(子met|小met)",m.content):
            printe(f"Received message in MyName :D")
            if m.author.top_role.id == 844359217984700446 or m.author.top_role.id == 1020521550945996900:
                await m.channel.send("お呼びでしょうか？")
            else:
                await m.channel.send("呼んだ？")

        if re.match("(heyかに|おいに！|heyかにさん！|heyカニさん！|heyかにさん|heyカニさん|かにさん！|カニさん！)",m.content):
            printe("Calling to Crab55e")
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            if re.match("(heyかに|heyカニ|heyかにさん|heyカニさん)",m.content):
                async with m.channel.typing():
                    await asyncio.sleep(1)
                await m.channel.send(random.choice(["<@776726560929480707> 呼ばれてるよ～","<@776726560929480707> よばれてるよ～～"]))
            elif m.content == "おいに！":
                await m.channel.send("<@776726560929480707> おい！！！")
            else:
                m.channel.send("<@776726560929480707> おーい")

        if re.match("(おはよう|おはようございます|おはようございます！|おはようございます～|おはよう！|おはよう～|ohayou|oha|ohayou!|おはようです|おはようです～|おはようです！|おはようです！！|おはようです～～)",m.content):
            printe(f"Received morning message")
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            if m.author.top_role.id == 844359217984700446 or m.author.top_role.id == 1020521550945996900:
                await m.channel.send("おはようございます")
            else:
                await m.channel.send(random.choice(["おはよ～～","おはよう～","おはよう～～","おは"]))

        if m.content.endswith("ｗ") or m.content.startswith("w"):
            temp_rn = random.randrange(1,3)
            if temp_rn == 1:
                async with m.channel.typing():
                    await asyncio.sleep(random.uniform(1,2))
            if m.content.endswith("www") or m.content.endswith("ｗｗｗ"):
                await m.channel.send("wwww")

            elif m.content.endswith("ww") or m.content.endswith("ｗｗ"):
                await m.channel.send("ww")

            elif m.content.endswith("w") or m.content.endswith("ｗ"):
                await m.channel.send("w")

        if m.content == "がんば":
            await asyncio.sleep(1.5)
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            await m.channel.send("がんば")

        if "なす" in m.content:
            temp_rn = random.randrange(1,10)
            if temp_rn == 1:
                async with m.channel.typing():
                    await asyncio.sleep(random.uniform(1,3))
                temp_rn = random.randrange(1,50)
                if temp_rn == 1:
                    await m.reply(content="なす？\nhttps://cdn.discordapp.com/attachments/845185615678144532/1060025135735771176/IMG_1150.png",mention_author=False)
                else:
                    await m.reply("なす？\nhttps://media.discordapp.net/attachments/1055151855950372874/1055756068728361010/image.gif",mention_author=False)

        if "バイオハザード" in m.content:
            temp_rn = random.randrange(1,4)
            if temp_rn == 1:
                async with  m.channel.typing():
                    await asyncio.sleep(random.randrange(1,2))
                await m.reply("バイアハザードね？",mention_author=False)

        if "hyocei" in m.content:
            temp_rn = random.randrange(1,3)
            if temp_rn == 1:
                async with m.channel.typing():
                    await asyncio.sleep(random.uniform(1,2))
                await m.channel.send("Hyocei最強！")
        if m.content == "!sc cae tree.sync()" and m.author.id == 776726560929480707:
            printe("Sync...",label="Inter")
            await tree.sync()
            await m.channel.send("executed:",{m.content.lstrip("!sc crab-execute ")})

    async def on_invite_create(self, invite: discord.Invite):
        if invite.channel.name:
            printe(f"Invite Created by {invite.inviter} to {invite.channel.name}",label="Event")
        elif invite.guild.name:
            printe(f"Invite Created by {invite.inviter} to {invite.guild.name}",label="Event")
        invite_create_embed = discord.Embed(title="Invite Create Event",url=invite.url,description=f"```{invite.url}```")
        invite_create_embed.set_author(name=invite.inviter,icon_url=invite.inviter.avatar.url)
        invite_create_embed.set_footer(text=f"at: {dt.now().strftime(strftime_arg)}")
        invite_create_embed.add_field(name="Inviter",value=invite.inviter.mention)
        invite_create_embed.add_field(name="Max uses",value=str(invite.max_uses))
        invite_create_embed.add_field(name="Max age",value=seconds_to_string(invite.max_age,"%w週間, %d日 %h時間%m分 %s秒"))
        invite_create_embed.add_field(name="Temporary member",value=str(invite.temporary))
        await client.get_channel(LOG_CHANNEL_IDS["server_events"]).send(embed=invite_create_embed)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        printe(f"Reaction added by {user}",label="Event")
        reaction_add_embed = discord.Embed(title="Reaction add event",url=reaction.message.jump_url,description=f"{reaction.emoji} by<@{user.id}> total: **{reaction.count}**")
        reaction_add_embed.set_author(name=user,icon_url=user.avatar.url)
        await client.get_channel(LOG_CHANNEL_IDS["message_events"]).send(embed=reaction_add_embed)

        if reaction.count == 5 and reaction.message.guild.id == 842320961033601044:
            printe("Received over 5 reactioned message")
            reactioned_5_embed = discord.Embed(title="話題の話題だ！",url=f"{reaction.message.jump_url}",description=f"{reaction.emoji}by <@{user.id}>")
            reactioned_5_embed.set_author(icon_url=f"{user.avatar.url}",name=f"{user}")
            # it's channel is kanb-room
            await client.get_channel(966297997216448512).send(embed=reactioned_5_embed)
            return

        if (reaction.message.id == latest_temp_datas["actioned_brocked_word_message_id"]) and (reaction.emoji == "❗"):
            brocked_word_description_embed = discord.Embed(title="メッセージが記録されています",description=f"該当のメッセージには禁止されたワードが含まれている可能性があるため記録されています",color=0x4444ff)
            await reaction.message.channel.send(embed=brocked_word_description_embed)
            latest_temp_datas["actioned_brocked_word_message_id"] = None

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        printe(f"Reaction removed by {user}",label="Event")
        reaction_add_embed = discord.Embed(title="Reaction remove event",url=reaction.message.jump_url,description=f"{reaction.emoji} by<@{user.id}> total: **{reaction.count}**")
        reaction_add_embed.set_author(name=user,icon_url=user.avatar.url)
        await client.get_channel(LOG_CHANNEL_IDS["message_events"]).send(embed=reaction_add_embed)

    async def on_app_command_completion(self, interaction: discord.Interaction, command: discord.app_commands.Command):
        printe(f"{interaction.user} issued command: /{command.qualified_name}")
        app_command_completion_embed = discord.Embed(title=f"{interaction.user.display_name} issued command: /{command.qualified_name}",description=f"")
        app_command_completion_embed.set_author(name=interaction.user,icon_url=interaction.user.avatar.url)
        app_command_completion_embed.set_footer(text=f"at: {dt.now().strftime(strftime_arg)}, uid: {interaction.user.id}")
        await client.get_channel(LOG_CHANNEL_IDS["message_events"]).send(embed=app_command_completion_embed)

    async def on_member_join(self, member: discord.Member):
        printe(f"Member joined: {member}, to {member.guild.name}",label="Event")

client = MiniMet(intents=intents)
tree = app_commands.CommandTree(client=client)



@tree.command()
async def help(interaction: discord.Interaction):
    help_embed=discord.Embed()
    help_embed.add_field(name="これ。", value="</help:1063776235156672632>", inline=False)
    help_embed.add_field(name="サーバーのIPなどを表示", value="</status:1063778904533385306>", inline=False)
    help_embed.add_field(name="サーバーの招待リンクを取得", value="</invite:1063779546949767219>", inline=False)
    help_embed.add_field(name="サーバーのwebリンクを表示", value="</web:1063780119430312017>", inline=False)
    help_embed.add_field(name="サーバーの参加者を確認", value="`!sc list`(<#845185615678144532>でのみ動作)", inline=False)
    help_embed.add_field(name="サーバーのマップのリンクを確認", value="</map:1063780759552405544>", inline=False)
    await interaction.response.send_message(embed=help_embed)

@tree.command()
async def status(interaction: discord.Interaction):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory()
    status_embed=discord.Embed(title="ステータス", description="IPやバージョン等の情報", color=0x6f5134)
    status_embed.add_field(name="Java Edition - IP", value="`mets.feathermc.gg`", inline=False)
    status_embed.add_field(name="Bedrock Edition - IP", value="`hot.ssnetwork.io`", inline=False)
    status_embed.add_field(name="Bedrock Edition - Port", value="`48718`")
    status_embed.add_field(name="CPU Usage",value=f"{cpu_usage}%", inline=False)
    status_embed.add_field(name="Memory Usage",value=f"{memory_usage.percent}%")
    status_embed.set_footer(text="ver:1.19.3, 情報更新: 2023/01/27")
    await interaction.response.send_message(embed=status_embed)

@tree.command()
async def invite(interaction: discord.Interaction):
    invite_embed = discord.Embed(title="招待リンク",description="サーバーの招待リンクです\nいろんなところ共有してください！\n**```https://discord.mets-svr.com```**",color=0x22ff22)
    view = discord.ui.View().add_item(discord.ui.Button(label='招待リンク', url='https://discord.mets-svr.com/'))
    await interaction.response.send_message(view=view,embed=invite_embed)

@tree.command()
async def web(interaction: discord.Interaction):
    web_embed = discord.Embed(title="webサイト",description="サーバーの公式webサイトです\n更新がめんどくてめんどくて...\n**```https://mets-svr.com```**",color=0x22ff22)
    view = discord.ui.View().add_item(discord.ui.Button(label='webサイト', url='https://mets-svr.com/'))
    await interaction.response.send_message(view=view,embed=web_embed)

@tree.command()
async def map(interaction: discord.Interaction):
    web_embed = discord.Embed(title="マップ",description="サーバーのマップです\n空からワールドを眺めたりできます\n動作していないこともあります...\n**```https://mets-svr.com/map```**",color=0x22ff22)
    view = discord.ui.View().add_item(discord.ui.Button(label='マップ', url='https://mets-svr.com/map'))
    await interaction.response.send_message(view=view,embed=web_embed)

@tree.command()
async def dayone(interaction: discord.Interaction):
    printe(f"issued /dayone command by @{interaction.user}")
    await interaction.response.send_message(content="\:D",ephemeral=True)
    event_channel_id = interaction.channel.id
    async with interaction.channel.typing():
        await asyncio.sleep(random.uniform(1,2))
    await client.get_channel(event_channel_id).send("だよね！！！")

@tree.context_menu()
async def dayone_msg(interaction: discord.Interaction, message: discord.Message):
    if last_actioned_times["dayone_msg"].second == dt.now().second:
        return
    async with message.channel.typing():
        await asyncio.sleep(random.uniform(0.1,1))
    if re.match("(死ね|嫌い)",message.content):
        await message.reply("？",mention_author=False)
    else:
        await message.reply("だよね！！！！",mention_author=False)
    last_actioned_times["dayone_msg"] = dt.now()
    await interaction.response.send_message(content="\:D",ephemeral=True)

client.run(token=BOT_TOKEN)
