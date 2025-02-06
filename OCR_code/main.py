import os
import re
import cv2
from utils.image_util import plt_imshow, put_text
from ocr_engines import easyocr_engine, tesseract_engine, paddleocr_engine


# 1. OCR 엔진 선택
OCR_ENGINE = "tesseract"  # "easyocr", "tesseract", "paddleocr" 중 선택

# 2. OCR 엔진 초기화 및 설정
if OCR_ENGINE == "easyocr":
    engine = easyocr_engine.initialize_engine()
    selected_engine = easyocr_engine
elif OCR_ENGINE == "tesseract":
    engine = tesseract_engine.initialize_engine()
    selected_engine = tesseract_engine
elif OCR_ENGINE == "paddleocr":
    engine = paddleocr_engine.initialize_engine()
    selected_engine = paddleocr_engine

# 3. 작업 파일 경로 설정
input_folder = os.path.join(os.getcwd(), "OCR_sample") # 작업할 .png 추가해두기
output_folder = os.path.join(os.getcwd(), "OCR_result")
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    image_path = os.path.join(input_folder, filename)

    try:
        # 4. OCR 실행
        ocr_data = selected_engine.run_ocr(engine, image_path) # 엔진 객체 전달

        if ocr_data:
            # 5. 텍스트와 영역 추출
            extracted_text, boxes = selected_engine.extract_text_and_boxes(ocr_data)

            # 6. 결과 이미지 생성
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = selected_engine.draw_results(img, boxes)

            # 7. 이미지 저장
            base_filename = os.path.splitext(filename)[0]
            output_image_path = os.path.join(output_folder, f"{base_filename}_{OCR_ENGINE}.png")
            plt_imshow(title=OCR_ENGINE,img=img, save_path=output_image_path)

            # 8. 텍스트 파일 저장
            output_text_path = os.path.join(output_folder, f"{base_filename}_{OCR_ENGINE}.txt")
            with open(output_text_path, "w", encoding="utf-8") as f:
                text = "\n".join(extracted_text)
                text = re.sub(r'\n{2,}', '\n', text)
                f.write(text)

            print(f"작업 완료: {output_image_path}, {output_text_path}")
        else:
            print(f"Error: OCR 실행 실패 - {filename}")

    except Exception as e:
        print(f"Error {filename}: {e}")

print("OCR processing complete.")