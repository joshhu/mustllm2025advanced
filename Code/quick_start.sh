#!/bin/bash

echo "🚀 LINE Bot with Gemini AI - 快速開始"
echo "=================================="

# 檢查Python版本
echo "🔍 檢查Python版本..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ $python_version"
else
    echo "❌ Python3 未安裝"
    exit 1
fi

# 安裝依賴
echo "📦 安裝依賴套件..."
pip3 install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ 依賴套件安裝完成"
else
    echo "❌ 依賴套件安裝失敗"
    exit 1
fi

# 檢查.env檔案
if [[ ! -f ".env" ]]; then
    echo "⚠️  .env檔案不存在"
    echo "📝 請運行設定工具："
    echo "python3 setup_linebot.py"
    echo ""
    echo "或手動複製並編輯："
    echo "cp .env.example .env"
    echo "nano .env"
    exit 1
fi

echo "✅ .env檔案已存在"

# 啟動程式
echo "🚀 啟動LINE Bot..."
echo "📍 服務將運行在 http://localhost:5000"
echo "🔗 Webhook URL: http://你的網域/callback"
echo ""
echo "💡 開發環境可使用 ngrok:"
echo "   ngrok http 5000"
echo ""
echo "按 Ctrl+C 停止服務"
echo ""

python3 linebot_gemini.py