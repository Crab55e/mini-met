from requests import post

url = "https://discord.com/api/webhooks/1091706673112043610/XOUgSJ64B19U8H92BuDB-4smnga3jcl-xe8Est7yCaDAKd24Ib_fWOhRvbV2NT7FImkr"

contents_json = {
    "username": "子met",
    "avatar_url": "https://cdn.discordapp.com/avatars/985953475726815243/58c648eb1afeffe566fb2a965c520512.webp?size=100",
    "embeds": [
        {
            "title": "1. マインクラフトを起動します",
            "description": "サーバーに参加するためにはMinecraftを起動する必要があります\nなお、サーバーの対応しているバージョン以外での参加はできません\n詳しくは</status:1063778904533385306>から確認してください\n\n",
            "color": 0x22aa44,
            "author": {
                "name": "Met's - Join guide",
                "icon_url": "https://cdn.discordapp.com/avatars/985953475726815243/58c648eb1afeffe566fb2a965c520512.webp?size=100"
            },
            "image": {
                "url": "https://cdn.discordapp.com/attachments/804239123895681028/1091903692669722745/mix.png"
            },
            "fields": [
                {
                    "name":"Java Editionの場合",
                    "value":"アプリケーションの一覧から、\"Minecraft Launcher\"を検索し、起動します\nサーバーの対応するバージョンのMinecraftを起動します\n対応バージョンについては、できる限り最新バージョンを維持します。\nですがリリースから間もない場合は対応していない場合もありますので</status:1063778904533385306>から確認してください"
                }, {
                    "name":"統合版の場合",
                    "value":"PCの場合アプリケーション一覧から、モバイルの場合はホーム画面などからMinecraftを起動します"
                }, {
                    "name":"その他の場合",
                    "value":"それ以外のプラットフォームから参加したい場合のガイドはありません\nもしわからない場合は個別にサポートを求めることもできます\n<#1074249460051353620>からチケットを開いて状況を説明してください"
                }
            ]
        }
    ]
}

headers = {
    'Content-Type': 'application/json'
}

res = post(url, headers=headers, json=contents_json)
print(res.text,res.status_code)
