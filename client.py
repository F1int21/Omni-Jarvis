import requests
from PIL import ImageGrab
import io

# Делаем скриншот всего экрана
screenshot = ImageGrab.grab()

# Сохраняем картинку в память
img_bytes = io.BytesIO()
screenshot.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Отправляем на сервер
files = {'file': ('screen.png', img_bytes, 'image/png')}
response = requests.post('http://localhost:8000/post', files=files, timeout=60)

# Печатаем, что вернул сервер
print('Код ответа:', response.status_code)
print('Ответ сервера:')
print(response.json())