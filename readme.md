# TangotestMaker
https://tangotest-maker.com <br>
実際に運営しているサイトのURLです。
使い方などはURLの先から確認できます。

This software is released under the MIT License, see LICENSE.txt.

ソースコードなどは以下から確認できます。<br>
https://github.com/KaitoShinomiya/Tangotestmaker_sakura
## About
本ウェブアプリは、単語テストを作成するサービスです。<br>
パソコンからのアクセスでは塾講師向けの印刷用プリント、スマートフォンからのアクセスでは生徒向けの4択クイズウェブアプリを提供します。<br>
利用者に合わせて最適な方法を提供しています。<br>

### パソコンからの表示
<img src="https://tangotestmaker.herokuapp.com/static/images/PC.PNG" width="700">

### スマートフォンからの表示
<img src="https://tangotestmaker.herokuapp.com/static/images/SP.PNG" width="300">

<br>

### サンプル
実際に動いているサーバーのURLは以下の通りです↓。<br>
https://tangotest-maker.com <br>

## SET UP
terminalでherokuの準備<br>
管理のためのサーバアクセス時は、初回に以下の処理を行ってください。
(管理端末とサーバとの連携のため)
```Bash
heroku login
heroku remote add heroku "URL"

#もしbuildpackがなかったら(現状使ってないけどimportしてるからインストールしとかないとエラー出る)
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 1 https://github.com/KaitoShinomiya/wkhtmltopdf-buildpack.git

heroku commit -m "commit message"
heroku push heroku master
or
heroku push heroku "local repositry":master 
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
英検出る順対応、ターゲット1400に対応<br>
<br>
アップロードのフローをしっかり作っておこう。<br>
まずbooklistに登録<br>
そのあと単語テストのリストを作成<br>
sshして中に入っているsql_upload.pyでインサート<br>

ログインページ作成→そこからデータのアップロードを可能にしたい。

## About API for smartphone

smartphone向けのテストデータ受け渡し用にAPIを開放しています。
Post先は/return_test_spです。
レスポンスのJSONは以下の形で送信されます。

```js
const quiz = {
    1: {
        question: 'information',
        answers: ['情報', '作る', '食べ物', '走る'],
        correct: '情報'
    }, 2: {
        question: 'eat',
        answers: ['食べる', '作る', '走る', '遊ぶ'],
        correct: '食べる'
    }, 3: {
        question: 'can',
        answers: ['できる', 'すべき', 'しなければならない', 'できない'],
        correct: 'できる'
    }
};
```

## Next works
・JS拡充


## Future Vision
・自然言語処理を用い、類似度の高いものを中心に出題。<br>
→意味の似ている類似度の高い単語を中心に出題。<br>

・合成音声を使ったリスニング機能
