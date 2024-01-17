import datetime
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    '''Модель задачи.'''
    STATUS_CHOICES = (
        ('complete', 'Выполнен'),
        ('not_complete', 'Не выполнен'),
        ('in_progress', 'В работе'),
        ('cancel', 'Отменен'),
        ('trail', 'Отстает'),
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Название задачи',
        help_text='Введите название задачи',
    )
    description = models.TextField(
        max_length=200,
        verbose_name='Описание группы',
        help_text='Добавьте текст описания группы',
    )
    date_create = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата создания задачи',
    )
    deadline = models.DateField(verbose_name='Срок закрытия задачи')
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, verbose_name='Статус задачи')
    type = models.CharField(
        max_length=200,
        verbose_name='Тип задачи',
        help_text='Выберите тип задачи',
    )

    class Meta:
        ordering = ('-title',)
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title
