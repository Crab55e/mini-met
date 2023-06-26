from requests import post

url = "https://discord.com/api/webhooks/1091706673112043610/XOUgSJ64B19U8H92BuDB-4smnga3jcl-xe8Est7yCaDAKd24Ib_fWOhRvbV2NT7FImkr"

contents_json = {
    "username": "子met",
    "avatar_url": "https://cdn.discordapp.com/avatars/985953475726815243/58c648eb1afeffe566fb2a965c520512.webp?size=100",
    "embeds": [
        {
            "title": "2. サーバーに参加する",
            "description": "マルチプレイの画面を開く、アドレスなどの情報を入力して接続します\nアドレスについては上と同じく</status:1063778904533385306>から確認してください\nまた、臨時でイベントなどを別のサーバーのIPを<#1074260079035039845>などで公開することもあります",
            "color": 0x44cc66,
            "image": {
                "url": "https://media.discordapp.net/attachments/804239123895681028/1091919432412037267/mix-j.png"
            },
            "fields": [
                {
                    "name":"Java Editionの場合",
                    "value":"ホーム画面から -> マルチプレイ -> サーバーを追加を押して、アドレスを入力します\nアドレスについては</status:1063778904533385306>から確認できます<#1074249472617480192>などで実行してみてください\nアドレスの入力が終わったら、完了を押します追加したサーバーを選択して、サーバーに接続を押します"
                }, {
                    "name":"統合版の場合",
                    "value":"ホーム画面から -> 遊ぶ -> サーバーを押して下にスクロールして\"サーバーを追加\"を押します\nサーバー名を適当に入力して、サーバーアドレスとポートを入力します\n保存を押して、画面から該当のサーバーを選択してサーバーに参加を押します"
                }, {
                    "name":"その他の場合",
                    "value":"それ以外のプラットフォームから参加したい場合は、特別な設定が必要になるかもしれません\n個別にサポートを求める場合は<#1074249460051353620>でチケットを開き使用しているデバイスとその他状況を説明してください"
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
