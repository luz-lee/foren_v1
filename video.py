from utils import extract_frames, create_video_from_frames, create_logo_image  # utils.py에서 함수 가져오기
import numpy as np
import random
import cv2
from PIL import Image, ImageDraw
from moviepy.editor import VideoFileClip

# FFT(푸리에 변환)를 통한 워터마크 삽입 (이미지에서 재사용)
from image import add_watermark

# 프레임별 워터마크 삽입 함수
def add_watermark_to_video(frames, watermark_text, num_logos=1):
    watermarked_frames = []
    highlight_frames = []
    for frame in frames:
        watermarked_frame, highlight_frame = add_watermark(frame, watermark_text, num_logos)
        watermarked_frames.append(watermarked_frame)
        highlight_frames.append(np.array(highlight_frame))
    return watermarked_frames, highlight_frames

# 동영상 워터마크 삽입 함수 (Gradio용)
def process_video(video_path, watermark_text, num_logos=1):
    frames = extract_frames(video_path)
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    watermarked_frames, highlight_frames = add_watermark_to_video(frames, watermark_text, num_logos)
    
    watermarked_output_path = "watermarked_output.mp4"
    highlight_output_path = "highlighted_output.mp4"
    
    create_video_from_frames(watermarked_frames, fps, watermarked_output_path)
    create_video_from_frames(highlight_frames, fps, highlight_output_path)
    
    # 원본 동영상의 오디오 트랙을 추출하여 워터마킹된 동영상에 추가
    original_clip = VideoFileClip(video_path)
    watermarked_clip = VideoFileClip(watermarked_output_path)
    
    watermarked_clip = watermarked_clip.set_audio(original_clip.audio)
    
    # 오디오가 포함된 최종 동영상 저장
    watermarked_clip.write_videofile(watermarked_output_path, codec="libx264", audio_codec="aac")
    
    return video_path, watermarked_output_path, highlight_output_path, watermarked_output_path
