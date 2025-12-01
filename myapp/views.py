from django.shortcuts import render,HttpResponse
from .models import *
from django.db.models import Count
from itertools import zip_longest 

# Create your views here.
def home(request):
    return HttpResponse("hello")

def index(request):
    c_id=Main_category.objects.annotate(product_count=Count('product'))
    contaxt={'c_id':c_id}
    return render(request,'index.html',contaxt)

def cart(request):
    c_id=Main_category.objects.all()
    contaxt={'c_id':c_id}
    return render(request,'cart.html',contaxt)

def checkout(request):
    c_id=Main_category.objects.all()
    contaxt={'c_id':c_id}
    return render(request,'checkout.html',contaxt)

def contact(request):
    c_id=Main_category.objects.all()
    contaxt={'c_id':c_id}
    return render(request,'contact.html',contaxt)

def detail(request):
    c_id=Main_category.objects.all()
    contaxt={'c_id':c_id}
    return render(request,'detail.html',contaxt)

def find_price_range(request):
    price_range=Price_range.objects.all()
    r_w_p=[]
    for product in price_range:
        if product.min_price is not None and product.max_price is not None and product.min_price != "" and product.max_price != "":
            range=Product.objects.filter(product_price__gte=product.min_price,product_price__lte=product.max_price).distinct()
            r_w_p.append(range.count())
   
    price_id=list(zip_longest(price_range,r_w_p,fillvalue=0))
    total_price_product=sum(r_w_p)
    return price_id,total_price_product,price_range


def shop(request):
    c_id=Main_category.objects.all()
    color_id=Color.objects.annotate(product_count=Count('product'))
    size_id=Size.objects.annotate(product_count=Count('product'))
    total_color_product=Product.objects.filter(color__isnull=False).count()
    total_size_product=Product.objects.filter(size__isnull=False).count()
    price_id,total_price_product,price_range=find_price_range(request)
    # price_range=Price_range.objects.all()
    # r_w_p=[]
    # for product in price_range:
    #     if product.min_price is not None and product.max_price is not None and product.min_price != "" and product.max_price != "":
    #         range=Product.objects.filter(product_price__gte=product.min_price,product_price__lte=product.max_price).distinct()
    #         r_w_p.append(range.count())
   
    # price_id=list(zip_longest(price_range,r_w_p,fillvalue=0))
    # total_price_product=sum(r_w_p)

    sub=request.GET.get('s_id')
    if sub:
        p_id=Product.objects.filter(sub_cat__id=sub)
    else:   
        p_id=Product.objects.all()

    contaxt= {
        "p_id":p_id,
        "c_id":c_id,
        "color_id":color_id,
        "size_id":size_id,
        "sub":sub ,  
        "total_color_product":total_color_product,
        "total_size_product":total_size_product,
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id
    }
    return render(request,'shop.html',contaxt)

def color_filter(request):
    # Support POST (form) and fallback to GET, accept multiple values
    selected_color = request.POST.getlist('color') or request.GET.getlist('color') or []
   
    if selected_color:
        p_id = Product.objects.filter(color__id__in=selected_color).distinct()
    else:
        p_id = Product.objects.all()

    price_id,total_price_product,price_range=find_price_range(request)
    contaxt = {
        "p_id": p_id,
        "c_id": Main_category.objects.all(),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id

    }
    return render(request, 'shop.html', contaxt)

def size_filter(request):
    selected_size=request.GET.getlist('size') or request.POST.getlist('size') or []
    if selected_size:
        p_id=Product.objects.filter(size__id__in=selected_size).distinct()
    else:
        p_id=Product.objects.all()

    price_id,total_price_product,price_range=find_price_range(request)
    contaxt={
        "p_id":p_id,
        "c_id": Main_category.objects.all(),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id

    }
    return render(request,'shop.html',contaxt)

def price_filter(request):
    selected_price=request.POST.getlist('price') or request.GET.getlist('price') or []
    min_price=[]
    max_price=[]
    for price in selected_price:
        price_id=Price_range.objects.get(id=price)
        min_price.append(price_id.min_price)
        max_price.append(price_id.max_price)
    minimum_price=min(min_price)
    maximum_price=max(max_price)
    if minimum_price is not None and maximum_price is not None and minimum_price != "" and maximum_price != "":
        p_id=Product.objects.filter(product_price__gte=minimum_price,product_price__lte=maximum_price).distinct()
    else:
        p_id=Product.objects.all()

    price_id,total_price_product,price_range=find_price_range(request)
    contaxt={
        "p_id":p_id,
        "c_id": Main_category.objects.all(),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id

    }
    return render(request,'shop.html',contaxt)

   