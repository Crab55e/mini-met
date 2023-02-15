# initial variables
console_prefix = "[MM.GChat]"

# libraries
print(console_prefix,"Importing Libraries...")
from datetime import datetime as dt
from time import sleep
import asyncio
import discord
import json
print(console_prefix,"Libraries has been Imported!")

# main variables
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot_token = "ﾄｹﾝｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯ"

global_chat_data = open("storage/json/global_chat.json","r",encoding="utf-8")
global_chat_data = json.load(global_chat_data)
mini_met = client.get_user(985254515798327296)
print(console_prefix,"Variables has been Defined!")

print(console_prefix,"trying main task")
try:
    # 起動時イベント
    @client.event
    async def on_ready():
        now = dt.now()
        log_channel = client.get_channel(965269631050862622)
        global all_guild
        all_guild = []
        for guild in global_chat_data["guilds"]:
            all_guild.append(guild)

        on_ready_log_embed = discord.Embed(title=f":white_check_mark: 子metのグローバルチャット機能が起動しました",description="ステータス:",color=0x00ff00)
        on_ready_log_embed.add_field(name="起動日時: ",value=f"{now.strftime('%Y年 %m月 %d日  %H時%M分 %S秒')}")
        on_ready_log_embed.add_field(name="総Guild: ",value=f"{all_guild}")
        await log_channel.send(embed=on_ready_log_embed)
        print(console_prefix,"Global Chat Feature is READY!!!")

    @client.event
    async def on_message(m):
        global global_chat_data
        global all_guild

        # コマンド
        if m.content.startswith("!sc gchat"):
            print(console_prefix,f"{m.author} issued command: {m.content}")
            if m.content == "!sc gchat regist":
                try:
                    global_chat_data["guilds"][str(m.guild.id)]["gchat_channel"] = m.channel.id
                    global_chat_data["guilds"][str(m.guild.id)]["name"] = m.guild.name
                    global_chat_data_tmp = open("storage/json/global_chat.json","w",encoding="utf-8")
                    global_chat_data_tmp.write(json.dumps(global_chat_data))
                    global_chat_data_tmp.close()
                    for guild in global_chat_data["guilds"]:
                        all_guild.append(guild)
                    global_chat_data = open("storage/json/global_chat.json","r",encoding="utf-8")
                    global_chat_data = json.load(global_chat_data)
                    regist_success_embed = discord.Embed(title="グローバルチャットに登録しました",description=f"- サーバー: {m.guild.name}\n- チャンネル: <#{m.channel.id}>\n- 登録を解除したい場合は<@776726560929480707>のDMで")
                    await m.channel.send(embed=regist_success_embed)
                    print(console_prefix,f"joined global chat by {m.guild.name}")
                except Exception as e:
                    print(console_prefix,"Registing error:",e)
                    await m.channel.send(embed=discord.Embed(title="登録中にエラーが発生しました",description="ID申請が完了していない場合は<@776726560929480707>へ申請を、内部エラーであると思われる場合は報告をお願いします"))

            if m.content == "!sc gchat server-list" or m.content == "!sc gchat svrList":
                guild_names = []
                for server_id in global_chat_data["guilds"]:
                    guild_names.append(client.get_guild(int(server_id)).name)
                global_chat_data_embed = discord.Embed(title=f"参加サーバー 一覧")
                for guild_name in guild_names:
                    global_chat_data_embed.add_field(name="|",value=f"{guild_name}")
                await m.channel.send(embed=global_chat_data_embed)
            if m.content == "!sc gchat reload":
                m.channel.send("再読み込み中...")
                try:
                    global_chat_data = open("storage/json/global_chat.json","r",encoding="utf-8")
                    global_chat_data = json.load(global_chat_data)
                    await m.channel.send("変数が正常にリロードされました")
                except Exception as e:
                    print(console_prefix,f"Reload error:",e)
                    await m.channel.send(f"再読み込みに失敗しました")
                print(console_prefix,"Reloading variables...")
            if m.content.startswith("!sc gchat mod"):
                for moderator_id in global_chat_data["moderator_ids"]:
                    if m.author.id == moderator_id:
                        if m.content.startswith("!sc gchat mod block-user "):
                            command = m.content.lstrip("!sc gchat mod block-user")
                            if command.startswith("<@") and command.endswith(">"):
                                command = command.lstrip("<@")
                                command = command.rstrip(">")
                            global_chat_data["blocked_user_ids"].append(int(command))
                            global_chat_data_tmp = open("storage/json/global_chat.json","w",encoding="utf-8")
                            global_chat_data_tmp.write(json.dumps(global_chat_data))
                            global_chat_data_tmp.close
                            gc_block_success_embed = discord.Embed(title=f"{client.get_user(int(command)).name}のグロチャ発言権を剥奪しました",description=f"ユーザー: <@{client.get_user(int(command)).id}>\nモデレータ: <@{m.author.id}>",color=0xff0000)
                            await m.channel.send(embed=gc_block_success_embed)
            pass

        elif not m.author.bot:
            for blocked_user_id in global_chat_data["blocked_user_ids"]:
                if blocked_user_id == m.author.id:
                    await m.add_reaction("🛑")
                    return
            for a_guild_id_0 in global_chat_data["guilds"]:
                if m.channel.id == global_chat_data["guilds"][a_guild_id_0]["gchat_channel"]:
                    if m.mention_everyone == True:
                        await m.add_reaction("❌")
                        return
                    if len(m.mentions) >= 2:
                        await m.add_reaction("❌")
                        return
                    gc_message_embed = discord.Embed(description=f"{m.content}")
                    gc_message_embed.set_author(name=f"{m.author.display_name} | {m.author.top_role.name}",icon_url=f"{m.author.avatar.url}")
                    if m.attachments:
                        gc_message_embed.set_image(url=f"{m.attachments[0].url}")
                    gc_message_embed.add_field(name="info",value=f"ID: {m.author.id} | Server: {m.guild.name} | **[link]({m.jump_url})**")

                    for a_guild_id_1 in global_chat_data["guilds"]:
                        if m.channel.id != global_chat_data["guilds"][a_guild_id_1]["gchat_channel"]:
                            gchat_channel = client.get_channel(global_chat_data["guilds"][a_guild_id_1]["gchat_channel"])
                            await gchat_channel.send(embed=gc_message_embed)
                            successfully_sent = True
                    if successfully_sent == True:
                        await m.add_reaction("✅")
                        await asyncio.sleep(1)
                        await m.remove_reaction("✅",discord.Object(985254515798327296))

                    print(console_prefix,f"sent gchat message: \"{m.content}\" by \"{m.author}\"")
                    pass

    client.run(bot_token)
except Exception as e:
    print(console_prefix,f"EXCEPTION!!!: {e}")
    sleep(100)
