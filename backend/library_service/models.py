from django.db import models
from django.contrib.auth.models import User

# TODO: создать директорию models для логического разделения моделей по файлам

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



class Section(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание")
    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"
    def __str__(self):
        return self.name

class Library(models.Model):
    location = models.CharField(max_length=255, verbose_name="Место")
    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.location

class Catalog(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Филиал")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Секция")
    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталоги"

    def __str__(self):
        return f"Catalog {self.id} in Branch {self.library.location}, Section {self.section.name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    exemplar_id = models.CharField(max_length=255)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"Exemplar ID {self.exemplar_id} in Order {self.order.id}"