import extractor
from classificator import Classificator
from appeal_card import AppealCard

appeal_values = extractor.extract()

_category = Classificator.predict(appeal_values.get('текст_обращения'))

appeal = AppealCard(
    number=appeal_values.get('номер_обращения'),
    date=appeal_values.get('дата_обращения'),
    author=appeal_values.get('автор'),
    email=appeal_values.get('email'),
    telephone=appeal_values.get('телефон'),
    city=appeal_values.get('населенный_пункт'),
    address=appeal_values.get('адрес'),
    social_status=appeal_values.get('социальное_положение'),
    addressee=appeal_values.get('адресат'),
    appeal_text=appeal_values.get('текст_обращения'),
    category=_category
)

print(vars(appeal))