# ファイル名検索（電子帳簿）

![ファイル名検索](https://s3.ap-northeast-1.amazonaws.com/media-new.eranger.co.jp/wp-content/uploads/20220921113907/screen_of_searchbyfilename.png )

  

## 目的
電子帳簿保存法（2022/1/1施行。2023/12/31まで宥恕期間）における電子取引情報に関する要求のうち、  
- 「⽇付・⾦額・取引先」で検索できるようにする  
  
を満たすことが意外と大変なため、これを補助するために作っています。
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
となっていることを前提にしています。上で「マーカー」とは「検索対象とするための任意の文字列」のことです。デフォルトでは「###」が指定されています。（jsonで変更可能です）    
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

  

## 稼働環境
Linuxファイルサーバー（Samba）の利用を想定しています。   
Python3が導入されていること   
Flaskが利用可能なこと   
  


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
- DOC_FORMAT: 検索対象とする拡張子です
- DOC_PATH: 検索対象とするディレクトリ（絶対パス）です。
  

### データベース（SQLite）の初期化  
`$APP_PATH`にて以下のようにSQLiteデータベースを初期化してください。
  
    
    export FLASK_APP=flaskr
    flask init-db


  

## 起動
### 起動
`$APP_PATH`で以下のように起動します。  
以下ではport番号=12345で起動しています。
    
    export FLASK_APP=flaskr
    flask run --host=0.0.0.0 --port=12345

以下のようなメッセージが出ればアプリケーションは稼働しています。  
警告`WARNING`が出ますが、プロダクションユースであればちゃんとしたHTTPサーバーを使うべきであるという意味ですので、アプリケーションを試用する分には問題ありません。  
  
    * Serving Flask app "flaskr"
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: off


### ユーザー登録


### ログインとファイル名の一覧



