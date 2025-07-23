import os

from gigachat import GigaChat
from dotenv import load_dotenv
import re

load_dotenv()
gigachat_credentials = os.getenv('GIGACHAT_CREDENTIALS')
giga = GigaChat(
    credentials=gigachat_credentials,
    verify_ssl_certs=False)

def extract_prompts(text):

    prompt_fields = f"""
        "Ты - секретарь государственной организации, которому поступило обращение гражданина. Твоя задача:
        Проанализируй предоставленный текст обращения гражданина и извлеки ключевые поля в структурированном формате.
        Ответ представь в формате текста со следующими полями:
        номер_обращения,
        дата_обращения (в формате "DD.MM.YYYY"),
        автор (ФИО гражданина),
        email (если указан),
        телефон (если указан),
        населенный_пункт (если указан. название поля "населенный_пункт" пиши именно так и никак иначе),
        адрес (если указан),
        социальное_положение (если указано),
        адресат (кому направлено обращение. указать ФИО или организацию).
        Если какое-то поле отсутствует в тексте, укажи для него значение "не указано".
        Не пиши кроме названия поля и его значения никаких пояснений, ничего не придумывай сверх поставленной задачи.
        Формат вывода:
        название поля: значение поля
        Не вставляй никаких лишних символов, сохраняй такой формат вывода.
        Предоставленный текст:
        {text}
        """
    fields = giga.chat(prompt_fields).choices[0].message.content
    # print(fields)
    return fields

def extract_full_appeal(text):

    prompt_full_appeal = f"""
        "Ты - секретарь государственной организации, которому поступило обращение гражданина. Твоя задача:
        Проанализируй предоставленный текст обращения гражданина.
        Извлеки из него один вид информации:
        текст_обращения (полный текст обращения, написанный гражданином. Не нужно указывать остальную информацию).
        Не пиши кроме текста обращения никаких пояснений, ничего не придумывай сверх поставленной задачи.
        Формат вывода:
        текст_обращения: текст
        Не вставляй никаких лишних символов, сохраняй такой формат вывода.
        Предоставленный текст:
        {text}
        """

    full_appeal = giga.chat(prompt_full_appeal).choices[0].message.content
    # print(full_appeal)
    return full_appeal

def extract_fields(fields, full_appeal):
    new = fields.split(sep='  \n', maxsplit=-1)
    pattern = r":\s*(.*)"

    result = {}
    for item in new:
        match = re.search(pattern, item)
        if match:
            key = item.split(':')[0].strip()
            value = match.group(1).strip()
            result[key] = value

    key2, value2 = full_appeal.split(sep=': ', maxsplit=--1)
    result[key2] = value2
    return result
