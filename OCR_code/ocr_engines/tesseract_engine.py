# Tesseract 설치(https://github.com/UB-Mannheim/tesseract/wiki)
# C:\Program Files\Tesseract-OCR -> 환경변수 등록 

import pytesseract # pip install pytesseract
from PIL import Image
from utils.image_util import put_text
import cv2

def initialize_engine(tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
    """Tesseract 엔진 초기화"""
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    return None  # Tesseract는 reader 객체가 필요 없음

def run_ocr(engine, image_path):  # engine은 None이 될 수 있음
    """Tesseract 실행"""
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='kor', config='--psm 11')
    except Exception as e:
        print(f"Tesseract 오류: {e}")
        return None

def extract_text_and_boxes(ocr_data):
    """Tesseract 결과에서 텍스트와 박스 추출"""
    extracted_text = []
    boxes = []
    n_boxes = len(ocr_data['level'])
    for i in range(n_boxes):
        if ocr_data['text'][i] != '':
            text = ocr_data['text'][i]
            (x, y, w, h) = (ocr_data['left'][i], ocr_data['top'][i],
                             ocr_data['width'][i], ocr_data['height'][i])
            tl = (x, y)
            br = (x + w, y + h)
            extracted_text.append(text)
            boxes.append((tl, br, text))  # tl: top-left, br: bottom-right, text
    return extracted_text, boxes

def draw_results(img, boxes):
    """이미지에 텍스트 박스 그리기"""
    for tl, br, text in boxes:
        cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        img = put_text(img, text, tl[0], tl[1] - 20, font_size=15)
    return img