from image import decode_watermark  # 이미지 디코딩 함수 가져오기
from PIL import Image
import cv2

# 이미지 워터마크 디코딩 함수
def decode_uploaded_images(original_img, watermarked_img):
    decoded_watermark = decode_watermark(original_img, watermarked_img)
    return Image.fromarray(decoded_watermark)

# 동영상 워터마크 디코딩 함수 (Gradio용)
def decode_video(original_video_path, watermarked_video_path):
    original_frames = extract_frames(original_video_path)
    watermarked_frames = extract_frames(watermarked_video_path)
    video = cv2.VideoCapture(original_video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    decoded_frames = decode_watermark_from_video(original_frames, watermarked_frames)
    
    decoded_output_path = "decoded_output.mp4"
    create_video_from_frames(decoded_frames, fps, decoded_output_path)
    
    return original_video_path, watermarked_video_path, decoded_output_path, decoded_output_path
