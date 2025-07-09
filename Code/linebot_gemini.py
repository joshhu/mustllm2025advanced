#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot with Google Gemini AI
使用Google Gemini模型的LINE聊天機器人
"""

import os
import logging
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Flask應用
app = Flask(__name__)

class GeminiLineBotConfig:
    """配置類別"""
    def __init__(self):
        # LINE Bot配置
        self.LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        self.LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
        
        # Google Gemini配置
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        
        # 驗證必要的環境變數
        self._validate_config()
    
    def _validate_config(self):
        """驗證配置是否完整"""
        missing_vars = []
        
        if not self.LINE_CHANNEL_ACCESS_TOKEN:
            missing_vars.append('LINE_CHANNEL_ACCESS_TOKEN')
        if not self.LINE_CHANNEL_SECRET:
            missing_vars.append('LINE_CHANNEL_SECRET')
        if not self.GOOGLE_API_KEY:
            missing_vars.append('GOOGLE_API_KEY')
        
        if missing_vars:
            raise ValueError(f"缺少必要的環境變數: {', '.join(missing_vars)}")

class GeminiChatBot:
    """Google Gemini聊天機器人"""
    
    def __init__(self, api_key):
        """初始化Gemini模型"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 設定系統提示詞
        self.system_prompt = """
        你是一個友善且有幫助的AI助手。請用繁體中文回應用戶的問題。
        特點：
        - 回答要簡潔明瞭
        - 保持友善和禮貌的語調
        - 如果不確定答案，請誠實說明
        - 可以提供實用的建議和資訊
        """
        
        # 對話歷史（簡單版本，實際應用中建議使用資料庫）
        self.conversation_history = {}
    
    def generate_response(self, user_id, message):
        """生成回應"""
        try:
            # 獲取或初始化用戶的對話歷史
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # 構建完整的對話上下文
            conversation = [self.system_prompt]
            
            # 添加歷史對話（保留最近10輪對話）
            recent_history = self.conversation_history[user_id][-10:]
            for entry in recent_history:
                conversation.append(f"用戶: {entry['user']}")
                conversation.append(f"助手: {entry['assistant']}")
            
            # 添加當前用戶訊息
            conversation.append(f"用戶: {message}")
            
            # 組合成完整的提示詞
            full_prompt = "\n".join(conversation)
            
            # 調用Gemini API
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                assistant_reply = response.text.strip()
                
                # 保存對話到歷史
                self.conversation_history[user_id].append({
                    'user': message,
                    'assistant': assistant_reply,
                    'timestamp': datetime.now().isoformat()
                })
                
                return assistant_reply
            else:
                return "抱歉，我暫時無法回應這個問題。"
                
        except Exception as e:
            logger.error(f"Gemini API錯誤: {str(e)}")
            return "抱歉，系統發生錯誤，請稍後再試。"
    
    def clear_history(self, user_id):
        """清除用戶的對話歷史"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
            return "對話歷史已清除！"
        return "沒有找到對話歷史。"

# 初始化配置和服務
config = GeminiLineBotConfig()
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)
gemini_bot = GeminiChatBot(config.GOOGLE_API_KEY)

@app.route("/", methods=['GET'])
def home():
    """健康檢查端點"""
    return "LINE Bot with Gemini AI is running! 🤖"

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Bot webhook callback"""
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    logger.info(f"Request body: {body}")
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理文字訊息"""
    user_id = event.source.user_id
    user_message = event.message.text.strip()
    
    logger.info(f"收到用戶 {user_id} 的訊息: {user_message}")
    
    try:
        # 特殊指令處理
        if user_message.lower() in ['清除歷史', 'clear', 'reset']:
            reply_text = gemini_bot.clear_history(user_id)
        elif user_message.lower() in ['help', '幫助', '說明']:
            reply_text = """
🤖 LINE Bot with Gemini AI

功能說明：
• 直接輸入任何問題，我會用AI回答
• 輸入「清除歷史」可以重置對話
• 輸入「幫助」查看此說明

我會記住我們的對話內容，讓聊天更自然！
            """.strip()
        else:
            # 使用Gemini生成回應
            reply_text = gemini_bot.generate_response(user_id, user_message)
        
        # 發送回覆
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        
        logger.info(f"已回覆用戶 {user_id}: {reply_text[:50]}...")
        
    except Exception as e:
        logger.error(f"處理訊息時發生錯誤: {str(e)}")
        error_message = "抱歉，系統發生錯誤，請稍後再試。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=error_message)
        )

if __name__ == "__main__":
    print("🚀 啟動 LINE Bot with Gemini AI...")
    print("📝 請確保已設定所有必要的環境變數")
    print("🌐 服務將在 http://0.0.0.0:5000 運行")
    
    # 在生產環境中，建議使用 gunicorn 等 WSGI 服務器
    app.run(host='0.0.0.0', port=5000, debug=True)