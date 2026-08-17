import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import os
import json
from datetime import datetime

# Импорт твоего CV-модуля
from ai_vision import find_text_center

from core.intent import run_agent

app = FastAPI(title="Omni-Jarvis Vision Server")

# Конфиг: список целей для поиска. Расширишь под кнопки 1С (например, "Новый", "Записать", "Terminal")
TARGETS = ["Файл", "file", "terminal", "записать", "новая", "провести", "правка", "вид"]

# Папка для временных файлов (рабочая директория)
TEMP_IMAGE = "server_get.png"

@app.post("/post")
async def handle_ocr_request(file: UploadFile = File(...)):
    """
    Эндпоинт принимает скриншот, возвращает координаты центра целевого текста.
    """
    # 1. Валидация размера (защита от OOM)
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Read error: {str(e)}")

    # 2. Жесткая перезапись файла (защита диска C от мусора)
    try:
        with open(TEMP_IMAGE, "wb") as buffer:
            buffer.write(contents)
    except IOError as e:
        raise HTTPException(status_code=500, detail=f"Disk write error: {str(e)}")

    # 3. Запуск ИИ-зрения. Тайминг для твоего понимания производительности.
    print(f"[{datetime.now().strftime('%H:%M:%S')}] OCR started for {file.filename}")
    result = find_text_center(TEMP_IMAGE, TARGETS)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] OCR finished")

    # 4. Формируем JSON-ответ строго по спецификации
    if result:
        return {
            "status": "success",
            "x": result['x'],
            "y": result['y'],
            "matched_text": result['text'],
            "confidence": round(result['confidence'], 3)
        }
    else:
        return {
            "status": "not_found",
            "message": f"None of {TARGETS} found"
        }

# Точка входа для прямого запуска (python server.py)
@app.post("/command")
async def handle_command(command: dict):
    """
    Эндпоинт для текстовых команд.
    Принимает JSON: {"command": "текст команды"}
    Возвращает результат выполнения агента (симуляция).
    """
    text = command.get("command", "")
    if not text:
        raise HTTPException(status_code=400, detail="Поле 'command' обязательно")
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Команда: {text}")
    result = run_agent(text)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Результат: {result}")
    
    return {"status": "ok", "result": result}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)