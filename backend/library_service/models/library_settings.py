from typing import Self
from django.db import models


class LibrarySettings(models.Model):
    lock = models.CharField(max_length=1, null=False, primary_key=True, default="X")
    max_books_per_order = models.PositiveIntegerField(verbose_name="Максимальное количество книг в заказе", default=5)
    max_books_per_reader = models.PositiveIntegerField(verbose_name="Максимальное количество книг на руках", default=10)
    max_borrow_days = models.PositiveIntegerField(verbose_name="Максимальное количество дней на выдачу", default=14)
    max_extensions = models.PositiveIntegerField(verbose_name="Максимальное количество продлений", default=2)
    overdue_fine_per_day = models.DecimalField(
        verbose_name="Штраф за просрочку (в день)", max_digits=6, decimal_places=2, default=10.00
    )
    holidays = models.JSONField(verbose_name="Список календарных выходных", default=list)

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
