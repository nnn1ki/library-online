from django.db import models
from django.contrib.auth.models import User

from library_service.models.catalog import Library

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order {self.id} by User {self.user.id}"

class OrderHistory(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PROCESSING = "processing", "Собирается"
        READY = "ready", "Готов к выдаче"
        DONE = "done", "Выполнен"
        CANCELLED = "cancelled", "Отменен"
        ERROR = "error", "Ошибка"
        ARCHIVED = "archived", "Заархивирован"

    description = models.TextField()
    status = models.CharField(max_length=255, choices=Status.choices)
    date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="statuses")
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

    def __str__(self):
        return f"History for Order {self.order.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="books")
    exemplar_id = models.CharField(max_length=255)
    handed = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    order_to_return = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"Exemplar ID {self.exemplar_id} in Order {self.order.id}"