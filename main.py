# initial
import ctypes

ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11),0x0007)

def printe(content,mode: str = None,label: str = None):
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
import subprocess
import MeCab

from datetime import datetime as dt
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from typing import Union, Optional, Any
from time import sleep
from googletrans import Translator
from multiprocessing import Process
from mcclient import SLPClient



# variables
intents = discord.Intents.all()
client = discord.Client(intents=intents)

global_chat_data = open("storage/json/global_chat.json","r",encoding="utf-8")
global_chat_data = json.load(global_chat_data)
brocked_words = open("storage/json/brocked_words.json","r",encoding="utf-8")
brocked_words = json.load(brocked_words)
STRFTIME_ARG = "%Y-%m-%d %H:%M.%S"
already_one_time_executed = False
nasu_regex = "(、|。|ﾟ|゜|゛|”|\"|a|A|ａ|n|N|ｎ|s|S|ｓ|t|T|u|U|ｕ|す|ス|ｽ|っ|ッ|つ|ツ|ｯ|な|ナ|ﾅ|🍆)*"
latest_temp_datas = {
    "actioned_brocked_word_message_id":0,
    "reactioned_message_id":0,
    "received_dm_user_id":776726560929480707,
    "openable_discord_message_link":0,
    "ikaf_generic_disclaimer":0
}
last_actioned_times = {
    "dayone_msg": dt.now()
}
create_select_menu_selected_roles = {"users":{}}

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
BOT_TOKEN = "ﾄｹﾝｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯ"
METS_SERVER_ID = 842320961033601044
MINI_MET_ID = 985254515798327296
CRAB55E_DISCORD_USER_ID = 776726560929480707
THEME_COLOR_HEX = 0x3da45d
STRFTIME_ARG = "%Y-%m-%d %H:%M.%S"
AUTH_IMAGE_FONT = ImageFont.truetype("C:/Windows/Fonts/NotoSerifJP-ExtraLight.otf", 100)
AUTH_IMAGE_RAW = Image.open("storage/images/auth/raw.png")
NOT_MENTIONABLE = discord.AllowedMentions.none()
CHANNEL_IDS = {
    "member_joining_leaving": 1074249512605986836,
    "message_events": 1074249514065596446,
    "member_events": 1074249515554582548,
    "bot_log": 1074249516871602227,
    "server_events": 1074249522215137290,
    "auto_moderations": 1074249523423105035,
    "voice_events": 1074249525117603860,
    "report_datas": 1017828972240838745,
    "shiritori_channel":999269935370997761,
    "self_introduction":949994602427994113
}
HTTP_AUTHORIZATION_HEADERS = {"Authorization":f"Bot {BOT_TOKEN}"}
SERVER_ADDRESSES = {
    "bedrock": {
        "ip": "join.mets-svr.com",
        "port": "19132"
    },
    "java": {
        "ip": "join.mets-svr.com",
        "port": "25565"
    }
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

def remove_prefix_string(string: str = None, prefix: str = "!") -> str:
    if string.startswith(prefix):
        while string.startswith(prefix):
            string = string.lstrip(prefix)
        return string
    else:
        return string

def zorome_check(number: int, include_single_digit: Optional[bool] = False) -> bool:
    if include_single_digit == False:
        return len(set(int(c) for c in str(number))) == 1 and len(str(number)) != 1
    else:
        return len(set(int(c) for c in str(number))) == 1
    return False

class RolePanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="",emoji="🔉",style=discord.ButtonStyle.green, custom_id="role_panel:allow_notify")
    async def allow_notify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = client.get_guild(METS_SERVER_ID).get_role(1074249437305643070)
        member = client.get_guild(METS_SERVER_ID).get_member(interaction.user.id)
        if role in member.roles:
            await member.remove_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を剥奪しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )
        else:
            await member.add_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を付与しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )

    @discord.ui.button(label="",emoji="🚀",style=discord.ButtonStyle.green, custom_id="role_panel:bump_up")
    async def bump_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = client.get_guild(METS_SERVER_ID).get_role(1074249438928838707)
        member = client.get_guild(METS_SERVER_ID).get_member(interaction.user.id)
        if role in member.roles:
            await member.remove_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を剥奪しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )
        else:
            await member.add_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を付与しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )

    @discord.ui.button(label="",emoji="☎️",style=discord.ButtonStyle.green, custom_id="role_panel:dm_ok")
    async def dm_ok(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = client.get_guild(METS_SERVER_ID).get_role(1074249435179122708)
        member = client.get_guild(METS_SERVER_ID).get_member(interaction.user.id)
        if role in member.roles:
            await member.remove_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を剥奪しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )
        else:
            await member.add_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を付与しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )

    @discord.ui.button(label="",emoji="🔉",style=discord.ButtonStyle.green, custom_id="role_panel:dm_ng")
    async def dm_ng(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = client.get_guild(METS_SERVER_ID).get_role(1074249436311584818)
        member = client.get_guild(METS_SERVER_ID).get_member(interaction.user.id)
        if role in member.roles:
            await member.remove_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を剥奪しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )
        else:
            await member.add_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を付与しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )

    @discord.ui.button(label="",emoji="💻",style=discord.ButtonStyle.green, custom_id="role_panel:java")
    async def java(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = client.get_guild(METS_SERVER_ID).get_role(1074249427050561556)
        member = client.get_guild(METS_SERVER_ID).get_member(interaction.user.id)
        if role in member.roles:
            await member.remove_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を剥奪しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )
        else:
            await member.add_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を付与しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )

    @discord.ui.button(label="",emoji="📱",style=discord.ButtonStyle.green, custom_id="role_panel:bedrock")
    async def bedrock(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = client.get_guild(METS_SERVER_ID).get_role(1074249428581490789)
        member = client.get_guild(METS_SERVER_ID).get_member(interaction.user.id)
        if role in member.roles:
            await member.remove_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を剥奪しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )
        else:
            await member.add_roles(role, reason="toggled role by role-panel")
            await interaction.response.send_message(f"{role.mention}を付与しました",
            ephemeral=True,
            delete_after=1.5,
            allowed_mentions=NOT_MENTIONABLE
            )

class ConfirmCloseWelcomeChannel(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="閉じる", style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete(reason=f"Closed welcome-channel by {interaction.user}")

class CloseWelcomeChannel(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="このチャンネルを閉じる", style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="閉じても大丈夫ですか？",
            description="""
この操作を取り消すことはできません
その後もし何か困ったことがあれば<#1074249460051353620>、または<@&1074249415679815780>のメンバーへ相談してください
"""[1:-1],
            color=0xff2222
)
        await interaction.response.send_message(embed=embed, view=ConfirmCloseWelcomeChannel())
class MiniMet(discord.Client):
    async def setup_hook(self) -> None:
        self.add_view(RolePanel())

    async def on_ready(self):
        global already_one_time_executed
        printe(f"{client.user.name} is Ready!!!",label="Event")
        printe(f"at {dt.now().strftime(STRFTIME_ARG)}")
        # if already_one_time_executed == False:
        #     await tree.sync()
        #     printe("executed sync.")
        #     already_one_time_executed = True
        await client.change_presence(activity=discord.Game(name=f"/help | mets-svr.com/mini-met | i\'m mini-met!"))

    async def on_dm_message(self, m: discord.Message):
        printe(f"dm message: \"{m.clean_content}\" by @{m.author}",label="Event")
        # talker
        if m.author.id != latest_temp_datas["received_dm_user_id"]:
            await client.get_channel(1065610631618764821).send(embed=discord.Embed().set_author(name=f"DMの送信先が{m.author}に変更されました",icon_url=m.author.display_avatar.url))
        dm_channel_embed = discord.Embed(description=f"{m.content}")
        dm_channel_embed.set_author(name=m.author,icon_url=m.author.display_avatar.url)
        dm_channel_embed.set_footer(text=f"at: {dt.now().strftime(STRFTIME_ARG)}, Connecting ID: {m.author.id}")
        await client.get_channel(1065610631618764821).send(embed=dm_channel_embed)
        latest_temp_datas["received_dm_user_id"] = m.author.id
        return

    async def on_message(self, m: discord.Message):
        global latest_temp_datas
        if m.author.id == MINI_MET_ID:
            return
        if not type(m.channel) == discord.channel.DMChannel:
            printe(f"message: \"{m.clean_content}\" by @{m.author}, in #{m.channel.name}",label="Event")
        else:
            await self.on_dm_message(m=m)
        if m.author.bot:
            return

        if re.match(r"(かに|kani|\:crab\:|crab)",m.content):
            await client.get_user(776726560929480707).send(
                embed=discord.Embed(
                    title="かにだ",
                    url=m.jump_url,
                    description=m.content
                ).set_author(
                        icon_url=m.author.display_avatar.url,
                        name=m.author.display_name
                )
            )
        if re.match(r"(かえ|加恵|カエ)",m.content):
            await client.get_user(940522481079451708).send(
                embed=discord.Embed(
                    title="かえだ",
                    url=m.jump_url,
                    description=m.content
                ).set_author(
                icon_url=m.author.display_avatar.url,
                name=m.author.display_name
                )
            )
        if m.content.startswith("!sc bword",0) and m.channel.id == 1074148934081073182:
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

        if re.match(r"\<\@\d*\>",m.content):
            printe("Received mention message",label="MentionLog")
            mention_embed = discord.Embed(title="mention message log", url=m.jump_url, description=" ", color=0xffd152)
            mention_embed.add_field(name="content: ", value=f"{m.content}", inline=False)
            await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=mention_embed)

        if re.match(r"https://(canary\.)?discord\.com/channels/\d*/\d*/\d*/?",m.content):
            printe("Messsage link in message content")
            latest_temp_datas["openable_discord_message_link"] = m.id
            await m.add_reaction("🔗")

        if re.match(r"https?://btnmaker\.me",m.content):
            await m.delete()

        if "ikafジェネリック免責事項" in m.content:
            latest_temp_datas["ikaf_generic_disclaimer"] = m.id
            await m.add_reaction("ℹ️")

        if m.channel.id == CHANNEL_IDS["self_introduction"]:
            for self_introduction_message_line in m.content.splitlines():
                if re.match(r"^(?i)(名前|MCID|ID|ゲーマータグ|((java edition|java|je)(/|\|| |　|または|か|／)(bedrock edition|bedrock|be|pocket edition|pe))(edition|プラットフォーム))",m.content):
                    await m.add_reaction(":thumbsup:")
                elif True:
                    pass
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
            elif command == "今のドル円教えて":
                async with m.channel.typing():
                    dolyen_rate = "https://www.gaitameonline.com/rateaj/getrate"
                    dolyen_rate = requests.get(dolyen_rate)
                    dolyen_rate = dolyen_rate.json()
                    dolyen_rate = dolyen_rate["quotes"][20]
                    dolyen_rate_embed = discord.Embed(title=f"{dolyen_rate['currencyPairCode']}",description=f"High: {dolyen_rate['high']}\nLow: {dolyen_rate['low']}")
                await m.channel.send(embed=dolyen_rate_embed)
            elif command.startswith("明日の") and command.endswith("の天気教えて"):
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
                    weather_info_embed_title = discord.Embed(
                        color=0xcccccc,title=f"天気by気象庁",
                        url="https://www.jma.go.jp/jma/",
                        description=f'{jma_data["publishingOffice"]} | {jma_data["reportDatetime"]}'
)
                    weather_info_embed_rainluck = discord.Embed(
                        color=0x88ff88,
                        title=f"降水確率",
                        description=f'`{jma_data["timeSeries"][1]["timeDefines"][1]}`'
)
                    weather_info_embed_weather = discord.Embed(
                        color=0xff8888,
                        title=f"天気",
                        description=f'`{jma_data["timeSeries"][0]["timeDefines"][1]}`'
)
                    weather_info_embed_temp = discord.Embed(
                        color=0x8888ff,title=f"気温",
                        description=f'`{jma_data["timeSeries"][1]["timeDefines"][0]}` ～ `{jma_data["timeSeries"][1]["timeDefines"][1]}`'
)
                    try:
                        for weather in jma_data["timeSeries"][0]["areas"]:
                            weather_info_embed_weather.add_field(
                                inline=False,
                                name=f'エリア: {weather["area"]["name"]}',
                                value=f'**天気**: {weather["weathers"][1].replace("　","")}\n**風**: {weather["winds"][1].replace("　","")}\n**波**: {weather["waves"][1].replace("　","")}'
)
                    except Exception as e:
                        printe(f"Exception! It\'s keyerror of \"waves\"?\n{e}","error")
                        for weather in jma_data["timeSeries"][0]["areas"]:
                            weather_info_embed_weather.add_field(
                                inline=False,
                                name=f'エリア: {weather["area"]["name"]}',
                                value=f'**天気**: {weather["weathers"][1].replace("　","")}\n**風**: {weather["winds"][1].replace("　","")}'
)

                        for rainluck in jma_data["timeSeries"][1]["areas"]:
                            weather_info_embed_rainluck.add_field(
                                name=f'エリア: {rainluck["area"]["name"]}',
                                value=f'{rainluck["pops"][1]}%'
)

                        for area in jma_data["timeSeries"][2]["areas"]:
                            weather_info_embed_temp.add_field(
                                name=f'エリア: {area["area"]["name"]}',
                                value=f'最低気温: {area["temps"][0]}\n最高気温: {area["temps"][1]}'
)
                await m.channel.send(embeds=[weather_info_embed_title,weather_info_embed_weather,weather_info_embed_rainluck,weather_info_embed_temp])

        if m.content == "<@985254515798327296>":
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,3))
            await m.channel.send("</help:1063776235156672632>でコマンドのヘルプを表示できるよ")
            return

        if m.channel.id == 1065610631618764821:
            await client.get_user(latest_temp_datas["received_dm_user_id"]).send(m.content)
            return

        with open("storage/json/gobis.json","r") as gobis_database:
            gobis_database = json.loads(gobis_database.read())
            

    ### 生きるこめたん
#         if m.channel.id == 1074045647390507149 and random.randrange(1,10) == 1:
#             async with m.channel.typing():
#                 await asyncio.sleep(1)
#             printe("Rinning...")
#             rinna_request_body = {
#     "rawInput": "",
#     "outputLength": 25
# }
#             rinna_request_body["rawInput"] = f"B: {m.content} A:"
#             rinna_request_header = {
#     "Content-Type": "application/json",
#     "Cache-Control": "no-cache",
#     "Ocp-Apim-Subscription-Key": "a6b45fdff3844ad2853a5311014c3280",
#     }
#             rinna_response = requests.post("https://api.rinna.co.jp/models/cce",headers=rinna_request_header, json=rinna_request_body)
#             await m.channel.send(json.loads(rinna_response.text)["answer"])
        if re.match(r"(子met|小met)",m.content):
            printe(f"Received message in MyName :D")
            if m.author.top_role.id == 844359217984700446 or m.author.top_role.id == 1020521550945996900:
                await m.channel.send("お呼びでしょうか？")
            else:
                await m.channel.send("呼んだ？")
        if "🥕" in m.content and m.guild.id == METS_SERVER_ID and m.author.id != 796350579286867988:
            with open("storage/json/ninjins.json", "r") as f:
                ninjins_json = json.load(f)
            ninjins_json["total_ninjins"] += m.content.count("🥕")
            ninjins_json["total_ninjin_messages"] += 1
            with open("storage/json/ninjins.json", "w") as f:
                json.dump(ninjins_json, f)
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            await m.channel.send("にんじんだぞ！！！！<@796350579286867988>")
        
        if re.fullmatch(r"(?i)(hey|おい)(かわ|kawa)(さん|san)?(!|！|~|～){1,10}?",m.content):
            if random.randrange(1,50) == 1:
                printe("Calling to Kawasan")
                async with m.channel.typing():
                    await asyncio.sleep(random.uniform(1,2))
                choiced_kawasan_mention = random.choice(["<@964438295440396320>","<@628513445964414997>"]) 
                await m.channel.send(f"{choiced_kawasan_mention} HEY")
        if re.fullmatch(r"(?i)(おい|hey)(かえ|加絵|カエ)(さん)?(!|！|~|～){1,10}?",m.content):
            printe("Calling to Kae")
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            await m.channel.send("助けてっ！かえぱんま～ん！！！！||<@940522481079451708>||")
        if re.fullmatch(r"(?i)(hey|oi|おい)(kani|ni|に|かに|カニ|蟹)(さん|san)?(!|！|~|～){1,10}?",m.content):
            printe("Calling to Crab55e")
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            if re.fullmatch(r"(?i)hey(kani|ni|かに|カニ|蟹)(san|さん)?(!|！|~|～){1,10}?",m.content):
                async with m.channel.typing():
                    await asyncio.sleep(1)
                await m.channel.send(random.choice(["<@776726560929480707> 呼ばれてるよ～","<@776726560929480707> よばれてるよ～～"]))
            elif m.content == "おいに！":
                await m.channel.send("<@776726560929480707> おい！！！")
            else:
                await m.channel.send("<@776726560929480707> おーい")

        if re.fullmatch(r"(おは|oha)(よう|よ|you|yo)?(ございます)?(なす|ナス|茄子|nasu)?！{1,10}?",m.content):
            printe(f"Received morning message")
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            if m.author.top_role.id == 844359217984700446 or m.author.top_role.id == 1020521550945996900:
                await m.channel.send("おはようございます")
            else:
                await m.channel.send(random.choice(["おはよ～～","おはよう～","おはよう～～","おは"]))

        if m.content.endswith("ｗ") or m.content.endswith("w"):
            temp_rn = random.randrange(1,3)
            if re.match(r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+",m.content):
                pass
            elif temp_rn == 1:
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

        if m.channel.id == CHANNEL_IDS["shiritori_channel"]:
            printe("answering shiritori...",label="Shiritori")
            with open("storage/json/shiritori.json", "r") as file:
                shiritori_end_character = m.content[-1]
                file = file.read()
                shiritori_database = json.loads(file)
                if True:
                    for hira_start_character in shiritori_database["hiraganas"]:
                        if shiritori_end_character == hira_start_character:
                            shiritori_answer = random.choice(shiritori_database["hiraganas"][hira_start_character])
                            await m.channel.send(shiritori_answer)
                            break
                    for kata_start_character in shiritori_database["katakanas"]:
                        if shiritori_end_character == kata_start_character:
                            shiritori_answer = random.choice(shiritori_database["katakanas"][kata_start_character])
                            await m.channel.send(shiritori_answer)
                            break
                with open("storage/json/shiritori.json", "w") as file_writeable:
                    for hira_start_character in shiritori_database["hiraganas"]:
                        if shiritori_end_character == hira_start_character:
                            shiritori_database["hiraganas"][hira_start_character].append(m.content)
                    for kata_start_character in shiritori_database["katakanas"]:
                        if shiritori_end_character == kata_start_character:
                            shiritori_database["katakanas"][kata_start_character].append(m.content)
                    json.dump(shiritori_database, file_writeable)
                    file_writeable.close()


    async def on_invite_create(self, invite: discord.Invite):
        if invite.channel.name:
            printe(f"Invite Created by {invite.inviter} to {invite.channel.name}",label="Event")
        elif invite.guild.name:
            printe(f"Invite Created by {invite.inviter} to {invite.guild.name}",label="Event")
        invite_create_embed = discord.Embed(title="Invite Create Event",url=invite.url,description=f"```{invite.url}```")
        invite_create_embed.set_author(name=invite.inviter,icon_url=invite.inviter.display_avatar.url)
        invite_create_embed.set_footer(text=f"at: {dt.now().strftime(STRFTIME_ARG)}")
        invite_create_embed.add_field(name="Inviter",value=invite.inviter.mention)
        invite_create_embed.add_field(name="Max uses",value=str(invite.max_uses))
        invite_create_embed.add_field(name="Max age",value=seconds_to_string(invite.max_age,"%w週間, %d日 %h時間%m分 %s秒"))
        invite_create_embed.add_field(name="Temporary member",value=str(invite.temporary))
        await client.get_channel(CHANNEL_IDS["server_events"]).send(embed=invite_create_embed)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        printe(f"Reaction added by {user}",label="Event")
        reaction_add_embed = discord.Embed(title="Reaction add event",url=reaction.message.jump_url,description=f"{reaction.emoji} by<@{user.id}> total: **{reaction.count}**")
        reaction_add_embed.set_author(name=user,icon_url=user.display_avatar.url)
        await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=reaction_add_embed)

        if reaction.count == 5 and reaction.message.guild.id == 842320961033601044:
            printe("Received over 5 reactioned message")
            reactioned_5_embed = discord.Embed(title="話題の話題だ！",url=f"{reaction.message.jump_url}",description=f"{reaction.emoji}by <@{user.id}>")
            reactioned_5_embed.set_author(icon_url=f"{user.display_avatar.url}",name=f"{user}")
            # it's channel is kanb-room
            await client.get_channel(1074148727616442408).send(embed=reactioned_5_embed)
            return

        if (reaction.message.id == latest_temp_datas["actioned_brocked_word_message_id"]) and (reaction.emoji == "❗"):
            brocked_word_description_embed = discord.Embed(title="メッセージが記録されています",description=f"該当のメッセージには禁止されたワードが含まれている可能性があるため記録されています",color=0x4444ff)
            await reaction.message.channel.send(embed=brocked_word_description_embed)
            latest_temp_datas["actioned_brocked_word_message_id"] = 0
        if (reaction.message.id == latest_temp_datas["openable_discord_message_link"]) and (reaction.emoji == "🔗"):
            printe("Opening message link in reaction message")
            jump_url = re.match(r"https://(canary\.)?discord\.com/channels/\d*/\d*/\d*/?",reaction.message.content).group()
            message_status_ids = jump_url.lstrip("https://discord.com/channels/").split("/")
            message_status_ids = jump_url.lstrip("https://canary.discord.com/channels/").split("/")
            request_url = f"https://discord.com/api/v10/channels/{message_status_ids[1]}/messages/{message_status_ids[2]}"
            result_message_json = json.loads(requests.get(url=request_url,headers=HTTP_AUTHORIZATION_HEADERS).text)
            try:
                message_link_opener_reactions = "リアクション: "
                for reaction_of_message_json in result_message_json["reactions"]:
                    if reaction_of_message_json["emoji"]["id"] is None:
                        message_link_opener_reactions += f'{reaction_of_message_json["emoji"]["name"]}×{reaction_of_message_json["count"]}, '
                    else:
                        message_link_opener_reactions += f'<:{reaction_of_message_json["emoji"]["name"]}:{reaction_of_message_json["emoji"]["id"]}>×{reaction_of_message_json["count"]}'
            except KeyError:
                printe("it's message link is not reactioned")
            message_link_opener_embed = discord.Embed(description=f'{result_message_json["content"]}\n\n{message_link_opener_reactions}')
            message_link_opener_embed.set_author(
                icon_url=f'https://cdn.discordapp.com/avatars/{result_message_json["author"]["id"]}/{result_message_json["author"]["avatar"]}.webp?size=100',
                name=f'{result_message_json["author"]["username"]}#{result_message_json["author"]["discriminator"]}'
)
            message_link_opener_embed.set_footer(text=f'at: {dt.now().strftime(STRFTIME_ARG)}')
            await reaction.message.channel.send(embed=message_link_opener_embed)
            latest_temp_datas["openable_discord_message_link"] = 0
        if (reaction.message.id == latest_temp_datas["ikaf_generic_disclaimer"]) and (reaction.emoji == "ℹ️"):
            ikaf_generic_disclaimer_embed = discord.Embed(
                title="ikafジェネリック免責事項",
                description="""
**これは私個人のあくまで個人の主観に基づいた文章です**
※ とても偏った根拠のない妄想である可能性があります
※ 個人的な感情が大きく含まれています
※ このメッセージはただこんなとらえ方もできるよねと妄想したのを共有したかっただけです
※ この鯖ではない鯖での発言の画像が含まれます
※ あまり触れるのもよくないとはわかっています
※ 回りくどい言い方をしている箇所があります
※ おおごとにはしたくないです
※ すべて憶測です
※ 独り言だと思って読んでください
※ 間違っている可能性もあります
※ 問題があったらこのメッセージを容赦なく削除してください
※ 悪意が含まれる可能性があります
※ 堅苦しい書き方してるけど癖なので気にしないでくれ
※ 上の内容はすべて私の免責のためなので別に必ず読む必要はなかった(ha
"""[1:-1]
)
            ikaf_generic_disclaimer_embed.add_field(name="以下の内容は上記に記した事項を踏まえたうえで読んでください",value="という便利なやつ")
            await reaction.message.channel.send(embed=ikaf_generic_disclaimer_embed)
            latest_temp_datas["ikaf_generic_disclaimer"] = 0

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        printe(f"Reaction removed by {user}",label="Event")
        reaction_add_embed = discord.Embed(title="Reaction remove event",url=reaction.message.jump_url,description=f"{reaction.emoji} by<@{user.id}> total: **{reaction.count}**")
        reaction_add_embed.set_author(name=user,icon_url=user.display_avatar.url)
        await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=reaction_add_embed)

    async def on_app_command_completion(self, interaction: discord.Interaction, command: Union[app_commands.Command,app_commands.ContextMenu]):
        printe(f"{interaction.user} issued command: /{command.qualified_name}")
        if type(command) == app_commands.Command:
            app_command_completion_embed = discord.Embed(
                title=f"{interaction.user.display_name} issued Command: /{command.qualified_name}",
                description=f"**Params: **\n{command.parameters}"
                )
        elif type(command) == app_commands.ContextMenu: 
            app_command_completion_embed = discord.Embed(
                title=f"{interaction.user.display_name} issued ContextMenu: /{command.qualified_name}",
                description=f"**Type: **\n{command.type}"
                )
        app_command_completion_embed.set_author(name=interaction.user,icon_url=interaction.user.display_avatar.url)
        app_command_completion_embed.set_footer(text=f"at: {dt.now().strftime(STRFTIME_ARG)}, uid: {interaction.user.id}")
        await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=app_command_completion_embed)

    async def on_member_join(self, member: discord.Member):
        printe(f"Member joined: {member}, to {member.guild.name}",label="Event")
        # Anti Prefix Exclamation
        if member.display_name.startswith("!"):
            printe(f"activated anti exclamation by {member}",label="AutoMod")
            edited_name = remove_prefix_string(string=member.display_name,prefix="!")
            await member.edit(nick=edited_name)
            if member.guild.id == 1020519633268256821:
                await client.get_channel(1041280225209749536).send(
                    embed=discord.Embed(
                        title="anti-prefix-exclamation",
                        description=f"\"{member.display_name}\" to \"{edited_name}\""
                    ).set_author(
                        name=member,
                        icon_url=member.display_avatar.url
                    )
                )
            elif member.guild.id == METS_SERVER_ID:
                await client.get_channel(1074249515554582548).send(
                    embed=discord.Embed(
                        title="anti-prefix-exclamation",
                        description=f"\"{member.display_name}\" to \"{edited_name}\""
                    ).set_author(
                        name=member,
                        icon_url=member.display_avatar.url
                    )
                )
        
        # Welcome Message
        if member.guild.id == METS_SERVER_ID:
            member_count = member.guild.member_count
            if zorome_check(member_count):
                if "7" in str(member_count):
                    description = f"Met\'s サーバーへようこそ、あなたは**記念すべき{member_count}人目**のメンバーです！ラッキーセブン！🥳🎉🎂"
                elif "4" in str(member_count):
                    description = f"Met\'s サーバーへようこそ、あなたは**{member_count}人目**のメンバーです！不吉！！"
                elif "6" in str(member_count):
                    description = f"Met\'s サーバーへようこそ、あなたは**{member_count}人目**のメンバーです！不吉！！"
                else:
                    description = f"Met\'s サーバーへようこそ、あなたは**記念すべき{member_count}人目**のメンバーです！🥳"
            else:
                description = f"Met\'s サーバーへようこそ、あなたは{member_count}人目のメンバーです！"
            description = description  + "\n\nここではサーバーに参加するまでの流れを紹介します\n質問などがあればぜひ<#1074249460051353620>から"
            welcome_message_embed = discord.Embed(
                title="⛏️Met\'s サーバーへようこそ！！！⛏️",
                description=description,
                color=THEME_COLOR_HEX
            )
            welcome_message_embed.set_author(
                name="マスコットキャラクター、子met",
                icon_url="https://cdn.discordapp.com/avatars/985254515798327296/5be9873b75e509b699c52db52f9e99ec.webp?size=256"
            )
            welcome_message_embed_introduction = discord.Embed(
                title="1. 自己紹介をする",
                description=f"""
<#949994602427994113>で自己紹介を書きましょう
以下にテンプレートがあるので、必要に応じて書き変えて使いましょう

もし、上記のチャンネルが\"アクセスなし\"となっているならば
先に右下のルール確認などを終わらせましょう
更に、現在はセキュリティ向上のためbot認証を入れています
AuttajaというbotからDMが届くためそちらのガイドに従って認証してください
もしわからなければ<#1074249460051353620>でヘルプを求めましょう
```
名前：{member.name}
好きなもの＆事：マイクラ！
JAVA/統合：主にJava Edition、たまに統合版
MCID：Maikuraman
どこから来たか：○○の掲示板
一言：冒険が大好きです！一緒にダンジョン攻略しませんか？
```
"""[1:-1],
                color=THEME_COLOR_HEX
            )
            welcome_message_embed_whitelist = discord.Embed(
                title="2. ホワイトリスト登録をする",
                description="""
<#1074249454741368943>でホワイトリストに登録しましょう
自分のMCID(ゲーム内での名前)を送ります
統合版、Javaのどちらを使用しているかも明記すると良いでしょう
例: 「java版: Notch61」
"""[1:-1],
                color=THEME_COLOR_HEX
            )
            welcome_message_embed_join = discord.Embed(
                title="3. 参加する",
                description=f"""
サーバーに参加します
IPは、
Java版: `{SERVER_ADDRESSES["java"]["ip"]}`
統合版: `{SERVER_ADDRESSES["bedrock"]["ip"]}`(ポート: `{SERVER_ADDRESSES["bedrock"]["port"]}`)
詳しくは<#1074249451041992776>、または<#1074249460051353620>でサポートを受けることもできます、遠慮なくお問い合わせください
"""[1:-1],
                color=THEME_COLOR_HEX
            )
            welcome_message_embed_talking = discord.Embed(
                title="5. その他",
                description="""
何か不明な点や質問などあれば**ぜひ**<#1074249460051353620>へ
それでは行ってらっしゃい！
"""[1:-1]
            )
            embeds = [
                welcome_message_embed,
                welcome_message_embed_introduction,
                welcome_message_embed_whitelist,
                welcome_message_embed_join,
                welcome_message_embed_talking
            ]

            if not member.dm_channel:
                await member.create_dm()
            if member.dm_channel:
                member_dm_permissions = member.dm_channel.permissions_for(member.guild.me)
            try:
                await member.send(embeds=embeds)
                printe("Sent welcome message on DM")
            except discord.errors.Forbidden:
                welcome_channel_overwrites = {
                    member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True
                        )
                }
                welcome_channel = await member.guild.create_text_channel(
                    name=f"ようこそ！{member.display_name}",
                    topic=f"{member}さん専用のウェルカムチャンネルです",
                    reason="text-channel created by welcome-message feature",
                    overwrites=welcome_channel_overwrites
                )
                await welcome_channel.send(content=member.mention,embeds=embeds,view=CloseWelcomeChannel())
                printe(f"Sent welcome message on #{welcome_channel.name}")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        printe("received member update",label="Event")
        if after.display_name.startswith("!"):
            printe(f"activated anti exclamation by {after}",label="AutoMod")
            edited_name = remove_prefix_string(string=after.display_name,prefix="!")
            await after.edit(nick=edited_name)
            if after.guild.id == 1020519633268256821:
                await client.get_channel(1041280225209749536).send(
                    embed=discord.Embed(
                        title="anti-prefix-exclamation",
                        description=f"\"{after.display_name}\" to \"{edited_name}\""
                    ).set_author(
                        name=after,
                        icon_url=after.display_avatar.url
                    )
                )
            elif after.guild.id == METS_SERVER_ID:
                await client.get_channel(1074249515554582548).send(
                    embed=discord.Embed(
                        title="anti-prefix-exclamation",
                        description=f"\"{after.display_name}\" to \"{edited_name}\""
                    ).set_author(
                        name=after,
                        icon_url=after.display_avatar.url
                    )
                )

client = MiniMet(intents=intents)
tree = app_commands.CommandTree(client=client)



@tree.command(name="help",description="子metのヘルプを表示")
@app_commands.guilds(METS_SERVER_ID)
async def help(interaction: discord.Interaction):
    help_embed=discord.Embed()
    help_embed.add_field(name="これ。", value="</help:1063776235156672632>", inline=False)
    help_embed.add_field(name="サーバーのIPなどを表示", value="</status:1063778904533385306>", inline=False)
    help_embed.add_field(name="サーバーの招待リンクを取得", value="</invite:1063779546949767219>", inline=False)
    help_embed.add_field(name="サーバーのwebリンクを表示", value="</web:1063780119430312017>", inline=False)
    help_embed.add_field(name="サーバーの参加者を確認", value="`!sc list`(<#1074249466024034334>でのみ動作)", inline=False)
    help_embed.add_field(name="サーバーのマップのリンクを確認", value="</map:1063780759552405544>", inline=False)
    await interaction.response.send_message(embed=help_embed)

@tree.command(name="status",description="サーバーのIPなどを表示")
@app_commands.guilds(METS_SERVER_ID)
async def status(interaction: discord.Interaction):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory()
    game_server_response = SLPClient("localhost",port=25565).get_status().res
    status_embed=discord.Embed(title="ステータス", description="IPやバージョン等の情報", color=0x6f5134)
    status_embed.add_field(name="Java Edition - IP", value=f'`{SERVER_ADDRESSES["java"]["ip"]}`', inline=True)
    status_embed.add_field(name="Bedrock Edition - IP", value=f'`{SERVER_ADDRESSES["bedrock"]["ip"]}`', inline=True)
    status_embed.add_field(name="Bedrock Edition - Port", value=f'`{SERVER_ADDRESSES["bedrock"]["port"]}`', inline=True)
    status_embed.add_field(name="CPU Usage",value=f"{cpu_usage}%", inline=True) 
    status_embed.add_field(name="Memory Usage",value=f"{memory_usage.percent}%", inline=True)
    status_embed.add_field(name="Game Server",value=f"{game_server_response['status']}", inline=True)
    status_embed.set_footer(text="ver:1.19.4, 情報更新: 2023/04/03")
    await interaction.response.send_message(embed=status_embed)

@tree.command(name="invite",description="サーバーの招待リンクを取得")
@app_commands.guilds(METS_SERVER_ID)
async def invite(interaction: discord.Interaction):
    invite_embed = discord.Embed(title="招待リンク",description="サーバーの招待リンクです\nいろんなところ共有してください！\n**```https://discord.mets-svr.com```**",color=0x22ff22)
    view = discord.ui.View().add_item(discord.ui.Button(label='招待リンク', url='https://discord.mets-svr.com/'))
    await interaction.response.send_message(view=view,embed=invite_embed)

@tree.command(name="web",description="サーバーのwebリンクを表示")
@app_commands.guilds(METS_SERVER_ID)
async def web(interaction: discord.Interaction):
    web_embed = discord.Embed(title="webサイト",description="サーバーの公式webサイトです\n更新がめんどくてめんどくて...\n**```https://mets-svr.com```**",color=0x22ff22)
    view = discord.ui.View().add_item(discord.ui.Button(label='webサイト', url='https://mets-svr.com/'))
    await interaction.response.send_message(view=view,embed=web_embed)

@tree.command(name="map",description="サーバーのマップのリンクを確認")
@app_commands.guilds(METS_SERVER_ID)
async def map(interaction: discord.Interaction):
    web_embed = discord.Embed(title="マップ",description="サーバーのマップです\n空からワールドを眺めたりできます\n動作していないこともあります...\n**```https://mets-svr.com/map```**",color=0x22ff22)
    view = discord.ui.View().add_item(discord.ui.Button(label='マップ', url='https://mets-svr.com/map'))
    await interaction.response.send_message(view=view,embed=web_embed)

@tree.command(name="alert",description="ユーザーに警告を送信します")
@app_commands.describe(
    content="警告内容",
    to="送信先(デフォルトでは、今居るチャンネルに送信されます)",
    title="警告のタイトル",
    attachment="送付ファイル",
    author="送信元のユーザーを明記"
)
@app_commands.checks.has_permissions(administrator=True)
async def alert(
    interaction: discord.Interaction,
    content: str,
    to: discord.Member,
    title: Optional[str] = "無題の警告",
    attachment: Optional[discord.Attachment] = None,
    author: Optional[bool] = False
):
    embed = discord.Embed(title=title,description=content)
    embed.set_footer(text=f"{to.guild.name} - {dt.now().strftime(STRFTIME_ARG)}")
    if author == True:
        embed.set_author(
            name=interaction.user,
            icon_url=interaction.user.display_avatar.url,
            url=f"https://discord.com/channels/@me/{interaction.user.id}"
        )
    if attachment is not None:
        file = await attachment.to_file()
        await to.send(embed=embed,file=file)
    else:
        await to.send(embed=embed)
    await interaction.response.send_message("正常に送信されました↓",embed=embed,ephemeral=True)


# FIXME: なんか、なんだadd-todoのコマンドが捜査してないから直す
@tree.command(name="add-todo",description="開発者用-追加予定の要素をメモする")
@app_commands.describe(
    label="バグ、改善案、新機能",
    title="タイトル",
    description="説明"
)
@app_commands.guilds(METS_SERVER_ID)
async def add_todo(interaction: discord.Interaction, label: str, title: str, description: str):
    embed = discord.Embed(title=f"{label}: {title}",description=description)
    embed.set_author(icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"uid: {interaction.user.id}, at: {dt.now().strftime(STRFTIME_ARG)}")
    if label == "バグ" or label == "改善案" or label == "新機能":
        match label:
                case "バグ": embed.color = 0xff0000
                case "改善案": embed.color = 0x00ff00
                case "新機能": embed.color = 0x0000ff
    await client.get_channel(1072469158530396190).send(embed=embed)
    await interaction.response.send_message(content=f"**{title}**をTODOに追加しました",ephemeral=True)

class ExecuteExec(discord.ui.Modal, title="execute"):
    code = discord.ui.TextInput(
        label="コード",
        style=discord.TextStyle.long,
        placeholder="コードを入力してください",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id != 776726560929480707:
            await interaction.response.send_message("🚫使用が許可されていません🚫")
            return
        try:
            exec(self.code.value, globals(), locals())
            await interaction.response.send_message(f"実行しました\n```py\n{self.code.value}\n```")
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{self.code.value}\n```", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(title="execute内部エラー",description=error,color=0xff0000)
        await client.get_channel(1074249516871602227).send(embed=embed)
        await interaction.response.send_message(f"内部エラーにより処理に失敗しました", ephemeral=True)

class ExecuteSubproc(discord.ui.Modal, title="execute as subprocess"):
    code = discord.ui.TextInput(
        label="コード",
        style=discord.TextStyle.long,
        placeholder="コードを入力してください",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id != 776726560929480707:
            await interaction.response.send_message("🚫使用が許可されていません🚫")
            return
        await interaction.response.send_message(f"以下のコードを、subprocessとして実行中です\n```py\n{self.code.value}\n```")
        try:
            with open("storage/temp/python/execute.py","w") as file:
                file.write(self.code.value)
            process = subprocess.Popen("py storage/temp/python/execute.py",bufsize=-1)
            await process.wait()
            result = process.stdout.decode("utf-8")
            await interaction.user.send(f"{interaction.created_at.strftime(STRFTIME_ARG)}に受け取ったsubprocessの実行が終了しました\n```py\n{result}\n```")
        except Exception as e:
            await interaction.channel.send(f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{self.code.value}\n```")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(title="execute内部エラー",description=error,color=0xff0000)
        await client.get_channel(1074249516871602227).send(embed=embed)
        await interaction.response.send_message(f"内部エラーにより処理に失敗しました", ephemeral=True)

@tree.command(name="execute",description="Pythonのプログラムを実行する（開発者用）")
@app_commands.describe(
    code="実行対象のコード(入力しない場合はテキストボックスで入力します)",
    ephemeral="実行結果のログを隠すか(コードが短文の時にのみ有効)",
    to_subprocess="subprocessとして実行するか"
)
async def execute(
    interaction: discord.Interaction,
    code: Optional[str] = None,
    ephemeral: Optional[bool] = True,
    to_subprocess: Optional[bool] = False
):
    if interaction.user.id != 776726560929480707:
        await interaction.response.send_message("🚫使用が許可されていません🚫")
        return
    if to_subprocess == False:
        if code is not None:
            try:
                exec(code, globals(), locals())
                if ephemeral == True:
                    await interaction.response.send_message(f"実行しました\n```py\n{code}\n```",ephemeral=True)
                else:
                    await interaction.response.send_message(f"実行しました\n```py\n{code}\n```",ephemeral=False)
            except Exception as e:
                if ephemeral == True:
                    await interaction.response.send_message(f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{code}\n```", ephemeral=True)
                else:
                    await interaction.response.send_message(f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{code}\n```", ephemeral=True)
        else:
            await interaction.response.send_modal(ExecuteExec())
    else:
        if code is not None:
            if ephemeral == True:
                await interaction.response.send_message(f"以下のコードを、subprocessとして実行中です\n```py\n{code}\n```")
            else:
                await interaction.response.send_message(f"以下のコードを、subprocessとして実行中です\n```py\n{code}\n```")
            try:
                with open("storage/temp/python/execute.py","w") as file:
                    file.write(code)
                process = subprocess.Popen("py storage/temp/python/execute.py",bufsize=-1)
                await process.wait()
                result = process.stdout.decode("utf-8")
                await interaction.user.send(f"{interaction.created_at.strftime(STRFTIME_ARG)}に受け取ったsubprocessの実行が終了しました\n```py\n{result}\n```")
            except Exception as e:
                await interaction.response.send_message(f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{code}\n```", ephemeral=True)
        else:
            await interaction.response.send_modal(ExecuteSubproc())

@tree.command(name="report",description="違反やトラブルなどを報告する")
@app_commands.describe(
    title="タイトル - 報告の内容を簡潔に伝えてください",
    description="説明 - 報告の詳細(マークダウンを使用できます、改行には<br>を使用します)",
    user="ユーザー - 報告対象のユーザー(discordユーザーがわかる場合)",
    user_name="ユーザー名 - 報告対象のユーザーの名前(discordユーザーが分からない場合、代わりに使用されます)",
    attachment="参考ファイル - 報告する内容をより分かりやすく伝えるための添付ファイル",
)
async def report(
    interaction: discord.Interaction,
    title: str,
    description: str,
    user: Optional[discord.User] = None,
    user_name: Optional[str] = None,
    attachment: Optional[discord.Attachment] = None
):
    description = description.replace("<br>","\n")
    embed = discord.Embed(title=title,description=description)
    if user is not None:
        embed.set_author(icon_url=user.display_avatar.url,name=user)
    if user_name is not None:
        embed.set_author(name=user_name)
    if attachment is not None:
        file = await attachment.to_file()
        await client.get_channel(CHANNEL_IDS["report_datas"]).send(embed=embed,file=file)
    else:
        await client.get_channel(CHANNEL_IDS["report_datas"]).send(embed=embed)
    await interaction.response.send_message("正常に送信されました、報告ありがとうございます",ephemeral=True)

# TODO: グロチャ機能用のコマンドを作る
@tree.command(name="global-chat",description="グローバルチャットのコマンド")
async def global_chat(interaction: discord.Interaction):
    return

@tree.command(name="dayone",description="こめたんに共感してもらう")
async def dayone(interaction: discord.Interaction):
    await interaction.response.send_message(content="\:D",ephemeral=True)
    event_channel_id = interaction.channel.id
    async with interaction.channel.typing():
        await asyncio.sleep(random.uniform(1,2))
    await client.get_channel(event_channel_id).send("だよね！！！")

@tree.command(name="group-categorize",description="選んだ値をランダムにグループ分けする"
)
@app_commands.describe(
    users="スペースで値を区切る",
    members="何人ずつにメンバーを分けるか"
)
async def group_categorize(interaction: discord.Interaction, users: str, members: int):
    if not (" " in users):
        await interaction.response.send_message("値が1つしかないか、またはスペースによって区切られていません",ephemeral=True)
        return
    users = users.split(" ")
    if len(users) < members:
        await interaction.response.send_message(f"ユーザー数に対するグループのメンバーが多すぎます\n**{len(users)}**人 | **{members}**メンバー",ephemeral=True)
        return
    result = {}
    while 0 >= len(users):
        i = i + 1
        result[f"group_{i}"] = []
        for j in range(members):
            user = random.choice(users)
            result[f"group_{i}"].append(user)
            users.remove(user)
    result = json.dumps(result,indent=4)
    await interaction.response.send_message(result)

@tree.command(name="temp-role",description="時間を指定して一定期間だけ指定のロールを付与できます")
@app_commands.describe(
    target="ロールを付与するユーザー",
    role="付与するロール",
    duration="付与する時間(1s = 1秒, 1m = 1分, 1h = 1時間, 1d = 1日, 1w = 1週間 \",\"で値を区切ります。例: 1w,2d,3h,4m,5s)",
    notify_to_dm="終了時にDMへ通知する先のメンバー"
)
@app_commands.guild_only()
@app_commands.checks.has_permissions(administrator=True)
async def temp_role(
    interaction: discord.Interaction,
    target: discord.Member,
    role: discord.Role,
    duration: str,
    notify_to_dm: Optional[discord.Member] = None
):
    durations = duration.split(",")
    wait_duration = 0
    for duration in durations:
        try:
            if duration.endswith("w"):
                duration = duration.rstrip("w")
                duration = int(duration) * 604800
            elif duration.endswith("d"):
                duration = duration.rstrip("d")
                duration = int(duration) * 86400
            elif duration.endswith("h"):
                duration = duration.rstrip("h")
                duration = int(duration) * 3600
            elif duration.endswith("m"):
                duration = duration.rstrip("m")
                duration = int(duration) * 60
            elif duration.endswith("s"):
                duration = duration.rstrip("s")
                duration = int(duration)
            else:
                await interaction.response.send_message("引数、`duration`の指定が間違っています",ephemeral=True)
                return
            wait_duration += duration
        except TypeError:
            await interaction.response.send_message("引数、`duration`の指定が間違っています",ephemeral=True)
            return
    await target.add_roles(role,reason="temp-role feature")
    embed_text = f"{target.mention}に{role.mention}を付与しました\nこのロールは{seconds_to_string(wait_duration,'**%w**週間 **%d**日 **%h**時間 **%m**分 **%s**秒後')}に剥奪されます"
    embed = discord.Embed(description=embed_text)
    embed.set_author(icon_url=target.display_avatar.url,name=target)
    await interaction.response.send_message(embed=embed)
    await asyncio.sleep(wait_duration)
    if notify_to_dm is not None:
        notify_embed = discord.Embed(title="temp-role機能の効果が終了しました",description=f"付与: {interaction.user.mention}\n付与先: {target.mention}")
        notify_embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
        notify_embed.set_footer(text="このメッセージはtemp-role機能を使用したユーザーによって通知されました")
        await notify_to_dm.send(embed=notify_embed)
    await target.remove_roles(role,reason="temp-role feature")

class Feedback(discord.ui.Modal, title="フィードバック"):

    feedback = discord.ui.TextInput(
        label="フィードバックの内容",
        style=discord.TextStyle.long,
        placeholder="メッセージを入力してください",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="新フィードバック！",description=f"{self.feedback.value}")
        embed.set_author(name=interaction.user,icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"uid: {interaction.user.id}, at {dt.now().strftime(STRFTIME_ARG)}")
        await client.get_channel(1072420523390287962).send(embed=embed)
        await interaction.response.send_message("フィードバックをありがとうございました。", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(title="feedback内部エラー",description=error,color=0xff0000)
        await client.get_channel(1072420523390287962).send(embed=embed)
        await interaction.response.send_message(f"内部エラーにより処理に失敗しました", ephemeral=True)

@tree.command(name="feedback",description="子metに対する改善案やバグ報告などのフィードバックを送信します")
async def feedback(interaction: discord.Interaction):
    await interaction.response.send_modal(Feedback())

# TODO: 埋め込み作成コマンドを実装する
class GenerateEmbed(discord.ui.Modal, title="埋め込み作成"):
    def __init__(
        self,
        *,
        title: str = discord.utils.MISSING,
        timeout: Optional[float] = None,
        custom_id: str = discord.utils.MISSING,
    ) -> None:
        if title is discord.utils.MISSING and getattr(self, 'title', discord.utils.MISSING) is discord.utils.MISSING:
            raise ValueError('Modal must have a title')
        elif title is not discord.utils.MISSING:
            self.title = title
        self.custom_id: str = os.urandom(16).hex() if custom_id is discord.utils.MISSING else custom_id

        super().__init__(timeout=timeout)

    title = discord.ui.TextInput(
        label="title",
        style=discord.TextStyle.short,
        max_length=256,
        required=False,
        placeholder="タイトルを入力してください"
    )
    description = discord.ui.TextInput(
        label="description",
        style=discord.TextStyle.long,
        max_length=4096,
        required=False,
        placeholder="説明欄を入力してください(マークダウンも使用できます)"
    )
    fields = discord.ui.TextInput(
        label="fields",
        style=discord.TextStyle.long,
        required=False,
        placeholder='JSON形式で入力します。例: [{"name":"好きな食べ物","value":"カステラ"},{"name":"好きな動物","value":"かに"}]'
    )
    footer = discord.ui.TextInput(
        label="footer",
        style=discord.TextStyle.short,
        max_length=2048,
        required=False,
        placeholder="フッターのテキストを入力してください"
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title.value,description=self.description.value,color=self.color,url=self.url)
        if self.author_icon is not None and self.author_name is not None:
            embed.set_author(icon_url=self.author_icon,name=self.author_name)
        if self.image is not None:
            embed.set_image(url=self.image.url)
        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail.url)
        if self.footer is not None:
            embed.set_footer(text=self.footer.value)
        if self.fields is not None:
            try:
                self.fields = json.loads(self.fields)
                for field in self.fields:
                    embed.add_field(name=field["name"],value=field["value"])
            except Exception as e:
                await interaction.response.send_message("fields処理中にエラーが発生しました",ephemeral=True)
                await client.get_channel(CHANNEL_IDS["bot_log"]).send(f"GenerateEmbed.Fields: {e}")
                return

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("embedを生成しました", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(title="generate_embed内部エラー",description=error,color=0xff0000)
        await client.get_channel(CHANNEL_IDS["bot_log"]).send(embed=embed)
        await interaction.response.send_message(f"内部エラーにより処理に失敗しました", ephemeral=True)

@tree.command(name="generate-embed",description="埋め込みメッセージを送信します")
@app_commands.describe(
    color="16進数のRGBカラーコードでラインの色を指定します",
    url="title要素のリンク先",
    author_icon="author属性のアイコン画像",
    author_name="author属性の名前",
    image="image属性の画像",
    thumbnail="thumbnail要素の画像"
)
async def generate_embed(
    interaction: discord.Interaction,
    color: Optional[str] = None,
    url: Optional[str] = None,
    author_icon: Optional[discord.Attachment] = None,
    author_name: Optional[str] = None,
    image: Optional[discord.Attachment] = None,
    thumbnail: Optional[discord.Attachment] = None
):
    if (color is not None) and (len(color) != 6):
        await interaction.response.send_message("colorの長さが正しくありません",ephemeral=True)
        return
    elif (color is not None) and (len(color) == 6):
        try:
            color = hex(int(color, 16))
        except ValueError:
            await interaction.response.send_message("colorの値が正しくありません",ephemeral=True)
            return
    if (url is not None) and (not re.fullmatch(r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+",url)):
        await interaction.response.send_message("urlの指定が正しくありません",ephemeral=True)
        return

    await interaction.response.send_modal(GenerateEmbed(color,url,author_icon,author_name,image,thumbnail,title="埋め込み作成"))

@tree.command(name="speedtest",description="botサーバーの回線速度を測ります")
async def speedtest(interaction: discord.Interaction):
    await interaction.response.send_message("計測中...")
    async with interaction.channel.typing():
        process = subprocess.run(["speedtest","--json"], capture_output=True)
        speed = json.loads(process.stdout)
        speed["download"] = round(speed["download"] / 1024 / 1024,3)
        speed["upload"] = round(speed["upload"] / 1024 / 1024,3)
    await interaction.channel.send(content=f':arrow_up: up: {speed["upload"]}Mbps\n:arrow_down: down: {speed["download"]}Mbps\nping: {speed["ping"]}ms')

@tree.command(name="gobi", description="語尾関連の規制や検知を行います")
@app_commands.describe(
    user="処理対象のユーザー",
    gobi="語尾",
    action="語尾が含まれていなかった場合のアクション",
    duration_days="期間(日数)",
    gobi_aliase="メインの語尾に合致しなかった場合のエイリアス語尾"
)
@app_commands.choices(
    action=[
        app_commands.Choice(name="メッセージ削除",value="delete_message"),
        app_commands.Choice(name="リアクション警告",value="reaction_warn"),
        app_commands.Choice(name="子metによる指摘",value="minimet_warn"),
        app_commands.Choice(name="60秒タイムアウト",value="timeout_60sec")
    ]
)
async def gobi(interaction: discord.Interaction, user: discord.User, gobi:str, action: str, duration_days: int, gobi_aliase: Optional[str] = None):
    with open("storage/json/gobis.json","r") as gobis:
        gobis = json.loads(gobis.read())
        gobis[f"{user.id}"] = {}
        gobis[f"{user.id}"]["gobi"] = gobi
        gobis[f"{user.id}"]["action"] = action
        gobis[f"{user.id}"]["gobi_aliase"] = gobi_aliase
        gobis[f"{user.id}"]["duration_days"] = duration_days,
        gobis[f"{user.id}"]["start_timestamp"] = str(dt.now())
        with open("storage/json/gobis.json","w") as gobis_writable:
            gobis_writable.write(json.dumps(gobis))
    embed = discord.Embed(title="語尾を登録しました",description=f"{user.mention}の語尾を`{gobi}`に設定しました\n\n**action**: `{action}`\n**duration**: `{duration_days}`\n**gobi_aliase**: `{gobi_aliase}`")
    embed.set_author(name=user,icon_url=user.avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="encode", description="文字列をエンコード / デコードします")
@app_commands.describe(
    string="処理対象の文字列",
    convertion_type="変換のタイプ",
    ephemeral="実行結果を隠すかどうか",
    decode="デコードするかどうか"
)
@app_commands.choices(
    convertion_type=[
        app_commands.Choice(name="UTF-8",value="utf-8"),
        app_commands.Choice(name="UTF-16",value="utf-16"),
        app_commands.Choice(name="UTF-32",value="utf-32"),
        app_commands.Choice(name="Shift-JIS",value="shift-jis"),
        app_commands.Choice(name="cp932",value="cp932"),
        app_commands.Choice(name="Unicode Escape",value="unicode-escape")
    ]
)
async def encode(interaction: discord.Interaction, string: str, convertion_type: str, ephemeral: bool, decode: bool):
    if decode == False:
        result = string.encode(convertion_type)
    else:
        result = string.decode(convertion_type)
    
    if ephemeral == False:
        await interaction.response.send_message(f"`{result}`")
    else:
        await interaction.response.send_message(f"`{result}`",ephemeral=True)

@tree.context_menu(name="だよね！！！")
async def dayone_msg(interaction: discord.Interaction, message: discord.Message):
    if last_actioned_times["dayone_msg"].second == dt.now().second:
        return
    async with message.channel.typing():
        await asyncio.sleep(random.uniform(0.1,1))
    if re.match(r"(死ね|嫌い)",message.content):
        await message.reply("？",mention_author=False)
    else:
        await message.reply("だよね！！！！",mention_author=False)
    last_actioned_times["dayone_msg"] = dt.now()
    await interaction.response.send_message(content="\:D",ephemeral=True)

@tree.context_menu(name="ぎふぃふぃけーと")
async def gifificate(interaction: discord.Interaction, message: discord.Message):
    try:
        printe(f"Gififing {message.attachments[0].filename} and otherfiles...")
    except IndexError:
        await interaction.response.send_message("該当のメッセージには送付ファイルが含まれていません",ephemeral=True)
        return
    result_files = []
    if random.randrange(1,50) == 1:
        response_message = "🚫使用制限にかかりました\nmini-met premiumにご登録いただければ月々777円で100万種類以上の機能にアクセスできます\n詳細↓||嘘です！！！！！！！！！！！！！！||"
        await interaction.response.send_message(response_message)
        return
    for attachment in message.attachments:
        await attachment.save(f"storage/images/gifificated/{message.id}-by-{message.author.id}.png")
        result_file = await attachment.to_file(filename=f"gifificated-{attachment.filename}.gif")
        result_files.append(result_file)
    await interaction.response.send_message(content="ぎっふぃっふぃ...",files=result_files)

class ReportThisMessage(discord.ui.Modal, title="匿名でメッセージを報告"):
    name = discord.ui.TextInput(
        label="表示名",
        style=discord.TextStyle.long,
        max_length=128,
        required=True,
        placeholder="識別のための表示名を入力してください（出来るだけ１種類の物を繰り返し使うようにしてください）"
    )
    report_title = discord.ui.TextInput(
        label="タイトル",
        style=discord.TextStyle.long,
        max_length=256,
        required=True,
        placeholder="報告の内容を簡潔にタイトルに表してください"
    )
    content = discord.ui.TextInput(
        label="内容",
        style=discord.TextStyle.long,
        max_length=4000,
        required=True,
        placeholder="報告の内容に対して詳細に教えてください（どのユーザーが、どういった違反をしたのかなど）"
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"詳細: {self.report_title.value}",description=self.content.value)
        embed.set_author(icon_url=interaction.guild.icon.url,name=self.name.value)
        embed.set_footer(text=f"AT: {dt.now().strftime(STRFTIME_ARG)}, InteraUID: {interaction.user.id}")
        await client.get_channel(CHANNEL_IDS["report_datas"]).send(embed=embed)
        await interaction.response.send_message("正常に送信されました、報告ありがとうございます", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(title="report_this_message内部エラー",description=error,color=0xff0000)
        await client.get_channel(CHANNEL_IDS["bot_log"]).send(embed=embed)
        await interaction.response.send_message("内部エラーにより処理に失敗しました", ephemeral=True)

class ReportConfirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="報告する", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("報告中...", ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("キャンセル中...", ephemeral=True)
        self.value = False
        self.stop()

@tree.context_menu(name="報告する")
async def report_this_messsage(interaction: discord.Interaction, message: discord.Message):
    # view = ReportConfirm()
    # await interaction.response.send_message("本当に報告しますか？",view=view,ephemeral=True)
    # await view.wait()
    # if view.value is None:
    #     return
    # elif view.value == False:
    #     return
    embed = discord.Embed(title="メッセージが報告されました", description=f"メッセージ: {message.content}\n\n**しばらくした後に詳細が送られます**", url=message.jump_url)
    embed.set_author(icon_url=message.author.display_avatar.url,name=message.author)
    embed.set_footer(text=f"AT: {dt.now().strftime(STRFTIME_ARG)}, InterUID: {interaction.user.id}, MID: {message.id}")
    await client.get_channel(CHANNEL_IDS["report_datas"]).send(embed=embed)
    await interaction.response.send_modal(ReportThisMessage())

@tree.context_menu(name="翻訳する")
async def translate_this(interaction: discord.Interaction, message: discord.Message):
    message.content = message.content.replace("parrot","parakeet")
    message.content = message.content.replace("Parrot","Parakeet")
    message.content = message.content.replace("PARROT","PARAKEET")
    if not re.fullmatch(nasu_regex,message.content):
        translator = Translator()
        translated_content = translator.translate(message.content,dest="ja").text
        embed = discord.Embed(title="日本語翻訳",description=translated_content)
        embed.set_author(name=message.author,icon_url=message.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    else:
        translated_content = message.content.replace("🍆な🍆","あ").replace("🍆ナ🍆","い").replace("🍆ﾅ🍆","う").replace("🍆na🍆","え").replace("🍆NA🍆","お").replace("🍆つ🍆","か").replace("🍆っ🍆","き").replace("🍆ツ🍆","く").replace("🍆ッ🍆","け").replace("🍆ｯ🍆","こ").replace("🍆tu🍆","さ").replace("🍆TU🍆","し").replace("🍆す🍆","す").replace("🍆ス🍆","せ").replace("🍆ｽ🍆","そ").replace("🍆su🍆","た").replace("🍆SU🍆","ち").replace("🍆なっ🍆","つ").replace("🍆ナッ🍆","て").replace("🍆ﾅｯ🍆","と").replace("🍆なす🍆","な").replace("🍆ナス🍆","に").replace("🍆ﾅｽ🍆","ぬ").replace("🍆nasu🍆","ね").replace("🍆NASU🍆","の").replace("🍆っす🍆","は").replace("🍆ッス🍆","ひ").replace("🍆ｯｽ🍆","ふ").replace("🍆ﾅす🍆","へ").replace("🍆なｽ🍆","ほ").replace("🍆ナす🍆","ま").replace("🍆なス🍆","み").replace("🍆NAｽ🍆","む").replace("🍆ナｽ🍆","め").replace("🍆ﾅス🍆","も").replace("🍆ｎａｓｕ🍆","や").replace("🍆ｎａ🍆","ゆ").replace("🍆ｓｕ🍆","よ").replace("🍆ns🍆","ら").replace("🍆ﾅっす🍆","り").replace("🍆ﾅｯす🍆","る").replace("🍆ナっｽ🍆","れ").replace("🍆なっsu🍆","ろ").replace("🍆NaSu🍆","わ").replace("🍆nAｽ🍆","を").replace("🍆ナｯす🍆","ん").replace("🍆Nasu🍆","ゃ").replace("🍆Na🍆","ゅ").replace("🍆Su🍆","ょ").replace("🍆nA🍆","っ").replace("🍆なs🍆","ぁ").replace("🍆ナs🍆","ぃ").replace("🍆ﾅs🍆","ぅ").replace("🍆nas🍆","ぇ").replace("🍆NAs🍆","ぉ")
        embed = discord.Embed(title="なす語翻訳",description=translated_content)
        embed.set_author(name=message.author,icon_url=message.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)

class ContextMenuOther(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="click", style=discord.ButtonStyle.green)
    async def click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("res",ephemeral=True)
    @discord.ui.button(label="krique", style=discord.ButtonStyle.green)
    async def krique(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("lath",ephemeral=True)

@tree.context_menu(name="その他")
async def rinna(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(view=ContextMenuOther(),ephemeral=True)
#     async with message.channel.typing():
#         await asyncio.sleep(1)
#     printe("Replying as Rinna")
#     rinna_request_body = {
#     "rawInput": "",
#     "outputLength": 25
# }
#     rinna_request_body["rawInput"] = f"B: {message.content} A:"
#     rinna_request_header = {
#     "Content-Type": "application/json",
#     "Cache-Control": "no-cache",
#     "Ocp-Apim-Subscription-Key": "a6b45fdff3844ad2853a5311014c3280",
# }
#     rinna_response = requests.post("https://api.rinna.co.jp/models/cce",headers=rinna_request_header, json=rinna_request_body)
#     await message.reply(json.loads(rinna_response.text)["answer"],mention_author=False)

client.run(token=BOT_TOKEN)
