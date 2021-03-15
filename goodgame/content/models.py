from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='внешний ID')
    name = models.TextField(verbose_name='имя пользователя')

    def __str__(self):
        return f'{self.external_id}-{self.name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Message(models.Model):
    profile = models.ForeignKey(Profile, verbose_name='профиль', on_delete=models.PROTECT)
    text = models.TextField(verbose_name='сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время отправки')

    def __str__(self):
        return f'{self.pk}-{self.profile.name}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name = 'сообщения'
