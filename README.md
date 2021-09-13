# HU-schedule-scraping
北大のシラバスから時間割をスクレイピングするツール

## 使い方
versionが93.0.4577.63.0のchromeとpipenvをインストール

パッケージのインストール
```
pipenv sync --dev
```

データを取得する。
```
pipenv run scraping [termID] [facultyID]
```

termIDとfacultyIDはtable.pyを参照してください。  
facultyIDは「all」と入力可能で、全ての学部を一度にスクレイピングします。
