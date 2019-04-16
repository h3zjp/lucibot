## るしぼっと4 Readme（取扱説明書 兼 設計仕様書）
::BotName= Lucibot4  
::BotDate= 2019/4/16  
::Version= 4.0.4.3  
::Admin= Lucida（lucida3rd@mstdn.mynoghra.jp）  
::github= https://github.com/lucida3rd/lucibot  


  
  
**★★★るしぼっとについては現在、サブアカウントでのみ動作します。★★★***
  
  


## 概要
python3で作成したmastodonクラウド環境下で動くことを前提にしたbotです。  
通常の（？）botの他、手持ちのアカウントに対して通知を支援する機能を付加することもできます。  



## 目次
* [システム要件・セットアップなど](#iSetup)
* [バージョンアップ手順](#iVerup)
* [起動方法](#iStart)
* [機能説明](#iFunction)
  * [コマンドライン](#iCommLine)
  * [ユーザ登録機能について](#iUserReg)
  * 各機能詳細
    * [連合TL監視機能](#iPTLfunc)

    * [アクション通知機能](#iActionInd)
    * [リプライブースト機能](#iReplyBoost)
    * [ホームブースト機能](#iHomeBoost)
    * [周期トゥート機能](#iCircleToot)


    * [リプライ機能](#iReplyFunc)
    * [ランダムトゥート機能](#iRandomToot)
    * [ワード学習機能](#iWordStudy)
    * [トラヒック表示機能](#iTrafficView)
    * [ハード監視機能](#iHardLook)
    * [ユーザ収集機能](#iUserCorrect)
    * [自動フォロー機能](#iAutoFollow)
    * [twitter連携機能](#iTwitter)


    * [ログ機能](#iLogging)
    * [bot排他機能](#iExclusive)
* [免責事項](#iDisclaimer)



<a id="iSetup"></a>
## システム要件・セットアップなど
るしぼっとのシステム要件、セットアップ方法については、別紙のセットアップ手順書に記載しています。よくお読みください。
* [セットアップ手順書](https://github.com/lucida3rd/lucibot/readme_setup.md)



<a id="iVerup"></a>
## バージョンアップ手順
るしぼっとリポジトリのmasterから最新版をpullする方法です。  
- ※forkしてる場合はforkリポジトリにmasterを反映してから実行します。

1.セットアップしたサーバにログインし、るしぼっと用ユーザに切り替えます。  
　そしてるしぼっとのcloneフォルダにcdします。  

```
# su - [ユーザ名]
$ pwd
/home/[ユーザ名]/bot
　　※cloneフォルダにいることを確認します
```

2.最新版のリストをfetchします。

```
$ git fetch
　original->master と出たら、githubに最新版があります。
```

3.アップデートします。

```
$ git stash　※stashは不要と思いますが念のため
$ git pull
  pullされたファイル一覧が出ればOKです。
$ exit
　作業は終わりです。
```



<a id="iStart"></a>
## 起動方法
コマンドラインにて以下を入力するとコンソールが起動します。

```
$ python3 run.py
```

初回は初期化処理を実施しますので、画面に従って入力します。  
  
るしぼっとには、bot動作させるアカウントの他、手持ちのmastodonアカウントに対するファボ、
ブースト通知機能を持たせたり、定期的に固定トゥートを送信させる支援機能を備えてます。
アカウントの種類は以下の４種類です。各種類毎に利用できる機能が異なります。

* アカウントの種類

  * Master User：  
    botで使うアカウント。るしぼっとには1個しか登録できない。botの機能をほとんどが利用できる。  

  * Administrator User：  
    Master UserやSub Userからの通知を受け取るアカウント。るしぼっとには1個しか登録できない。通知を受け取るだけで、botの機能は利用できないが、PR User、Sub Userと併用登録できる。  

  * PR User：  
    Sub Userのうち、周期トゥート機能が利用できるアカウント。るしぼっとには1個しか登録できない。その他、Sub Userと同じ通知機能が利用できる。  

  * Sub User：  
    他のmastodonアカウントから、ファボ、ブースト、フォロー、メンションを受け取ったときに通知を自動トゥートできるアカウント。るしぼっとには複数ユーザ登録できる。  

* アカウントが利用できる機能  

| 機能                  | データ取得先   | Master |   PR   |   Sub   |   Sub                 |
|-----------------------|----------------|--------|--------|---------|-----------------------|
| 連合TL監視機能        | 連合TL         |   〇   |   －   |   －    |                       |
| アクション通知機能    | 通知TL         |   －   |   〇   |   〇    |                       |
| リプライブースト機能  | 通知TL         |   －   |   〇   |   〇    |                       |
| リプライ機能          | 通知TL         |   〇   |   －   |   〇    |                       |
| ホームブースト機能    | ホームTL       |   －   |   －   |   〇    |                       |
| 周期トゥート機能      | －             |   －   |   〇   |   －    | PR User専用機能       |
| ランダムトゥート機能  | 連合TL         |   〇   |   －   |   －    |                       |
| ワード学習機能        | 連合・ローカル |   〇   |   〇   |   〇    |                       |
| トラヒック機能        | 連合・ローカル |   〇   |   〇   |   〇    | 通知はMasterのみ実施  |
| ハード監視機能        | －             |   〇   |   －   |   －    |                       |
| ユーザ収集機能        | 連合・ローカル |   〇   |   〇   |   〇    |                       |
| 自動フォロー機能      | 連合・ローカル |   〇   |   ？   |   ？    |                       |


コンソールでは、mastodonアカウントの登録や削除、botの機能設定や、botの起動、停止操作がおこなえます。画面に従って操作してください。  



----
<a id="iFunction"></a>
## 機能説明
botの機能を以下に説明します。  
各機能を説明します。  


  
  
  **機能については仕様見直し中で確定ではありません**
  
  


るしぼっと4から、各機能を有効、無効、調整するにはコンソールから変更できるようになりました。細かいパラメータ変更は従来通り、コンフィグファイル（設定）を編集します。  
コンフィグファイルは toot/config.txt です。  



<a id="iCommLine"></a>
## コマンドライン  ★るしぼっと4新機能

るしぼっとを実行する時にはコマンドライン引数が必要になります。  
引数が無かったり、認識外のコマンドではるしぼっとは実行されません。  

```実行コマンド
# python3 run.py [コマンド] [※ユーザ名など(コマンドによる)]
  詳しくは python3 run.py を入力するか、readme_runcommand.txt を参照ください。
```



<a id="iUserReg"></a>
## ユーザ登録機能について

るしぼっと4からはbotとして利用するアカウントの他に、サブのアカウントを登録することができるようになりました。
サブアカウントはbotの機能は制限されますが、アクティビティを上げる（と思われる）いくつかの機能を利用できます。

* 登録アカウントに対するリアクションを通知先アカウントに通知させる
* 学習情報やトラヒックを収集させる
* 一斉トゥートを投げる（手動限定）

```
※ユーザ登録時の注意：
　ユーザ登録、更新をおこなう際、登録に使用するアカウントが登録されているmastodonサーバに対して
　認証アプリ登録をおこないます。その際、通信不良をおこしたり、mastodonに認識されない場合、
　登録が失敗となります。メンテナンス情報などにも注意してください。
```



<a id="iPTLfunc"></a>
## 連合TL監視機能

連合TLのトゥートを解析し、設定したワードのなかで反応します。
　機能有効：LookPTL=on
　　ワードファイル：toot/lltl.txt
　　　※中身はサンプルを参考にしてください

・ファボ（ニコる）：PTL_Favo=on
　TLのトゥートに設定したワードを見つけると、そのトゥートをファボります。
　フォロワーが対象です。

・ブースト：PTL_Boot=on
　TLのトゥートに設定したワードを見つけると、そのトゥートをブーストします。
　フォロワーが対象です。

・紐づけエアリプ：PTL_HRip=on
　TLのトゥートに設定したワードを見つけると、そのトゥートに対してエアリプします。
　トゥートに対して関連付けもおこないます。（相手には通知されません）
　フォロワーが対象です。

・エアリプ：PTL_ARip=on
　TLのトゥートに設定したワードを見つけると、そのトゥートに対してエアリプします。
　相手には通知されません。
　フォロワーが対象です。

・ワード監視：PTL_WordOpe=on
　TLのトゥートを解析し、設定したワードを見つけると任意のアカウントにDM通知をおこないます。
　フォロワーでなくても反応します。



<a id="iActionInd"></a>
## アクション通知機能

トゥートをファボ、ブーストされた時に、トゥートの内容（140字のハイライト）、URLをトゥートします。
またフォローされた時にもその旨をpublicに通知します（オプション）。Twitterライクな機能です。  
公開トゥートと未収載トゥートが対象です。（未収載はオプションでOFF可）  
　利用権限：Master × / PR 〇 / User 〇  
　機能有効：IND_Favo=on  
　　　※IND_FavoTag  トゥートに付加するタグを指定します。  
　　　※IND_Favo_CW=on　通知の内容をCWで隠します。  
　　　※IND_Follow=on　フォローされた時に通知します。  



<a id="iReplyBoost"></a>
## リプライブースト機能

リプライされた時に、自動ブーストする機能です。フォロワー向けの通知機能となります。  
公開トゥート、未収載トゥートが対象、非公開トゥートはファボします。  
　利用権限：Master × / PR 〇 / User 〇  
　機能有効：RIP_Favo=on  
　　　※IND_Favo_Unl=on　未収載トゥートもブーストします。Offの時はファボします。  



<a id="iHomeBoost"></a>
## ホームブースト機能

ホームTLのうち、特定のパターン（タグ）を見つけた時にブーストする機能です。フォロワー向けの通知機能となります。  
例えば、リモートの自分のトゥートをフォロワーに自動ブーストさせたい時に使える機能です。
（この場合リモートの自分をフォローしておく必要があります）  
公開トゥート、未収載トゥートが対象です。  
　利用権限：Master × / PR × / User 〇  
　機能有効：HTL_Boost=on  
　　ホームブーストファイル：toot/hboost.txt  
　　　※中身はサンプルを参考にしてください  



<a id="iCircleToot"></a>
## 周期トゥート機能

指定した時間に任意のトゥートをおこなう機能です。時間は1日毎の定時間、毎時1回が指定できます。  
PR User限定の機能です。  
　利用権限：Master × / PR 〇 / User ×  
　機能有効：CircleToot=on  
　　周期トゥートファイル：toot/ctoot.txt  
　　　※中身はサンプルを参考にしてください  
　　　※時間を*で指定すると毎時間トゥートします。例：*.5..毎時5分  
　　　※トゥートファイルは1行目は公開範囲を指定します。  
　　　　p..公開、l..未収載、u..非公開  
　　　　2行目以降に任意のトゥートを入れます（タグにも対応）  



<a id="iRandomToot"></a>
## ランダムトゥート機能

botが学習した単語を組み合わせて適当にトゥートします。
新設の場合は学習を開始してから1時間以上経たないと機能が動かない仕様です。
　機能有効：RandToot=on
　　getRandVal：トゥート頻度。（範囲：0-100）
　　　getRandRangeは乱数の幅で100以上で設定します。
　　　getRandVal÷getRandRangeが1分ごとにトゥートする確率となります。



<a id="iReplyFunc"></a>
## リプライ機能

botがリプライを受信した際、設定したワードを見つけるとランダムにリプライを返します。
　　ワードファイル：toot/reply.txt
　　　※中身はサンプルを参考にしてください



<a id="iWordStudy"></a>
## ワード学習機能

連合TLのなかから短い単語を抽出し、辞書としてcsv保管する機能です。
学習した単語は、ランダムトゥートやリプライで使用されます。
また任意にリプライを送って単語を学習させることもできます。
ただし禁止ワードは収集されません。
　機能有効：WordStudy=on
　　studyNum：1周における学習対象トゥート数
　　studyNax：辞書に記録できる最大単語数。これを越えて学習する場合、古いものから忘れていきます。
　　　辞書ファイル：user/userdic.csv
　　　禁止ワードファイル：toot/xxword.txt



<a id="iTrafficView"></a>
## トラヒック表示機能

1時間ごとの連合トゥートの個数を集計し、トゥートします。
トラヒック収集開始の最初の1時間分は計測を捨てます。
　機能有効：Traffic=on
　　集計対象インスタンス：toot/traffic.txt
　　　　選択外のトゥートは --Others-- で集計します。



<a id="iHardLook"></a>
## ハード監視機能

サーバのメモリ、スワップ、ディスク残量をチェックし、毎日0時に管理者にDMで送る。
内部ではcsvファイルに記録する。（log配下に保存される）
bot本体とは別のプロセスで動作する。
　機能有効：LookHard=on



<a id="iUserCorrect"></a>
## ユーザ収集機能

連合でトゥートしたユーザを自動的に収集し、csv保管する機能です。
フォロー、フォロワーの内部管理にも使われます。この機能は停止できない仕様です。
ユーザ収集除外リストに登録したドメインからも収集されますが、フォローはしません。またリムーブします。
（リムーブ時のユーザ数が多いと対象者の全リムーブに時間がかかります）
　ユーザ収集ファイル：user/usercorr.csv
　ユーザ収集除外リスト：toot/usercorr_rem.txt



<a id="iAutoFollow"></a>
## 自動フォロー機能

ユーザ収集機能で収集したユーザのなかから対象のユーザを自動的にフォローします。
1ユーザ1回だけ自動的にフォローします。
　→収集されてないユーザはフォローしません。
　→鍵垢はフォローしません。
　→フォローリクエストしていた場合は自動解除します。
　　リクエスト解除前に承認されると、フォロワーになれます。
30日間活動のないユーザを自動リムーブします。
ユーザ収集除外リストに登録したドメイン対象になると自動リムーブします。
　機能有効：AutoFollow=on
　　　1回のフォローの上限数は getFollowMnum に整数を入力します。
　　　AIPが食われたり、サーバの負荷がかなり増加するため、通常いじらないでください。



<a id="iTwitter"></a>
## twitter連携機能

APIを取得したアカウントに連携し、トゥートをツイートします。
その他有効にするにはTwitter APIを取得する必要があります。（twitter APIの取得方法参照）
　機能有効：Twitter=on

3.twitterとの機能を使う場合twitterからAPIを取得します。
　以下＜twitter APIの取得方法＞をご参照ください。

※twitter連携はマスターアカウントのみの連携となる仕様です。



<a id="iLogging"></a>
## ログ機能

操作記録や異常記録を log フォルダ以下にログファイルを記録します。
ファイルは日別に分かれます。
　ログレベル：LogLevel
　　a：全てのログを記録　　　　　　　（LevelA,B,C）
　　b：重要なログと気になるログを記録（LevelA,Bのみ、LevelCは記録しない）
　　c：重要なログだけ記録　　　　　　（LevelAログのみ、LevelB,Cは記録しない）



<a id="iExclusive"></a>
## bot排他機能

botの二重処理を抑止するため、排他機能を実装してます。
先行プロセスが処理途中、処理遅延などで後プロセスで再実行されたときにwaitをかけます。
先行プロセスの処理が完了し排他を解除するか、
後プロセスが最大90秒待っても排他が解除されなければロックを落とします。（実行は次回実行）
　機能有効：Lock=on
　　排他ロックファイル：data/_lock.txt



----
<a id="iDisclaimer"></a>
## 免責事項
* アーカイブなどに含まれるファイル類は消したりしないでください。誤動作の原因となります。
* 当ソースの改造、改造物の配布は自由にやってください。その際の著作権は放棄しません。
* 未改造物の再配布は禁止とします。
* 当ソースを使用したことによる不具合、損害について当方は責任を持ちません。全て自己責任でお願いします。
* 当ソースの仕様、不具合についての質問は受け付けません。自己解析、自己対応でお願いします。
* 使用の許諾、謝辞については不要です。
* その他、ご意見、ご要望については、mastodonのDMまでお送りください。



