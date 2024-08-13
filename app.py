import gradio as gr
from image import process_image
from video import process_video
from decode import decode_video, decode_uploaded_images

# Gradio 인터페이스 실행
with gr.Blocks(css="""
    .custom-textbox { border: 2px solid #000; padding: 10px; }
    .separator { margin-top: 10px; margin-bottom: 10px; border-bottom: 2px solid #ccc; }
""") as demo:
    with gr.Tab("이미지 워터마크"):
        gr.Markdown("### 이미지에 워터마크 삽입")
        with gr.Row():
            with gr.Column():
                img_input = gr.Image(type="numpy", label="이미지 업로드")
            with gr.Column():
                watermark_text = gr.Textbox(label="워터마크 텍스트 입력", elem_classes="custom-textbox")
                gr.Markdown(" ", elem_classes="separator")  # 텍스트 입력과 로고 개수 사이에 경계선 추가
                num_logos = gr.Slider(1, 100, step=1, label="로고 개수")
        with gr.Row():
            original_output = gr.Image(type="pil", label="원본 이미지")
            watermarked_output = gr.Image(type="pil", label="포렌식 워터마크 이미지")
            highlight_output = gr.Image(type="pil", label="하이라이트된 워터마크 위치")
            download_output = gr.File(label="워터마크가 포함된 이미지 다운로드")
        run_button = gr.Button("워터마크 삽입 실행")
        run_button.click(process_image, inputs=[img_input, watermark_text, num_logos], outputs=[original_output, watermarked_output, download_output, highlight_output])

    with gr.Tab("이미지 워터마크 디코딩"):
        gr.Markdown("### 이미지에서 워터마크 디코딩")
        with gr.Row():
            original_img = gr.Image(type="numpy", label="원본 이미지 업로드")
            watermarked_img = gr.Image(type="numpy", label="워터마크가 포함된 이미지 업로드")
        decoded_output = gr.Image(type="pil", label="디코딩된 워터마크")
        decode_button = gr.Button("워터마크 디코딩 실행")
        decode_button.click(decode_uploaded_images, inputs=[original_img, watermarked_img], outputs=decoded_output)

    with gr.Tab("동영상 워터마크"):
        gr.Markdown("### 동영상에 워터마크 삽입 및 디코딩")
        with gr.Row():
            with gr.Column():
                video_input = gr.Video(label="동영상 업로드")
            with gr.Column():
                watermark_text = gr.Textbox(label="워터마크 텍스트 입력", elem_classes="custom-textbox")
                gr.Markdown(" ", elem_classes="separator")  # 텍스트 입력과 로고 개수 사이에 경계선 추가
                num_logos = gr.Slider(1, 10, step=1, label="로고 개수")
        
        with gr.Row():
            original_output = gr.Video(label="원본 동영상")
            watermarked_output = gr.Video(label="워터마크가 삽입된 동영상")
            highlight_output = gr.Video(label="하이라이트된 동영상")
            download_output = gr.File(label="워터마크가 삽입된 동영상 다운로드")
        
        process_button = gr.Button("워터마크 삽입 실행")
        process_button.click(process_video, inputs=[video_input, watermark_text, num_logos], outputs=[original_output, watermarked_output, highlight_output, download_output])
    
    with gr.Tab("동영상 워터마크 디코딩"):
        gr.Markdown("### 동영상에서 워터마크 디코딩")
        with gr.Row():
            original_video_input = gr.Video(label="원본 동영상 업로드")
            watermarked_video_input = gr.Video(label="워터마크가 포함된 동영상 업로드")
        
        with gr.Row():
            decoded_output = gr.Video(label="디코딩된 워터마크 동영상")
            download_decoded_output = gr.File(label="디코딩된 동영상 다운로드")
        
        decode_button = gr.Button("워터마크 디코딩 실행")
        decode_button.click(decode_video, inputs=[original_video_input, watermarked_video_input], outputs=[original_video_input, watermarked_video_input, decoded_output, download_decoded_output])

demo.launch()
