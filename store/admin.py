from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory',
                         'inventory_status','total_price',
                           'collection']
    list_editable = ['unit_price', 'inventory','collection']
    ordering = ('title',)
    list_per_page = 10
    list_select_related = ('collection',)


    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory <10:
            return 'Low'
        else:
            return 'Ok'

    @admin.display(ordering='unit_price')
    def total_price(self,product):
        return product.unit_price * product.inventory


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ('first_name', 'last_name')
    list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at','customer','payment_status']
    list_per_page = 10
    list_editable = ['payment_status']
    list_select_related = ('customer',)
    

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ('title','products_count')

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (
            reverse('admin:store_product_changelist')
            +'?'
            +urlencode({'collection__id':str(collection.id)}))
        return format_html('<a href="{}">{}</a>',url ,collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))



