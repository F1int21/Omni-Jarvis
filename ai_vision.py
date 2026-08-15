import easyocr
from PIL import Image
READER = easyocr.Reader(['ru','en'], gpu=False)
def get_text_center(image_path: str, target_text: str) -> dict:
    try:
        img = Image.open(image_path)
        result = READER.readtext(image_path, detail=1)
        print("=== OCR RAW результат ===")
        for bbox, text, conf in result:
            print(f"text: |{text}| conf:{conf:.3f}")
        print("===================")
    except Exception as e:
        return {
            "found": False,
            "text": None, 
            "center_x": None, 
            "center_y": None, 
            "confidence": None,
            "error": f"image or ocr fail: {str(e)}"
            }
    target_lower = target_text.lower()
    for bbox, text, conf in result:
        if text.lower() == target_lower:
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            cx = int((min(xs) + max(xs)) / 2)
            cy = int((min(ys) + max(ys)) / 2)
            return {
                "found": True,
                "text": text,
                "center_x": cx,
                "center_y": cy,
                "confidence": float(round(conf, 3)),
                "error": None
            }
    return {
        "found": False, 
        "text": None, 
        "center_x": None, 
        "center_y": None, 
        "confidence": None,
        "error":"text_not_found"
        }
if __name__ == "__main__":
    res = get_text_center("server_get.png", "File")
    print(res)