from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN
from anecAPI import anecAPI
import telebot

bot = telebot.TeleBot(TOKEN)


