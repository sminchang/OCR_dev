import cv2
import numpy as np
import platform
from PIL import ImageFont, ImageDraw, Image
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os

def plt_imshow(title='image', img=None, figsize=(8, 5), save_path=None, dpi=300):
    """matplotlib을 사용하여 이미지를 보여주고, save_path가 지정되면 PNG 파일로 저장하는 함수"""
    plt.figure(figsize=figsize)

    if type(img) is str:
        img = cv2.imread(img)

    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []

            for i in range(len(img)):
                titles.append(title)

        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)

            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])

        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        # plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])

        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')


def put_text(image, text, x, y, color=(0, 255, 0), font_size=22):
    if type(image) == np.ndarray:
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(color_coverted)

    if platform.system() == 'Darwin':
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows':
        font = 'malgun.ttf'

    try:
        image_font = ImageFont.truetype(font, font_size)
    except IOError:
        print(f"폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        image_font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)

    draw.text((x, y), text, font=image_font, fill=color)

    numpy_image = np.array(image)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    return opencv_image