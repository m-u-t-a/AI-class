from classificator import Classificator
from appeal_card import AppealCard
from src.pdf_extractor import extract_text_from_pdf
from src.extractor import extract_fields, extract_prompts, extract_full_appeal

APPEAL_PATH = "../data/appeals/МЭДО_1.pdf"
text = extract_text_from_pdf(APPEAL_PATH)
fields = extract_prompts(text)
full_appeal = extract_full_appeal(text)
full_fields = extract_fields(fields, full_appeal)

_category = Classificator.predict(full_fields.get('текст_обращения'))

appeal = AppealCard(
    number=full_fields.get('номер_обращения'),
    date=full_fields.get('дата_обращения'),
    author=full_fields.get('автор'),
    email=full_fields.get('email'),
    telephone=full_fields.get('телефон'),
    city=full_fields.get('населенный_пункт'),
    address=full_fields.get('адрес'),
    social_status=full_fields.get('социальное_положение'),
    addressee=full_fields.get('адресат'),
    appeal_text=full_fields.get('текст_обращения'),
    category=_category
)

print(vars(appeal))