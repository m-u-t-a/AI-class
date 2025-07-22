import os

from gigachat import GigaChat
import pdfplumber
from dotenv import load_dotenv
import re
from appeal_card import AppealCard  # Импорт конкретного класса

load_dotenv()
GIGACHAT_CREDENTIALS = os.getenv('GIGACHAT_CREDENTIALS')

giga = GigaChat(
    credentials=GIGACHAT_CREDENTIALS,
    verify_ssl_certs=False)

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

appeal_path = "../data/appeals/МЭДО_1.pdf"

prompt_fields = f"""
"Ты - секретарь государственной организации, которому поступило обращение гражданина. Твоя задача:
Проанализируй предоставленный текст обращения гражданина и извлеки ключевые поля в структурированном формате.
Ответ представь в формате текста со следующими полями:
номер_обращения,
дата_обращения (в формате "DD.MM.YYYY"),
автор (ФИО гражданина),
email (если указан),
телефон (если указан),
населенный_пункт (если указан),
адрес (если указан),
социальное_положение (если указано),
адресат (кому направлено обращение. указать ФИО или организацию).
Если какое-то поле отсутствует в тексте, укажи для него значение "не указано".
Не пиши кроме названия поля и его значения никаких пояснений, ничего не придумывай сверх поставленной задачи.
Формат вывода:
название поля: значение поля
Не вставляй никаких лишних символов, сохраняй такой формат вывода.
Предоставленный текст:
{extract_text_from_pdf(appeal_path)}
"""

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
{extract_text_from_pdf(appeal_path)}
"""

fields = giga.chat(prompt_fields).choices[0].message.content

full_appeal = giga.chat(prompt_full_appeal).choices[0].message.content

appeal_text = fields + '  \n' + full_appeal

new = appeal_text.split(sep='  \n', maxsplit=-1)
pattern = r":\s*(.*)"

result = {}
for item in new:
    match = re.search(pattern, item)
    if match:
        key = item.split(':')[0].strip()
        value = match.group(1).strip()
        result[key] = value

appeal = AppealCard(
    number=result.get('номер_обращения'),
    date=result.get('дата_обращения'),
    author=result.get('автор'),
    email=result.get('email'),
    telephone=result.get('телефон'),
    city=result.get('населенный_пункт'),
    address=result.get('адрес'),
    social_status=result.get('социальное_положение'),
    addressee=result.get('адресат'),
    appeal_text=result.get('текст_обращения'),
    category='не указана'
)

print(vars(appeal))
