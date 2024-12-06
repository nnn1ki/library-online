from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order {self.id} by User {self.user.id}"

class History(models.Model):
    description = models.TextField()
    status = models.CharField(max_length=255)
    confirmed_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

    def __str__(self):
        return f"History for Order {self.order.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    exemplar_id = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"Exemplar ID {self.exemplar_id} in Order {self.order.id}"