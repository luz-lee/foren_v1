import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont
from utils import create_logo_image  # utils.py에서 함수 가져오기

# FFT(푸리에 변환)를 통한 워터마크 삽입
def add_watermark(img, watermark_text, num_logos=1, alpha=20):
    height, width = img.shape[:2]
    logo_size = (width // 10, height // 10)
    
    img_f = np.fft.fft2(img)
    
    random_wm = np.zeros(img.shape, dtype=np.uint8)
    highlight_img = Image.fromarray(img).convert("RGB")
    
    draw = ImageDraw.Draw(highlight_img)
    
    for _ in range(num_logos):
        img_wm = create_logo_image(watermark_text, logo_size)
        top_left_x = random.randint(0, width - logo_size[0])
        top_left_y = random.randint(0, height - logo_size[1])
        random_wm[top_left_y:top_left_y + logo_size[1], top_left_x:top_left_x + logo_size[0]] = img_wm
        
        draw.rectangle(
            [top_left_x, top_left_y, top_left_x + logo_size[0], top_left_y + logo_size[1]],
            outline="red", width=3
        )
    
    result_f = img_f + alpha * random_wm
    result = np.fft.ifft2(result_f)
    result = np.real(result)
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return result, highlight_img

# 워터마크 디코딩
def decode_watermark(img, watermarked_img, alpha=20):
    img_ori_f = np.fft.fft2(img)
    img_input_f = np.fft.fft2(watermarked_img)
    
    watermark = (img_ori_f - img_input_f) / alpha
    watermark = np.real(watermark)
    
    watermark = (watermark - watermark.min()) / (watermark.max() - watermark.min()) * 255
    watermark = watermark.astype(np.uint8)
    
    return watermark

# Gradio 인터페이스를 통한 워터마크 삽입
def process_image(img, watermark_text, num_logos):
    watermarked_img, highlight_img = add_watermark(img, watermark_text, num_logos)
    watermarked_image_pil = Image.fromarray(watermarked_img)
    
    # 현재 작업 디렉토리에 워터마크 이미지 파일로 저장
    output_path = "watermarked_image.png"
    watermarked_image_pil.save(output_path)
    
    return Image.fromarray(img), watermarked_image_pil, output_path, highlight_img

# Gradio 인터페이스를 통한 워터마크 디코딩
def decode_uploaded_images(original_img, watermarked_img):
    decoded_watermark = decode_watermark(original_img, watermarked_img)
    return Image.fromarray(decoded_watermark)
