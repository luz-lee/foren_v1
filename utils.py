import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

# 워터마크 텍스트를 개별 이미지로 변환하는 함수
def create_logo_image(text, image_size, font_size=30):
    img = Image.new('L', image_size, color=0)
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("arial.ttf", font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    textwidth, textheight = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    x = (image_size[0] - textwidth) // 2
    y = (image_size[1] - textheight) // 2
    draw.text((x, y), text, font=font, fill=255)
    
    img = np.array(img)
    img_rgb = np.stack([img] * 3, axis=-1)
    
    return img_rgb

# 동영상 프레임 추출 함수
def extract_frames(video_path):
    video = cv2.VideoCapture(video_path)
    frames = []
    success, image = video.read()
    while success:
        frames.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        success, image = video.read()
    return frames

# 동영상 재구성 함수
def create_video_from_frames(frames, fps, output_path):
    if not frames:
        raise ValueError("No frames available to create a video.")
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_path, codec="libx264")
