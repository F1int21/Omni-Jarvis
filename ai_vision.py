# ai_vision.py (добавить в конец)
import easyocr
import numpy as np

# Глобальный ридер — инициализация ОДИН РАЗ. Языки 'ru' + 'en' для 1С и терминалов.
_reader = None

def get_reader():
    global _reader
    if _reader is None:
        # GPU у тебя нет, ставим gpu=False. Квантование для скорости.
        _reader = easyocr.Reader(['ru', 'en'], gpu=False, quantize=True)
    return _reader

def find_text_center(image_path: str, target_strings: list) -> dict:
    """
    Ищет target_strings на изображении.
    Возвращает: {'x': int, 'y': int, 'text': str, 'confidence': float} или None
    """
    reader = get_reader()
    # detail=1 для получения bounding box'ов
    results = reader.readtext(image_path, detail=1, paragraph=False)
    print(f"[DEBUG] Распознанные тексты: {[text for (_, text, _) in results]}")
    for (bbox, text, confidence) in results:
        # Приводим к нижнему регистру для сравнения (1С любит капслок)
        clean_text = text.strip().lower()
        for target in target_strings:
            if target.lower() in clean_text:
                # bbox: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                xs = [p[0] for p in bbox]
                ys = [p[1] for p in bbox]
                cx = int(sum(xs) / 4)
                cy = int(sum(ys) / 4)
                return {'x': cx, 'y': cy, 'text': text, 'confidence': confidence}
    return None