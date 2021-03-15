from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='внешний ID', unique=True)
    name = models.TextField(verbose_name='имя пользователя')
    balance = models.FloatField(default=0, verbose_name='баланс')

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
        return f'{self.pk}-{self.value}руб-{self.profile.name}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
