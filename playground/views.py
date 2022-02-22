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

    pruduct_count=Product.objects.aggregate(count=Count('id'))

    return render(request, 'Aggregating.html', {'pruduct_count':pruduct_count})