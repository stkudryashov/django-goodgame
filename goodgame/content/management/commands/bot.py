from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot, Update

from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, CallbackQueryHandler

from telegram.utils.request import Request

from content.models import FullInfoUser, ClubInfo, CaseBody, CaseGrades, CaseReward, Mainlog

from random import choice
from datetime import datetime
from datetime import timedelta

import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def get_or_create_profile(f):
    def inner(update=None, context=None, user_id=None, club_id=None):
        try:
            chat_id = update.message.chat_id
            p, _ = FullInfoUser.objects.get_or_create(
                telegram_id=chat_id,
                user_id=chat_id,
                user_club='goodgame1',
                defaults={'nickname': update.message.from_user.name}
            )
            f(p.pk, p.user_club)
        except AttributeError:
            f(user_id, club_id)

    return inner


def case_back():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🔙  Назад  🔙', callback_data='CaseBack')]])
    return keyboard


def get_payment_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='100₽', callback_data='m100'),
                                                      InlineKeyboardButton(text='250₽', callback_data='m250'),
                                                      InlineKeyboardButton(text='500₽', callback_data='m500')],
                                                     [InlineKeyboardButton(text='1000₽', callback_data='m1000'),
                                                      InlineKeyboardButton(text='1500₽', callback_data='m1500'),
                                                      InlineKeyboardButton(text='2000₽', callback_data='m2000')]])
    return keyboard


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


def case_payments_last(user_id):
    now_time = datetime.now()
    last_lime = now_time - timedelta(hours=1)
    recently = Mainlog.objects.filter(clientid=user_id, recorddtime__gte=last_lime, cashadd__gte=0)

    pay_sum = 0
    if recently:
        for payment in recently:
            pay_sum += payment.cashadd

    return pay_sum


def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    button_press = data
    edit_message = (query.message.chat_id, query.message.message_id)

    user = FullInfoUser.objects.get(telegram_id=query.message.chat_id)
    today = datetime.today()

    club = ClubInfo.objects.get(id_name=user.user_club)
    bot = telepot.Bot(club.telegram_token)

    if data[0] == 'm':
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            data = data[1:]

            main_log = Mainlog(cashadd=float(data), clientid=user.user_id)
            main_log.save()

            bot.sendMessage(
                chat_id=user.telegram_id,
                text='Вы пополнили баланс на {}₽'.format(data),
                reply_markup=case_back()
            )
    elif 'CaseShow' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            case_show(user.user_id, club.id)
    elif 'CaseAbout' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            case_about(user.telegram_id, club.id)
    elif 'CaseHowOpen' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            case_how_open(user.telegram_id, club.id)
    elif 'CaseBack' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            # убрать именованные аргументы, оставить только значения, как в комменте ниже
            # case_messages(user.id, club.id_name)
            # костыль, чтобы у меня все работало
            case_messages(user_id=user.id, club_id=club.id_name)
    elif 'CasePayment' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            bot.sendMessage(
                chat_id=user.telegram_id,
                text=f'На какую сумму пополнение?',
                reply_markup=get_payment_keyboard()
            )
    elif 'CaseOpen' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            value = button_press.split(' ')[1]
            case_open(user.user_id, club.id, value)

    # elif data == 'CaseMyRewards':
    #     keyboard = []
    #     rewards = Reward.objects.filter(user_id=user.user_id, is_received=False)
    #     if rewards:
    #         for reward in rewards:
    #             keyboard.append([InlineKeyboardButton(reward.text, callback_data='re' + str(reward.pk))])
    #         keyboard.append([InlineKeyboardButton('🔙  Назад  🔙', callback_data='back')])
    #         query.message.edit_text(text='Открывай награды только при администраторе!\n\n'
    #                                      'Ваши доступные награды:', reply_markup=InlineKeyboardMarkup(keyboard))
    #     else:
    #         query.message.edit_text(text='У вас пока нет наград  😢', reply_markup=case_back())

    # elif data[0:2] == 're':
    #     del_pk = data[2:]
    #     reward = Reward.objects.get(pk=int(del_pk))
    #     reward.is_received = True
    #     reward.save()
    #     query.edit_message_text(
    #         text=f'Вы получили свой подарок:\n\n✨  {reward.text}  ✨',
    #         reply_markup=case_back()
    #     )


@get_or_create_profile
def case_messages(user_id, club_id):
    club = ClubInfo.objects.get(id_name=club_id)
    user = FullInfoUser.objects.get(id=user_id)

    bot = telepot.Bot(club.telegram_token)

    if CaseBody.objects.filter(club=club.id_name, date_start__lte=datetime.now(),
                               date_end__gte=datetime.now()).count() == 1:

        case_body = CaseBody.objects.get(club=club.id_name, date_start__lte=datetime.now(),
                                         date_end__gte=datetime.now())

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Открыть коробку  🎉', callback_data='CaseShow'),
                              InlineKeyboardButton(text='🎁  Призы  🎁', callback_data='CaseAbout')],
                             [InlineKeyboardButton(text='Как открыть коробку  ⁉', callback_data='CaseHowOpen')],
                             [InlineKeyboardButton(text='🥳  Мои подарки  🥳', callback_data='CaseMyRewards')],
                             [InlineKeyboardButton(text='💳  Пополнить баланс  💳', callback_data='CasePayment')]]
        )

        if case_body.image:
            bot.sendPhoto(chat_id=user.telegram_id, photo=case_body.image, reply_markup=keyboard)
        else:
            if case_body.message_text:
                bot.sendMessage(chat_id=user.telegram_id, text=case_body.message_text, reply_markup=keyboard)
            else:
                bot.sendMessage(chat_id=user.telegram_id, text='Привет, {}!'.format(user.nickname),
                                reply_markup=keyboard)
    else:
        bot.sendMessage(chat_id=user.telegram_id, text='Данная акция сейчас не активна')


def case_about(telegram_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    about_text = CaseBody.objects.get(club=club.id_name, date_start__lte=datetime.now(),
                                      date_end__gte=datetime.now()).about_text
    bot.sendMessage(chat_id=telegram_id, text=about_text, reply_markup=case_back())


def case_how_open(telegram_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    how_open = CaseBody.objects.get(club=club.id_name, date_start__lte=datetime.now(),
                                    date_end__gte=datetime.now()).how_open
    bot.sendMessage(chat_id=telegram_id, text=how_open, reply_markup=case_back())


def case_show(user_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    user = FullInfoUser.objects.get(user_id=user_id)
    case_grades = CaseGrades.objects.filter(club=club.id_name)

    if True:  # user.open_day != today.day
        pay_sum = case_payments_last(user.user_id)  # чек за последние сутки
        min_sum = case_grades.order_by('cost')[0].cost  # самый дешевый кейс

        if pay_sum < min_sum:  # если чек за последние сутки меньше, чем стоимость самого дешевого кейса
            bot.sendMessage(
                chat_id=user.telegram_id,
                text='За последние 24 часа {}₽\n\nНужно пополнится чтобы получить подарок  😢'.format(pay_sum),
                reply_markup=case_back())
        else:
            keyboard = []
            for case in case_grades:  # собираем клавиатуру из доступных кейсов
                if pay_sum >= case.cost:
                    keyboard.append([InlineKeyboardButton(
                        text=case.text,
                        callback_data='CaseOpen {}'.format(case.cost))]
                    )

            keyboard.append([InlineKeyboardButton(text='🔙  Назад  🔙', callback_data='CaseBack')])
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

            bot.sendMessage(
                chat_id=user.telegram_id,
                text='За последние 24 часа {}₽\n\nОткрой свой подарок  😉'.format(pay_sum),
                reply_markup=keyboard
            )
    # else:
    #     query.message.edit_text(
    #         text='Ты уже получил сегодня подарки\n\nВозвращайся завтра  😴',
    #         reply_markup=get_back_keyboard())


def case_open(user_id, club_id, value):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    user = FullInfoUser.objects.get(user_id=user_id)

    rewards = CaseGrades.objects.get(club=club.id_name, cost=value).rewards
    reward = choice(rewards.split(', '))

    user_reward = CaseReward(club_id=club.id_name, user_id=user.user_id, text=reward)
    user_reward.save()

    bot.sendMessage(chat_id=user.telegram_id, text='Поздравляем, ваш приз: {}!'.format(reward), reply_markup=case_back())


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
