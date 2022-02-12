import json
import requests
from config import currencies

class ConvertionException(Exception): # Класс исключений (ошибок)
    pass

class Converter:   # Основной класс
    @staticmethod
    def get_price(base, quote, amount):
        if quote == base:
            raise ConvertionException(f'Нельзя ковертировать {base} саму в себя')

        try:
            quote_tiker = currencies[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        try:
            base_tiker = currencies[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            money = float(amount.replace(',', '.'))  # заменяем в строке "," на "." чтоб избежать ошибки, далее преобразуем в число с плавающей точкой
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={base_tiker}_{quote_tiker}' # Запрос к API сайта
                         f'&compact=ultra&apiKey=88520063d1c75efd5134')
        rq = json.loads(r.content) # Преобразуем ответ в JSON

        convers = round(((rq[f'{base_tiker}_{quote_tiker}']) * money), 2)     # Пересчитываем на необходимую пользователю сумму и округляем до сотых
        texte = (f'\U0001F4B0 Стоимость {amount} {base_tiker} равна {convers} {quote_tiker} \U0001F4B0')  # Формируем сообщение для пользователя

        return texte