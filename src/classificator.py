import gradio as gra
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class Classificator:

    def predict(text):
        model_name = "SidorCrew/ruROBERTA-large-test_BY_MIKHAIL"

        tokenizer = AutoTokenizer.from_pretrained(model_name, max_len=512)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        classes = {0: 'Благоустройство городов и поселков. Обустройство придомовых территорий',
                   1: 'Выделение земельных участков для строительства, фермерства, садоводства и огородничества',
                   2: 'Газификация поселений',
                   3: 'Дорожное хозяйство',
                   4: 'Лечение и оказание медицинской помощи',
                   5: 'Оплата жилищно-коммунальных услуг (ЖКХ)',
                   6: 'Переработка вторичного сырья и бытовых отходов. Полигоны бытовых отходов',
                   7: 'Переселение из подвалов, бараков, коммуналок, общежитий, аварийных домов, ветхого жилья, санитарно-защитной зоны',
                   8: 'Получение места в детских дошкольных воспитательных учреждениях',
                   9: 'Социальное обеспечение, материальная помощь многодетным, пенсионерам и малообеспеченным слоям населения'}

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

        predicted_clases = np.array(probs.tolist()[0])
        max_val = predicted_clases.max()
        max_index = np.argmax(predicted_clases)
        indexes = [max_index]

        for index, value in np.ndenumerate(predicted_clases):
            if (index != max_index) and ((max_val - value) <= 0.2):
                indexes.append(int(index[0]))
        # print(probs)
        if len(indexes) == 1:
            return classes[indexes[0]]
        else:
            return classes[indexes[0]], classes[indexes[1]]

    def deploy(self, predict):
        app = gra.Interface(fn=predict, inputs="text", outputs="text")
        app.launch()
