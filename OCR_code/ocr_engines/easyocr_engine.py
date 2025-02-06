import easyocr # pip install easyocr
from utils.image_util import put_text
import cv2

def initialize_engine(lang_list=['ko']):
    """EasyOCR 엔진 초기화"""
    return easyocr.Reader(lang_list)

def run_ocr(reader, image_path):
    """EasyOCR 실행"""
    try:
        return reader.readtext(image_path)
    except Exception as e:
        print(f"EasyOCR 오류: {e}")
        return None

def extract_text_and_boxes(ocr_data):
    """EasyOCR 결과에서 텍스트와 박스 추출"""
    extracted_text = []
    boxes = []
    for (bbox, text, prob) in ocr_data:
        (tl, tr, br, bl) = bbox
        tl = tuple(map(int, tl))
        br = tuple(map(int, br))
        extracted_text.append(text)
        boxes.append((tl, br, text))  # tl: top-left, br: bottom-right, text
    return extracted_text, boxes

def draw_results(img, boxes):
    """이미지에 텍스트 박스 그리기"""
    for tl, br, text in boxes:
        cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        img = put_text(img, text, tl[0], tl[1] - 20, font_size=15)
    return img