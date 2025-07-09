#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot 設定工具
幫助用戶快速設定LINE Bot和Gemini API的參數
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """創建.env檔案"""
    print("🤖 LINE Bot with Gemini AI 設定工具")
    print("=" * 50)
    
    # 檢查.env檔案是否存在
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env檔案已存在")
        overwrite = input("是否要覆蓋現有的.env檔案？(y/N): ").lower()
        if overwrite != 'y':
            print("❌ 設定已取消")
            return False
    
    print("\n📝 請提供以下資訊：")
    print("💡 如果不確定如何取得這些資訊，請參考 README_LINEBOT.md")
    print()
    
    # 收集LINE Bot資訊
    print("🔹 LINE Bot 設定")
    print("前往 https://developers.line.biz/console/ 取得")
    line_access_token = input("請輸入 LINE Channel Access Token: ").strip()
    line_channel_secret = input("請輸入 LINE Channel Secret: ").strip()
    
    print()
    
    # 收集Gemini API資訊
    print("🔹 Google Gemini API 設定")
    print("前往 https://aistudio.google.com/app/apikey 取得")
    google_api_key = input("請輸入 Google API Key: ").strip()
    
    # 驗證輸入
    if not all([line_access_token, line_channel_secret, google_api_key]):
        print("❌ 所有欄位都是必填的！")
        return False
    
    # 創建.env檔案內容
    env_content = f"""# LINE Bot設定
# 從 LINE Developers Console 取得
LINE_CHANNEL_ACCESS_TOKEN={line_access_token}
LINE_CHANNEL_SECRET={line_channel_secret}

# Google Gemini API設定
# 從 Google AI Studio 取得
GOOGLE_API_KEY={google_api_key}

# Flask環境設定
FLASK_ENV=development
FLASK_DEBUG=true
"""
    
    # 寫入檔案
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print()
        print("✅ .env檔案創建成功！")
        print()
        return True
        
    except Exception as e:
        print(f"❌ 創建.env檔案時發生錯誤: {e}")
        return False

def check_dependencies():
    """檢查依賴套件"""
    print("🔍 檢查依賴套件...")
    
    required_packages = [
        'flask',
        'line-bot-sdk', 
        'google-generativeai',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (未安裝)")
            missing_packages.append(package)
    
    if missing_packages:
        print()
        print("⚠️  發現缺少的套件，請執行以下指令安裝：")
        print(f"pip install {' '.join(missing_packages)}")
        print()
        print("或者安裝所有依賴：")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 所有依賴套件都已安裝")
    return True

def test_configuration():
    """測試配置"""
    print("🧪 測試配置...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # 檢查環境變數
        line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        line_secret = os.getenv('LINE_CHANNEL_SECRET')
        google_key = os.getenv('GOOGLE_API_KEY')
        
        if not all([line_token, line_secret, google_key]):
            print("❌ 環境變數未正確設定")
            return False
        
        # 測試Gemini API連接
        try:
            import google.generativeai as genai
            genai.configure(api_key=google_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hello")
            print("✅ Gemini API 連接成功")
        except Exception as e:
            print(f"❌ Gemini API 測試失敗: {e}")
            return False
        
        print("✅ 配置測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 配置測試失敗: {e}")
        return False

def show_next_steps():
    """顯示後續步驟"""
    print()
    print("🎉 設定完成！")
    print("=" * 50)
    print("📋 後續步驟：")
    print()
    print("1. 設定 Webhook URL：")
    print("   - 前往 LINE Developers Console")
    print("   - 在你的Channel中設定 Webhook URL: https://你的網域/callback")
    print("   - 啟用 'Use webhook'")
    print()
    print("2. 啟動 LINE Bot：")
    print("   python linebot_gemini.py")
    print()
    print("3. 測試用 ngrok（開發環境）：")
    print("   # 另一個終端")
    print("   ngrok http 5000")
    print()
    print("📖 詳細說明請參考 README_LINEBOT.md")

def main():
    """主函數"""
    print("🚀 LINE Bot with Gemini AI 設定工具")
    print()
    
    # 選單
    while True:
        print("請選擇操作：")
        print("1. 設定環境變數(.env)")
        print("2. 檢查依賴套件")
        print("3. 測試配置")
        print("4. 完整設定流程")
        print("5. 顯示後續步驟")
        print("0. 離開")
        
        choice = input("\n請輸入選項 (0-5): ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            check_dependencies()
        elif choice == '3':
            test_configuration()
        elif choice == '4':
            print("🔄 執行完整設定流程...")
            if check_dependencies() and create_env_file() and test_configuration():
                show_next_steps()
        elif choice == '5':
            show_next_steps()
        elif choice == '0':
            print("👋 再見！")
            break
        else:
            print("❌ 無效的選項，請重新選擇")
        
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 設定已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        sys.exit(1)