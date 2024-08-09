# 台灣機車考照預約報名搶票工具

## 這是一個搶票工具，用於機車考照預約報名，該程式會自動計算30天後的民國日期並於凌晨00:00:05自動執行。

### 安裝
一般用戶請至[Realease](https://github.com/GinoLin980/Driver-License-Speedrun/releases)下載`Driver License Sign Up Speedrun.exe`, `imformation.toml`, `keywords.toml`, `msedgedriver.exe`並放在同目錄下。

隨後執行`Driver License Sign Up Speedrun.exe`並根據提示選擇，排程成功後請勿關閉程式。

若未能成功搶到，請隔天再次執行程式。

#### **監理站未必每天開放報名。**

Geeks們請用:
```
git clone git https://github.com/GinoLin980/Driver-License-Speedrun.git
pip install -r requirements.txt
```

___

### 拓展
這個程式目前支持
```
臺北市區監理所（含金門馬祖）
├── 士林監理站 (臺北市士林區承德路5段80號)
├── 基隆監理站 (基隆市七堵區實踐路296號)
└── 金門監理站 (金門縣金湖鎮黃海路六之一號)

臺北區監理所（北宜花）
├── 臺北區監理所 (新北市樹林區中正路248巷7號)
├── 板橋監理站 (新北市中和區中山路三段116號)
├── 宜蘭監理站 (宜蘭縣五結鄉中正路二段9號)
├── 花蓮監理站 (花蓮縣吉安鄉中正路二段152號)
├── 玉里監理分站 (花蓮縣玉里鎮中華路427號)
└── 蘆洲監理站 (新北市蘆洲區中山二路163號)
```

如果你要報考的監理站不在上面，你可以到`keywords.toml`拓展，格式如下
```toml
["監理所名稱"]
    ["監理所名稱.監理站名稱"]
            Station = "監理站名稱"
            First = ["初考關鍵字", "初考關鍵字"]
            Retake = ["重考關鍵字", "重考關鍵字"]
```
`監理所名稱`，`監理站名稱`與`關鍵字`請自行至[監理服務網 - 考照預約報名](https://www.mvdis.gov.tw/m3-emv-trn/exm/locations)查詢。

___

#### 有任何問題請至[Issue](https://github.com/GinoLin980/Driver-License-Speedrun/issues)提問。
