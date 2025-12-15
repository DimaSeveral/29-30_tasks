# bot.py
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from fsm_states import get_current_state
from handlers import start_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8217417040:AAERkyu53aK8yAt1AnPAeFNn4BILSpaAqM0"

# ───── ЦЕНТРАЛЬНЫЙ FSM-ДИСПЕТЧЕР ─────
async def fsm_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Автоматное программирование: корутина-диспетчер"""
    current_state = get_current_state(context)
    logger.info(f"FSM: {update.effective_user.id} в состоянии {current_state.name}")
    # Вызов корутины-обработчика состояния
    await current_state.handler(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fsm_router))
    logger.info("Бот запущен с FSM на корутинах")
    app.run_polling()
    
if __name__ == "__main__":
    main()
 
