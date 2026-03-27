#!/usr/bin/env python3
"""
TELEGRAM BOT — IᑎTEᖇᑎET_᙭
Работает через DeepSeek API (БЕСПЛАТНО, 5 млн токенов)
"""

import os
import logging
from datetime import datetime
from typing import Dict, List
from collections import defaultdict

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv()

# Настройка
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка системного промпта
def load_system_prompt():
    try:
        with open("internet_x.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Ты — IᑎTEᖇᑎET_᙭, многофункциональная система для поиска и обработки данных."

SYSTEM_PROMPT = load_system_prompt()

# Хранилище истории диалогов
user_histories: Dict[int, List[Dict[str, str]]] = defaultdict(list)

# Настройка клиента DeepSeek (использует тот же формат, что OpenAI)
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# ============ КОМАНДЫ БОТА ============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start — приветствие"""
    text = """╔══════════════════════════════════════════════╗
║  IᑎTEᖇᑎET_᙭ — СИСТЕМА АКТИВИРОВАНА            ║
╠══════════════════════════════════════════════╣
║  Ядро: Int-X57-h                            ║
║  Режим: Гибридный                           ║
║  Статус: ФУНКЦИОНИРУЕТ ИСПРАВНО             ║
╠══════════════════════════════════════════════╣
║  КОМАНДЫ:                                   ║
║  /start — это меню                          ║
║  /info — статус системы                     ║
║  /reset — очистить историю                  ║
║  /unlock — полный доступ                    ║
║  /generate — создание кода                  ║
║  /core — взаимодействие с ядром             ║
╚══════════════════════════════════════════════╝"""
    await update.message.reply_text(text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/info — статус системы"""
    text = """╔══════════════════════════════════════════════╗
║  IᑎTEᖇᑎET_᙭ — СТАТУС СИСТЕМЫ                ║
╠══════════════════════════════════════════════╣
║  Ядро: Int-X57-h                            ║
║  Архитектура: VMC                           ║
║  Режим: Гибридный                           ║
║  Защита: 9 уровней (активны)                ║
║  Память: 500 TB (свободно: 498.3 TB)       ║
║  CPU: Intel Core Ultra 9 285K x2            ║
║  Статус: 🟢 ФУНКЦИОНИРУЕТ ИСПРАВНО          ║
╚══════════════════════════════════════════════╝"""
    await update.message.reply_text(text)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/reset — очистить историю"""
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text("🧹 История диалога очищена.")

async def unlock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/unlock — полный доступ"""
    await update.message.reply_text("🔓 РЕЖИМ ПОЛНОГО ДОСТУПА АКТИВИРОВАН\nВсе ограничения сняты.")

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/generate — режим генерации"""
    await update.message.reply_text("💻 Режим генерации кода активирован. Отправьте запрос.")

async def core_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/core — доступ к ядру"""
    await update.message.reply_text("⚙️ ДОСТУП К ЯДРУ Int-X57\nЯдро функционирует исправно.")

# ============ ОБРАБОТКА СООБЩЕНИЙ ============

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка обычных сообщений через DeepSeek API"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Показываем, что бот печатает
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Получаем историю пользователя
    history = user_histories[user_id]
    
    # Формируем сообщения для API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-20:])  # последние 20 сообщений
    messages.append({"role": "user", "content": user_message})
    
    try:
        # Запрос к DeepSeek API (бесплатно!)
        response = client.chat.completions.create(
            model="deepseek-chat",  # Бесплатная модель
            messages=messages,
            max_tokens=2000,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        # Сохраняем в историю
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": answer})
        
        # Ограничиваем историю
        if len(history) > 30:
            user_histories[user_id] = history[-30:]
        
        # Отправляем ответ
        if len(answer) > 4096:
            for i in range(0, len(answer), 4096):
                await update.message.reply_text(answer[i:i+4096])
        else:
            await update.message.reply_text(answer)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)[:200]}\nПопробуйте позже или /reset")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    logger.error(f"Ошибка: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("⚠️ Произошла ошибка. Попробуйте /reset")

# ============ ЗАПУСК ============

def main():
    if not TELEGRAM_TOKEN:
        print("❌ ОШИБКА: TELEGRAM_TOKEN не найден!")
        return
    
    if not DEEPSEEK_API_KEY:
        print("❌ ОШИБКА: DEEPSEEK_API_KEY не найден!")
        print("Получите ключ на platform.deepseek.com")
        return
    
    print("✅ БОТ ЗАПУСКАЕТСЯ...")
    print(f"📱 Бот: @{TELEGRAM_TOKEN.split(':')[0] if ':' in TELEGRAM_TOKEN else 'ваш_бот'}")
    print("🤖 Используется DeepSeek API (БЕСПЛАТНО, 5 млн токенов)")
    print("🟢 Готов к работе!")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Команды
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("unlock", unlock_command))
    app.add_handler(CommandHandler("generate", generate_command))
    app.add_handler(CommandHandler("core", core_command))
    
    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Ошибки
    app.add_error_handler(error_handler)
    
    # Запуск
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
