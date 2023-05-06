from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Friends(models.Model):
    @dataclass
    class APPLICATION_STATUS:
        APPROVED = 'approved'
        PENDING = 'pending'

    APPLICATION_STATUS_CHOISE = (
        (APPLICATION_STATUS.APPROVED, 'уже друзья'),
        (APPLICATION_STATUS.PENDING, 'заявка в ожидании'),
    )

    friend_request_receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friends',
        verbose_name='Пользователь, получивший заявку на добавление в друзья')
    friend_request_sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend_of',
        verbose_name='Пользователь отправивший заявку на добавление в друзья')
    application_status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOISE,
        default=APPLICATION_STATUS.PENDING)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return (f'{self.friend_request_sender.username}')
