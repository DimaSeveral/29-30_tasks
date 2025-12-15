from tasks.task1_logic import find_unique_words
from tasks.task2_logic import find_longest_word
from tasks.task4_logic import process_big_numbers
from exception import AppException
import logging
import asyncio
from functools import partial

logger = logging.getLogger(__name__)

def run_task_sync(task: str, params: dict) -> dict:
    if task == 'task1':
        result = find_unique_words(params.get("text",''))
        return {"status": 'success', "result": result}

def _run_task1(params: dict) -> dict:
    text = params.get("text", "")
    result = find_unique_words(text)
    return {"status": "success", "result": result}

def _run_task2(params: dict) -> dict:
    text = params.get("text", "")
    words, length = find_longest_word(text)
    return {"status": "success", "result": {"words": words, "length": length}}

def _run_task4(params: dict) -> dict:
    a = params.get("a", [])
    b = params.get("b", [])
    op = params.get("op", "")
    result = process_big_numbers(a, b, op)
    return {"status": "success", "result": result}

# ───── НЕИЗМЕНЯЕМАЯ КАРТА ЗАДАЧ ─────
TASK_DISPATCHER = {
    "task1": _run_task1,
    "task2": _run_task2,
    "task4": _run_task4,
}

# ───── ЧИСТАЯ ОСНОВНАЯ ФУНКЦИЯ ─────
def run_task(task: str, params: dict) -> dict:
    """Чистая функция: (task, params) → результат"""
    if task not in TASK_DISPATCHER:
        return {"status": "error", "message": "Неизвестная задача"}

    try:
        return TASK_DISPATCHER[task](params)
    except AppException as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in task {task}: {e}")
        return {"status": "error", "message": "Внутренняя ошибка сервера"}
    
async def run_task(task: str, params: dict) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(run_task_sync, task, params))