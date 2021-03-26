from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='внешний ID')
    name = models.TextField(verbose_name='имя пользователя')
    balance = models.FloatField(default=0, verbose_name='баланс')
    open_day = models.PositiveIntegerField(default=0, verbose_name='день открытия')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')

    def __str__(self):
        return f'{self.external_id}-{self.name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class FullInfoUser(models.Model):
    user_id = models.IntegerField(unique=True, verbose_name='id в клубе')
    user_club = models.TextField(verbose_name='из какого клуба')
    nickname = models.TextField(verbose_name='имя пользователя')
    telegram_id = models.TextField(verbose_name='telegram id')

    def __str__(self):
        return f'{self.telegram_id}-{self.nickname}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class ClubInfo(models.Model):
    id_name = models.TextField(verbose_name='техническое название')
    text_name = models.TextField(verbose_name='название клуба')
    address = models.TextField(verbose_name='адрес клуба')
    telegram_token = models.TextField(verbose_name='telegram токен')

    def __str__(self):
        return f'{self.id_name}-{self.text_name}'

    class Meta:
        verbose_name = 'клуб'
        verbose_name_plural = 'клубы'


class CaseBody(models.Model):
    club = models.TextField(verbose_name='в каком клубе', default='')
    date_start = models.DateTimeField(verbose_name='начало акции')
    date_end = models.DateTimeField(verbose_name='конец акции')
    how_open = models.TextField(verbose_name='как открыть коробку', default='')
    about_text = models.TextField(verbose_name='о кейсах', default='')

    def __str__(self):
        return f'{self.club}-{self.date_end}'

    class Meta:
        verbose_name = 'кейс'
        verbose_name_plural = 'кейсы'


class Payment(models.Model):
    profile = models.ForeignKey(Profile, verbose_name='профиль', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время отправки')
    value = models.FloatField(verbose_name='размер платежа')

    def __str__(self):
        return f'pm-{self.pk}-id-{self.profile.external_id}-val-{self.value}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Reward(models.Model):
    profile = models.ForeignKey(Profile, verbose_name='владелец', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время получения')
    text = models.CharField(max_length=100, verbose_name='награда')
    is_received = models.BooleanField(default=False, verbose_name='получил')

    def __str__(self):
        return f'pm-{self.pk}-id-{self.profile.external_id}'

    class Meta:
        verbose_name = 'награда'
        verbose_name_plural = 'награды'


class Mainlog(models.Model):
    recorddtime = models.DateTimeField(auto_now_add=True, verbose_name='дата записи')
    cashadd = models.FloatField(verbose_name='размер платежа')
    clientid = models.IntegerField(verbose_name='id клиента')

    def __str__(self):
        return f'rtime-{self.recorddtime}-id-{self.clientid}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'
