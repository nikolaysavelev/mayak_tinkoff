from __future__ import annotations

from typing import Union, Optional, Tuple

from django.db import models
from django.db.models import QuerySet, Manager
from telegram import Update
from telegram.ext import CallbackContext

from dtb.settings import DEBUG
from tgbot.handlers.utils.info import extract_user_data_from_update
from utils.models import CreateUpdateTracker, nb, CreateTracker, GetOrNoneManager


class Strategy(CreateUpdateTracker):
    strategy_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, **nb)
    description = models.TextField()
    ti_link = models.URLField()

    objects = GetOrNoneManager()

    @classmethod
    def get_strategy_and_created(cls, update: Update, context: CallbackContext):  # -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        print('context', update.callback_query.data)

        data = extract_user_data_from_update(update)
        bata = {'strategy_name': update.callback_query.data}
        print(bata)
        # TODO здесь все ломалось - пока зкомитила - обратите внимание
        u, created = cls.objects.update_or_create(user_id=data["user_id"],
                                                  defaults=bata)
        if update.callback_query.data == 'sma':
            u.strategy_id = 0
        else:
            u.strategy_id = 1
        u.save()
        print(u)

        if created:
            print('hi DEBUG')

            #TODO написать функции фильтрации стратегий для рассыльщика

        return u, created

    def __str__(self):
        return "%s %s" % (self.user_id, self.strategy_name)


class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class User(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", **nb)
    deep_link = models.CharField(max_length=64, **nb)
    strategy_id = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    strategy_id = models.BooleanField(default=False)

    is_blocked_bot = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    objects = GetOrNoneManager()  # user = User.objects.get_or_none(user_id=<some_id>)
    admins = AdminUserManager()  # User.admins.all()

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_and_created(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        print('data', data)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            # Save deep_link to User model
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> User:
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @property
    def invited_users(self) -> QuerySet[User]:
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"


class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=100)
    stock_group = models.BinaryField()


class Signal(models.Model):
    signal_id = models.AutoField(primary_key=True)  # id сигнала
    strategy_id = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    last_price = models.FloatField()
    action_flag = models.BooleanField()
    time_created = models.DateTimeField()
    percent = models.FloatField()


class UserSignal(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    signal_id = models.ForeignKey(Signal, on_delete=models.CASCADE)
    status = models.BinaryField()


class Location(CreateTracker):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    objects = GetOrNoneManager()

    def __str__(self):
        return f"user: {self.user}, created at {self.created_at.strftime('(%H:%M, %d %B %Y)')}"

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)
        # Parse location with arcgis
        from arcgis.tasks import save_data_from_arcgis
        if DEBUG:
            save_data_from_arcgis(latitude=self.latitude, longitude=self.longitude, location_id=self.pk)
        else:
            save_data_from_arcgis.delay(latitude=self.latitude, longitude=self.longitude, location_id=self.pk)
