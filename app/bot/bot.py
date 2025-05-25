import logging
from datetime import datetime
from telebot import TeleBot
from telebot.types import Message
from app.bot.storage import storage
from app.services.habits import HabitsService
from app.services.users import UsersService
from app.database.session import Session
from app.bot.utils import correct_habit
from app.bot.keyboards import main_menu_keyboard as main_menu
from app.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = TeleBot(
    token=settings.bot_url,
    state_storage=storage,
    parse_mode='HTML'  
)


@bot.message_handler(commands=['start'])
def welcome_send(message: Message):
    """Handle /start command"""
    bot.delete_message(message.chat.id, message.message_id)
    tg_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    username = message.chat.username or ""

    try:
        user_service = UsersService.init_app(Session())
        user = user_service.get_user_by_tg_id(tg_id=tg_id)

        if user:
            welcome_msg = (f'С возвращением, {first_name}! 🤗\n'
                           f'Ваш трекер привычек готов к работе')
        else:
            welcome_msg = (f'Здравствуйте, {first_name}! 👋\n'
                           f'Давайте начнем формировать полезные привычки вместе')
            user_service.create_user(
                tg_id=tg_id,
                first_name=first_name,
                last_name=last_name,
                username=username
            )

        bot.send_message(message.chat.id, welcome_msg, reply_markup=main_menu())

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')
        logger.error(f"Error in welcome_send: {str(e)}")


@bot.message_handler(func=lambda message: message.text == 'Создать привычку')
def create_habit(message: Message):
    """Handle create habit command"""
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Введи название привычки:')
    bot.register_next_step_handler(message, wait_habit_by_user)


def wait_habit_by_user(message: Message):
    """Process habit name from user"""
    habit_name = message.text.strip().capitalize()

    if not correct_habit(habit_name):
        error_msg = ('Некорректное наименование привычки.\n'
                     'Название должно быть длиннее 5 символов')
        bot.reply_to(message, error_msg)
        bot.register_next_step_handler(message, wait_habit_by_user)
        return

    try:
        user_service = UsersService.init_app(Session())
        habit_service = HabitsService.init_app(Session())

        user = user_service.get_user_by_tg_id(message.chat.id)
        if not user:
            raise ValueError("Пользователь не найден")

        new_habit = habit_service.create_habit(
            user_id=user.id,
            name_habit=habit_name,
            date_start=datetime.now()
        )

        success_msg = (f'Вы успешно создали новую привычку: {habit_name}\n'
                       f'Дата: {new_habit.date_start.date()}')
        bot.send_message(message.chat.id, success_msg)

    except Exception as e:
        error_msg = f'Произошла ошибка: {str(e)}'
        bot.send_message(message.chat.id, error_msg)
        logger.error(f"Error in wait_habit_by_user: {str(e)}")


if __name__ == '__main__':
    bot.polling()
