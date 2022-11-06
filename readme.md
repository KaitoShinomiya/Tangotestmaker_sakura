# TangotestMaker
https://tangotest-maker.com (現在、サーバ載せ替えのために停止中)<br>
実際に運営しているサイトのURLです。
使い方はURLの先から確認できます。

This software is released under the MIT License, see LICENSE.txt.

ソースコードなどは以下から確認できます。<br>
https://github.com/KaitoShinomiya/Tangotestmaker_sakura

以前使っていたレポジトリはこちら <br>
https://github.com/KaitoShinomiya/Tangotest

## background
私自身、これまで約3年半、個別指導塾で英語の塾講師をしてきました(大学受験・高校受験・英検やTOEIC等の資格試験)
その中で感じた課題から本ウェブアプリケーションの開発・運用を行っています。課題は大きく2点あります。。

①生徒に授業時で行ってもらう単語テストは基本的に塾講師が手作りで作成しており、基本的に授業時間の事前に自宅などで準備をしなくてはいけません。<br>
②また一部単語帳は有志がエクセルなどでテストプリントを作成してくださり、公開しておりますが、2020年度に大学入試センター試験(センター試験)が終了し、2021年度より大学入学共通テスト(共通テスト)に切り替わったために、単語帳すべてが改定される事態となり、そのようなプリントも使えなくなってしまいました。<br>

これらの状況から、塾講師が手間をかけることなく、単語テストを行える状況を作り出すため、本アプリケーションの開発をはじめました。

## About
本ウェブアプリは、単語テストを作成するサービスです。<br>
パソコンからのアクセスでは塾講師向けの印刷用プリント、スマートフォンからのアクセスでは生徒向けの4択クイズウェブアプリを提供します。<br>
スマートフォンで行われたデータはサーバ側に送信され、いつでも結果を確認できる仕様としております。
利用者に合わせて最適な方法を提供しています。<br>
使用技術はHTML+CSS+JavaScript,python(flask),DBはMySQLです。<br>
これまではXserver上での展開、現在はさくらインターネットのVPSサーバに載せ替えを行っております。<r>
現在スマートフォン用の4択テストをReact実装を行っているため、バックエンドをpython(fastapi)に書き換えを行っております。



### パソコンからの表示
<img src="https://www.tangotest-maker.com/static/images/PC.PNG" width="700">

### スマートフォンからの表示
<img src="https://www.tangotest-maker.com/static/images/SP.PNG" width="300">

<br>

### サンプル
実際に動いているサーバーのURLは以下の通りです↓。<br>
https://www.tangotest-maker.com 現在停止中<br>

## SET UP
index.cgiを設定することにより、Xserver上での展開
```python
#!/home/user_name/.pyenv/versions/3.7.11/bin/python　#pythonの仮想環境のパス指定
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from app import app

CGIHandler().run(app)
```

## データについて
※make_test.py内で「・」を区切り文字として使用しているため、元データのcsvには・を使用しないこと。(、,-など使用してください。)


データはcsv形式での保存<br>
・1列目に英語、2列目に日本語のデータを記述<br><br>
・データ形式(CSV UTF-8(コンマ区切り)で保存)<br>

|   English |  Japanese  |
| ---- | ---- |
|  play  |  遊ぶ  |
|  see  |  見る  |
|  information | 情報 |

## Todo
・よりモダンなUIデザインへの変更のため、フロントエンドをReactに変更。<br>
・利用者からのフィードバックを反映。<br>
①単語テストのデータ拡充<br>
ターゲット1400に対応<br>
<br>

## About API for smartphone

smartphone向けのテストデータ受け渡し用にAPIを開放しています。
Post先は/return_test_sp_dataです。(現在動いていません。) 

レスポンスのJSONは以下の形で送信されます。

```js
const questions = [
        {
            questionText: 'information',
            answerOptions: [
                { answerText: '足跡', isCorrect: false },
                { answerText: 'おいしい', isCorrect: false },
                { answerText: '情報', isCorrect: true },
                { answerText: '掛け算', isCorrect: false },
            ],
        },
        {
            questionText: 'car',
            answerOptions: [
                { answerText: '電車', isCorrect: false },
                { answerText: '車', isCorrect: true },
                { answerText: '飛行機', isCorrect: false },
                { answerText: '船', isCorrect: false },
            ],
        },
    ];
```

## mysql_db.py
sql_info.jsonでSQLの接続情報を管理。Git上にSql_info_sample.jsonがあるのでそれを参考に環境に準じたアクセス情報に変更する必要あり。
```
{
  "host": "hostname",
  "port": "port_num",
  "user": "user_name",
  "password": "pass_for_sql",
  "database_data": "tangoDB_name",
  "database_user": "tangoUser_name"
}
```

## Next works
・Reactへの変更



## Future Vision
・自然言語処理を用い、類似度の高いものを中心に出題。<br>
→意味の似ている類似度の高い単語を中心に出題。<br>

・合成音声を使ったリスニング機能<br>
・よく間違える問題などを中心に出題する<br>
