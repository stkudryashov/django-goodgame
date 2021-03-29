from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot, Update

from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, CallbackQueryHandler

from telegram.utils.request import Request

from content.models import FullInfoUser, ClubInfo, CaseBody, CaseGrades, CaseReward, Mainlog

from random import choice, choices
from datetime import datetime
from datetime import timedelta

import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

time_delta = timedelta(minutes=5)


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
            club = ClubInfo.objects.get(id_name=p.user_club)
            f(p.pk, club.pk)
        except AttributeError:
            f(user_id, club_id)

    return inner


def case_is_active(f):
    def inner(user_id, club_id):
        club = ClubInfo.objects.get(id=club_id)
        user = FullInfoUser.objects.get(id=user_id)

        bot = telepot.Bot(club.telegram_token)

        if CaseBody.objects.filter(club=club.id_name, date_start__lte=datetime.now(),
                                   date_end__gte=datetime.now()).count() == 1:
            f(user_id, club_id)
        else:
            bot.sendMessage(chat_id=user.telegram_id, text='Данная акция сейчас не активна')

    return inner


def case_back():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🔙  Назад  🔙', callback_data='CaseBack')]])
    return keyboard


def case_payment():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='100₽', callback_data='m100'),
                                                      InlineKeyboardButton(text='250₽', callback_data='m250'),
                                                      InlineKeyboardButton(text='500₽', callback_data='m500')],
                                                     [InlineKeyboardButton(text='1000₽', callback_data='m1000'),
                                                      InlineKeyboardButton(text='1500₽', callback_data='m1500'),
                                                      InlineKeyboardButton(text='2000₽', callback_data='m2000')]])
    return keyboard


def case_payments_last(user_id):
    now_time = datetime.now()
    last_lime = now_time - time_delta

    recently_pays = Mainlog.objects.filter(clientid=user_id, recorddtime__gte=last_lime, cashadd__gte=0)
    pay_sum = 0
    if recently_pays:
        for payment in recently_pays:
            pay_sum += payment.cashadd

    recently_rewards = CaseReward.objects.filter(user_id=user_id, created_at__gte=last_lime)
    reward_sum = 0
    if recently_rewards:
        for reward in recently_rewards:
            reward_sum += reward.case_cost

    return pay_sum - reward_sum


def edit_messages(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    button_press = data
    edit_message = (query.message.chat_id, query.message.message_id)

    user = FullInfoUser.objects.get(telegram_id=query.message.chat_id)

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
            case_show(user.id, club.id)
    elif 'CaseAbout' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            case_about(user.id, club.id)
    elif 'CaseHowOpen' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            case_how_open(user.id, club.id)
    elif 'CaseBack' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            # убрать именованные аргументы, оставить только значения, как в комменте ниже
            # case_messages(user.id, club.id_name)
            # костыль, чтобы у меня все работало
            case_messages(user_id=user.id, club_id=club.id)
    elif 'CasePayment' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            bot.sendMessage(
                chat_id=user.telegram_id,
                text='На какую сумму пополнение?',
                reply_markup=case_payment()
            )
    elif 'CaseOpen' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            value = button_press.split(' ')[1]
            case_open(user.id, club.id, value)
    elif 'CaseMyRewards' in button_press:
        try:
            bot.deleteMessage(edit_message)
        except telepot.exception.TelegramError:
            pass
        finally:
            case_my_reward(user.id, club.id)
    # elif 'CaseReward' in button_press:
    #     try:
    #         bot.deleteMessage(edit_message)
    #     except telepot.exception.TelegramError:
    #         pass
    #     finally:
    #         reward_id = button_press.split(' ')[1]
    #         case_open_reward(user.id, club.id, reward_id)


@get_or_create_profile
def case_messages(user_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
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


@case_is_active
def case_about(user_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    user = FullInfoUser.objects.get(id=user_id)

    about_text = CaseBody.objects.get(club=club.id_name, date_start__lte=datetime.now(),
                                      date_end__gte=datetime.now()).about_text
    bot.sendMessage(chat_id=user.telegram_id, text=about_text, reply_markup=case_back())


@case_is_active
def case_how_open(user_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    user = FullInfoUser.objects.get(id=user_id)

    how_open = CaseBody.objects.get(club=club.id_name, date_start__lte=datetime.now(),
                                    date_end__gte=datetime.now()).how_open
    bot.sendMessage(chat_id=user.telegram_id, text=how_open, reply_markup=case_back())


@case_is_active
def case_show(user_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    user = FullInfoUser.objects.get(id=user_id)
    case_grades = CaseGrades.objects.filter(club=club.id_name)
    case_body = CaseBody.objects.get(club=club.id_name)

    now_time = datetime.now()
    last_lime = now_time - time_delta

    recently_open = CaseReward.objects.filter(
        user_id=user.user_id,
        created_at__gte=last_lime
    )  # сколько кейсов открыл за последние сутки

    if recently_open.count() < case_body.limit:
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
    else:
        bot.sendMessage(
            chat_id=user.telegram_id,
            text='Ты уже получил сегодня подарки\n\nВозвращайся завтра  😴',
            reply_markup=case_back())


def case_open(user_id, club_id, value):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    user = FullInfoUser.objects.get(id=user_id)

    if CaseBody.objects.filter(club=club.id_name, date_start__lte=datetime.now(),
                               date_end__gte=datetime.now()).count() == 1:
        rewards = CaseGrades.objects.get(club=club.id_name, cost=value).rewards
        weights = CaseGrades.objects.get(club=club.id_name, cost=value).weights

        if weights:
            try:
                weights = weights.split(', ')
                weights = [float(value) for value in weights]

                reward = choices(rewards.split(', '), weights=weights, k=1)[0]
            except ValueError:
                reward = choice(rewards.split(', '))
        else:
            reward = choice(rewards.split(', '))

        user_reward = CaseReward(club=club.id_name, user_id=user.user_id, text=reward, case_cost=value)
        user_reward.save()

        bot.sendMessage(chat_id=user.telegram_id, text='Поздравляем, ваш приз: {}!'.format(reward),
                        reply_markup=case_back())
    else:
        bot.sendMessage(chat_id=user.telegram_id, text='Данная акция сейчас не активна')


@case_is_active
def case_my_reward(user_id, club_id):
    club = ClubInfo.objects.get(id=club_id)
    bot = telepot.Bot(club.telegram_token)

    user = FullInfoUser.objects.get(id=user_id)

    user_rewards = CaseReward.objects.filter(club=club.id_name, user_id=user.user_id, is_received=False)

    reward_message = '🥳  Твои доступные награды:\n'
    if user_rewards:
        for reward in user_rewards:  # собираем сообщение с наградами
            reward_message += '\n• ' + reward.text

    if user_rewards:
        bot.sendMessage(
            chat_id=user.telegram_id,
            text=reward_message,
            reply_markup=case_back()
        )
    else:
        bot.sendMessage(
            chat_id=user.telegram_id,
            text='У вас пока нет наград  😢',
            reply_markup=case_back()
        )


# def case_open_reward(user_id, club_id, reward_id):
#     club = ClubInfo.objects.get(id=club_id)
#     bot = telepot.Bot(club.telegram_token)
#
#     user = FullInfoUser.objects.get(id=user_id)
#
#     reward = CaseReward.objects.get(id=reward_id)
#
#     reward.is_received = True
#     reward.save()
#
#     bot.sendMessage(
#         chat_id=user.telegram_id,
#         text='Вы получили свой подарок:\n\n✨  {}  ✨'.format(reward.text),
#         reply_markup=case_back()
#     )


class Command(BaseCommand):
    help = 'Good Game Bot'

    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)

        updater = Updater(bot=bot)

        case_handler = CommandHandler('case', case_messages)
        updater.dispatcher.add_handler(case_handler)

        buttons_handler = CallbackQueryHandler(callback=edit_messages, pass_chat_data=False)
        updater.dispatcher.add_handler(buttons_handler)

        updater.start_polling()
        updater.idle()
