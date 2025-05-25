from datetime import datetime

from telebot import TeleBot
from telebot.types import Message

from app.services.habits import HabitsService
from app.settings import settings

from app.services.users import UsersService
from app.database.session import Session
from app.bot.utils import correct_habit
from app.bot.keyboards import main_menu_keyboard as main_menu

token = settings.bot_url

bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome_send(message: Message):
    bot.delete_message(message.chat.id, message.message_id)
    tg_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    username = message.chat.username

    try:
        user_service = UsersService.init_app(Session())
        user = user_service.get_user_by_tg_id(tg_id=tg_id)
        if user:
            bot.send_message(message.chat.id, f'Добро пожаловать, {first_name}\n'
                                              f'Это твой личный трекер привычек', reply_markup=main_menu())
        else:
            bot.send_message(message.chat.id, f'Привет {first_name},\n'
                                              f'Хочешь добавить новую привычку?', reply_markup=main_menu())
            user_service.create_user(tg_id=tg_id, first_name=first_name, last_name=last_name, username=username)
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {e}')


@bot.message_handler(func=lambda message: message.text == 'Создать привычку')
def create_habit(message: Message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Введи название привычки:')
    bot.register_next_step_handler(message, wait_habit_by_user)


def wait_habit_by_user(message: Message):
    habit_name = message.text.capitalize()

    if not correct_habit(habit_name):
        bot.reply_to(message, 'Не корректная наименование привычки,\n'
                              'Отправь повторно должна быть больше 5 символов')
        bot.register_next_step_handler(message, wait_habit_by_user)
        return

    user_service = UsersService.init_app(Session())
    habit_service = HabitsService.init_app(Session())

    try:
        user = user_service.get_user_by_tg_id(message.chat.id)
        new_habit = habit_service.create_habit(user_id=user.id, name_habit=habit_name, date_start=datetime.now())
        if new_habit:
            bot.send_message(message.chat.id, f'Вы успешно создали новую привычку: {habit_name},\n'
                                              f'Дата: {new_habit.date_start.date()}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {e}')


if __name__ == '__main__':
    bot.polling()
