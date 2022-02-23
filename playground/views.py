from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q ,F
from django.db.models.aggregates import Count, Sum, Avg, Min, Max
from store.models import Customer, Product,Order,OrderItem,Promotion


def database_relational(request):
    products=Product.objects.select_related('collection').all()[:5]
    product_count=products.count()

    # orders = OrderItem.objects.prefetch_related('order__customer').select_related('order').order_by('order__placed_at')[0:5]
    orders= Order.objects.prefetch_related('orderitem_set__product').select_related('customer').order_by('placed_at')[0:30]
    order_count=orders.count()

    # for item22 in orders:
    #     if item22.orderitem_set.all():
    #         print(item22.orderitem_set.all()[0].product.title)

    customers =Customer.objects.filter(email__iendswith='.net')
    customer_count=customers.count()


    return render(request, 'database_relational.html', { 'name': 'mohamad',
                                            'products': list(products),
                                            'product_count': product_count,
                                            'customers':list(customers),
                                            'customer_count':customer_count,
                                            'orders':list(orders),
                                            'order_count':order_count,})



def Aggregating(request):

    pruduct_count=Product.objects.aggregate(Count('id'))
    pruduct_maxid=Product.objects.aggregate(max=Max('id'), min_price=Min('unit_price'))
    pruduct_avg_price=Product.objects.aggregate(avg_price=Avg('unit_price'))
    pruduct_sum_price=Product.objects.aggregate(sum_price=Sum('unit_price'))
    product_count_by_collection=Product.objects.filter(collection__id=3).aggregate(Count('id'))
    # How many orders do we have?
    order_count = Order.objects.aggregate(order_count = Count('id'))
    # How many units of product 1 have we sold?
    product_1_units_sold = OrderItem.objects.filter(product__id=1).aggregate(units_sold=Sum('quantity'))

    # How many orders has customer 1 placed?
    customer_1_orders = Order.objects.filter(customer__id=1).aggregate(order_count=Count('id'))

    # What is the min, max and average price of the products in collection 3?
    collection_3_products = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))


    return render(request, 'Aggregating.html', {'pruduct_count':pruduct_count,
                                                'pruduct_maxid':pruduct_maxid,
                                                'pruduct_avg_price':pruduct_avg_price,
                                                'pruduct_sum_price':pruduct_sum_price,
                                                'product_count_by_collection':product_count_by_collection,
                                                'order_count':order_count,
                                                'product_1_units_sold':product_1_units_sold,
                                                'customer_1_orders':customer_1_orders,})