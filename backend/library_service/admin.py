from django.contrib import admin
from .models import (
    UserProfile, Basket, BasketItem, Order,
    History, OrderItem, Section, Branch, Catalog
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'library_card', 'campus_id', 'mira_id', 'role']
    list_filter = ['role',]

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ['created_at',]


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'basket', 'book_id']
    list_filter = ['basket',]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_filter = ['user',]


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'status', 'confirmed_at', 'staff_id']
    list_filter = ['status', 'confirmed_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'exemplar_id', 'catalog']
    list_filter = ['order', 'catalog']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name',]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'location']
    search_fields = ['location',]


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'branch', 'section']
    list_filter = ['branch', 'section']
