
import telebot
from src.config import BOT_SECURITY
# telebot.AsyncTeleBot
bot = telebot.TeleBot(BOT_SECURITY['token'])