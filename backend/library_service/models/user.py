from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    library_card = models.CharField(verbose_name="Номер читательского билета", max_length=255)
    campus_id = models.CharField(verbose_name="ID кампуса",max_length=255)
    mira_id = models.CharField(verbose_name="ID mira",max_length=255)
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Profile for {self.user.username} ({self.role.name})"
    
class Basket(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Basket {self.id} for User {self.user.id}"

class BasketItem(models.Model):
    book_id = models.CharField(verbose_name="ID книги", max_length=255)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"Book ID {self.book_id} in Basket {self.basket.id}"