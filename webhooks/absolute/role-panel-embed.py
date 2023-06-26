from requests import post
from json import dumps

url = "https://discord.com/api/webhooks/985953475726815243/GCTQ_JoOxWFjxxnNipsg64YyqzpL3I1RhpTWRhuG3pm9rYbtFbeomwho9azLb3EpCtcr"
url = "https://discord.com/api/v10/channels/1074249452187033682/messages"

content_json = {
    "title": "ロールパネル",
    "description": "欲しいロールを選んでください",
    "color": 4039773,
    "fields": [
        {
            "name": "❗: 通知可",
            "value": "運営からの更新や連絡などの通知を受け取ります",
            "inline": False
        },
        {
            "name": "⭕: DM ok!",
            "value": "DMを送ってもいい場合に受け取ります",
            "inline": False
        },
        {
            "name": "❌: DM NG!",
            "value": "DMを送ってほしくない場合に受け取ります",
            "inline": False
        },
        {
            "name": "🚀: サーバー宣伝系bot通知(bump/up)",
            "value": "DISBOARDやディス速などの通知を受け取ります",
            "inline": False
        },
        {
            "name": "🟦: BE",
            "value": "Bedrock EditionやPEなどをメインにプレイする場合に受け取ります",
            "inline": False
        },
        {
            "name": "🟥: Java",
            "value": "Java Editionをメインにプレイする場合に受け取ります",
            "inline": False
        }
    ]
}

token = "OTg1MjU0NTE1Nzk4MzI3Mjk2.GDKTEo.b9fwsBeZFwDWvSl33S2aE_ap7KmQ6vTe63T3_I"

headers = {"Authorization":f"Bot {token}","Content-Type":"application/json"}
print("embed json:\n",contents_json)
res = post(url, headers=headers, data=dumps(contents_json))
print(res.text,res.status_code)
