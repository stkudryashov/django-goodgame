from django.db import models


class FullInfoUser(models.Model):
    user_id = models.IntegerField(unique=True, verbose_name='id в клубе')
    user_club = models.TextField(verbose_name='из какого клуба')
    nickname = models.TextField(verbose_name='имя пользователя')
    telegram_id = models.TextField(verbose_name='telegram id')

    def __str__(self):
        return '{}-{}'.format(self.telegram_id, self.nickname)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class ClubInfo(models.Model):
    id_name = models.TextField(default='goodgame', verbose_name='техническое название', null=True)
    text_name = models.TextField(blank=True, verbose_name='название клуба', null=True)
    address = models.TextField(blank=True, verbose_name='адрес клуба', null=True)
    telegram_token = models.TextField(blank=True, verbose_name='telegram токен', null=True)

    def __str__(self):
        return '{}-{}'.format(self.id_name, self.text_name)

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
    limit = models.PositiveIntegerField(blank=True, verbose_name='лимит кейсов в день', default=3)
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
    rewards = models.TextField(blank=True, verbose_name='призы через запятую с пробелом', null=True)
    weights = models.TextField(blank=True, verbose_name='веса через запятую с пробелом', null=True)

    def __str__(self):
        return '{}-{}'.format(self.club, self.cost)

    class Meta:
        verbose_name = 'настройка кейса'
        verbose_name_plural = 'настройка кейсов'


class CaseReward(models.Model):
    club = models.TextField(blank=True, verbose_name='id клуба', null=True)
    user_id = models.TextField(blank=True, verbose_name='владелец', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время получения')
    text = models.CharField(blank=True, max_length=100, verbose_name='награда', null=True)
    case_cost = models.IntegerField(blank=True, verbose_name='из какого кейса', null=True)
    is_received = models.BooleanField(default=False, verbose_name='получил')

    def __str__(self):
        return 'club-{}-id-{}'.format(self.club, self.user_id)

    class Meta:
        verbose_name = 'награда пользователя'
        verbose_name_plural = 'награды пользователей'


class Mainlog(models.Model):
    recorddtime = models.DateTimeField(auto_now_add=True, verbose_name='дата записи')
    cashadd = models.FloatField(verbose_name='размер платежа')
    clientid = models.IntegerField(verbose_name='id клиента')

    def __str__(self):
        return f'rtime-{self.recorddtime}-id-{self.clientid}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'
