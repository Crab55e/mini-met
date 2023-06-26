from requests import post
from json import dumps

url = "https://discord.com/api/webhooks/985953475726815243/GCTQ_JoOxWFjxxnNipsg64YyqzpL3I1RhpTWRhuG3pm9rYbtFbeomwho9azLb3EpCtcr"
url = "https://discord.com/api/v10/channels/985943677018988605/messages"

links_description = """
動作していない物がある場合は<#1074249460051353620>で報告してください

**1. ホームページ** https://mets-svr.com/
**2. リソースパック** https://rp.mets-svr.com/
**3. Discord招待リンク** https://discord.mets-svr.com/
**4. 公式Twitter** https://twitter.com/Mets_Server/
"""[1:-1]

rules_description = """
[利用規約](https://www.mets-svr.com/terms)
[コミュニティガイドライン](https://www.mets-svr.com/community-guideline)
[マインクラフトサーバー利用規約](https://www.mets-svr.com/minecraft)
"""[1:-1]

role_button = {
        "type": 2,
        "style": 5,
        "label": "ロール付与",
        "emoji": {"name":"🟢"},
        "url": "https://discord.com/channels/842320961033601044/1074249452187033682",
    }
whitelist_button = {
        "type": 2,
        "style": 5,
        "label": "ホワリス登録",
        "emoji": {"name":"📋"},
        "url": "https://discord.com/channels/842320961033601044/1074249454741368943",
    }
introduction_button = {
        "type": 2,
        "style": 5,
        "label": "自己紹介",
        "emoji": {"name":"📝"},
        "url": "https://discord.com/channels/842320961033601044/949994602427994113",
    }
help_button = {
        "type": 2,
        "style": 5,
        "label": "ヘルプ",
        "emoji": {"name":"📪"},
        "url": "https://discord.com/channels/842320961033601044/1074249460051353620",
    }


contents_json = {
    "username": "子met",
    "avatar_url": "https://cdn.discordapp.com/avatars/985953475726815243/58c648eb1afeffe566fb2a965c520512.webp",
    "embeds": [
        {
            "title": "リンク",
            "url":"https://mets-svr.com/links/",
            "description": links_description,
            "color": 0x22aa44,
            "author": {
                "name": "Met's - links",
                "icon_url": "https://cdn.discordapp.com/avatars/985953475726815243/58c648eb1afeffe566fb2a965c520512.webp",
                "url":"https://www.mets-svr.com"
            }
        }, {
            "title": "ルール",
            "url":"https://www.mets-svr.com/",
            "description": rules_description,
            "color":0x22aa44,
            "author": {
                "name": "Met's - rules",
                "icon_url": "https://cdn.discordapp.com/avatars/985953475726815243/58c648eb1afeffe566fb2a965c520512.webp",
                "url":"https://www.mets-svr.com"
            },
            "footer": {"text":"更新: 2023/04/25"}
        }
    ],
    "components": [
        {
            "type": 1,
            "components": [role_button,whitelist_button,introduction_button,help_button]
        }
    ]
}
token = "OTg1MjU0NTE1Nzk4MzI3Mjk2.GDKTEo.b9fwsBeZFwDWvSl33S2aE_ap7KmQ6vTe63T3_I"

headers = {"Authorization":f"Bot {token}","Content-Type":"application/json"}
print("embed json:\n",contents_json)
res = post(url, headers=headers, data=dumps(contents_json))
print(res.text,res.status_code)
