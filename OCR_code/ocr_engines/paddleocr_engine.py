# paddleocr은 python3.8에서 설치된다. 3.9 이상에서는 설치 안된다.

from paddleocr import PaddleOCR # pip install paddlepaddle paddleocr
from utils.image_util import put_text
import cv2

def initialize_engine(lang='korean'):
    """PaddleOCR 엔진 초기화"""
    return PaddleOCR(lang=lang)

def run_ocr(engine, image_path):
    """PaddleOCR 실행"""
    try:
        result = engine.ocr(image_path, cls=False)
        return result[0]
    except Exception as e:
        print(f"PaddleOCR 오류: {e}")
        return None

def extract_text_and_boxes(ocr_data):
    """PaddleOCR 결과에서 텍스트와 박스 추출"""
    extracted_text = []
    boxes = []
    for line in ocr_data:
        box = line[0]
        text = line[1][0]
        tl = (int(box[0][0]), int(box[0][1]))
        br = (int(box[2][0]), int(box[2][1]))
        extracted_text.append(text)
        boxes.append((tl, br, text))  # tl: top-left, br: bottom-right, text
    return extracted_text, boxes

def draw_results(img, boxes):
    """이미지에 텍스트 박스 그리기"""
    for tl, br, text in boxes:
        cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        img = put_text(img, text, tl[0], tl[1] - 20, font_size=15)
    return img
