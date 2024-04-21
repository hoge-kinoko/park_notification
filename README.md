# 駐騎場の時間をwebhook_url経由でお知らせしてくれるbot

## 使い方
### 準備
tmp/park_list.txtに以下のテキストを貼り付ける(コマンドのオプションで任意の場所を設定可能)

<details>
<summary>テキストの取得方法</summary>

1. F12などで検証ツールを出してコンソールタブへ移動。※PC版限定
2. ゲームで本鯖駐騎場タブを開いた瞬間にログに出てきた park_list をグローバル変数として保存。
3. 直後に出てくる temp1 の番号を覚えておく(グローバル変数として保存するたびに番号が増える)
4. 下記のスクリプトの2行目の temp1 を保存した番号の temp(番号) に置き換えて、コンソールに貼り付けてエンターキーを押すと出てくる文字を文字列をそのままコピーする。

```javascript
temp1.forEach(park => {
  protect_end_date = new Date(park.protect_end * 1000);
  let protect_end_at = `${protect_end_date.getFullYear()}/${(protect_end_date.getMonth() + 1).toString().padStart(2, '0')}/${protect_end_date.getDate().toString().padStart(2, '0')} ${protect_end_date.getHours().toString().padStart(2, '0')}:${protect_end_date.getMinutes().toString().padStart(2, '0')}:${protect_end_date.getSeconds().toString().padStart(2, '0')}`; // protect_end_atを0埋め
  park_no = String(park.id).slice(-2).padStart(2, '0'); // park_noを0埋め
  park_list.push({park_no: park_no, protect_end_at: protect_end_at, protect_end: park.protect_end, server_id: park.server_id})
});

park_list.sort((o, next_o) => {
  return o.protect_end - next_o.protect_end;
});

info_text = "【不定期お知らせ】免戦終了時間\n"
park_list.forEach(park => {
  emoji = park.server_id == 1344 ? ":shield:" : ":crossed_swords:"
  info_text += `${emoji}\`${park.server_id}鯖 ${park.park_no}番 ⏰${park.protect_end_at}\`\n`
})
info_text
```

</details>

```text
【不定期お知らせ】免戦終了時間
:shield:`1344鯖 01番 ⏰2024/04/20 09:07:24`
:shield:`1344鯖 08番 ⏰2024/04/21 14:00:38`
:shield:`1344鯖 02番 ⏰2024/04/21 16:55:04`
:shield:`1344鯖 10番 ⏰2024/04/21 17:05:43`
:crossed_swords:`1348鯖 03番 ⏰2024/04/21 17:43:36`
:shield:`1344鯖 07番 ⏰2024/04/21 17:47:03`
:crossed_swords:`1348鯖 12番 ⏰2024/04/21 17:50:57`
:crossed_swords:`1348鯖 05番 ⏰2024/04/21 18:00:07`
:crossed_swords:`1358鯖 04番 ⏰2024/04/21 18:10:07`
:shield:`1344鯖 09番 ⏰2024/04/21 18:21:31`
:shield:`1344鯖 11番 ⏰2024/04/21 19:00:04`
:shield:`1344鯖 06番 ⏰2024/04/21 19:11:39`
```

### 本体
```shell
WEBHOOK_URL="your webhook_url" pipenv run python main.py
# or
WEBHOOK_URL="your webhook_url" python main.py
```
現状 Flask 未使用なので、 pipenv なしでも動く

## 仕組み

- tmp/aram_list.txtに通知のログがある。
- tmp/park_list.txtの時間を見て、ログになければ通知する。
- 通知したらログに追加のシンプル仕様。
