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
    club = models.TextField(default='goodgame', verbose_name='в каком клубе', null=True)
    date_start = models.DateTimeField(blank=True, verbose_name='начало акции', null=True)
    date_end = models.DateTimeField(blank=True, verbose_name='конец акции', null=True)
    how_open = models.TextField(blank=True, verbose_name='как открыть коробку', null=True)
    about_text = models.TextField(blank=True, verbose_name='о кейсах', null=True)
    message_text = models.TextField(blank=True, verbose_name='сообщение', null=True)
    image = models.ImageField(blank=True, upload_to='images/cases/', verbose_name='изображение', null=True)

    def __str__(self):
        return '{}-{}'.format(self.club, self.date_end)

    class Meta:
        verbose_name = 'акция с кейсами'
        verbose_name_plural = 'акции с кейсами'


class CaseGrades(models.Model):
    club = models.TextField(blank=True, default='goodgame', verbose_name='в каком клубе', null=True)
    cost = models.IntegerField(blank=True, verbose_name='цена кейса', null=True)
    text = models.TextField(blank=True, verbose_name='текст на кнопке', null=True)
    rewards = models.TextField(blank=True, verbose_name='призы через запятую', null=True)

    def __str__(self):
        return '{}-{}'.format(self.club, self.cost)

    class Meta:
        verbose_name = 'настройка кейса'
        verbose_name_plural = 'настройки кейсов'


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
    user_id = models.TextField(verbose_name='владелец', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время получения')
    text = models.CharField(max_length=100, verbose_name='награда')
    is_received = models.BooleanField(default=False, verbose_name='получил')

    def __str__(self):
        return f'pm-{self.pk}-id-{self.user_id}'

    class Meta:
        verbose_name = 'награда'
        verbose_name_plural = 'награды'


class CaseRewards(models.Model):
    club = models.TextField(verbose_name='в каком клубе', default='')
    cost = models.CharField(max_length=8, verbose_name='цена кейса', default='')
    text = models.CharField(max_length=100, verbose_name='награда', default='')

    def __str__(self):
        return f'cost-{self.cost}-id-{self.club}'

    class Meta:
        verbose_name = 'список наград'
        verbose_name_plural = 'список наград'


class Mainlog(models.Model):
    recorddtime = models.DateTimeField(auto_now_add=True, verbose_name='дата записи')
    cashadd = models.FloatField(verbose_name='размер платежа')
    clientid = models.IntegerField(verbose_name='id клиента')

    def __str__(self):
        return f'rtime-{self.recorddtime}-id-{self.clientid}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'
