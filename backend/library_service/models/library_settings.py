from typing import Self
from django.db import models


def default_reader_notification_statuses():
    return ["processing", "ready", "cancelled"]


class LibrarySettings(models.Model):
    lock = models.CharField(max_length=1, null=False, primary_key=True, default="X")
    max_books_per_order = models.PositiveIntegerField(verbose_name="Максимальное количество книг в заказе", default=7)
    max_books_per_reader = models.PositiveIntegerField(verbose_name="Максимальное количество книг на руках", default=15)
    max_borrow_days = models.PositiveIntegerField(verbose_name="Максимальное количество дней на выдачу", default=2)
    holidays = models.JSONField(verbose_name="Список календарных выходных", default=list)
    logo = models.FileField(upload_to="logo/", verbose_name="Логотип на сервисе", null=True, blank=True)
    new_order_wait = models.FloatField(verbose_name="Срок ожидания нового заказа (в часах)", default=1)
    processing_order_wait = models.FloatField(verbose_name="Срок задержки исполнения заказа (в часах)", default=0.5)
    staff_digest_enabled = models.BooleanField(
        verbose_name="Отправлять сотрудникам уведомления о необработанных заказах",
        default=True,
    )
    staff_notification_active_hours = models.FloatField(
        verbose_name="Сотрудник считается недавно активным (в часах)",
        default=2,
    )
    staff_digest_stale_order_hours = models.FloatField(
        verbose_name="Через сколько часов заказ в NEW считается необработанным для рассылки",
        default=1,
    )
    reader_status_notifications_enabled = models.BooleanField(
        verbose_name="Отправлять читателю уведомления об изменении статуса заказа",
        default=True,
    )
    reader_notification_statuses = models.JSONField(
        verbose_name="Статусы заказа для уведомления читателя",
        default=default_reader_notification_statuses,
    )

    def save(self, *args, **kwargs):
        self.pk = "X"
        super().save(*args, **kwargs)

    async def asave(self, *args, **kwargs):
        self.pk = "X"
        return await super().asave(*args, **kwargs)

    @staticmethod
    def get_settings() -> Self:
        return LibrarySettings.objects.get_or_create(pk="X")[0]

    @staticmethod
    async def aget_settings() -> Self:
        return (await LibrarySettings.objects.aget_or_create(pk="X"))[0]

    class Meta:
        verbose_name = "Настройки библиотеки"
        verbose_name_plural = "Настройки библиотек"
