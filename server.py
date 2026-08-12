import uvicorn
from fastapi import FastAPI, UploadFile, File

#1. Создаем объект нашего сервера
app = FastAPI()

print("ДЖАРВИС: Инициализация домашнего сервер...")

#2. Создаем "почтовый ящик" (эндпоинт) /post, который ждет файл
@app.post("/post")
async def receive_screenshot(file: UploadFile = File(...)):
    print(f" СЕРВЕР: Поймал входящий пакет! Имя файла: {file.filename}")

    #Читаем байты присланного файла
    file_bytes = await file.read()

    #Сохраняем полученный скриншот на сервере под именем server_get.png
    with open("server_get.png", "wb") as f:
        f.write(file_bytes)

    print("СЕРВЕР: Скриншот успешно сохранен в локальное хранилище сервера!")
    return {"status": "success", "message": "Файл доставлен на домашний сервер!"}

#3. Запускам сервер на локальном адресе 127.0.0.1 и порт 8000
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)