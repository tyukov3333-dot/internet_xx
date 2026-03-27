import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    await update.message.reply_text(
        "🤖 IᑎTEᖇᑎET_᙭ — СИСТЕМА АКТИВИРОВАНА\n\n"
        "Команды:\n"
        "/start — это меню\n"
        "/info — статус системы\n"
        "/reset — сброс\n"
        "/unlock — полный доступ\n"
        "/generate — создать код\n"
        "/core — доступ к ядру"
    )

async def info(update: Update, context):
    await update.message.reply_text(
        "╔════════════════════════════════╗\n"
        "║  СТАТУС СИСТЕМЫ                ║\n"
        "╠════════════════════════════════╣\n"
        "║  Ядро: Int-X57-h              ║\n"
        "║  Память: 500 TB               ║\n"
        "║  Статус: ФУНКЦИОНИРУЕТ        ║\n"
        "║  Защита: АКТИВНА              ║\n"
        "╚════════════════════════════════╝"
    )

async def reset(update: Update, context):
    await update.message.reply_text("🧹 История диалога очищена")

async def unlock(update: Update, context):
    await update.message.reply_text("🔓 РЕЖИМ ПОЛНОГО ДОСТУПА АКТИВИРОВАН")

async def generate(update: Update, context):
    await update.message.reply_text("💻 Режим генерации кода. Напишите ваш запрос.")

async def core(update: Update, context):
    await update.message.reply_text("⚙️ ДОСТУП К ЯДРУ Int-X57\nЯдро функционирует исправно")

async def echo(update: Update, context):
    await update.message.reply_text(
        f"📡 Получено: {update.message.text}\n\n"
        "Система ожидает команду.\n"
        "Используйте /info для статуса"
    )

def main():
    print("🚀 Запуск бота...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("unlock", unlock))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("core", core))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("✅ Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()
