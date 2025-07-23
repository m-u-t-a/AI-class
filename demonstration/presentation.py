import gradio as gr
from gradio_pdf import PDF

from src.classificator import Classificator
from src.extractor import extract_fields, extract_prompts, extract_full_appeal
from src.pdf_extractor import extract_text_from_pdf

from typing import Dict

def format_appeal(data: Dict) -> str:
    return f"""
<div style='font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;'>
    <h1 style='color: #2b5876; border-bottom: 2px solid #2b5876; padding-bottom: 10px;'>Обращение АП РФ</h1>

    <table style='width: 100%; border-collapse: collapse; margin-bottom: 20px;'>
        <tr style='background-color: #f2f2f2;'>
            <td style='padding: 8px; border: 1px solid #ddd; width: 30%;'><strong>Номер обращения</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['номер_обращения']}</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Дата обращения</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['дата_обращения']}</td>
        </tr>
        <tr style='background-color: #f2f2f2;'>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Автор</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['автор']}</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Email</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['email']}</td>
        </tr>
        <tr style='background-color: #f2f2f2;'>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Телефон</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['телефон']}</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Населенный пункт</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['населенный_пункт']}</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Адрес</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['адрес']}</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Социальное положение</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['социальное_положение']}</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Адресат</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['адресат']}</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><strong>Текст обращения</strong></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>{data['текст_обращения']}</td>
        </tr>
    </table>

    <div style='background-color: #f8f9fa; padding: 15px; border-left: 4px solid #4e73df; margin-bottom: 20px;'>
        <h3 style='color: #2b5876; margin-top: 0;'>КЛАССИФИКАЦИЯ</h3>
        <p style='white-space: pre-line;'>{Classificator.predict(data['текст_обращения'])}</p>
    </div>
</div>
"""

def qa(doc: str):
    text = extract_text_from_pdf(doc)
    fields = extract_prompts(text)
    full_appeal = extract_full_appeal(text)
    full_fields = extract_fields(fields, full_appeal)
    # print(full_fields)
    return format_appeal(full_fields)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
        # 🗂 Система анализа обращений
        Загрузите PDF-документ для анализа текста обращения
        """)

    with gr.Tab("Загрузка PDF"):
        file_input = PDF(label="Вставь PDF")
        process_btn = gr.Button("Обработать")

    with gr.Tab("Результат"):
        html_output = gr.HTML()

    process_btn.click(qa, inputs=file_input, outputs=html_output)

demo.launch(share=True)
