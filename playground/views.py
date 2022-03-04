from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q ,F,Func,Value,ExpressionWrapper,DecimalField,FloatField,IntegerField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Sum, Avg, Min, Max
from store.models import Customer, Product,Order,OrderItem,Collection
from tags.models import TaggedItem



def home(request):
    return render(request, 'home.html', {})

def database_relational(request):
    products=Product.objects.select_related('collection').all()[:5]
    product_count=products.count()

    # orders = OrderItem.objects.prefetch_related('order__customer').select_related('order').order_by('order__placed_at')[0:5]
    orders= Order.objects.prefetch_related(
                                            'orderitem_set__product').select_related('customer').order_by('placed_at')[0:30]
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


def annotate(request):
    # How many orders do we have?
    order_item = OrderItem.objects.annotate(total_price=F('unit_price')*F('quantity'))
    t_unitprice=order_item.aggregate(total_unitprice=Sum('unit_price'))
    t_quantity=order_item.aggregate(total_quantity=Sum('quantity'))
    total=order_item.aggregate(total=Sum('total_price')) 

    return render(request, 'annotate.html', {'order_item':order_item,
                                                't_unitprice':t_unitprice,
                                                't_quantity':t_quantity,
                                                'total':total,})


def Database_Functions(request):
    # make new field in customer model with name 'full_name' that concatenates first_name and last_name
    customers = Customer.objects.annotate(full_name=Func(F('first_name'),Value(' '),F('last_name'), function='concat'))
    # make new field in customer model with name 'full_name' that concatenates first_name and last_name using Concat
    customers = Customer.objects.annotate(full_name=Concat('first_name',Value(' '),'last_name'))

    # use below adress for more databese function method
    # https://docs.djangoproject.com/en/4.0/ref/models/database-functions/

    return render(request, 'Database_Functions.html', {'customers':customers,})


def Grouping_Data(request):
    # group customer by number of orders
    customers = Customer.objects.annotate(count=Count('order'),
                                           full_name=Concat('first_name',Value(' '),'last_name')).order_by('id')

    return render(request, 'Grouping_Data.html', {'customers':customers,})

def  Expression_Wrappers(request):
    experetion = ExpressionWrapper(F('unit_price')*0.8, output_field = FloatField())
    products = Product.objects.annotate(discounted_price=experetion)[:5]

    # Customers with their last order ID
    customers = Customer.objects.annotate(last_order=Max('order__id'))[:5]

    # Collections and count of their products
    collection = Collection.objects.annotate(count_products=Count('product'))

    # Customers with more than 5 orders
    customers_more_than_5_orders = Customer.objects.annotate(count_orders=Count('order')).filter(count_orders__gt=5)

    # Customers and the total amount they’ve spent
    expression_for_customer=ExpressionWrapper(F('order__orderitem__unit_price') * F('order__orderitem__quantity'), output_field=FloatField())
    customers_and_total_spent = Customer.objects.annotate(total_spent=Sum(expression_for_customer))[:5]

    # Top 5 best-selling products and their total sales
    experesion_for_best_selling_products=ExpressionWrapper(F('orderitem__unit_price') * F('orderitem__quantity'), output_field=FloatField())
    best_selling_products = Product.objects.annotate(total_sales=Sum(experesion_for_best_selling_products)).order_by('-total_sales')[:5]

    

    return render(request, 'Expression_Wrappers.html', {'products':products,
                                                        'customers':customers,
                                                        'collection':collection,
                                                        'customers_more_than_5_orders':customers_more_than_5_orders,
                                                        'customers_and_total_spent':customers_and_total_spent,
                                                        'best_selling_products':best_selling_products,})


def Querying_Generic_Relationships(request):
    # making connection with tags app in generic mode and get all tags that are related to product
    tages = TaggedItem.objects.get_tags_for(Collection,2)


    return render(request, 'Querying_Generic_Relationships.html', {'tags':tages,})

def Creating_Objects(request):
    # create new collection
    # new_collection = Collection.objects.create(title='video games', featured_product_id=1)

    # collection =collection(title='video games', featured_product_id=1)
    # collection1.save()


    collection1 = Collection()
    collection1.title='video games'
    collection1.featured_product_id=1
    collection1.save()
    collid =collection1.id



    return render(request, 'Creating_Objects.html', {'new_collection':collection1,
                                                    'collid':collid,})

def Updating_Objects(request):
    # updating new collection

    collection = Collection.objects.get(id=11)
    collection.featured_product_id=None
    collection.save()

    Collection.objects.filter(id=11).update(featured_product_id=None)

    return render(request, 'Updating_Objects.html', {'collection':collection,})



