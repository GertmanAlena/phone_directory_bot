from email.message import Message
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from tok import TOKEN
from anecAPI import anecAPI
from telebot import types
import telebot
import logger

bot = telebot.TeleBot(TOKEN)
Phone_Book = {}
search_contact = []

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)

name = ''
surname = ''
comment = ''
telephon = 0

dict_Phone_Book = []

@bot.message_handler()

def hello(message: Message):
    logger.start()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    key_oll_contact = types.InlineKeyboardButton(text='просмотреть все контакты', callback_data='просмотреть все контакты')
    key_new_contact = types.InlineKeyboardButton(text='новый контакт', callback_data='новый контакт')
    key_search_contact_menu = types.InlineKeyboardButton(text='поиск контакта', callback_data='поиск контакта')
    keyboard.add(key_oll_contact, key_new_contact)
    key_del_contact = types.InlineKeyboardButton(text='удалить контакт', callback_data='удалить контакт')
    keyboard.add(key_search_contact_menu, key_del_contact)
    key_change_contact = types.InlineKeyboardButton(text='изменить контакт', callback_data='изменить контакт')
    key_export_contact = types.InlineKeyboardButton(text='экспорт  контактов', callback_data='экспорт  контактов')
    keyboard.add(key_change_contact, key_export_contact)
    key_import_contact = types.InlineKeyboardButton(text='импорт контактов', callback_data='импорт контактов')
    key_exit_contact = types.InlineKeyboardButton(text='выход', callback_data='выход')
    keyboard.add(key_import_contact, key_exit_contact)
    global dict_Phone_Book

    bot.reply_to(message, f'Приветствую тебя!, {message.from_user.first_name}! \n'
                            'что ты хочешь сделать?', reply_markup=keyboard)
    try:
        with open('contact.json', 'r', encoding='UTF-8') as file:
            dict_Phone_Book = json.load(file)
        return dict_Phone_Book
        
    except FileNotFoundError:
        with open('contact.json', 'w', encoding='UTF-8') as file:
            return []

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'новый контакт':
        bot.send_message(call.message.chat.id, 'Введите имя?')
        bot.register_next_step_handler(call.message, add_name)
    elif call.data == 'просмотреть все контакты':
        # bot.register_next_step_handler(call.message, show_contact)
        show_contact(call.message)
    elif call.data == 'поиск контакта': 
        # bot.send_message(call.message.chat.id, 'Давай поищем?')
        search_contact_menu(call.message)
    elif call.data == 'удалить контакт':
        pass
    elif call.data == 'изменить контакт':
        pass
    elif call.data == 'импорт контактов':
        hello
        bot.send_message(call.message.chat.id, 'Контакты импортированы!!!')
    elif call.data == 'выход':
        bot.send_message(call.message.chat.id, 'Пока')
        exit_add
    elif call.data == 'По номеру телефона':
        bot.send_message(call.message.chat.id, 'Введите номер, который нужно найти?')
        bot.register_next_step_handler(call.message, search_contact_phonnumber)
    elif call.data == 'По имени или фамилии':
        bot.send_message(call.message.chat.id, 'Введите имя?')
        bot.register_next_step_handler(call.message, search_contact_phonnumber_name)
    elif call.data == "yes":
        bot.send_message(call.message.chat.id, "Записываем в БД!нажми что-нибудь")
        Phone_Book_add()
    elif call.data == "Удалить":
        bot.send_message(call.message.chat.id, 'Какой контакт удаляем?')
        bot.register_next_step_handler(call.message, del_contact_phonnumber)
        
    elif call.data == "Выход в меню":
        hello(call.message)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуем еще раз!нажми что-нибудь")

def exit_add():
    return ConversationHandler.END

def show_contact(message: Message):
    global dict_Phone_Book
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Выход в меню', callback_data='Выход в меню')
    keyboard.add(key_menu)
    """Функция вывода всех контактов"""
    if len(dict_Phone_Book) == 0:
        bot.send_message(message.chat.id, 'справочник пуст, возвращайтесь в меню', reply_markup=keyboard)
    else:
        for i in dict_Phone_Book:
            bot.send_message(message.chat.id,f'ID: {i["id"]} Фамилия: {i["surname"]} Имя: {i["name"]} Телефон: {i["phon_number"]}')    
        bot.send_message(message.chat.id, 'Возвращаемся в меню', reply_markup=keyboard)

def add_name(message: Message):
    """
    добавляем name и сохраняем в dict
    """
    global name
    name = message.text.capitalize()
    # Phone_Book["name"] = name
    bot.send_message(message.from_user.id, 'Ведите фамилию?')
    bot.register_next_step_handler(message, add_surname)

def add_surname(message):
    """
    добавляем surname и сохраняем в dict
    """
    global surname
    surname = message.text.capitalize()
    bot.send_message(message.from_user.id, 'Ведите номер телефона?')
    bot.register_next_step_handler(message, add_telephon)

def add_telephon(message):
    """
    добавляем telephon и сохраняем в dict
    """
    global telephon
    telephon = message.text
    if telephon.isdigit():
        bot.send_message(message.from_user.id, 'Ведите комментарий к контакту?')
        bot.register_next_step_handler(message, add_comment)
    else:
        bot.send_message(message.from_user.id, 'попробуйте ввести ещё раз номер телефона')
        bot.register_next_step_handler(message, add_telephon)

def add_comment(message):
    """
    добавляем comment и сохраняем в dict
    """
    global comment
    comment = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_yes, key_no)
    bot.reply_to(message,f'Вы ввели следующие данные \nимя {name}\nфамилия {surname} \nномер телефона -> {telephon} \nкомментарий -> {comment} Верно?', reply_markup=keyboard)
    # bot.register_next_step_handler(message, callback_worker)

def Phone_Book_add():
    global name
    global surname
    global telephon
    global comment
    global id
    
    Phone_Book["name"] = name.title()
    Phone_Book["surname"] = surname.title()
    Phone_Book["phon_number"] = telephon
    Phone_Book["comment"] = comment.title()
    id = len(dict_Phone_Book)+1
    Phone_Book["id"] = id
    create_file(Phone_Book)
    return Phone_Book

def create_file(Phone_Book):
    """Функция добавления контакта"""
    try:
        with open('contact.json', 'r') as file:
            dict_Phone_Book = json.load(file)
    except:
        dict_Phone_Book = []

    dict_Phone_Book.append(Phone_Book)
    
    with open('contact.json', 'w', encoding="utf-8") as file:
        json.dump(dict_Phone_Book, file, indent=2, ensure_ascii = False)
    print('\033[30m\033[42m\033[4m {}\033[0m'.format('Контакт добавлен'))
    print('-'*50)
    return dict_Phone_Book

def search_contact_menu(message: Message):
    """Функция поиска контакта"""
    
    keyboard = types.InlineKeyboardMarkup()
    key_phon_number = types.InlineKeyboardButton(text='По номеру телефона', callback_data='По номеру телефона')
    key_name = types.InlineKeyboardButton(text='По имени или фамилии', callback_data='По имени или фамилии')
    # key_surname = types.InlineKeyboardButton(text='По фамилии', callback_data='По фамилии')
    key_menu = types.InlineKeyboardButton(text='Выход в меню', callback_data='Выход в меню')
    keyboard.add(key_phon_number, key_name)
    keyboard.add(key_menu)
    # update.message.reply_text(f'ответ {number_list} ещё посчитаем?')
    bot.reply_to(message, 'Выбирай, как будем искать', reply_markup=keyboard)

def search_contact_phonnumber(message):
    '''Поиск контакта по номеру телефона'''
    num = message.text
    global search_contact
    global dict_Phone_Book
    # with open('contact.json', 'r') as file:
    #     dict_Phone_Book = json.load(file)
    if len(dict_Phone_Book) == 0:
        bot.send_message(message.from_user.id,f'Ваш справочник пока еще пустой!')
        print('\033[43m\033[1m {} \033[0m'.format('Ваш справочник пока еще пустой!'))
    elif not message:
        bot.send_message(message.effective_chat.id, "Что искать, не понятно")
    else:
        count = 0
        for i in dict_Phone_Book:
            if i["phon_number"] == num:
                search_contact.append(i)
                count +=1
                bot.send_message(message.from_user.id,f'Нашёл!\nКонтакт №{count}\
                    \nФамилия: {i["surname"]}\
                    \nИмя: {i["name"]}\nТелефон: {i["phon_number"]}\nID: {i["id"]}')
        return search_contact
        # search_contact = ' '.join(filter(lambda j: num in j, dict_Phone_Book))

def search_contact_phonnumber_name(message):
    '''Поиск контакта по имени'''
    arg = message.text
    global search_contact
    global dict_Phone_Book
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Выход в меню', callback_data='Выход в меню')
    key_del = types.InlineKeyboardButton(text='Удалить', callback_data='Удалить')
    key_change = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    keyboard.add(key_menu, key_del, key_change)   
    if len(dict_Phone_Book) == 0:
        bot.send_message(message.from_user.id,f'Ваш справочник пока еще пустой!')
    elif not message:
        bot.send_message(message.effective_chat.id, "Что искать, не понятно")
    else:
        for i in dict_Phone_Book:
            # search_contact = ' '.join(filter(lambda j: arg in i["name"], dict_Phone_Book))
            if arg.capitalize() in i["name"] or arg.capitalize() in i["surname"]:    
                search_contact.append(i)
                bot.send_message(message.from_user.id,f'Нашёл!\n id {i["id"]}\nФамилия: {i["surname"]}\nИмя: {i["name"]}\
                    \nТелефон: {i["phon_number"]}')
    bot.send_message(message.chat.id, 'Что делаем дальше?', reply_markup=keyboard)
    return search_contact       
def del_contact_phonnumber(message: Message):
    '''Удаление контакта по его id'''
    arg = int(message.text)
    global dict_Phone_Book
    global search_contact
    print('search_contact- >',search_contact)
    if not message:
        bot.send_message(message.effective_chat.id, "Что удалять, не понятно")
    else:
        for i, j in enumerate(dict_Phone_Book): #   j - > {'name': 'Jfgvgnvn', 'surname': 'Jgf', 'phon_number': '6666', 'comment': 'Jh'}
            if j["id"] == arg:
                del dict_Phone_Book[i]                                             #   i - > 0
        with open('contact.json', 'w', encoding="utf-8") as file:
            json.dump(dict_Phone_Book, file, indent=2, ensure_ascii = False)
    return dict_Phone_Book


print('server started')
bot.polling(none_stop=True)
