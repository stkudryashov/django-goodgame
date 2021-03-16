from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot, Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, CallbackQueryHandler

from telegram.utils.request import Request
from content.models import Profile, Payment

from .messages import *

import datetime
from django.utils.timezone import utc

from random import choice


def get_or_create_profile(f):
    def inner(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        p, _ = Profile.objects.get_or_create(external_id=chat_id, defaults={'name': update.message.from_user.username})
        f(update, context, p)
    return inner


def get_main_keyboard():
    keyboard = [[InlineKeyboardButton('Открыть коробку  🎉', callback_data='open'),
                 InlineKeyboardButton('🎁  Призы  🎁', callback_data='about')],
                [InlineKeyboardButton('Как открыть коробку  ⁉', callback_data='how_open')],
                [InlineKeyboardButton('💳  Пополнить баланс  💳', callback_data='payment')]]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard():
    keyboard = [[InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')]]
    return InlineKeyboardMarkup(keyboard)


def get_payment_keyboard():
    keyboard = [[InlineKeyboardButton('100₽', callback_data='100'),
                 InlineKeyboardButton('250₽', callback_data='250'),
                 InlineKeyboardButton('500₽', callback_data='500')],
                [InlineKeyboardButton('1000₽', callback_data='1000'),
                 InlineKeyboardButton('1500₽', callback_data='1500'),
                 InlineKeyboardButton('2000₽', callback_data='2000')]]
    return InlineKeyboardMarkup(keyboard)


def get_loot_box_keyboard(value):
    if value == 250:
        keyboard = [[InlineKeyboardButton('💎  Кейс за 250  💎', callback_data='1box250')],
                    [InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')]]
    elif value == 500:
        keyboard = [[InlineKeyboardButton('💎  2 Кейса за 250  💎', callback_data='2box250')],
                    [InlineKeyboardButton('💎  Кейс за 500  💎', callback_data='1box250')],
                    [InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')]]
    elif value == 1000:
        keyboard = [[InlineKeyboardButton('💎  3 Кейса за 250  💎', callback_data='3box250')],
                    [InlineKeyboardButton('💎  2 Кейса за 500  💎', callback_data='2box250')],
                    [InlineKeyboardButton('💎  Кейс за 1000  💎', callback_data='1box250')],
                    [InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')]]
    elif value == 2000:
        keyboard = [[InlineKeyboardButton('💎  3 Кейса за 250  💎', callback_data='3box250')],
                    [InlineKeyboardButton('💎  3 Кейса за 500  💎', callback_data='3box250')],
                    [InlineKeyboardButton('💎  2 Кейса за 1000  💎', callback_data='2box250')],
                    [InlineKeyboardButton('💎  Кейс за 2000  💎', callback_data='1box250')],
                    [InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')]]

    return InlineKeyboardMarkup(keyboard)


@get_or_create_profile
def do_start(update: Update, context: CallbackContext, user):
    reply_markup = get_main_keyboard()
    update.message.reply_text(text=f'Привет, {user.name}!', reply_markup=reply_markup)


def get_payments_last(user):
    now_time = datetime.datetime.now().replace(tzinfo=utc)
    last_lime = now_time - datetime.timedelta(minutes=1)
    recently = Payment.objects.filter(profile=user, created_at__gte=last_lime)

    pay_sum = 0
    if recently:
        for payment in recently:
            pay_sum += payment.value

    return pay_sum


def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    user = Profile.objects.get(external_id=query.message.chat_id)
    today = datetime.datetime.today()

    if data[0].isdigit():
        count = data[0]
        data = data[1:]
        if data == 'box250':
            query.message.edit_text(
                text=f'Поздравляем! Вы выиграли:')
            for i in range(int(count)):
                loot = choice(box_250)
                query.message.reply_text(text=loot)
            user.open_day = today.day
            user.save()
        elif data == 'box500':
            query.message.edit_text(
                text=f'Поздравляем! Вы выиграли:')
            for i in range(int(count)):
                loot = choice(box_500)
                query.message.reply_text(text=loot)
            user.open_day = today.day
            user.save()
        elif data == 'box1000':
            query.message.edit_text(
                text=f'Поздравляем! Вы выиграли:')
            for i in range(int(count)):
                loot = choice(box_1000)
                query.message.reply_text(text=loot)
            user.open_day = today.day
            user.save()
        elif data == 'box2000':
            query.message.edit_text(
                text=f'Поздравляем! Вы выиграли:')
            for i in range(int(count)):
                loot = choice(box_2000)
                query.message.reply_text(text=loot)
            user.open_day = today.day
            user.save()

    if data == 'open':
        if user.open_day != today.day:
            pay_sum = get_payments_last(user)
            if pay_sum < 250:
                query.message.edit_text(
                    text=f'За последние 24 часа {pay_sum}₽\n\nНужно пополнится чтобы получить подарок  😢',
                    reply_markup=get_back_keyboard())
            elif pay_sum < 500:
                query.message.edit_text(
                    text=f'За последние 24 часа {pay_sum}₽\n\nОткрой свой подарок  😉',
                    reply_markup=get_loot_box_keyboard(250))
            elif pay_sum < 1000:
                query.message.edit_text(
                    text=f'За последние 24 часа {pay_sum}₽\n\nОткрой свои подарки  😍',
                    reply_markup=get_loot_box_keyboard(500))
            elif pay_sum < 2000:
                query.message.edit_text(
                    text=f'За последние 24 часа {pay_sum}₽\n\nОткрой свои подарки  😍',
                    reply_markup=get_loot_box_keyboard(1000))
            else:
                query.message.edit_text(
                    text=f'За последние 24 часа {pay_sum}₽\n\nОткрой свои подарки  😍',
                    reply_markup=get_loot_box_keyboard(2000))
        else:
            query.message.edit_text(
                text='Ты уже получил сегодня подарки\n\nВозвращайся завтра  😴',
                reply_markup=get_back_keyboard())
    elif data == 'about':
        query.message.edit_text(text=ABOUT_TEXT, reply_markup=get_back_keyboard())
    elif data == 'how_open':
        query.message.edit_text(text=HOW_OPEN_TEXT, reply_markup=get_back_keyboard())
    elif data == 'payment':
        query.message.edit_text(
            text=f'Ваш баланс: {user.balance}\nНа какую сумму пополнение?',
            reply_markup=get_payment_keyboard()
        )
    elif data == 'back':
        query.message.edit_text(text='Что вы хотите сделать?', reply_markup=get_main_keyboard())
    elif data.isdigit():
        payment = Payment(profile=user, value=float(query.data))
        user.balance += payment.value
        payment.save()
        user.save()
        query.message.edit_text(
            text=f'Вы пополнили баланс на {query.data}₽\nВаш баланс: {user.balance}₽',
            reply_markup=get_back_keyboard()
        )


def payment_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.data.isdigit():
        user = Profile.objects.get(external_id=query.message.chat_id)

        user.balance += float(query.data)
        user.save()


class Command(BaseCommand):
    help = 'Good Game Bot'

    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)

        updater = Updater(bot=bot)

        start_handler = CommandHandler('start', do_start)
        updater.dispatcher.add_handler(start_handler)

        buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=False)
        updater.dispatcher.add_handler(buttons_handler)

        updater.start_polling()
        updater.idle()


box_250 = ['1 час игры за пк', 'Полчаса игры за PS', 'Полчаса игры за ПК']
box_500 = ['Батончик', '1.5 часа за PC', 'Кола (0.5)', 'Пакет в зал Стандарт (ночной)']
box_1000 = ['Пакет в зал VIP (утренний)', 'Кола и батончик', '3 часа за PS']
box_2000 = ['Абонемент на посещение клуба (на все выходные)', 'Кальян', 'Пакет в зал VIP (ночной)']
