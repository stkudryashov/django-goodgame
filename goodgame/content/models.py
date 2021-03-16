from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='внешний ID', unique=True)
    name = models.TextField(verbose_name='имя пользователя')
    balance = models.FloatField(default=0, verbose_name='баланс')
    open_day = models.PositiveIntegerField(default=0, verbose_name='день открытия')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')

    def __str__(self):
        return f'{self.external_id}-{self.name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


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
