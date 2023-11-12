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
                raise ValueError(f"Error on printe()\nmode option is not matched value: {mode}")
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
import datetime
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
from mcrcon import MCRcon
from io import BytesIO



# variables
intents = discord.Intents.all()
client = discord.Client(intents=intents)

global_chat_data = open("storage/json/global_chat.json","r",encoding="utf-8")
global_chat_data = json.load(global_chat_data)
brocked_words = open("storage/json/brocked_words.json","r",encoding="utf-8")
brocked_words = json.load(brocked_words)
already_one_time_executed = False
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



# constants
with open("constant.json","r",encoding="utf-8") as f:
    ENV = json.loads(f.read())
BOT_TOKEN = ENV["bot_token"]
PROGRAM_ARGS = sys.argv[1:]
METS_SERVER_ID = 842320961033601044
MINI_MET_ID = 985254515798327296
CRAB55E_DISCORD_USER_ID = 776726560929480707
THEME_COLOR_HEX = 0x3da45d
DISSOKU_COOLDOWN_SECONDS = 3600
BUMP_COOLDOWN_SECONDS = 7200
STRFTIME_ARG = "%Y-%m-%d %H:%M.%S"
TIMESTAMP_STRFTIME_ARG = "%Y-%m-%d %H:%M:%S.%f"
MINI_MET_AVATAR_URL = "https://cdn.discordapp.com/embed/avatars/2.png"
EXTERNAL_RCON_PATH = "C:/Program Files/mcrcon-0.0.5-bin-windows/mcrcon.exe"
NASU_REGEX = "(、|。|ﾟ|゜|゛|”|\"|a|A|ａ|n|N|ｎ|s|S|ｓ|t|T|u|U|ｕ|す|ス|ｽ|っ|ッ|つ|ツ|ｯ|な|ナ|ﾅ|🍆)*"
DISCONNECT_LOG_REGEX = "com\.mojang\.authlib\.GameProfile\@[0-9a-fA-F]*\[id=[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}\,name\=(BE\.)?[a-zA-Z0-9_]{3,64}\,properties\=\{textures\=\[com\.mojang\.authlib\.properties\.Property\@[0-9a-fA-F]*\]\}\,legacy\=(true|false)]"
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
    "shiritori_channel": 999269935370997761,
    "self_introduction": 949994602427994113,
    "rinnable_channel": 1074045647390507149,
    "member_welcome_channel": 842320961033601046
}
HTTP_AUTHORIZATION_HEADERS = {"Authorization":f"Bot {BOT_TOKEN}"}
SERVER_ACCESS = {
    "domain": "join.mets-svr.com",
    "local_ip": "localhost",
    "global_ip": requests.get("https://checkip.amazonaws.com/").text,
    "ports": {
        "bedrock":19132,
        "proxy":25565,
        "java":25566,
        "rcon": 25575,
        "tap": 49152
    },
    "authentication": {
        "rcon_password": "5117585993e259caae453676e6711cf81a2ba11743441f7e51a9abe1447eb20c",
        "servertap_key": "b8db4afa-6caf-42be-9955-a2aeffe0fa5f"
    }
}
GLOBAL_CHAT_ALLOWED_GUILD_IDS = [
    METS_SERVER_ID,
    1020519633268256821, # JUICE SERVER
    1025542325247680553 # DATONI SERVER
]


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
    result = outstr.replace(
        "%w",str(weeks)
    ).replace(
        "%d",str(days)
    ).replace(
        "%h",str(hours)
    ).replace(
        "%m",str(minutes)
    ).replace(
        "%s",str(seconds)
    )
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

def image_to_jsoncomponent(image: Image.Image, size: tuple = (23, 23), char: str = "█") -> str:
    image.thumbnail(size, Image.LANCZOS)
    width, height = image.size
    pixel_data = []

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))[:3]
            hex_code = "{" + f'"text":"{char}","color":"#{r:02x}{g:02x}{b:02x}"' + "}"
            pixel_data.append(hex_code)

    colored_characters = ""
    for i in range(0, len(pixel_data), width):
        row = pixel_data[i:min(i + width, len(pixel_data))]
        row_text = ",".join(row)
        colored_characters += row_text + ",\"\\n\","
    return "[" + colored_characters[:-6] + "]"

def get_timestamp(time: dt | int | float, style_sign: str = "f") -> str:
    VALID_STYLE_SIGN_VALUES = ["t","T","d","D","f","F","R"]
    if len(style_sign) != 1:
        raise ValueError("関数get_timestampの引数、\"style_sign\"に長いやつが渡されました")
    for valid_value in VALID_STYLE_SIGN_VALUES:

        if style_sign != valid_value:
            raise ValueError("関数get_timestampの引数、\"style_sign\"に有効じゃないやつが渡されました")

    if type(time) == dt:
        return f"<t:{round(time.timestamp())}:{style_sign}>"
    elif type(time) == int:
        return f"<t:{time}:{style_sign}>"
    elif type(time) == float:
        return f"<t:{round(time)}:{style_sign}>"
    else:
        raise TypeError("関数get_timestampの引数、\"time\"に有効じゃない型の値が渡されました")

class timescale:
    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    week = day * 7
    month = day * 31

class RolePanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="",emoji="❗",style=discord.ButtonStyle.green, custom_id="role_panel:allow_notify")
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

    @discord.ui.button(label="",emoji="🔇",style=discord.ButtonStyle.green, custom_id="role_panel:dm_ng")
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


class ConfirmCloseWelcomeChannel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="閉じる", style=discord.ButtonStyle.red, custom_id="welcome_channel:close/confirm_and_delete")
    async def confirm_and_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete(reason=f"Closed welcome-channel by {interaction.user}")

class CloseWelcomeChannel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="このチャンネルを閉じる", style=discord.ButtonStyle.red, custom_id="welcome_channel:close/confirm_question")
    async def confirm_question(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="閉じても大丈夫ですか？",
            description="""
この操作を取り消すことはできません
その後もし何か困ったことがあれば<#1074249460051353620>、または<@&1074249415679815780>のメンバーへ相談してください
"""[1:-1],
            color=0xff2222
)
        await interaction.response.send_message(embed=embed, view=ConfirmCloseWelcomeChannel())

class NewMemberAuthButton(discord.ui.View):
    def __init__(
        self,
        member: discord.Member,
        join_message: discord.Message
    ):
        super().__init__(timeout=None)
        self.value = None
        self.member: discord.Member = member
        self.join_message: discord.Message = join_message

    @discord.ui.button(label="このメンバーを認証する", emoji="✅", style=discord.ButtonStyle.green)
    async def authenticate_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        if type(interaction.user) != discord.Member:
            printe("Returning because interaction user is not member.",label="NewMemberAUth")
            return

        member_role = interaction.guild.get_role(1074249440132603975)
        active_user_role = interaction.guild.get_role(1074249433652412427)

        if not (active_user_role in interaction.user.roles):
            await interaction.response.send_message(
                f"あなたは<@&1074249433652412427>を持たないメンバーであるため、新規ユーザーを認証する権限がありません",
                ephemeral=True,
                delete_after=5.0
            )
            return
        
        if member_role in self.member.roles:
            await interaction.response.send_message(
                f"{self.member}は既に認証されています",
                ephemeral=True,
                delete_after=5.0
            )
            return

        await self.member.add_roles(member_role,reason=f"{self.member} was authenticated by {interaction.user}")
        printe(f"{self.member} was authenticated by {interaction.user}",label="NewMemberAuth")

        embed = discord.Embed(
            color=0x22ff22
        ).set_author(
            name=f"{interaction.user}によって{self.member}が認証されました",
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed)

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
            await interaction.response.send_message(
                f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{self.code.value}\n```",
                ephemeral=True
            )

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(title="execute内部エラー",description=error,color=0xff0000)
        await client.get_channel(1074249516871602227).send(embed=embed)
        await interaction.response.send_message(f"内部エラーにより処理に失敗しました", ephemeral=True)

class JoinToWhitelist(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="統合版", style=discord.ButtonStyle.green, custom_id="join_to_whitelist:bedrock")
    async def bedrock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("res: JoinToWhitelist.bedrock.res")

    @discord.ui.button(label="Java版", style=discord.ButtonStyle.green, custom_id="join_to_whitelist:java")
    async def java(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("res: JoinToWhitelist.java.res")

class TranslateMenu(discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.value = None
        self.message: discord.Message = message

    @discord.ui.button(label="メッセージを公開/Show to others", style=discord.ButtonStyle.green)
    async def open_message(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.message.reply(
            f"by {interaction.user.mention}",
            embeds=interaction.message.embeds,
            mention_author=False,
            allowed_mentions=NOT_MENTIONABLE
        )
        await interaction.response.send_message("公開しました",ephemeral=True)

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

class ContextMenuOther(discord.ui.View):
    def __init__(self, message: discord.Message):
        super().__init__()
        self.value = None
        self.message = message
    @discord.ui.button(label='古代なす語翻訳', style=discord.ButtonStyle.green,)
    async def not_found(self, interaction: discord.Interaction, button: discord.ui.Button):
        nasu_bin = self.message.content.replace("なす","0").replace("なっす","1").replace(" ","").replace("　","")
        try:
            nasu_bin = int(nasu_bin, 2)
        except ValueError as e:
            await interaction.response.send_message(f"該当のメッセージは古代なす語で構成されていません:\n`{e}`",ephemeral=True)
            return
        nasu_hex = hex(nasu_bin)[2:]
        translated_content = bytearray.fromhex(nasu_hex).decode("utf-8")
        embed = discord.Embed(title="古代なす語翻訳",url=self.message.jump_url,description=translated_content)
        embed.set_author(name=self.message.author,icon_url=self.message.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)

class MemberContextMenuMain(discord.ui.View):
    def __init__(
        self,
        member: discord.Member
    ):
        super().__init__(timeout=None)
        self.value = None
        self.member = member
    @discord.ui.button(label="まだ何もない", style=discord.ButtonStyle.gray)
    async def not_found(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("res",ephemeral=True)

class AddAdminNote(discord.ui.Modal, title="ノートを追加"):
    def __init__(
        self,
        parent_interaction: discord.Interaction,
        target_member: discord.Member
    ):
        super().__init__(timeout=None)
        self.parent_interaction = parent_interaction
        self.target_member = target_member
        self.title = f"\"{parent_interaction.user.display_name}\"にノートを追加"

    content = discord.ui.TextInput(
        label="内容",
        placeholder="入力してください",
        required=True,
        max_length=256
    )

    description = discord.ui.TextInput(
        label="詳細(任意)",
        placeholder="マークダウンを使用できます",
        style=discord.TextStyle.long,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        with open("storage/json/admin_notes.json", "r", encoding="utf-8") as f:
            note: list = json.loads(f.read())
        page = {
            "author_id": interaction.user.id,
            "content": self.content.value,
            "description": self.description.value,
            "member_id": self.target_member.id,
            "timestamp": dt.now().isoformat()
        }

        note.append(page)

        with open("storage/json/admin_notes.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(note))



        recorded_time = dt.fromisoformat(page["timestamp"])
        embed = discord.Embed(
            title=page["content"],
            description=page["description"],
            color=0x2b2d31
        )
        embed.set_author(
            name=str(self.target_member),
            icon_url=self.target_member.display_avatar.url
        )
        embed.set_footer(
            text=recorded_time.strftime(STRFTIME_ARG),
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message("以下の内容をノートに書き込みました", embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(f"内部エラーが発生しました: {error}", ephemeral=True)
        raise error

class MemberContextMenuMainForAdmin(discord.ui.View):
    def __init__(
        self,
        member: discord.Member
    ):
        super().__init__(timeout=None)
        self.value = None
        self.member = member
    @discord.ui.button(label="ノートを追加", style=discord.ButtonStyle.gray)
    async def write_note(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AddAdminNote(interaction, self.member))
    
    @discord.ui.button(label="ノートを開く", style=discord.ButtonStyle.gray)
    async def open_note(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("storage/json/admin_notes.json", "r", encoding="utf-8") as f:
            notes = json.loads(f.read())
        selected_pages = []
        for page in notes:
            if page["member_id"] == self.member.id:
                selected_pages.append(page)

        embeds = []
        for page in selected_pages:
            member = client.get_guild(METS_SERVER_ID).get_member(page["member_id"])
            author = client.get_guild(METS_SERVER_ID).get_member(page["author_id"])
            recorded_time = dt.fromisoformat(page["timestamp"])
            embed = discord.Embed(
                title=page["content"],
                description=page["description"],
                color=0x2b2d31
            )
            embed.set_author(
                name=str(member),
                icon_url=member.display_avatar.url
            )
            embed.set_footer(
                text=recorded_time.strftime(STRFTIME_ARG),
                icon_url=author.display_avatar.url
            )
            embeds.append(embed)
        await interaction.response.send_message(embeds=embeds, ephemeral=True)

class SetBirthday(discord.ui.Modal, title="誕生日を設定"):
    def __init__(self):
        super().__init__(timeout=None)

    date = discord.ui.TextInput(
        label="誕生日",
        placeholder="2023-01-02 または 03-04 の形式で入力してください",
        required=True,
        max_length=10,
        min_length=5
    )

    async def on_submit(self, interaction: discord.Interaction):
        birthdate_matched = re.fullmatch(
            r"(nnnn-nn-nn|nn-nn)".replace("n","\\d"),
            self.date.value
        )
        if not(birthdate_matched):
            embed = discord.Embed(
                title="無効な形式の入力です",
                description=f"入力: `{self.date.value}`\n例: `2021-05-13`または`05-13`",
                color=0xff0000
            )
            await interaction.response.send_message(
                embed=embed,
                view=SetBirthdayRetryButton(),
                ephemeral=True
            )
            return
        with open("storage/json/birthdays.json","r",encoding="utf-8") as f:
            birthdays_database_r = json.loads(f.read())

        birthdays_database_r[str(interaction.user.id)] = {
            "value": self.date.value,
            "submitted_at": dt.now().isoformat()
        }

        with open("storage/json/birthdays.json","w",encoding="utf-8") as f:
            f.write(json.dumps(birthdays_database_r))

        await interaction.response.send_message("success")

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(f"内部エラーが発生しました: {error}", ephemeral=True)
        raise error

class SetBirthdayRetryButton(discord.ui.View):
    def __init__(
        self,
    ):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="リトライ", style=discord.ButtonStyle.gray)
    async def open_note(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetBirthday())

class GlobalChatSelectTargetChannel(discord.ui.View):
    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        channel_types=[discord.ChannelType.text],
        placeholder="登録したいチャンネルを選択してください",
        min_values=1,
        max_values=1
    )
    async def selected_channel(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        return await interaction.response.send_message(f'GlobalChatSelectTargetChannel.selected_channel.{select.values[0].mention}')


class GlobalChatCommand(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="global-chat",
            description="グロチャ関連のコマンド"
        )

    @app_commands.command(
        name="submit",
        description="チャンネルをグロチャに接続する"
    )
    async def submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("GlobalChatCommand.submit.res",view=GlobalChatSelectTargetChannel())



class MiniMet(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        self.tree.add_command(GlobalChatCommand())

    async def setup_hook(self) -> None:
        self.add_view(RolePanel())
        self.add_view(CloseWelcomeChannel())
        self.add_view(ConfirmCloseWelcomeChannel())

        if "--sync" in PROGRAM_ARGS:
            await self.tree.sync()
            printe("Synchronized command tree")
        if "--sync-for-mets" in PROGRAM_ARGS:
            await self.tree.sync(guild=discord.Object(id=METS_SERVER_ID))
            printe("Synchronized command tree of mets-server")

    async def on_ready(self):
        global already_one_time_executed
        printe(f"{client.user.name} is Ready!!!",label="Event")
        printe(f"at {dt.now().strftime(STRFTIME_ARG)}")

        await client.change_presence(
            activity=discord.Activity(
                name="/help | mets-svr.com/mini-met | i\'m mini-met!",
                type=discord.ActivityType.competing
            )
        )

    async def on_dm_message(self, m: discord.Message):
        printe(f"dm message: \"{m.clean_content}\" by @{m.author}",label="Event")
        # talker
        if m.author.id != latest_temp_datas["received_dm_user_id"]:
            await client.get_channel(1065610631618764821).send(
                embed=discord.Embed().set_author(
                    name=f"DMの送信先が{m.author}に変更されました",
                    icon_url=m.author.display_avatar.url
                )
            )
        dm_channel_embed = discord.Embed(description=f"{m.content}")
        dm_channel_embed.set_author(name=m.author,icon_url=m.author.display_avatar.url)
        dm_channel_embed.set_footer(text=f"at: {dt.now().strftime(STRFTIME_ARG)}, Freq ID: {m.author.id}")
        files = [await a.to_file() for a in m.attachments] if m.attachments != [] else None
        await client.get_channel(1065610631618764821).send(embed=dm_channel_embed,files=files)
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

        if m.content == "かにかに！かに！" and m.guild.id == 939072966908596255:
            join_to_whitelist_embed = discord.Embed(
                title="ホワイトリスト認証",
                description="サーバーのホワイトリストに追加することで、参加できるようになります\n使っているプラットフォームを統合版またはJava版から選んでください",
                color=THEME_COLOR_HEX
            )
            await m.channel.send(
                "↓みたいな感じでホワリス追加を自動化したい\nMCIDとDiscord名を紐づけたシステムとかデータベースを作れるぞ",
                view=JoinToWhitelist(),
                embed=join_to_whitelist_embed
            )
            return

        if re.match(r"(かに|kani|🦀|crab)",m.content):
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

        if re.match(r"\<\@\d*\>",m.content) and m.guild.id == METS_SERVER_ID:
            printe("Received mention message",label="MentionLog")
            mention_embed = discord.Embed(
                title="Mention message log",
                url=m.jump_url,
                description=m.content
            )
            mention_embed.set_author(name=m.author, icon_url=m.author.display_avatar.url)
            mention_embed.set_footer(text=f"at: {dt.now().strftime(STRFTIME_ARG)}, uid: {m.author.id}, mid: {m.id}")
            await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=mention_embed)

        if m.guild.id == METS_SERVER_ID and m.type.value == 7:
            await m.channel.send(view=NewMemberAuthButton(member=m.author, join_message=m))

        if m.content.startswith("!fwhitelist add") and m.channel.id == 1074249475167621171:
            user_info = m.content.lstrip("!fwhitelist add ")

            if not (re.fullmatch(
                r"(BE.)?[a-zA-Z0-9]{3,64} ?\+ ?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
                ,user_info
                )
            ):
                match_result = re.search(
                    r"(BE.)?[a-zA-Z0-9_]{3,64} ?\+ ?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                    user_info
                )
                if match_result:
                    invalid_part = user_info[match_result.start():match_result.end()]
                    await m.reply(f"有効なユーザー名とUUIDのセットではありません\n```{invalid_part}```以下のような構文を参考にしてください\n```SuperTestUser123+00000000-0000-0000-0009-01f9d89da5ab```")
                else:
                    await m.reply("有効なユーザー名とUUIDのセットではありません、以下のような構文を参考にしてください\n```SuperTestUser123+00000000-0000-0000-0009-01f9d89da5ab```")
            else:
                user_info = user_info.replace(" ", "").split("+")
                user_data = {
                    "uuid": user_info[1],
                    "name": user_info[0]
                }
                with open("C:/Users/crab_/OneDrive/デスクトップ/main-server/whitelist.json", "r", encoding="utf-8") as f:
                    whitelist: list = json.loads(f.read())
                whitelist.append(user_data)
                with open("C:/Users/crab_/OneDrive/デスクトップ/main-server/whitelist.json", "w", encoding="utf-8") as f:
                    additional_data = json.dumps(whitelist)
                    f.write(additional_data)
                await m.reply(f"```json\n{json.dumps(user_data, indent=4)}\n```\n({len(additional_data)}文字) をホワリスに書き込みました")
                with MCRcon(
                    SERVER_ACCESS["local_ip"],
                    SERVER_ACCESS["authentication"]["rcon_password"],
                    SERVER_ACCESS["ports"]["rcon"]
                ) as mcr:
                    execution = mcr.command("whitelist reload")
                    await m.reply(f"ホワリスを再読み込みしました: {execution}",mention_author=False)


        if m.interaction is not None:
            printe("Interaction in message.")
            if m.interaction.name == "dissoku up" and m.channel.id == 1074249472617480192: # bot commands channel
                timestamp = get_timestamp(dt.now().timestamp() + DISSOKU_COOLDOWN_SECONDS, "R")
                dissoku_up_notify = discord.Embed(
                    title="up通知",
                    description=f"upを検知しました、{timestamp}にもう一度通知します"
                )
                await m.channel.send(embed=dissoku_up_notify)
                await asyncio.sleep(DISSOKU_COOLDOWN_SECONDS)
                dissoku_up_notify = discord.Embed(
                    title="up通知",
                    description="**up**のクールダウンが終わりました\n</dissoku up:828002256690610256>から**up**が出来ます"
                )
                await m.channel.send("<@&1074249438928838707>",embed=dissoku_up_notify)

            if m.interaction.name == "bump" and m.channel.id == 1074249472617480192: # bot commands channel
                timestamp = get_timestamp(dt.now().timestamp() + BUMP_COOLDOWN_SECONDS, "R")
                bump_notify = discord.Embed(
                    title="bump通知",
                    description=f"bumpを検知しました、{timestamp}にもう一度通知します"
                )
                await m.channel.send(embed=bump_notify)
                await asyncio.sleep(BUMP_COOLDOWN_SECONDS)
                bump_notify = discord.Embed(
                    title="bump通知",
                    description="**bump**のクールダウンが終わりました\n</bump:947088344167366698>から**bump**出来ます"
                )
                await m.channel.send("<@&1074249438928838707>",embed=bump_notify)

        if re.match(r"https?:\/\/.*chonmage\.png.*\/?",m.content):
            await m.delete()
        if "<:crab:1108300671654043648>" in m.content or "<:__:1108301886471295069>" in m.content or "<:rewsnghbyeaiumghuipaemhgaeupimhg:1108302306258206750>" in m.content or"<a:rewsnghbyeaiumghugraehgeamhuieag:1108303848621211718>" in m.content or "<:kanininininiinniiinniinn:1108302015785873418>" in m.content:
            await m.delete()

        if re.match(r"https://(canary\.)?discord\.com/channels/\d*/\d*/\d*/?",m.content):
            printe("Messsage link in message content")
            latest_temp_datas["openable_discord_message_link"] = m.id
            await m.add_reaction("🔗")

#         if m.channel.id == 1074249466024034334: # DiscordSRV CHannel
#             if m.attachments != []:
#                 for a in m.attachments:
#                     if a.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
#                         mcify_image = Image.open(BytesIO(await a.read()))
#                         mcify_jsonized = '{"text":"[添付画像]","color":"#22ffff","hoverEvet":{"action":"show_text","value":<ImageComponent>}}'.replace(
#                             "<ImageComponent>",
#                             image_to_jsoncomponent(mcify_image)
#                         )
#                         # NOTE: 改行したあとreplaceで改行を治してます、見やすいんで
#                         mcify_rcon_command = f"""
# {EXTERNAL_RCON_PATH}
#  -H {RCON_ACCESS['local_ip']}
#  -P {RCON_ACCESS['port']}
#  -p {RCON_ACCESS['password']}
#  \"tellraw @a {mcify_jsonized}\"
# """[1:-1].replace("\n","")
#                         process = subprocess.Popen(mcify_rcon_command,bufsize=-1)
#                         process.wait()
#                         await m.add_reaction("📸")
#             elif re.fullmatch(r"https?:\/\/.*\.discord\.com\/.*\.(png|jpg|jpeg|gif)",m.content):
#                 "リンクの画像だった場合の処理"

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
                await m.channel.send(
                    embeds=[
                        weather_info_embed_title,
                        weather_info_embed_weather,
                        weather_info_embed_rainluck,
                        weather_info_embed_temp
                    ]
                )

        if m.content == "<@985254515798327296>":
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,3))
            await m.channel.send("</help:1063776235156672632>でコマンドのヘルプを表示できるよ")
            return

        if m.content.startswith("!changeFreqTo ") and m.guild.id == 939072966908596255:
            try:
                freq_id = int(m.content.lstrip("!changeFreqTo "))
            except ValueError:
                await m.channel.send("使用できないIDです")
                return
            latest_temp_datas["received_dm_user_id"] = freq_id
            dm_connected_user = client.get_user(freq_id)
            await m.channel.send(
                embed=discord.Embed().set_author(
                    name=f"DMの送信先を{dm_connected_user}({freq_id})に変更しました",
                    icon_url=m.author.display_avatar.url
                )
            )
            return

        if m.channel.id == 1065610631618764821:
            sendable_dm_content = m.content
            dm_channel_delete_after = None
            dm_channel_use_tts = False
            files = [await a.to_file() for a in m.attachments] if m.attachments != [] else None
            if "--showAuthor" in m.content:
                sendable_dm_content = sendable_dm_content.replace("--showAuthor","")
                sendable_dm_content += f"by{m.author.name}"
            if "--deleteAfterASecond" in m.content:
                sendable_dm_content = sendable_dm_content.replace("--deleteAfterASecond","")
                dm_channel_delete_after = 1
            if "--deleteAfterAMinute" in m.content:
                sendable_dm_content = sendable_dm_content.replace("--deleteAfterAMinute","")
                dm_channel_delete_after = 60
            if "--deleteAfterAHour" in m.content:
                sendable_dm_content = sendable_dm_content.replace("--deleteAfterAHour","")
                dm_channel_delete_after = 3600
            if "--useTTS" in m.content:
                sendable_dm_content = sendable_dm_content.replace("--useTTS","")
                dm_channel_use_tts = True
            await client.get_user(latest_temp_datas["received_dm_user_id"]).send(
                sendable_dm_content,
                files=files,
                delete_after=dm_channel_delete_after,
                tts=dm_channel_use_tts
            )
            return

        if m.channel.id == 1111569746815615056 and m.attachments != []:
            await m.attachments[0].save("C:/Users/crab_/OneDrive/デスクトップ/saved-bgimage.png")
            printe(f"activated bgimage changer, saved image: {m.attachments[0].filename}")
            ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:/Users/crab_/OneDrive/デスクトップ/saved-bgimage.png" , 0)
            await m.add_reaction("✅")

    ### 生きるこめたん
        if re.match(r"((子|小)met|こめたん)",m.content):
            printe(f"My name is in the received message :D")
            kometan_messages = ["こめたん" in msg.content async for msg in m.channel.history(limit=10)]
            if any(kometan_messages[1:]):
                printe(f"kometans is already sent by others: {kometan_messages}")
                return
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(.25,2))
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
                printe("Calling to Kawasan")
                return
                async with m.channel.typing():
                    await asyncio.sleep(random.uniform(1,2))
                # choiced_kawasan_mention = random.choice(["<@964438295440396320>","<@628513445964414997>"])
                await m.channel.send(f"<@964438295440396320> HEY")
        if re.fullmatch(r"(?i)(おい|hey)(かえ|加絵|カエ)(さん)?(!|！|~|～){1,10}?",m.content):
            printe("Calling to Kae")
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            await m.channel.send("助けてっ！かえぱんま～ん！！！！||<@940522481079451708>||")
        if re.fullmatch(r"(?i)(hey|oi|おい)(kani|ni|に|かに|カニ|蟹)(さん|san)?(!|！|~|～){1,10}?",m.content):
            printe("Calling to Crab55e")
            async with m.channel.typing():
                await asyncio.sleep(
                    random.uniform(1,2)
                )
            if re.fullmatch(r"(?i)hey(kani|ni|かに|カニ|蟹)(san|さん)?(!|！|~|～){1,10}?",m.content):
                async with m.channel.typing():
                    await asyncio.sleep(1)
                await m.channel.send(
                    random.choice(
                        [
                            "<@776726560929480707> 呼ばれてるよ～",
                            "<@776726560929480707> よばれてるよ～～"
                        ]
                    )
                )
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
            async for history_message in m.channel.history(limit=10):
                if history_message.content == "がんば":
                    return
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
                    await m.reply(content="なす？\nhttps://cdn.discordapp.com/attachments/1014533269183803462/1107601002804293722/yonda.gif",mention_author=False)
                else:
                    await m.reply("なす？\nhttps://media.discordapp.net/attachments/1055151855950372874/1055756068728361010/image.gif",mention_author=False)

        if re.fullmatch(r"(グー|チョキ|パー|ぐー|ちょき|ぱー)(!|~|！|～)?",m.content):
            async with m.channel.typing():
                await asyncio.sleep(1)
            await m.channel.send(f'{random.choice(["グー","チョキ","パー"])}！！')

        if (m.channel.id == CHANNEL_IDS["shiritori_channel"] or m.channel.id == 1030093892273590345) and not m.author.bot: # juice shiritori channel
            printe("Detected shiritori",label="Shiritori")
            if len(m.content) >= 50:
                printe("is too long content",label="Shiritori")
                return
            if m.content.startswith(("|","(","（","!","!EXCLUDE")):
                printe("is invalid answer",label="Shiritori")
                return

            with open("storage/json/shiritori_database.json", "r",encoding="utf-8") as shiritori_file:
                shiritori_data = json.loads(shiritori_file.read())
            if random.randrange(1,5) == 1:
                printe(f"Answering shiritori: {m.content}",label="Shiritori")
                try:
                    shiritori_answering_content = random.choice(shiritori_data[m.content])
                    async with m.channel.typing():
                        await asyncio.sleep(0.25)
                    await m.channel.send(shiritori_answering_content)
                    printe(f"Answered Shiritori: {shiritori_answering_content}")
                except KeyError:
                    printe(f"IDK Content...",label="Shiritori")
            else:
                printe("Writing content to Database...",label="Shiritori")
                async for history_message in m.channel.history(limit=2):
                    if not (history_message.content == m.content):
                        try:
                            shiritori_data[history_message.content].append(m.content)
                        except KeyError:
                            shiritori_data[history_message.content] = []
                            shiritori_data[history_message.content].append(m.content)
                with open("storage/json/shiritori_database.json", "w",encoding="utf-8") as shiritori_file:
                    shiritori_file.write(json.dumps(shiritori_data))
                printe("Writed.",label="Shiritori")

        if m.channel.id == CHANNEL_IDS["rinnable_channel"] and random.randrange(1,50) == 1:
            async with m.channel.typing():
                await asyncio.sleep(1)
            printe("Replying as Rinna")
            rinna_request_body = {
                "rawInput": "",
                "outputLength": 25,
                "character":"rinna",
                "firstPerson":"こめたん"
            }

            rinna_request_body["rawInput"] = f"B: {m.content}A:"
            rinna_request_header = {
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
                "Ocp-Apim-Subscription-Key": "HIDED"
            }
            rinna_response = requests.post(
                "https://api.rinna.co.jp/models/cce",
                headers=rinna_request_header,
                json=rinna_request_body
            )
            rinna_answer_content = json.loads(rinna_response.text)["answer"]
            rinna_answer_content = rinna_answer_content.replace(
                    "〈あなた〉",
                    m.author.name
                ).replace(
                    "〈わたし〉",
                    "こめたん"
                )
            await m.reply(rinna_answer_content,mention_author=False)
        # if m.author.id == 945878551805165608 and m.guild.id == METS_SERVER_ID:
        #     kae = client.get_user(940522481079451708)
        #     pencil_message_notify_embed = discord.Embed(
        #         title="ﾋﾟﾂｯ",
        #         url=m.jump_url,
        #         description=m.content
        #     ).set_author(
        #         icon_url=m.author.avatar.url,
        #         name=m.author
        #     )
        #     await kae.send(embed=pencil_message_notify_embed)
        if m.content == "/break 2B_enpitsu":
            normal_enpitsu = discord.File("storage/images/static/normal.png")
            broken_enpitsu = discord.File("storage/images/static/break.png")
            not_broken_enpitsu_message = await m.channel.send(files=[normal_enpitsu])
            await asyncio.sleep(1)
            await not_broken_enpitsu_message.edit(attachments=[broken_enpitsu])


    async def on_invite_create(self, invite: discord.Invite):
        if not invite.guild.id == METS_SERVER_ID:
            return
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

    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.User,discord.Member]):
        if user.bot:
            return
        printe(f"Reaction added by {user}",label="Event")
        reaction_add_embed = discord.Embed(
            title="Reaction add event",
            url=reaction.message.jump_url,
            description=f"{reaction.emoji} by<@{user.id}> total: **{reaction.count}**"
        )
        reaction_add_embed.set_author(name=user,icon_url=user.display_avatar.url)
        if user.guild.id == METS_SERVER_ID:
            await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=reaction_add_embed)

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
            ikaf_generic_disclaimer_embed.add_field(
                name="以下の内容は上記に記した事項を踏まえたうえで読んでください",
                value="という便利なやつ"
            )
            await reaction.message.channel.send(embed=ikaf_generic_disclaimer_embed)
            latest_temp_datas["ikaf_generic_disclaimer"] = 0

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        printe(f"Reaction removed by {user}",label="Event")
        reaction_add_embed = discord.Embed(
            title="Reaction remove event",
            url=reaction.message.jump_url,
            description=f"{reaction.emoji} by<@{user.id}> total: **{reaction.count}**"
        )
        reaction_add_embed.set_author(name=user,icon_url=user.display_avatar.url)
        if user.guild.id == METS_SERVER_ID: 
            await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=reaction_add_embed)

    async def on_app_command_completion(
        self,
        interaction: discord.Interaction,
        command: Union[app_commands.Command,app_commands.ContextMenu]
    ):
        printe(f"{interaction.user} issued command: /{command.qualified_name}")
        if type(command) == app_commands.Command:
            params_description = "**Params: **"
            for param in command.parameters:
                params_description += f"\n| `{param.display_name}` / {param.description}"
            app_command_completion_embed = discord.Embed(
                title=f"{interaction.user.display_name} issued Command: \"/{command.qualified_name}\"",
                description=params_description
                )
        elif type(command) == app_commands.ContextMenu:
            app_command_completion_embed = discord.Embed(
                title=f"{interaction.user.display_name} issued ContextMenu: \"{command.qualified_name}\"",
                description=f"**Type: **\n{command.type}"
                )
        app_command_completion_embed.set_author(name=interaction.user,icon_url=interaction.user.display_avatar.url)
        app_command_completion_embed.set_footer(text=f"at: {dt.now().strftime(STRFTIME_ARG)}, uid: {interaction.user.id}")
        await client.get_channel(CHANNEL_IDS["message_events"]).send(embed=app_command_completion_embed)

    async def on_member_join(self, member: discord.Member):
        printe(f"Member joined: {member}, to {member.guild.name}",label="Event")

        # if member.guild.id == METS_SERVER_ID:
        #     pass
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
                    description = f"Met\'s サーバーへようこそ！！！"
                elif "6" in str(member_count):
                    description = f"Met\'s サーバーへようこそ！！！"
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
                icon_url=MINI_MET_AVATAR_URL
            )
            welcome_message_embed_introduction = discord.Embed(
                title="1. 自己紹介をする",
                description=f"""
<#949994602427994113>で自己紹介を書きましょう
テンプレートがあるので、必要に応じて書き変えて使いましょう

もし、上記のチャンネルが\"アクセスなし\"となっているならば
先に右下のルール確認などを終わらせましょう

更に、現在はセキュリティ向上のため認証システムを入れています
<#842320961033601046>で<@&1074249433652412427>の誰かが認証してくれるのを待ちましょう
もしわからなければ<#1074249460051353620>でヘルプを求めましょう
```
名前：{member.global_name if member.global_name != None else member.name}
好きなもの＆事：マイクラ！
JAVA/統合：主にJava Edition、たまに統合版
MCID：{member.name}
どこから来たか：○○の掲示板
一言：冒険が大好きです！一緒にダンジョン攻略しませんか？
```
"""[1:-1],
                color=THEME_COLOR_HEX
            )
            welcome_message_embed_whitelist = discord.Embed(
                title="2. ホワイトリスト登録をする",
                description=f"""
<#1074249454741368943>でホワイトリストに登録しましょう
自分のMCID(ゲーム内での名前)を送ります
例: 「java版: Notch61」
統合版を使用している場合は一度<#1074249454741368943>で申請をした後、認可される前に
IP:{SERVER_ACCESS["domain"]}、ポート{SERVER_ACCESS["ports"]["bedrock"]}に接続する必要があります
<@&1074249415679815780>によって追加されると、サーバーに入れるようになります！
"""[1:-1],
                color=THEME_COLOR_HEX
            )
            welcome_message_embed_join = discord.Embed(
                title="3. 参加する",
                description=f"""
サーバーに参加します
IPは、
Java版: `{SERVER_ACCESS["domain"]}`
統合版: `{SERVER_ACCESS["domain"]}`(ポート: `{SERVER_ACCESS["ports"]["bedrock"]}`)
詳しくは<#1074249451041992776>、または<#1074249460051353620>でサポートを受けることもできます、遠慮なくお問い合わせください
"""[1:-1],
                color=THEME_COLOR_HEX
            )
            now = dt.now()
            welcome_channel_delete_time = now + datetime.timedelta(days=3)
            welcome_channel_delete_time = f"<t:{round(welcome_channel_delete_time.timestamp())}:R>"
            welcome_message_embed_talking = discord.Embed(
                title="4. 終わりに",
                description=f"""
何か不明な点や質問などあれば**ぜひ**<#1074249460051353620>
このチャンネルはあなたのためのチャンネルです、ある程度自由に使っていただいて構いませんが
{welcome_channel_delete_time}に削除されますのでご注意ください
それでは行ってらっしゃい！
"""[1:-1],
                color=0x2b2d31
            )
            embeds = [
                welcome_message_embed,
                welcome_message_embed_introduction,
                welcome_message_embed_whitelist,
                welcome_message_embed_join,
                welcome_message_embed_talking
            ]
            welcome_channel_overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True
                )
            }
            welcome_channel_category = member.guild.get_channel(1145334535949656105)
            # 1145334535949656105
            welcome_channel = await welcome_channel_category.create_text_channel(
                name=f"{member.display_name}！ようこそ！",
                topic=f"{member}さん専用のウェルカムチャンネルです",
                reason="text-channel created by welcome-message feature",
                overwrites=welcome_channel_overwrites
            )
            await welcome_channel.send(content=member.mention,embeds=embeds,view=CloseWelcomeChannel())
            printe(f"Sent welcome message on #{welcome_channel.name}")
            await asyncio.sleep(timescale.day * 3)
            await welcome_channel.delete(reason="text-channel deleted by welcome-message feature")

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
tree = client.tree



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
    await interaction.response.defer()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory()
    proxy_server_status = SLPClient(SERVER_ACCESS["local_ip"],port=SERVER_ACCESS["ports"]["proxy"]).get_status()
    game_server_status = SLPClient(SERVER_ACCESS["local_ip"],port=SERVER_ACCESS["ports"]["java"]).get_status()
    tap_endpoint = f'http://{SERVER_ACCESS["local_ip"]}:{SERVER_ACCESS["ports"]["tap"]}/v1/server'
    tap_headers = {"key": SERVER_ACCESS["authentication"]["servertap_key"]}
    raw_tap_plugin_status = requests.get(tap_endpoint, headers=tap_headers).text
    tap_plugin_status = json.loads(raw_tap_plugin_status)
    tps = float(tap_plugin_status["tps"])
    if tps >= 19.0:
        tps_message = "正常"
    elif tps >= 15.0:
        tps_message = "少し低め"
    elif tps >= 10.0:
        tps_message = "低い"
    elif tps >= 5.0:
        tps_message = "かなり低い"
    elif tps >= 0.0:
        tps_message = "異常"

    status_embed = discord.Embed(title="ステータス", description="IPやバージョン等の情報", color=THEME_COLOR_HEX)
    status_embed.add_field(name="Java / IP", value=f'`{SERVER_ACCESS["domain"]}`', inline=True)
    status_embed.add_field(name="統合版 / IP", value=f'`{SERVER_ACCESS["domain"]}`', inline=True)
    status_embed.add_field(name="統合版 / ポート", value=f'`{SERVER_ACCESS["ports"]["bedrock"]}`', inline=True)
    status_embed.add_field(name="CPU使用率",value=f"{cpu_usage}%", inline=True)
    status_embed.add_field(name="メモリ使用率",value=f"{memory_usage.percent}%", inline=True)
    status_embed.add_field(name="TPS",value=f'{tps} / {tps_message}', inline=True)
    status_embed.add_field(name="メイン鯖",value=f"{game_server_status.res['status']}", inline=True)
    status_embed.add_field(name="プロキシ鯖",value=f"{proxy_server_status.res['status']}", inline=True)
    status_embed.set_footer(text=f"ver: {proxy_server_status.version.name.replace('Velocity ','')}, 情報更新: 2023/08/31")
    await interaction.followup.send(embed=status_embed)

@tree.command(name="invite",description="サーバーの招待リンクを取得")
@app_commands.guilds(METS_SERVER_ID)
async def invite(interaction: discord.Interaction):
    invite_embed = discord.Embed(
        title="招待リンク",
        description="サーバーの招待リンクです\nいろんなところ共有してください！\n**```https://discord.mets-svr.com```**",
        color=0x22ff22
    )
    view = discord.ui.View().add_item(discord.ui.Button(label='招待リンク', url='https://discord.mets-svr.com/'))
    await interaction.response.send_message(view=view,embed=invite_embed)

@tree.command(name="web",description="サーバーのwebリンクを表示")
@app_commands.guilds(METS_SERVER_ID)
async def web(interaction: discord.Interaction):
    web_embed = discord.Embed(
        title="webサイト",
        description="サーバーの公式webサイトです\n更新がめんどくてめんどくて...\n**```https://mets-svr.com```**",
        color=0x22ff22
    )
    view = discord.ui.View().add_item(discord.ui.Button(label='webサイト', url='https://mets-svr.com/'))
    await interaction.response.send_message(view=view,embed=web_embed)

@tree.command(name="map",description="サーバーのマップのリンクを確認")
@app_commands.guilds(METS_SERVER_ID)
async def map(interaction: discord.Interaction):
    web_embed = discord.Embed(
        title="マップ",
        description="サーバーのマップです\n空からワールドを眺めたりできます\n動作していないこともあります...\n**```http://map.mets-svr.com/```**",
        color=0x22ff22
    )
    view = discord.ui.View().add_item(discord.ui.Button(label='マップ', url='http://map.mets-svr.com/'))
    await interaction.response.send_message(view=view,embed=web_embed)

@tree.command(name="set-birthday",description="誕生日を設定して、関連する様々な機能を有効化します")
@app_commands.guilds(METS_SERVER_ID)
async def set_birthday(interaction: discord.Interaction):
    await interaction.response.send_modal(SetBirthday())
# @tree.command(name="set-birthday", description="誕生日を設定して、関連する様々な機能を有効化します")
# @app_commands.guilds(METS_SERVER_ID)
# async def set_birthday(interaction: discord.Interaction):
#     await interaction.response.send_modal(SetBirthday())



manage_promote_contents = app_commands.Group(name="sc", description="マイクラ鯖に関するコマンド")


global_books = app_commands.Group(name="books", description="本を読み、出版し、修正し、提供できます")
@global_books.command(name="write", description="本を出版します")
async def write(interaction: discord.Interaction):
    await interaction.response.send_message("books.write.res")

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
    embed = discord.Embed(title=title,description=content,color=0xff1111)
    embed.set_footer(text=f"{to.guild.name} - {dt.now().strftime(STRFTIME_ARG)}")
    if author == True:
        embed.set_author(
            name=interaction.user,
            icon_url=interaction.user.display_avatar.url,
            url=f"https://discord.com/users/{interaction.user.id}"
        )
    if attachment is not None:
        file = await attachment.to_file()
        await to.send(embed=embed,file=file)
    else:
        await to.send(embed=embed)
    await interaction.response.send_message("正常に送信されました↓",embed=embed,ephemeral=True)

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
            await interaction.response.send_message(
                f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{self.code.value}\n```",
                ephemeral=True
            )

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
            await interaction.user.send(
                f"{interaction.created_at.strftime(STRFTIME_ARG)}に受け取ったsubprocessの実行が終了しました\n```py\n{result}\n```"
            )
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
                    await interaction.response.send_message(
                        f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{code}\n```", ephemeral=True)
                else:
                    await interaction.response.send_message(f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{code}\n```",
                    ephemeral=True
                )
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
                await interaction.user.send(
                    f"{interaction.created_at.strftime(STRFTIME_ARG)}に受け取ったsubprocessの実行が終了しました\n```py\n{result}\n```"
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"エラーが発生しました\n```py\n{e}\n```コード: \n```py\n{code}\n```",
                    ephemeral=True
                )
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
        await interaction.response.send_message(
            f"ユーザー数に対するグループのメンバーが多すぎます\n**{len(users)}**人 | **{members}**メンバー",
            ephemeral=True
        )
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
    embed_text = f"""
{target.mention}に{role.mention}を付与しました
このロールは{seconds_to_string(wait_duration,'**%w**週間 **%d**日 **%h**時間 **%m**分 **%s**秒後')}に剥奪されます
"""[1:-1]
    embed = discord.Embed(description=embed_text)
    embed.set_author(icon_url=target.display_avatar.url,name=target)
    await interaction.response.send_message(embed=embed)
    await asyncio.sleep(wait_duration)
    if notify_to_dm is not None:
        notify_embed = discord.Embed(
            title="temp-role機能の効果が終了しました",
            description=f"付与: {interaction.user.mention}\n付与先: {target.mention}"
        )
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
        *args,
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
    await interaction.response.defer()
    async with interaction.channel.typing():
        process = subprocess.run(["speedtest","--json"], capture_output=True)
        speed = json.loads(process.stdout)
        speed["download"] = round(speed["download"] / 1024 / 1024,3)
        speed["upload"] = round(speed["upload"] / 1024 / 1024,3)
    await interaction.followup.send(
        content=f':arrow_up: up: {speed["upload"]}Mbps\n:arrow_down: down: {speed["download"]}Mbps\nping: {speed["ping"]}ms'
    )

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

@tree.command(name="get-timestamp", description="モダンなタイムスタンプを作成します")
@app_commands.describe(
    time="時間（例: 「2021/05/13 08:42.30」）",
    time_format="出力フォーマット"
)
@app_commands.choices(
    time_format=[
        app_commands.Choice(name="<時間>:<分>",value="t"),
        app_commands.Choice(name="<時間>:<分>.<秒>",value="T"),
        app_commands.Choice(name="<年>/<月>/<日>",value="d"),
        app_commands.Choice(name="<年>年<月>月/<日>",value="D"),
        app_commands.Choice(name="<年>年<月>月/<日> <時間>:<分>（デフォルト）",value="f"),
        app_commands.Choice(name="<年>年<月>月/<日> <曜日> <時間>:<分>",value="F"),
        app_commands.Choice(name="<年または月、日、分、秒><前または後>（相対）",value="R")
    ]
)
async def get_timestamp(interaction: discord.Interaction, time: str, time_format: Optional[str] = "f"):
    time_space_separated = time.replace("/"," ").replace(":"," ").replace("."," ")
    try:
        time_list = [int(s) for s in time_space_separated.split(" ")]
    except ValueError:
        error_message = f"""
指定された時間の形式に無効な文字が含まれています: `{time}`
以下のようなフォーマットを参考にもう一度お試しください
```2021/05/13 08:42.30```
"""[1:-1]
        await interaction.response.send_message(error_message, ephemeral=True)
        return

    if len(time_list) != 6:
        error_message = f"""
指定された時間の形式が正しくありません: `{time}`
以下のようなフォーマットを参考にもう一度お試しください
```2021/05/13 08:42.30```
"""[1:-1]
        await interaction.response.send_message(error_message, ephemeral=True)
        return

    dt_time = dt(time_list[0], time_list[1], time_list[2], time_list[3], time_list[4], time_list[5])
    timestamp_int = int(dt_time.timestamp())
    await interaction.response.send_message(f"出力: `<t:{timestamp_int}:{time_format}>`\n参考: <t:{timestamp_int}:{time_format}>")


@tree.command(name="ping", description="ただのping")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! {latency}ms")



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
        response_message = """
🚫使用制限にかかりました
mini-met premiumにご登録いただければ月々777円で100万種類以上の機能にアクセスできます
詳細↓||嘘です！！！！！！！！！！！！！！||
"""[1:-1]
        await interaction.response.send_message(response_message)
        return
    for attachment in message.attachments:
        await attachment.save(f"storage/images/gifificated/{message.id}-by-{message.author.id}.png")
        result_file = await attachment.to_file(filename=f"gifificated-{attachment.filename}.gif")
        result_files.append(result_file)
    await interaction.response.send_message(content="ぎっふぃっふぃ...",files=result_files)

@tree.context_menu(name="報告する")
async def report_this_messsage(interaction: discord.Interaction, message: discord.Message):
    # view = ReportConfirm()
    # await interaction.response.send_message("本当に報告しますか？",view=view,ephemeral=True)
    # await view.wait()
    # if view.value is None:
    #     return
    # elif view.value == False:
    #     return
    embed = discord.Embed(
        title="メッセージが報告されました",
        description=f"メッセージ: {message.content}\n\n**しばらくした後に詳細が送られます**", url=message.jump_url
    )
    embed.set_author(icon_url=message.author.display_avatar.url,name=message.author)
    embed.set_footer(text=f"AT: {dt.now().strftime(STRFTIME_ARG)}, InterUID: {interaction.user.id}, MID: {message.id}")
    await client.get_channel(CHANNEL_IDS["report_datas"]).send(embed=embed)
    await interaction.response.send_modal(ReportThisMessage())

@tree.context_menu(name="Translate/翻訳")
async def translate_this(interaction: discord.Interaction, message: discord.Message):
    if not re.fullmatch(NASU_REGEX,message.content):
        translated = Translator().translate(
            message.content,
            dest=str(interaction.locale) if len(interaction.locale) == 2 else str(interaction.locale)[:2]
        )
        embed = discord.Embed(title=f"Translated {translated.src}-to-{translated.dest}",url=message.jump_url, description=translated.text)
        embed.set_author(name=message.author,icon_url=message.author.display_avatar.url)
        await interaction.response.send_message(embed=embed,ephemeral=True,view=TranslateMenu(message))
    else:
        translated_content = message.content.replace(
            "🍆な🍆","あ").replace(
            "🍆ナ🍆","い").replace(
            "🍆ﾅ🍆","う").replace(
            "🍆na🍆","え").replace(
            "🍆NA🍆","お").replace(
            "🍆つ🍆","か").replace(
            "🍆っ🍆","き").replace(
            "🍆ツ🍆","く").replace(
            "🍆ッ🍆","け").replace(
            "🍆ｯ🍆","こ").replace(
            "🍆tu🍆","さ").replace(
            "🍆TU🍆","し").replace(
            "🍆す🍆","す").replace(
            "🍆ス🍆","せ").replace(
            "🍆ｽ🍆","そ").replace(
            "🍆su🍆","た").replace(
            "🍆SU🍆","ち").replace(
            "🍆なっ🍆","つ").replace(
            "🍆ナッ🍆","て").replace(
            "🍆ﾅｯ🍆","と").replace(
            "🍆なす🍆","な").replace(
            "🍆ナス🍆","に").replace(
            "🍆ﾅｽ🍆","ぬ").replace(
            "🍆nasu🍆","ね").replace(
            "🍆NASU🍆","の").replace(
            "🍆っす🍆","は").replace(
            "🍆ッス🍆","ひ").replace(
            "🍆ｯｽ🍆","ふ").replace(
            "🍆ﾅす🍆","へ").replace(
            "🍆なｽ🍆","ほ").replace(
            "🍆ナす🍆","ま").replace(
            "🍆なス🍆","み").replace(
            "🍆NAｽ🍆","む").replace(
            "🍆ナｽ🍆","め").replace(
            "🍆ﾅス🍆","も").replace(
            "🍆ｎａｓｕ🍆","や").replace(
            "🍆ｎａ🍆","ゆ").replace(
            "🍆ｓｕ🍆","よ").replace(
            "🍆ns🍆","ら").replace(
            "🍆ﾅっす🍆","り").replace(
            "🍆ﾅｯす🍆","る").replace(
            "🍆ナっｽ🍆","れ").replace(
            "🍆なっsu🍆","ろ").replace(
            "🍆NaSu🍆","わ").replace(
            "🍆nAｽ🍆","を").replace(
            "🍆ナｯす🍆","ん").replace(
            "🍆Nasu🍆","ゃ").replace(
            "🍆Na🍆","ゅ").replace(
            "🍆Su🍆","ょ").replace(
            "🍆nA🍆","っ").replace(
            "🍆なs🍆","ぁ").replace(
            "🍆ナs🍆","ぃ").replace(
            "🍆ﾅs🍆","ぅ").replace(
            "🍆nas🍆","ぇ").replace(
            "🍆NAs🍆","ぉ")
        embed = discord.Embed(title="なす語翻訳",description=translated_content)
        embed.set_author(name=message.author,icon_url=message.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)

@tree.context_menu(name="その他")
async def other(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(view=ContextMenuOther(message),ephemeral=True)

@tree.context_menu(name="子met")
async def main(interaction: discord.Interaction, member: discord.Member):
    userinfo_embed = discord.Embed(
        color=0x2b2d31
    ).set_author(name=member, icon_url=member.display_avatar.url)
    valid_ids = [r.id for r in interaction.user.roles]
    if not (1074249415679815780 in valid_ids or 1074177848337764372 in valid_ids):
        await interaction.response.send_message(view=MemberContextMenuMain(member=member), embed=userinfo_embed, ephemeral=True)
    else:
        await interaction.response.send_message(view=MemberContextMenuMainForAdmin(member=member), embed=userinfo_embed, ephemeral=True)

client.run(token=BOT_TOKEN)
