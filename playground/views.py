import email
from itertools import count
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Customer, Product


def say_hello(request):
    products=Product.objects.filter(description__isnull=True)
    product_count=products.count()
    customers =Customer.objects.filter(email__iendswith='.net')
    customer_count=customers.count()


    return render(request, 'hello.html', { 'name': 'mohamad',
                                            'products': list(products),
                                            'product_count': product_count,
                                            'customers':list(customers),
                                            'customer_count':customer_count})
