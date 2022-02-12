import telebot
from config import TOKEN, currencies
from extensions import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help']) # Вызывается по команде /start и /help содержит инструкцию
def help_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Для ковертации введите:\n'      
                          ' <имя первой валюты>, цену которой хотите узнать\n '
                          '<имя второй валюты>, в которой надо узнать цену первой валюты\n '
                          '<количество первой валюты>\n'
                          'формат запроса:\n'
                          '<имя первой валюты> <имя второй валюты> <количество первой валюты>\n'
                          'пример:\n'
                          'биткоин доллар 1\n\n'
                          'для вызова списка всех доступных валют введите:\n'
                          '/values')

@bot.message_handler(commands=['values']) # Вызывается по команде /values выводит список доступных для конвертации валют
def help_start(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():     # Цыкл обрабатывет содержащийся в config словарь и выводит название ключей пользователю
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler()    # Принимает сообщение от пользователя
def converter(message: telebot.types.Message):
    values = message.text.title().split()     # передаём переменной сообщение пользователя (список) и форматируем каждый
                                                # элемент списка к первой заглавной букве для соответствия ключам словаря
    try:
        if len(values) > 3:
            raise ConvertionException('Слишком много параметров')

        if len(values) < 3:
            raise ConvertionException('Слишком ммало параметров')
        
        answer = Converter.get_price(*values)    # Создаём объект класса

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка ввода \n {e}')   # Отлавливаем ошибки ввода пользователя

    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера \n{e}')    # Ошибки не зависящеие от ввода пользователя

    else:
        bot.reply_to(message, answer)   # Если всё успешно формируем ответ пользователю


bot.polling(none_stop=True)   # Запуск бота

