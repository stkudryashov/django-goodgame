from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot, Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, CallbackQueryHandler

from telegram.utils.request import Request
from content.models import Payment, Reward, ClubInfo, FullInfoUser, CaseBody, Mainlog

from random import choice

import datetime


def get_or_create_profile(f):
    def inner(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        p, _ = FullInfoUser.objects.get_or_create(telegram_id=chat_id,
                                                  user_id=chat_id,
                                                  user_club='goodgame1',
                                                  defaults={'nickname': update.message.from_user.name})
        f(update, context, p)
    return inner


def get_main_keyboard():
    keyboard = [[InlineKeyboardButton('Открыть коробку  🎉', callback_data='open'),
                 InlineKeyboardButton('🎁  Призы  🎁', callback_data='about')],
                [InlineKeyboardButton('Как открыть коробку  ⁉', callback_data='how_open')],
                [InlineKeyboardButton('🥳  Мои подарки  🥳', callback_data='my_rewards')],
                [InlineKeyboardButton('💳  Пополнить баланс  💳', callback_data='payment')]]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard():
    keyboard = [[InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')]]
    return InlineKeyboardMarkup(keyboard)


def get_payment_keyboard():
    keyboard = [[InlineKeyboardButton('100₽', callback_data='m100'),
                 InlineKeyboardButton('250₽', callback_data='m250'),
                 InlineKeyboardButton('500₽', callback_data='m500')],
                [InlineKeyboardButton('1000₽', callback_data='m1000'),
                 InlineKeyboardButton('1500₽', callback_data='m1500'),
                 InlineKeyboardButton('2000₽', callback_data='m2000')]]
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


# @get_or_create_profile
# def do_start(update: Update, context: CallbackContext, user):
#     reply_markup = get_main_keyboard()
#     update.message.reply_text(text=f'Привет, {user.name}!', reply_markup=reply_markup)


def get_payments_last(user):
    now_time = datetime.datetime.now()
    last_lime = now_time - datetime.timedelta(minutes=1)
    recently = Mainlog.objects.filter(clientid=user.user_id, recorddtime__gte=last_lime)

    pay_sum = 0
    if recently:
        for payment in recently:
            pay_sum += payment.cashadd

    return pay_sum


def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    user = FullInfoUser.objects.get(telegram_id=query.message.chat_id)
    today = datetime.datetime.today()

    if data[0].isdigit():
        count = data[0]
        data = data[1:]
        query.message.edit_text(
            text=f'Поздравляем! Вы выиграли:')
        if data == 'box250':
            for i in range(int(count)):
                loot = choice(box_250)
                Reward(profile=user, text=loot).save()
                query.message.reply_text(text=loot)
        elif data == 'box500':
            for i in range(int(count)):
                loot = choice(box_500)
                Reward(profile=user, text=loot).save()
                query.message.reply_text(text=loot)
        elif data == 'box1000':
            for i in range(int(count)):
                loot = choice(box_1000)
                Reward(profile=user, text=loot).save()
                query.message.reply_text(text=loot)
        elif data == 'box2000':
            for i in range(int(count)):
                loot = choice(box_2000)
                Reward(profile=user, text=loot).save()
                query.message.reply_text(text=loot)
        user.open_day = today.day
        user.save()
        query.message.reply_text(text='Назад на главную', reply_markup=get_back_keyboard())
    elif data == 'open':
        if True: # user.open_day != today.day
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
        about_text = CaseBody.objects.get(club=user.user_club).about_text
        query.message.edit_text(text=about_text, reply_markup=get_back_keyboard())
    elif data == 'how_open':
        how_open = CaseBody.objects.get(club=user.user_club).how_open
        query.message.edit_text(text=how_open, reply_markup=get_back_keyboard())
    elif data == 'payment':
        query.message.edit_text(
            text=f'На какую сумму пополнение?',
            reply_markup=get_payment_keyboard()
        )
    elif data == 'my_rewards':
        keyboard = []
        rewards = user.reward_set.filter(is_received=False)
        if rewards:
            for reward in rewards:
                keyboard.append([InlineKeyboardButton(reward.text, callback_data='re' + str(reward.pk))])
            keyboard.append([InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')])
            query.message.edit_text(text='Открывай награды только при администраторе!\n\n'
                                         'Ваши доступные награды:', reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            query.message.edit_text(text='У вас пока нет наград  😢', reply_markup=get_back_keyboard())
    elif data == 'back':
        query.message.edit_text(text='Что вы хотите сделать?', reply_markup=get_main_keyboard())
    elif data[0] == 'm':
        data = data[1:]
        mainlog = Mainlog(cashadd=float(data), clientid=user.user_id)
        mainlog.save()
        query.message.edit_text(
            text=f'Вы пополнили баланс на {data}₽',
            reply_markup=get_back_keyboard()
        )
    elif data[0:2] == 're':
        del_pk = data[2:]
        reward = Reward.objects.get(pk=int(del_pk))
        reward.is_received = True
        reward.save()
        query.edit_message_text(
            text=f'Вы получили свой подарок:\n\n✨  {reward.text}  ✨',
            reply_markup=get_back_keyboard()
        )


@get_or_create_profile
def case_messages(update: Update, context: CallbackContext, user):
    club = ClubInfo.objects.get(id_name=user.user_club)

    # bot = telepot.Bot(club.telegram_token)

    if CaseBody.objects.filter(club=club.id_name, date_start__lte=datetime.datetime.now(),
                               date_end__gte=datetime.datetime.now()).count() == 1:

        case_body = CaseBody.objects.get(club=club.id_name, date_start__lte=datetime.datetime.now(),
                                         date_end__gte=datetime.datetime.now())

        keyboard = [[InlineKeyboardButton('Открыть коробку  🎉', callback_data='open'),
                     InlineKeyboardButton('🎁  Призы  🎁', callback_data='about')],
                    [InlineKeyboardButton('Как открыть коробку  ⁉', callback_data='how_open')],
                    [InlineKeyboardButton('🥳  Мои подарки  🥳', callback_data='my_rewards')],
                    [InlineKeyboardButton('💳  Пополнить баланс  💳', callback_data='payment')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        if case_body.image:
            update.message.reply_photo(photo=case_body.image, reply_markup=reply_markup)
        else:
            update.message.reply_text(text=f'Привет, {user.nickname}!', reply_markup=reply_markup)
    else:
        update.message.reply_text(text=f'Данная акция сейчас не активна')


class Command(BaseCommand):
    help = 'Good Game Bot'

    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)

        updater = Updater(bot=bot)

        case_handler = CommandHandler('case', case_messages)
        updater.dispatcher.add_handler(case_handler)

        buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=False)
        updater.dispatcher.add_handler(buttons_handler)

        updater.start_polling()
        updater.idle()


box_250 = ['1 час игры за пк', 'Полчаса игры за PS', 'Полчаса игры за ПК']
box_500 = ['Батончик', '1.5 часа за PC', 'Кола (0.5)', 'Пакет в зал Стандарт (ночной)']
box_1000 = ['Пакет в зал VIP (утренний)', 'Кола и батончик', '3 часа за PS']
box_2000 = ['Абонемент на посещение клуба (на все выходные)', 'Кальян', 'Пакет в зал VIP (ночной)']
