## るしぼっと4 Readme（取扱説明書 兼 設計仕様書）
::BotName= Lucibot4 (deverop)  
::BotDate= 2019/11/20  
::Version= 4.1.4.2.d  
::Admin= Lucida（lucida3rd@mstdn.mynoghra.jp）  
::github= https://github.com/lucida3rd/lucibot  



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
    * [ランダムトゥート機能](#iRandomToot)
    * [リプライ機能](#iReplyFunc)
    * [ワード学習機能](#iWordStudy)
    * [トラヒック表示機能](#iTrafficView)
    * [トレンド機能](#iTrend)
    * [ハード監視機能](#iHardLook)
    * [ユーザ収集機能](#iUserCorrect)
    * [自動フォロー機能](#iAutoFollow)
    * [手動トゥート機能](#iManualToot)
    * [twitter連携機能](#iTwitter)
    * [twitterリーダ機能](#iTwitterReader)
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
    botで使うアカウント。るしぼっとには1個しか登録できない。  
    botの機能のほとんどが利用できる。  

  * Administrator User：  
    Master UserやSub Userからの通知を受け取るアカウント。るしぼっとには1個しか登録できない。  
    Sub Userと併用登録できる。  

  * Sub User：  
    他のmastodonアカウントから、ファボ、ブースト、フォロー、メンションを受け取ったときに通知を自動トゥートできるアカウント。
    るしぼっとには複数ユーザ登録できる。  

* アカウントが利用できる機能  

| 機能                  | データ取得先   | Master |   Sub   |  備考                |
|-----------------------|----------------|--------|---------|----------------------|
| 連合TL監視機能        | 連合TL         |   〇   |   －    |                      |
| アクション通知機能    | 通知TL         |   －   |   〇    |                      |
| 周期トゥート機能      | －             |   〇   |   －    |                      |
| ランダムトゥート機能  | －             |   〇   |   －    |                      |
| ワード学習機能        | 連合TL         |   〇   |   －    |MasterドメインはSub   |
| ユーザ収集機能        | 連合TL         |   〇   |   －    |MasterドメインはSub   |
| トラヒック機能        | ローカルTL     |   〇   |   〇    |                      |
| トレンド機能          | －             |   〇   |   〇    |MasterドメインはSub   |
| 自動フォロー機能      | 通知TL         |   〇   |   －    |                      |
| リプライ機能          | 通知TL         |   〇   |   〇    |                      |
| リプライブースト機能  | 通知TL         |   －   |   〇    |                      |
| ホームブースト機能    | ホームTL       |   －   |   〇    |                      |
| ハード監視機能        | －             |   〇   |   －    |                      |
| 手動トゥート機能      | －             |   〇   |   △    |Subは同報配信のみ     |
| Twitter連携機能       | Twitter TL     |   〇   |   －    |                      |
| Twitterリーダ機能     | Twitter TL     |   〇   |   〇    |状況による            |
| ログ機能              | －             |   〇   |   〇    |                      |
| 排他機能              | －             |   〇   |   〇    |                      |

コンソールでは、mastodonアカウントの登録や削除、botの機能設定や、botの起動、停止操作がおこなえます。画面に従って操作してください。  



----
<a id="iFunction"></a>
## 機能説明
botの各機能を以下に説明します。  
るしぼっと4から、各機能を有効、無効、調整するにはコンソールから変更できるようになりました。  



<a id="iCommLine"></a>
## コマンドライン  
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
* ファボ（ニコる）：PTL_Favo=on  
　TLのトゥートに設定したワードを見つけると、そのトゥートをファボります。  
　フォロワーが対象です。  
* ブースト：PTL_Boot=on  
　TLのトゥートに設定したワードを見つけると、そのトゥートをブーストします。  
　フォロワーが対象です。  
* 紐づけエアリプ：PTL_HRip=on  
　TLのトゥートに設定したワードを見つけると、そのトゥートに対してエアリプします。  
　トゥートに対して関連付けもおこないます。（相手には通知されません）  
　フォロワーが対象です。  
* エアリプ：PTL_ARip=on  
　TLのトゥートに設定したワードを見つけると、そのトゥートに対してエアリプします。  
　相手には通知されません。  
　フォロワーでなくても反応します。  
* ワード監視：PTL_WordOpe=on  
　TLのトゥートを解析し、設定したワードを見つけると任意のアカウントにDM通知をおこないます。  
　相手には通知されません。  
　フォロワーでなくても反応します。  



<a id="iActionInd"></a>
## アクション通知機能
トゥートをファボ、ブーストされた時に、トゥートの内容（140字のハイライト）、URLをトゥートします。  
またフォローされた時にもその旨をpublicに通知します。Twitterライクな機能です。  
SubUserのみの機能です。  
制限時間内に通知回数が閾値を超えると自動的に規制抑止されます。（規制時間が終わると自動解除されます）  
　機能有効：IND_Favo=on  
　　　※IND_ActionTag  トゥートに付加するタグを指定します。  
　　　※IND_Favo=on　  ファボされた時に通知します。  
　　　※IND_Follow=on　フォローされた時に通知します。  



<a id="iCircleToot"></a>
## 周期トゥート機能
指定した時間に任意のトゥートをおこなう機能です。時間は1日毎の定時間、毎時1回が指定できます。  
PR User限定の機能です。  
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



<a id="iWordStudy"></a>
## ワード収集機能
タイムラインのトゥートをMeCabで分解し、辞書情報としてデータベースに保管する機能です。  
学習した単語は、ランダムトゥートやリプライで使用されます。  
また任意にリプライを送って単語を学習させることもできます。  
ただし禁止ワードは収集されません。  
　機能有効：WordStudy=on  
　　studyNum：1周における学習対象トゥート数  
　　studyNax：辞書に記録できる最大単語数。これを越えて学習する場合、古いものから忘れていきます。  
　　　禁止ワードファイル：toot/xxword.txt



<a id="iUserCorrect"></a>
## ユーザ収集機能
連合でトゥートしたユーザを自動的に収集し、データベースに保管する機能です。  
フォロー、フォロワーの内部管理にも使われます。この機能は停止できない仕様です。  



<a id="iTrafficView"></a>
## トラヒック表示機能
1時間ごとの連合トゥートの個数を集計し、トゥートします。  
トラヒック収集開始の最初の1時間分は計測を捨てます。  
この情報はデータベースに記録されます。  
　機能有効：Traffic=on  



<a id="iTrend"></a>
## トレンド
1時間ごとに任意のドメインのトレンドを集計し、botでトゥートします。  
トゥートは非公開でおこなわれます。  
この情報はデータベースに記録されます。  
　機能有効：Trend=on  

補足：  
　botでトゥートする際、botのドメインでハッシュタグ検索できないものは無駄を省くため除外されます。  



<a id="iAutoFollow"></a>
## 自動フォロー機能
この機能はMasterUser専用の機能です。  
ユーザ収集機能で収集したユーザから何らかのアクションをされた場合、自動的にフォローします。  
フォローされた場合は、無条件でリフォローします。それ以外は以下の条件に従います。  
　機能有効：AutoFollow=on  

上記以外の条件では次のように動作します。  
  * フォロー以外のアクションでは、過去にフォローしたことがある場合、フォローしません。  
　* 収集されてないユーザはフォローしません。  
　* 鍵垢はフォローしません。  
  * 30日間活動のないユーザを自動リムーブします。  
  * ユーザ収集除外リストに登録したドメイン対象になると自動リムーブします。  



<a id="iReplyFunc"></a>
## リプライ機能
botがリプライを受信した際、設定したワードを見つけるとランダムにリプライを返します。  
　　ワードファイル：toot/reply.txt  
　　　※中身はサンプルを参考にしてください  



<a id="iReplyBoost"></a>
## リプライブースト機能
サブアカウント専用の支援機能です。  
リプライされた時に、自動ブーストする機能です。フォロワー向けの通知機能となります。  
公開トゥート、未収載トゥートが対象、非公開トゥートはファボします。  
　機能有効：RIP_Favo=on  



<a id="iHomeBoost"></a>
## ホームブースト機能
サブアカウント専用の支援機能です。  
ホームTLのうち、特定のパターン（タグ）を見つけた時にブーストする機能です。フォロワー向けの通知機能となります。  
例えば、リモートの自分のトゥートをフォロワーに自動ブーストさせたい時に使える機能です。  
（この場合リモートの自分をフォローしておく必要があります）  
twitterが有効の場合は、twitterに転送することもできます。  
公開トゥート、未収載トゥートが対象です。  
　機能有効：HTL_Boost=on  
　　ホームブーストファイル：toot/hboost.txt  
　　　※中身はサンプルを参考にしてください  



<a id="iHardLook"></a>
## ハード監視機能
サーバのメモリ、スワップ、ディスク残量をチェックし、毎日0時に管理者にDMで送ります。  
内部ではcsvファイルに記録します。（log配下に保存される）  
　機能有効：LookHard=on  



<a id="iManualToot"></a>
## 手動トゥート機能
クライアントから手動でトゥートをおこなう機能です。  
3種類の送信方法があります。  
* 手動トゥート  
  任意のアカウント１つでトゥートします。  
  通常通り public / unlisted / private / direct の公開範囲が切替できます。  
* 同報配信トゥート  
  るしぼっとに登録されているすべてのアカウントで一斉配信をおこないます。  
  masterアカウントはpublic固定、subアカウントはpublic / unlistedの公開範囲が切替できます。  
  ※subアカウントのpublicトゥートは、多数の連合鯖に同じトゥートが送信されるため、多用は避けましょう。  



<a id="iTwitter"></a>
## twitter連携機能
APIを取得したアカウントに連携し、トゥートをツイートします。  
またTwitterタイムライン上の指定ユーザのツイートをmastodonにトゥートします。  
本機能を有効にするにはTwitter APIを取得する必要があります。（＜twitter APIの取得方法＞参照）  
　機能有効：Twitter=on  

＜ツイートされる内容＞  
* 1時間ごとのmastodonトラヒック  
* 同報配信トゥート  



<a id="iTwitterReader"></a>
## twitterリーダ機能
twitter上のホームタイムラインからパターンを読み取り、mastodonにトゥートします。  
また1時間ごとにtwitterのトレンドをmastodonにトゥートします。  
twitterのパターン、トゥートを送信するアカウントはパターンファイルで指定します。  
本機能を有効にするにはTwitter連携設定をする必要があります。（＜twitter連携機能＞参照）  
　機能有効：Twitter=on  
　　twitterリーダ ファイル：toot/twitter_reader.txt    
　　　※中身はサンプルを参考にしてください  



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



