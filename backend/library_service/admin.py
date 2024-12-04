from django.contrib import admin
from library_service.models.user import *
from library_service.models.catalog import *
from library_service.models.order import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "library_card", "campus_id", "mira_id",]

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_filter = ["created_at",]


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ["id", "basket", "book_id"]
    list_filter = ["basket",]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_filter = ["user",]


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "status", "confirmed_at", "staff_id"]
    list_filter = ["status", "confirmed_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "exemplar_id"]
    list_filter = ["order"]

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "address"]
    search_fields = ["location",]

@admin.register(LibraryDatabase)
class LibraryDatabaseAdmin(admin.ModelAdmin):
    list_display = ["id", "database", "library"]
