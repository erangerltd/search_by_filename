# ファイル名検索（電子帳簿保存法支援）

![ファイル名検索](https://s3.ap-northeast-1.amazonaws.com/media-new.eranger.co.jp/wp-content/uploads/20220922104815/dencho-list.png)

  

## このアプリケーションの目的
電子帳簿保存法（2022/1/1施行。2023/12/31まで宥恕期間）における電子取引情報の保存を想定しています。  
  
ファイルサーバーにこれらのデータを保存した場合、要求される  
- 「⽇付・⾦額・取引先」で検索できること  
  
を`ファイルサーバーのみの機能で満たすこと`は（ファイルサーバーのスペックなどに依存しますが）意外と大変です。  
また、調査時に`検索した結果を整形したリストとして印刷する`ことも同様です。  
このアプリケーションは、これらの点のみにフォーカスして電子帳簿保存法を支援するためのものです。  


### 特記事項
改ざん防止、改ざんの検知の機能はありませんのでご注意ください。  


電子帳簿保存法やその要求・解釈については、詳しくは国税庁のホームページをご参照ください。   
- [国税庁パンフレット](https://www.nta.go.jp/publication/pamph/sonota/0021011-068.pdf)
- [国税庁電子帳簿保存法一問一答 電子取引関連](https://www.nta.go.jp/law/joho-zeikaishaku/sonota/jirei/pdf/0022006-083_06.pdf)
  
  
  
## 機能
特定のフォルダーにあるファイルを名前（一部）で検索する簡易ツールです。   
国税庁の資料にあるようにファイル名が
>
> yyyymmdd_取引先名_金額_任意文字列_マーカー.pdf（pngなど）
>
となっていることを前提にしています。上で「マーカー」とは`ファイルを検索対象に含めるための文字列`のことです。デフォルトでは「###」が指定されています。（jsonで変更可能です）  

その他の機能は以下です。  
- 利用ユーザーの登録・ログイン機能
- 検索フォルダー指定機能（json）
- 検索対象ファイル（拡張子）指定機能（json）
- 日付（yyyymmdd）での期間絞り込み機能
- フリーワードでの絞り込み機能（部分一致検索）
- 金額での絞り込み機能（フリーワードとして）
- 絞り込み結果のCSVダウンロード機能
- ファイルリストからのデータダウンロード機能
- 最終登録更新日時、ファイルサイズ表示機能
  

### 検索機能
  
![検索ボックス](https://s3.ap-northeast-1.amazonaws.com/media-new.eranger.co.jp/wp-content/uploads/20220922105709/dencho-search.png)
  
  
利用用途として`期間を指定した検索`を想定しています。
- 特定の期間における特定の取引先
- 特定の期間における特定の金額
- 特定の期間における特定のキーワード
  

検索開始日は入力必須です。入力がない場合には、画面を開いた日（年月）の２ヶ月前の１日が設定されます。  
`特定の金額`、`特定のキーワード`を指定したい場合には、`フリーワード`欄を利用してください。複数検索には対応していません。  
フリーワードでの検索は部分一致検索となっています。ファイル名中にメモを入れるなどすると便利かと思います。  
  
`CSVダウンロード機能`は画面に表示されたファイル名のリストを`整形した文書（Excel）`として利用するためのものです。  



## 稼働環境
- Linuxファイルサーバー（Samba）の利用を想定しています。   
- Python3が導入されていること   
- Flaskが利用可能なこと   
  


## ライセンス
MITライセンス  
なお、コードの多くは[Flaskのチュートリアル](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/index.html)からお借りしました。
  
  


## 初期設定
python3で`Flask`が実行できる環境であれば、アプリケーションはソースコードを配備するだけで稼働します。  
以下ではアプリケーションを配備したディレクトリを`$APP_PATH`と呼びます。
  


### 設定ファイルの説明
設定ファイルが`$APP_PATH/instances/dencho_config.json`にあります。ご利用環境に合わせて変更してください。
  

    {
        "DOC_KEY": "###",
        "DOC_FORMAT":[
            "pdf", "png", "jpg"
        ],
        "DOC_PATH":[
            "/home/経理保管資料/電子帳簿保存法"
        ]
    }

- DOC_KEY: ファイルを検索対象とするためのマーカーです（上記）
- DOC_FORMAT: 検索対象とする拡張子です。複数指定可。
- DOC_PATH: 検索対象とするディレクトリ（絶対パス）です。指定したディレクトリの配下にあるファイルを再帰的に検索します。複数指定可。
  


### データベース（SQLite）の初期化  
`$APP_PATH`にて以下のようにSQLiteデータベースを初期化してください。
  
    
    export FLASK_APP=flaskr
    flask init-db


  
## アプリケーションの起動
### 起動
`$APP_PATH`で以下のように起動します。  
以下ではport番号=12345で起動しています。
    
    export FLASK_APP=flaskr
    flask run --host=0.0.0.0 --port=12345

以下のようなメッセージが出ればアプリケーションは稼働しています。  
警告`WARNING`が出ますが、`プロダクションユースの場合にはちゃんとしたHTTPサーバーを使うべきである`という意味ですので、アプリケーションを試用する分には問題ありません。  
  
    * Serving Flask app "flaskr"
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: off

> FlaskはWSGIに対応していますので、必要に応じてHTTPサーバーを変更することができます。  
> [wikipedia: Web Server Gateway Interface(WSGI)](https://ja.wikipedia.org/wiki/Web_Server_Gateway_Interface)  

ブラウザーより指定したポートにアクセスするとログイン画面が表示されます。  
たとえば、ローカルホスト（`127.0.0.1`）からアクセスする場合には`127.0.0.1:12345`にアクセスします。  
  
![ログイン](https://s3.ap-northeast-1.amazonaws.com/media-new.eranger.co.jp/wp-content/uploads/20220922102644/dencho-login.png )



### ユーザー登録
ログインするためにはユーザーを登録する必要があります。  
ユーザーを登録するには`127.0.0.1:12345/auth/register`にアクセスし、以下の画面より登録してください。  
  
![ユーザー登録](https://s3.ap-northeast-1.amazonaws.com/media-new.eranger.co.jp/wp-content/uploads/20220922103716/dencho-register.png)  



### ログインとファイル名の一覧
再び`127.0.0.1:12345`にアクセスし、上で登録したユーザーでログインするとファイルの一覧が表示されます。
  
  
![ファイル名検索](https://s3.ap-northeast-1.amazonaws.com/media-new.eranger.co.jp/wp-content/uploads/20220922104815/dencho-list.png)
  

- ファイル名をクリックするとダウンロードされます。
- 検索結果のリストに`最終変更日時`が出力されますが、これはファイルが保管もしくは改変された日時を表しています。国税庁資料にあるタイムスタンプを正確に表すものではありませんのでご注意ください。
