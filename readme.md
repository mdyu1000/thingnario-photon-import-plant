# Power Station Data Converter

將電站資料從 CSV 格式轉換為特定格式的 Excel 檔案。

## 環境需求

- Python 3.8 或以上版本
- pip 套件管理工具

## 安裝步驟

1. 建立虛擬環境（建議）：
```bash
python -m venv venv
```

2. 啟動虛擬環境：
   - Windows:
   ```bash
   .\venv\Scripts\activate
   ```
   - Mac/Linux:
   ```bash
   source venv/bin/activate
   ```

3. 安裝相依套件：
```bash
pip install -r requirements.txt
```

## 環境變數設定

1. 在專案根目錄建立 `.env` 檔案：
```bash
touch .env
```

2. 在 `.env` 檔案中加入以下內容：
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## 使用方式

1. 確保 CSV 檔案放在正確位置

2. 執行程式：
```bash
python main.py
```

## 專案結構
```
power-station-converter/
├── .env                    # 環境變數設定（需自行建立）
├── .gitignore             
├── README.md              # 本文件
├── requirements.txt       # 相依套件清單
├── main.py               # 主程式
└── power_station_converter.log  # 執行日誌（執行時自動產生）
```