import json
import datetime
import discord
import ctypes

ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 0x0007)
STRFTIME_ARG = "%Y-%m-%d %H:%M.%S"

def log(content: str = "Empty") -> str:
    print(f"\033[032m[{datetime.datetime.now().strftime(STRFTIME_ARG)} / NEListen]", content,"\033[0m")
    return f"[NEListen] {content}"


log("Loading...")


intents = discord.Intents.all()
client = discord.Client(intents=intents)

with open("env.json","r") as f:
    ENV = json.loads(f.read())
BOT_TOKEN = ENV["bot_token"]
CONTENTS_FILE_PASS = "C:/Users/crab_/OneDrive/デスクトップ/codes/python-codes/auto-postings/contents.json"
METS_SERVER_ID = 842320961033601044


@client.event
async def on_ready():
    # 変数
    log_channel = client.get_channel(1074249516871602227)
    now = datetime.datetime.now()

    # 起動メッセージ
    log("Ready!")
    log(f"status:\n- at {now.strftime(STRFTIME_ARG)}\n- discord.py ver: {discord.__version__}")
    on_ready_log_embed = discord.Embed(
        title=f":white_check_mark: イベントが出来たら宣伝の内容に追加するやつが起動しました",
        description=now.strftime(STRFTIME_ARG),
        color=0x00ff00
    )
    await log_channel.send(embed=on_ready_log_embed)


@client.event
async def on_scheduled_event_create(event: discord.ScheduledEvent):
    log("Catched new event")
    if event.guild.id != METS_SERVER_ID:
        log("Isn't mets event")
        return
    log("Catched event has mets event!, opening data-file...")
    with open(CONTENTS_FILE_PASS, "r", encoding="utf-8") as file_read:
        contents_json = json.loads(file_read.read())

    contents_json["events"]["enabled"] = True
    contents_json["events"]["contents"][f"{event.id}"] = {
        "enable": True,
        "name": event.name,
        "description": discord.utils.remove_markdown(event.description),
        "times":
            {
                "start": event.start_time.strftime(STRFTIME_ARG),
                "end": event.end_time.strftime(STRFTIME_ARG)
            }
    }
    with open(CONTENTS_FILE_PASS, "w", encoding="utf-8") as file_write:
        file_write.write(json.dumps(contents_json))
    log(f"Writed new event: {event.name}")


@client.event
async def on_scheduled_event_delete(event: discord.ScheduledEvent):
    log("Catched deleted event")
    if event.guild.id != METS_SERVER_ID:
        log("Isn't mets event")
        return
    log("Catched event has mets event!, opening data-file...")
    with open(CONTENTS_FILE_PASS, "r", encoding="utf-8") as file_read:
        contents_json = json.loads(file_read.read())

    contents_json["events"]["enabled"] = True
    contents_json["events"]["contents"].pop(f"{event.id}")

    if len(contents_json["events"]["contents"]) >= 0:
        contents_json["events"]["enabled"] = False

    with open(CONTENTS_FILE_PASS, "w", encoding="utf-8") as file_write:
        file_write.write(json.dumps(contents_json))
    log(f"Deleted event: {event.name}")


@client.event
async def on_scheduled_event_update(before: discord.ScheduledEvent, after: discord.ScheduledEvent):
    log("Catched updated event")
    if before.guild.id != METS_SERVER_ID:
        log("Isn't mets event")
        return
    log("Catched event has mets event!, opening data-file...")
    with open(CONTENTS_FILE_PASS, "r", encoding="utf-8") as file_read:
        contents_json = json.loads(file_read.read())

    contents_json["events"]["enabled"] = True
    contents_json["events"]["contents"][f"{after.id}"] = {
        "enable": True,
        "name": after.name,
        "description": discord.utils.remove_markdown(after.description),
        "times":
            {
                "start": after.start_time.strftime(STRFTIME_ARG),
                "end": after.end_time.strftime(STRFTIME_ARG)
            }
    }
    with open(CONTENTS_FILE_PASS, "w", encoding="utf-8") as file_write:
        file_write.write(json.dumps(contents_json))
    log(f"Writed updated event: {after.name}({before.name})")

client.run(BOT_TOKEN)
