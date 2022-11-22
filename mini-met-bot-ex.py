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
bot_token = "ﾄｹﾝｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯｯ"

guild_id = "842320961033601044"
guild = client.get_guild(guild_id)
mode_flag = 0
mes = ["俺","僕","私","私"]
me = random.choice(mes)
brocked_words = open("brocked_words.json","r",encoding="utf-8")
brocked_words = json.load(brocked_words)
brocked_word_wait_sec = 15

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
        global mode_flag
        print(console_prefix,"received Message event")
        global brocked_words
        # ワードフィルター
        if m.author.id != 985254515798327296:
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
            await m.channel.send("呼んだ？")
            print(console_prefix,f"received message:) {m.content}")


        # 僕にメンションを送る
        if m.content == "heyかに" or m.content == "おいに！" or m.content == "heyかにさん！" or m.content == "heyカニさん！" or m.content == "heyかにさん" or m.content == "heyカニさん" or m.content == "かにさん！" or m.content == "カニさん！":
            await m.channel.send("<@776726560929480707>おい！！！！")
            print(console_prefix,f"called for Crab55e")

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
            link_embed=discord.Embed(title="[Discordリンク]", url="https://discord.mets-svr.com/", description="このサーバーのdiscordのリンクです...")
            await m.channel.send(embed=link_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        # ワードフィルター コマンド
        if m.content.startswith("!sc bword",0) and m.channel.id == 1011965676962984047:
            print(console_prefix,f"{m.author} issued command: {m.content}")
            # 登録
            if m.content.startswith("!sc bword add ",0):
                msg_content = m.content.replace("!sc bword add ","")
                bword_temp_r = open("brocked_words.json","r",encoding="utf-8")
                bword_temp_r = json.load(bword_temp_r)
                bword_temp_r.append(msg_content)
                bword_temp_r = json.dumps(bword_temp_r)
                bword_temp_w = open("brocked_words.json","w",encoding="utf-8")
                bword_temp_w.write(bword_temp_r)
                bword_temp_w.close()

                bword_appended_embed = discord.Embed(title=f"\"{msg_content}\" をワードフィルターに追加しました",description="削除機能は未実装っていうね   ")
                await m.channel.send(embed=bword_appended_embed)
                print(console_prefix,f"Appended {msg_content}")
            if m.content.startswith("!sc bword list",0):
                brocked_words_list = ""
                for a_brocked_word in brocked_words:
                    brocked_words_list = brocked_words_list + "`" + a_brocked_word + "`, "
                await m.channel.send(brocked_words_list)
                print(console_prefix,"Sent brocked word list")

        # リロード コマンド
        if m.content == "!sc reload":
            await m.channel.send("再読み込み中...")
            brocked_words = open("brocked_words.json","r",encoding="utf-8")
            brocked_words = json.load(brocked_words)
            await m.channel.send("変数が更新されました")
            print(console_prefix,f"{m.author} issued command: {m.content}")

        # ｼｰｸﾚｯﾄ
        if m.content == "!sc dakuhore" or m.content == "!sc だくほれ":
            dakuhore_embed=discord.Embed(title="[だくほれ]", url="https://mets-svr.com/dakuhore/", description="カルロスさん。彼氏。かわさん。MEE6。世界史の先生。[詳しく](http://mets-svr.com/だくほれ/)")
            await m.channel.send(embed=dakuhore_embed)
            print(console_prefix,f"{m.author} issued command: {m.content}")

        # 朝の挨拶
        if m.content == 'おはよう' or m.content == 'おはようございます' or m.content == 'おはようございます！' or m.content == 'おはようございます～' or m.content == 'おはよう！' or m.content == 'おはよう～' or m.content == 'ohayou' or m.content == 'oha' or m.content == 'ohayou!'or m.content == 'おはようです'or m.content == 'おはようです～'or m.content == 'おはようです！'or m.content == 'おはようです！！'or m.content == 'おはようです～～':
            print(console_prefix,f"received morning message: {m.content}, from: {m.author}")
            mrn_pattern = ["おはよう～", "おはようございます！", "おはようございます～"]
            mrn_msg = random.choice(mrn_pattern)
            async with m.channel.typing():
                await asyncio.sleep(random.uniform(1,2))
            print(console_prefix,f"sent morning message: {mrn_msg}")
            await m.channel.send(mrn_msg)

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
            await m.reply(content="だよね！！！",mention_author=False)




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
    error_log_url = "https://discord.com/api/webhooks/1004379654406275072/JlIh2V8CyTfwV3nv_WL5qDIltE_D72hKMmvNlicontOINdlYEoIiJrsmYowqF1M34DtE"
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
