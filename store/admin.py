from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory']
    list_editable = ['unit_price', 'inventory']
    ordering = ('title',)
    list_per_page = 5


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ('first_name', 'last_name')
    list_per_page = 10

class collectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured_product')

admin.site.register(models.Collection, collectionAdmin)

