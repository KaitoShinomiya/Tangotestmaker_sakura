# TangotestMaker
https://tangotest-maker.com <br>
実際に運営しているサイトのURLです。
使い方はURLの先から確認できます。

This software is released under the MIT License, see LICENSE.txt.

ソースコードなどは以下から確認できます。<br>
https://github.com/KaitoShinomiya/Tangotestmaker_sakura
## About
本ウェブアプリは、単語テストを作成するサービスです。<br>
パソコンからのアクセスでは塾講師向けの印刷用プリント、スマートフォンからのアクセスでは生徒向けの4択クイズウェブアプリを提供します。<br>
利用者に合わせて最適な方法を提供しています。<br>
.htaccessでスマホ用とパソコン用のアクセスの分離<br>
スマホはReactAppを表示する、react hook用いてルーティング
パソコンはこれまでと同様に。
### パソコンからの表示
<img src="https://www.tangotest-maker.com/static/images/PC.PNG" width="700">

### スマートフォンからの表示
<img src="https://www.tangotest-maker.com/static/images/SP.PNG" width="300">

<br>

### サンプル
実際に動いているサーバーのURLは以下の通りです↓。<br>
https://www.tangotest-maker.com <br>

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
Post先は/return_test_sp_dataです。
レスポンスのJSONは以下の形で送信されます。

```js
const questions = [
        {
            questionText: 'information ?',
            answerOptions: [
                { answerText: 'New York', isCorrect: false },
                { answerText: 'London', isCorrect: false },
                { answerText: 'Paris', isCorrect: true },
                { answerText: 'Dublin', isCorrect: false },
            ],
        },
        {
            questionText: 'Who is CEO of Tesla?',
            answerOptions: [
                { answerText: 'Jeff Bezos', isCorrect: false },
                { answerText: 'Elon Musk', isCorrect: true },
                { answerText: 'Bill Gates', isCorrect: false },
                { answerText: 'Tony Stark', isCorrect: false },
            ],
        },
    ];
```

##mysql_db.py
sql_info.jsonでSQLの接続情報を管理。Git上にSql_info_sample.jsonがあるのでそれを参考に環境に準じたアクセス情報に変更する必要あり。
```
{
  "host": "hostname",
  "port": "port_num",
  "user": "user_name",
  "password": "pass_for_sql",
  "database_data": "tangodata_name",
  "database_user": "tangouser_name"
}
```

## Next works
・Reactへの変更



## Future Vision
・自然言語処理を用い、類似度の高いものを中心に出題。<br>
→意味の似ている類似度の高い単語を中心に出題。<br>

・合成音声を使ったリスニング機能<br>
・よく間違える問題などを中心に出題する<br>
