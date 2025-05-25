from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton('Создать привычку')
    keyboard.add(button_1)
    return keyboard