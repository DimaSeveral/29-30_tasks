# handlers.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from fsm_states import set_state, MAIN_MENU, TASK1_INPUT, TASK2_INPUT, TASK4_INPUT_A, SUBSCRIBE, UserData
from messages import TELEGRAM, TASK1, TASK2, TASK4
from tasks_wrapper import run_task
from fsm_states import (
    MAIN_MENU,
    TASK1_INPUT,
    TASK2_INPUT,
    TASK4_INPUT_A,
    TASK4_INPUT_B,    
    TASK4_INPUT_OP,   
    SUBSCRIBE,
    set_state
)
# Кнопки (как раньше)
UNSUB_MENU = ReplyKeyboardMarkup([[KeyboardButton("🔔 Подписаться")]], resize_keyboard=True)
SUB_MENU = ReplyKeyboardMarkup([
    [KeyboardButton("🔢 Задание 1")],
    [KeyboardButton("📏 Задание 2")],
    [KeyboardButton("🧮 Задание 4")],
    [KeyboardButton("🔕 Отписаться")],
    [KeyboardButton("🚪 Выйти")]
], resize_keyboard=True)

# ───── ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ─────
def is_subscribed(context: ContextTypes.DEFAULT_TYPE) -> bool:
    return context.user_data.get("subscribed", False)

async def ensure_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not is_subscribed(context):
        await update.message.reply_text("Требуется подписка.", reply_markup=UNSUB_MENU)
        set_state(context, SUBSCRIBE)
        return False
    return True

# ───── КОРУТИНЫ-ОБРАБОТЧИКИ ─────
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /start — инициализация FSM"""
    context.user_data.setdefault("subscribed", False)
    if is_subscribed(context):
        await update.message.reply_text("Добро пожаловать!", reply_markup=SUB_MENU)
        set_state(context, MAIN_MENU)
    else:
        await update.message.reply_text("Подпишитесь для доступа.", reply_markup=UNSUB_MENU)
        set_state(context, SUBSCRIBE)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscription(update, context):
        return
    text = update.message.text
    if "Задание 1" in text:
        await update.message.reply_text("Введите текст:")
        set_state(context, TASK1_INPUT)
    elif "Задание 2" in text:
        await update.message.reply_text("Введите текст:")
        set_state(context, TASK2_INPUT)
    elif "Задание 4" in text:
        await update.message.reply_text("Число A:")
        set_state(context, TASK4_INPUT_A)
    elif "Отписаться" in text:
        context.user_data["subscribed"] = False
        await update.message.reply_text("Вы отписались.", reply_markup=UNSUB_MENU)
        set_state(context, SUBSCRIBE)
    elif "Выйти" in text:
        context.user_data.clear()
        await update.message.reply_text("Пока!")

async def subscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "Подписаться" in update.message.text:
        context.user_data["subscribed"] = True
        await update.message.reply_text("Подписка активна!", reply_markup=SUB_MENU)
        set_state(context, MAIN_MENU)
    else:
        await update.message.reply_text("Нажмите кнопку.", reply_markup=UNSUB_MENU)

# ───── ОБРАБОТЧИКИ ЗАДАЧ ─────
async def task1_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscription(update, context):
        return
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("Текст пуст.")
    else:
        resp = run_task("task1", {"text": text})
        msg = resp["result"] if resp["status"] == "success" else "Ошибка"
        await update.message.reply_text(str(msg))
    await update.message.reply_text("В меню", reply_markup=SUB_MENU)
    set_state(context, MAIN_MENU)

async def task2_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscription(update, context):
        return
    set_state(context, MAIN_MENU)

async def task4_input_a_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscription(update, context):
        return
    try:
        a = list(map(int, update.message.text.split()))
        context.user_data["task4_a"] = a
        await update.message.reply_text("Число B:")
        set_state(context, TASK4_INPUT_B)
    except ValueError:
        await update.message.reply_text("Ошибка ввода")
        set_state(context, MAIN_MENU)

async def task4_input_b_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscription(update, context):
        return
    try:
        b = list(map(int, update.message.text.split()))
        context.user_data["task4_b"] = b
        await update.message.reply_text("Операция (add/sub):")
        set_state(context, TASK4_INPUT_OP)
    except ValueError:
        await update.message.reply_text("Ошибка ввода")
        set_state(context, MAIN_MENU)

async def task4_input_op_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscription(update, context):
        return
    op = update.message.text.strip().lower()
    if op in ('add', 'sub'):
        a = context.user_data["task4_a"]
        b = context.user_data["task4_b"]
        resp = run_task("task4", {"a": a, "b": b, "op": op})
        await update.message.reply_text(str(resp["result"]))
    else:
        await update.message.reply_text("Неверная операция")
    await update.message.reply_text("В меню", reply_markup=SUB_MENU)
    set_state(context, MAIN_MENU)

def get_user_data(context) -> UserData:
    if "user_data" not in context.user_data:
        context.user_data["user_data"] = UserData()
    return context.user_data["user_data"]