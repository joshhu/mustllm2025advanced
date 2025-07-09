# LINE Bot with Google Gemini AI

使用Google Gemini模型的LINE聊天機器人，支援對話記憶功能。

## 🚀 功能特色

- ✅ 使用最新的Google Gemini 1.5 Flash模型
- ✅ 支援對話記憶（每位用戶獨立記憶）
- ✅ 繁體中文回應
- ✅ 簡單的指令系統
- ✅ 完整的錯誤處理
- ✅ 生產環境就緒

## 📋 系統需求

- Python 3.8+
- LINE Developers帳號
- Google AI Studio API Key

## 🛠️ 安裝步驟

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定LINE Bot

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 創建新的 Provider（如果還沒有）
3. 創建新的 Messaging API Channel
4. 取得以下資訊：
   - **Channel Access Token**
   - **Channel Secret**

### 3. 設定Google Gemini API

1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 創建新的API Key
3. 複製API Key

### 4. 設定環境變數

```bash
# 複製範例檔案
cp .env.example .env

# 編輯 .env 檔案，填入你的資訊
nano .env
```

在 `.env` 檔案中填入：
```env
LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_ACCESS_TOKEN
LINE_CHANNEL_SECRET=你的_LINE_CHANNEL_SECRET
GOOGLE_API_KEY=你的_GOOGLE_API_KEY
```

### 5. 設定Webhook URL

1. 回到LINE Developers Console
2. 在你的Channel設定中，找到「Webhook settings」
3. 設定Webhook URL: `https://你的網域/callback`
4. 啟用「Use webhook」

## 🏃‍♂️ 運行程式

### 開發環境
```bash
python linebot_gemini.py
```

### 生產環境
```bash
gunicorn -w 4 -b 0.0.0.0:5000 linebot_gemini:app
```

## 🔧 使用方式

### 基本聊天
直接在LINE中傳送任何訊息給Bot，它會使用Gemini AI回應。

### 特殊指令
- `幫助` 或 `help` - 顯示功能說明
- `清除歷史` 或 `clear` - 清除對話記憶

## 📁 檔案結構

```
Code/
├── linebot_gemini.py      # 主程式
├── requirements.txt       # Python依賴套件
├── .env.example          # 環境變數範例
├── .env                  # 實際環境變數（需自行創建）
└── README_LINEBOT.md     # 說明文件
```

## 🔒 安全性注意事項

1. **永遠不要將 `.env` 檔案提交到版本控制**
2. **定期更換API Keys**
3. **在生產環境中使用HTTPS**
4. **考慮實施速率限制**

## 🚀 部署選項

### Heroku部署
1. 安裝Heroku CLI
2. 創建 `Procfile`:
   ```
   web: gunicorn linebot_gemini:app
   ```
3. 設定Config Vars（環境變數）
4. 推送到Heroku

### Railway部署
1. 連接GitHub儲存庫
2. 設定環境變數
3. 自動部署

### ngrok（開發測試用）
```bash
# 安裝ngrok
npm install -g ngrok

# 啟動程式
python linebot_gemini.py

# 另一個終端
ngrok http 5000
```

## 🐛 常見問題

### Q: Bot沒有回應
A: 檢查以下項目：
- Webhook URL是否正確設定
- 環境變數是否正確
- 程式是否正常運行
- LINE Channel設定是否正確

### Q: Gemini API錯誤
A: 確認：
- API Key是否正確
- 是否有API配額
- 網路連線是否正常

### Q: 對話記憶不工作
A: 目前使用記憶體儲存，重啟程式會清除記憶。生產環境建議使用Redis或資料庫。

## 🔄 進階功能

### 添加資料庫支援
可以整合Redis或MySQL來持久化對話記憶：

```python
# 範例：使用Redis
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

### 添加圖片識別
Gemini支援圖片分析，可以擴展為多模態機器人。

### 添加語音回覆
可以整合TTS服務提供語音回覆。

## 📞 技術支援

如有問題，請檢查：
1. Python版本是否符合需求
2. 依賴套件是否正確安裝
3. 環境變數是否正確設定
4. API配額是否足夠

## 📄 授權

此程式僅供學習和研究用途使用。