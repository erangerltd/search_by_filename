# ファイル名検索（電子帳簿）

![ファイル名検索](https://s3.ap-northeast-1.amazonaws.com/media-new.eranger.co.jp/wp-content/uploads/20220921113907/screen_of_searchbyfilename.png )

## 機能
特定のフォルダーにあるファイルを名前（一部）で検索する簡易ツールです。 
  
## 目的
電子帳簿保存法（2022/1/1施行。2023/12/31まで宥恕期間）における電子取引情報に関する要求のうち、  
- 「⽇付・⾦額・取引先」で検索できるようにする  
  
を満たすことが意外と大変なため、これを補助するために作っています。
改ざん防止、改ざんの検知の機能はありませんのでご注意ください。  
  
電子帳簿保存法やその要求・解釈については、詳しくは国税庁のホームページをご参照ください。   
- [国税庁パンフレット](https://www.nta.go.jp/publication/pamph/sonota/0021011-068.pdf)
- [国税庁電子帳簿保存法一問一答 電子取引関連](https://www.nta.go.jp/law/joho-zeikaishaku/sonota/jirei/pdf/0022006-083_06.pdf)
  

## 稼働環境
Linuxファイルサーバー（Samba）の利用を想定しています。   
Python3が導入されていること   
Flaskが利用可能なこと   

