from utils import extract_frames, create_video_from_frames, create_logo_image
import numpy as np
import cv2
from PIL import Image, ImageDraw
from moviepy.editor import VideoFileClip

def add_watermark(img, watermark_text, location, alpha=20):
    img_f = np.fft.fft2(img)
    random_wm = np.zeros(img.shape, dtype=np.uint8)
    
    img_wm = create_logo_image(watermark_text, (location[2], location[3]))
    random_wm[location[1]:location[1] + location[3], location[0]:location[0] + location[2]] = img_wm
    
    result_f = img_f + alpha * random_wm
    result = np.fft.ifft2(result_f)
    result = np.real(result)
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return result

def add_watermark_to_video(frames, watermark_text, num_logos=1, alpha=20):
    height, width = frames[0].shape[:2]
    logo_size = (width // 10, height // 10)
    
    locations = [
        (
            np.random.randint(0, width - logo_size[0]),
            np.random.randint(0, height - logo_size[1]),
            logo_size[0],
            logo_size[1]
        )
        for _ in range(num_logos)
    ]

    watermarked_frames = []
    highlight_frames = []
    for frame in frames:
        watermarked_frame = frame.copy()
        highlight_frame = frame.copy()

        for location in locations:
            watermarked_frame = add_watermark(watermarked_frame, watermark_text, location, alpha)
            highlight_frame = add_highlight(highlight_frame, location)

        if watermarked_frame is not None:
            watermarked_frames.append(watermarked_frame)
        if highlight_frame is not None:
            highlight_frames.append(highlight_frame)
    
    return watermarked_frames, highlight_frames

def add_highlight(img, location, color=255):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.rectangle(
        [location[0], location[1], location[0] + location[2], location[1] + location[3]],
        outline=color, width=3
    )
    return np.array(img_pil)

def process_video(video_path, watermark_text, num_logos=1):
    frames = extract_frames(video_path)
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    watermarked_frames, highlight_frames = add_watermark_to_video(frames, watermark_text, num_logos)
    
    if not watermarked_frames or not highlight_frames:
        raise ValueError("No frames were generated during watermarking.")

    watermarked_output_path = "watermarked_output.mp4"
    highlight_output_path = "highlighted_output.mp4"
    
    create_video_from_frames(watermarked_frames, fps, watermarked_output_path)
    create_video_from_frames(highlight_frames, fps, highlight_output_path)
    
    original_clip = VideoFileClip(video_path)
    watermarked_clip = VideoFileClip(watermarked_output_path)
    
    watermarked_clip = watermarked_clip.set_audio(original_clip.audio)
    
    watermarked_clip.write_videofile(watermarked_output_path, codec="libx264", audio_codec="aac")
    
    return video_path, watermarked_output_path, highlight_output_path, watermarked_output_path
