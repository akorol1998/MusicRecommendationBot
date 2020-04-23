
import telebot
from config import BotMarkUp

def create_markup():
	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	markup.row(*BotMarkUp.COMMANDS_FSTROW)
	markup.row(*BotMarkUp.COMMANDS_SCNDROW)
	return markup
