import requests
import pyautogui
from PIL import ImageGrab
import io
import sys

# Делаем скриншот
screenshot = ImageGrab.grab()
#screenshot.thumbnail((1280, 720))

# Конвертируем в байты
img_bytes = io.BytesIO()
screenshot.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Отправка на сервер
files = {'file': ('screen.png', img_bytes, 'image/png')}
try:
    response = requests.post('http://localhost:8000/post', files=files, timeout=120)
    data = response.json()
    print('Ответ:', data)
    
    if data.get('status') == 'success':
        x, y = data['x'], data['y']
        print(f'Клик в ({x}, {y}) по тексту "{data["matched_text"]}"')
        pyautogui.click(x, y)
    else:
        print('Объект не найден')
        sys.exit(1)
except Exception as e:
    print('Ошибка:', e)
    sys.exit(1)