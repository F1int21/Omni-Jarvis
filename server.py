from  fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
import uvicorn
import time
import asyncio
from ai_vision import get_text_center
app = FastAPI(title="Omni-Jarvis Backend Server", version="0.4.3")
SAVE_SCREENSHOT_PATH = "server_get.png"
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"status":"error", "error":str(exc)}
    )
@app.post("/post")
async def receive_screenshot(target_text: str, file: UploadFile = File(...)):
    t_start = time.perf_counter()
    with open(SAVE_SCREENSHOT_PATH, "wb") as buffer:
        buffer.write(await file.read())
    try:
        vision_result = await asyncio.to_thread(get_text_center, SAVE_SCREENSHOT_PATH, target_text)
        print(f"[SERVER DEBUG] vision_result = {vision_result}")
    except Exception as err:
        print(f"[SERVER ERROR] Ошибка потока OCR: {repr(err)}")
        return {"status":"error", "error": str(err)}
    processing_ms = round((time.perf_counter() - t_start)*1000, 2)
    return {
        "status":"ok",
        "processing_ms": processing_ms,
        "vision": vision_result
    }
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)