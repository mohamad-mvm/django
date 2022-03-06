from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline

from tags.models import TaggedItem

from . import models
# Register your models here.

# making custom filter for product inventory
class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return (
            ('<10', 'low'),
        )

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        return queryset


# add 2 forms together inline
class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num =1
    max_num = 10
    extra = 0
    

class TagInLine(GenericTabularInline):
    model = TaggedItem




@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory',
                    'inventory_status','total_price',
                    'collection']
    list_editable = ['unit_price', 'inventory','collection']
    list_filter = ['collection','last_update',InventoryFilter]
    ordering = ('title',)
    list_per_page = 10
    list_select_related = ('collection',)
    search_fields = ['title']
    inlines = [TagInLine]

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        product_count =queryset.update(inventory=0)
        self.message_user(
            request,
            f'{product_count} products inventory cleared',
            messages.SUCCESS,)


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
    list_display = ['customer_name', 'membership','order_count']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='first_name')
    def customer_name(self,customer):
        url = (reverse('admin:store_order_changelist')
                        + '?'
                        +urlencode({'customer__id':str(customer.id)}))
        return format_html('<a href="{}">{} </a>',url,customer.first_name + ' ' + customer.last_name )

    @admin.display(ordering='order_count')
    def order_count(self,customer):
        return str(customer.order_count) + ' Order'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(order_count=Count('order'))
        return qs


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at','customer','payment_status']
    inlines = [OrderItemInline]
    autocomplete_fields=['customer']
    list_per_page = 10
    list_editable = ['payment_status']
    list_select_related = ('customer',)
    

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ('title','products_count')
    search_fields = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (
            reverse('admin:store_product_changelist')
            +'?'
            +urlencode({'collection__id':str(collection.id)}))
        return format_html('<a href="{}">{}</a>',url ,collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))



