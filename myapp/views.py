from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.db.models import Count
from django.db.models.functions import Random
from itertools import zip_longest 
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    return HttpResponse("hello")

def index(request):

    if "email_id" in request.session or "user_name" in request.session:  
        user_name=Register.objects.get(email_id=request.session['email_id'])
        c_id = Main_category.objects.annotate(product_count=Count('product'))
        cart_id=Cart.objects.filter(user=user_name)
        cart_product_ids = Cart.objects.filter(user=user_name).values_list('product_id', flat=True)
        wishlist_id=Wishlist.objects.filter(user=user_name)
        wishlist_product_ids = Wishlist.objects.filter(user=user_name).values_list('product_id', flat=True)
        trandy_product=Product.objects.order_by('?')[:8]  #random 8 products
        random_just_arrived = Product.objects.order_by('-id').order_by('?')[:8] #latest 8 products randomly

        for category in c_id:
            random_product = Product.objects.filter(main_cat=category).order_by('?').first()
            category.random_product = random_product
    
        contaxt = {'c_id': c_id,'user_name':user_name,'cart_id':cart_id,
                   'trandy_product':trandy_product,'just_arrived_product':random_just_arrived,
                   'cart_product_ids': cart_product_ids,
                   'wishlist_id':wishlist_id,
                   'wishlist_product_ids': wishlist_product_ids
                   }
        return render(request, 'index.html', contaxt)
    else:
        return render(request,'login.html')

def cart(request):
    if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        c_id=Main_category.objects.all()
        product_id=request.GET.get('product_id')
        
        if not product_id:
            cart_id=Cart.objects.filter(user=user_name)
            total_amount=0
            for i in cart_id:
                total_amount=i.total_price + total_amount if 'total_amount' in locals() else i.total_price
            if total_amount >=999:
                shipping_amount=50
            else:
                shipping_amount=0
            final_total_amount=total_amount + shipping_amount
            contaxt={'c_id':c_id,
                     'user_name':user_name,
                     'cart_id':cart_id,
                     'wishlist_id':Wishlist.objects.filter(user=user_name),
                     'total_amount':total_amount,
                     'shipping_amount':shipping_amount,
                     'final_total_amount':final_total_amount
                     }
            return render(request,'cart.html',contaxt)
        else:
            selected_product=Product.objects.get(id=product_id) 
            cart_id=Cart.objects.filter(user=user_name)

            total_amount=0
            for i in cart_id:
                total_amount=i.total_price + total_amount if 'total_amount' in locals() else i.total_price
            if total_amount >=999:
                shipping_amount=50
            else:
                shipping_amount=0
            final_total_amount=total_amount + shipping_amount
            contaxt={'c_id':c_id,
                    'user_name':user_name,
                    'selected_product':selected_product,
                    'cart_id':cart_id,
                    'total_amount':total_amount,
                    'shipping_amount':shipping_amount,
                    'final_total_amount':final_total_amount
                    }
            return render(request,'cart.html',contaxt)
    else:
        return render(request,'login.html')

def wishlist(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        c_id=Main_category.objects.all()
        cart_id=Cart.objects.filter(user=user_name)
        wishlist_id=Wishlist.objects.filter(user=user_name)
        cart_product_ids = Cart.objects.filter(user=user_name).values_list('product_id', flat=True)
        
         # Pagination: 8 items per page (change page_size as needed)
        paginator = Paginator(wishlist_id, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

         # Preserve other query params (without page) for pagination links
        query_params = request.GET.copy()
        query_params.pop('page', None)
        query_string = query_params.urlencode()

        contaxt={'c_id':c_id,
                 'page_obj': page_obj,
                 'query_string': query_string,
                 'user_name':user_name,
                 'wishlist_id':wishlist_id,
                 'cart_id':cart_id,
                'cart_product_ids': cart_product_ids
                 }
        return render(request,'wishlist.html',contaxt)
     else:
        return render(request,'login.html')  

def checkout(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        c_id=Main_category.objects.all()
        cart_id=Cart.objects.filter(user=user_name)
        billing_addres_id=Billing_address.objects.filter(user=user_name).first()
        discount_id=Discount.objects.all()
        if billing_addres_id:
            first_name=billing_addres_id.first_name
            last_name=billing_addres_id.last_name
            email_id=billing_addres_id.email_id
            phone_no=billing_addres_id.phone_no
            address_l1=billing_addres_id.address_l1
            address_l2=billing_addres_id.address_l2
            country=billing_addres_id.country
            city=billing_addres_id.city
            state=billing_addres_id.state
            zip_code=billing_addres_id.zip_code
        else:
            first_name = last_name = email_id = phone_no = address_l1 = address_l2 = country = city = state = zip_code = ""

        # total_amount=0
        # for i in cart_id:
        #     total_amount=i.total_price + total_amount if 'total_amount' in locals() else i.total_price
        # if total_amount >=999:
        #     shipping_amount=50
        # else:
        #     shipping_amount=0

        total_amount=0
        for i in cart_id:
            total_amount=i.total_price + total_amount if 'total_amount' in locals() else i.total_price
        if total_amount >=999:
            shipping_amount=50
        else:
            shipping_amount=0
       
        
        discount_amount = 0
        how_discount=0
        for discount in discount_id:
            # Case 1: Below X (min is None)
            if discount.min_amount is None and discount.max_amount is not None:
                if total_amount <= discount.max_amount:
                    discount_amount = (total_amount * discount.discount_percentage) / 100
                    how_discount=discount.discount_percentage
                    break

            # Case 2: Above X (max is None)
            elif discount.max_amount is None and discount.min_amount is not None:
                if total_amount >= discount.min_amount:
                    discount_amount = (total_amount * discount.discount_percentage) / 100
                    how_discount=discount.discount_percentage
                    break

            # Case 3: Normal range
            elif discount.min_amount is not None and discount.max_amount is not None:
                if discount.min_amount <= total_amount <= discount.max_amount:
                    discount_amount = (total_amount * discount.discount_percentage) / 100
                    how_discount=discount.discount_percentage
                    break

        final_total_amount=(total_amount + shipping_amount)- discount_amount
       
        contaxt={'c_id':c_id,
                     'user_name':user_name,
                     'billing_addres_id':billing_addres_id,
                     'cart_id':cart_id,
                     'wishlist_id':Wishlist.objects.filter(user=user_name),
                     'total_amount':total_amount,
                     'shipping_amount':shipping_amount,
                     'discount_amount':discount_amount,
                     "how_discount":how_discount,
                     'final_total_amount':final_total_amount,
                     'first_name':first_name,'last_name':last_name,'email_id':email_id,'phone_no':phone_no,'address_l1':address_l1,
                      'address_l2':address_l2,'country':country,'city':city,'state':state,'zip_code':zip_code
                     }
        return render(request,'checkout.html',contaxt)
     else:
        return render(request,'login.html')

def contact(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        cart_id=Cart.objects.filter(user=user_name)
        c_id=Main_category.objects.all()
        contaxt={'c_id':c_id,'cart_id':cart_id,'user_name':user_name,'wishlist_id':Wishlist.objects.filter(user=user_name),}
        return render(request,'contact.html',contaxt)
     else:
        return render(request,'login.html')

def detail(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        user_email=request.session.get('email_id')
        product_id=request.GET.get('product_id')
        c_id=Main_category.objects.all()
        cart_id=Cart.objects.filter(user=user_name)
        cart_product_ids = Cart.objects.filter(user=user_name).values_list('product_id', flat=True)
        # Get a random product if no product_id is provided
        if not product_id:
            product = Product.objects.order_by(Random()).first()
            random_product_id = product.id
            selected_product = Product.objects.get(id=random_product_id)
        else:   
            selected_product = Product.objects.get(id=product_id)

       # Get user's previous rating
        try:
            rating_obj = Rating.objects.get(register_user=user_name, product=selected_product)
            user_rating = rating_obj.rating
            user_review = rating_obj.review  # optional: get review too
            
        except Rating.DoesNotExist:
            user_rating = 0
            user_review = ""

        contaxt={
                'c_id':c_id,
                 'selected_product':selected_product,
                 'cart_product_ids': cart_product_ids,
                 'cart_id':cart_id,
                 'wishlist_id':Wishlist.objects.filter(user=user_name),
                 'size_id': Size.objects.all(),
                'color_id': Color.objects.all(),
                 'user_name':user_name,
                 'user_email':user_email,
                 'user_rating':user_rating,
                 'user_review':user_review,
                 }
        
        return render(request,'detail.html',contaxt)
     else:
        return render(request,'login.html')

def find_price_range(request):
        price_range=Price_range.objects.order_by('-id')
        r_w_p=[]
        for product in price_range:
            if product.min_price is not None and product.max_price is not None and product.min_price != "" and product.max_price != "":
                range=Product.objects.filter(product_price__gte=product.min_price,product_price__lte=product.max_price).distinct()
                r_w_p.append(range.count())
   
        price_id=list(zip_longest(price_range,r_w_p,fillvalue=0))
        total_price_product=sum(r_w_p)
        return price_id,total_price_product,price_range


def shop(request):
     
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        c_id=Main_category.objects.all()
        color_id=Color.objects.annotate(product_count=Count('product'))
        size_id=Size.objects.annotate(product_count=Count('product'))
        total_color_product=Product.objects.filter(color__isnull=False).count()
        total_size_product=Product.objects.filter(size__isnull=False).count()
        cart_id=Cart.objects.filter(user=user_name)
        price_id,total_price_product,price_range=find_price_range(request)

        cart_product_ids = Cart.objects.filter(user=user_name).values_list('product_id', flat=True)
        wishlist_product_ids = Wishlist.objects.filter(user=user_name).values_list('product_id', flat=True) 
        sub=request.GET.get('s_id')
        cat=request.GET.get('cat_id')
        if sub:
            p_id=Product.objects.filter(sub_cat__id=sub)
        elif cat:
            p_id=Product.objects.filter(main_cat__id=cat)   
        else:   
            p_id=Product.objects.all()
        
         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

         # Preserve other query params (without page) for pagination links
        query_params = request.GET.copy()
        query_params.pop('page', None)
        query_string = query_params.urlencode()

        contaxt= {
        "p_id":p_id,
        "page_obj": page_obj,
        "cart_id":cart_id,
        'wishlist_id':Wishlist.objects.filter(user=user_name),
        "query_string": query_string,
        "c_id":c_id,
        "color_id":color_id,
        "size_id":size_id,
        "cart_product_ids": cart_product_ids,
        "wishlist_product_ids": wishlist_product_ids,
        "sub":sub ,  
        "total_color_product":total_color_product,
        "total_size_product":total_size_product,
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id
        }
        return render(request,'shop.html',contaxt)
     else:
        return render(request,'login.html')

def color_filter(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        # Prefer GET for filter vals (fall back to POST)
        selected_color = request.GET.getlist('color') or request.POST.getlist('color') or []
   
        if selected_color:
            p_id = Product.objects.filter(color__id__in=selected_color).distinct()
        else:
            p_id = Product.objects.order_by('-id')

        price_id,total_price_product,price_range=find_price_range(request)

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Preserve other query params (without page) for pagination links
        query_params = request.GET.copy()
        query_params.pop('page', None)
        query_string = query_params.urlencode()

       
        contaxt = {
        "p_id": p_id,
        "page_obj": page_obj,
        "query_string": query_string,
        "c_id": Main_category.objects.all(),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "cart_id":Cart.objects.filter(user=user_name),
        'wishlist_id':Wishlist.objects.filter(user=user_name),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id

        }
        return render(request, 'shop.html', contaxt)
     else:
        return render(request,'login.html')

def size_filter(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        # Prefer GET for filter vals (fall back to POST)
        selected_size = request.GET.getlist('size') or request.POST.getlist('size') or []
        if selected_size:
            p_id=Product.objects.filter(size__id__in=selected_size).distinct()
        else:
            p_id=Product.objects.order_by('-id')

        price_id,total_price_product,price_range=find_price_range(request)

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query_params = request.GET.copy()
        query_params.pop('page', None)
        query_string = query_params.urlencode()

        
        contaxt={
        "p_id":p_id,
        "page_obj": page_obj,
        "query_string": query_string,
        "c_id": Main_category.objects.all(),
         "cart_id":Cart.objects.filter(user=user_name),
         'wishlist_id':Wishlist.objects.filter(user=user_name),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id

        }
        return render(request,'shop.html',contaxt)
     else:
        return render(request,'login.html')



def price_filter(request):
    if 'email_id' in request.session or 'user_name' in request.session:

        user_name = Register.objects.get(email_id=request.session['email_id'])

        # POST ya GET se price ids
        selected_price = request.POST.getlist('price') or request.GET.getlist('price') or []

        min_price = []
        max_price = []

        # sirf tab loop chale jab price selected ho
        if selected_price:
            for price in selected_price:
                price_id = Price_range.objects.get(id=price)
                min_price.append(price_id.min_price)
                max_price.append(price_id.max_price)

            minimum_price = min(min_price)
            maximum_price = max(max_price)

            p_id = Product.objects.filter(
                product_price__gte=minimum_price,
                product_price__lte=maximum_price
            ).distinct()
        else:
            # ❗ Next page ya direct hit pe
            p_id = Product.objects.order_by('-id')

        # sidebar price data
        price_id, total_price_product, price_range = find_price_range(request)

        # Pagination
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query_params = request.GET.copy()
        query_params.pop('page', None)
        query_string = query_params.urlencode()


        context = {
            "p_id": p_id,
            "page_obj": page_obj,
            "query_string": query_string,
            "c_id": Main_category.objects.all(),
            "color_id": Color.objects.annotate(product_count=Count('product')),
            "size_id": Size.objects.annotate(product_count=Count('product')),
            "total_color_product": Product.objects.filter(color__isnull=False).count(),
            "total_size_product": Product.objects.filter(size__isnull=False).count(),
             "cart_id":Cart.objects.filter(user=user_name),
             'wishlist_id':Wishlist.objects.filter(user=user_name),
            "total_price_product": total_price_product,
            "price_range": price_range,
            "price_id": price_id,
        }

        return render(request, 'shop.html', context)

    else:
        return render(request, 'login.html')


def view_details(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        user_email=request.session.get('email_id')
        product = request.GET.get('product_id')
        selected_product = Product.objects.get(id=product)
        c_id = Main_category.objects.all()
        cart_product_ids = Cart.objects.filter(user=user_name).values_list('product_id', flat=True)
        
        # Get user's previous rating
        try:
            rating_obj = Rating.objects.get(register_user=user_name, product=product)
            user_rating = rating_obj.rating
            user_review = rating_obj.review  # optional: get review too
        except Rating.DoesNotExist:
            user_rating = 0
            user_review = ""

        contaxt = {
                'selected_product': selected_product,
                'c_id': c_id,
                'cart_product_ids': cart_product_ids,
                'size_id': Size.objects.all(),
                'color_id': Color.objects.all(),
                 "cart_id":Cart.objects.filter(user=user_name),
                 'wishlist_id':Wishlist.objects.filter(user=user_name),
                'user_email':user_email,
                'user_name':user_name,
                'user_rating':user_rating,
                'user_review':user_review

            }
        return render(request, 'detail.html', contaxt)
     else:
        return render(request,'login.html')
    
def search(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        search_data = request.POST.get('search', '').strip()  # Get search data from POST request
        if search_data:
            p_id=Product.objects.filter(product_name__icontains=search_data)
        else:
            p_id=Product.objects.order_by('-id')  
            
        price_id,total_price_product,price_range=find_price_range(request)

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        contaxt={
            "p_id": p_id,
            "page_obj": page_obj,
            "c_id": Main_category.objects.all(),
            "color_id": Color.objects.annotate(product_count=Count('product')),
            "size_id": Size.objects.annotate(product_count=Count('product')),
            "total_color_product":Product.objects.filter(color__isnull=False).count(),
            "total_size_product":Product.objects.filter(size__isnull=False).count(),
             "cart_id":Cart.objects.filter(user=user_name),
             'wishlist_id':Wishlist.objects.filter(user=user_name),
            "total_price_product":total_price_product,
            "price_range":price_range,
            "price_id":price_id
        }
        return render(request,'shop.html',contaxt)
     else:
        return render(request,'login.html')

def login(request):
    if request.method == "POST":
        email_id = request.POST.get('email_id', '').strip()
        password = request.POST.get('password', '')
        if not email_id or not password:
            return render(request, 'login.html', {'alert': 'Please enter both email and password.', "c_id": Main_category.objects.all()})
        user_qs = Register.objects.filter(email_id=email_id)
        if not user_qs.exists():
            return render(request, 'login.html', {'alert': 'Email not registered.', "c_id": Main_category.objects.all()})
        user = user_qs.first()
        if password == user.password:
            request.session['email_id'] = email_id
            request.session['user_name'] = user.full_name
            return redirect('index')
        return render(request, 'login.html', {'alert': 'Invalid Password.', "c_id": Main_category.objects.all()})
    return render(request, 'login.html', {"c_id": Main_category.objects.all()})

def register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        email_id = request.POST.get('email_id', '').strip()
        phone_no = request.POST.get('phone_no', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if not all([full_name, email_id, phone_no, password, confirm_password]):
            return render(request, 'register.html', {'alert': 'Please fill all fields.', "c_id": Main_category.objects.all()})
        if password != confirm_password:
            return render(request, 'register.html', {'alert': 'Passwords do not match.', "c_id": Main_category.objects.all()})
        Register.objects.create(full_name=full_name, email_id=email_id, phone_no=phone_no, password=password, confirm_password=confirm_password)
        request.session['email_id'] = email_id
        return redirect('login')
    return render(request, 'register.html', {"c_id": Main_category.objects.all()})

def logout_view(request):
    # remove only auth/session keys so messages framework keeps working normally
    request.session.pop('email_id', None)
    request.session.pop('user_name', None)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def latest_products(request):
    # Display products ordered by latest (assuming 'id' indicates order of addition)
    if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        price_id,total_price_product,price_range=find_price_range(request)
        p_id=Product.objects.order_by('-id')

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

       
        contaxt= {
        "p_id":p_id,
        "page_obj": page_obj,
        "c_id": Main_category.objects.all(),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
         "cart_id":Cart.objects.filter(user=user_name),
         'wishlist_id':Wishlist.objects.filter(user=user_name),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id
        }
        return render(request,'shop.html',contaxt)
    else:
        return render(request,'login.html')

def popular_products(request):
    if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        price_id,total_price_product,price_range=find_price_range(request)
        p_id=Product.objects.order_by('?')  # Random order simulates popularity for this example

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        contaxt= {
        "p_id":p_id,
        "page_obj": page_obj,
        "c_id": Main_category.objects.all(),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
         "cart_id":Cart.objects.filter(user=user_name),
         'wishlist_id':Wishlist.objects.filter(user=user_name),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id
        }
        return render(request,'shop.html',contaxt)
    else:
        return render(request,'login.html')


def best_rated_products(request):
    # Display products ordered by best average rating
    if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        price_id,total_price_product,price_range=find_price_range(request)
        rated_products = Rating.objects.values('product').annotate(avg_rating=Count('rating')).order_by('-avg_rating')
        product_ids = [item['product'] for item in rated_products]
        p_id = Product.objects.filter(id__in=product_ids)

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

       
        contaxt= {
        "p_id":p_id,
        "page_obj": page_obj,
        "c_id": Main_category.objects.all(),
        "color_id": Color.objects.annotate(product_count=Count('product')),
        "size_id": Size.objects.annotate(product_count=Count('product')),
        "total_color_product":Product.objects.filter(color__isnull=False).count(),
        "total_size_product":Product.objects.filter(size__isnull=False).count(),
         "cart_id":Cart.objects.filter(user=user_name),
         'wishlist_id':Wishlist.objects.filter(user=user_name),
        "total_price_product":total_price_product,
        "price_range":price_range,
        "price_id":price_id
        }
        return render(request,'shop.html',contaxt)
    else:
        return render(request,'login.html')



def save_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if not product_id:
            return HttpResponse("Product ID missing")
 
        try:
            selected_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponse("Product matching query does not exist")

        rating = request.POST.get('rating')
        review = request.POST.get('review')
        name = request.POST.get('name')
        email = request.POST.get('email')
        if not rating:
            messages.error(request, "Please give a rating before submitting.")
            return redirect(f'/view_details?product_id={product_id}')
        rating = float(rating)
        # Get the logged-in Register instance
        user_name=Register.objects.get(email_id=request.session['email_id'])
        # Update if exists, else create
        obj, created = Rating.objects.update_or_create(
            register_user=user_name,
            product=selected_product,
            name=name,
            email=email,
            defaults={"rating": rating, "review": review}
        )

        return redirect(f'/view_details?product_id={product_id}')
    return render(request,'index.html')



def add_to_cart(request):
    user_name=Register.objects.get(email_id=request.session['email_id'])
    product_id = request.GET.get('product_id')
    exists = Cart.objects.filter(user=user_name, product__id=product_id).exists()
    if exists:
        cart_item = Cart.objects.get(user=user_name, product__id=product_id)
        quantity = cart_item.quantity + int(request.POST.get('quantity', 1))
    else:
        quantity=request.POST.get('quantity',1)
    if not product_id:
        return HttpResponse("Product ID missing")   
    try:
        selected_product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product matching query does not exist")
    
    image=selected_product.product_img
    price=selected_product.product_price
    name=selected_product.product_name
    total_price=price*int(quantity)

    cart_obj,created = Cart.objects.update_or_create(
            product=selected_product,
            user=user_name,
            defaults={"quantity":quantity,
            "image":image,
            "price":price,
            "name":name,
            "total_price":total_price}
            
    )
    return redirect(f'/cart?product_id={product_id}')

<<<<<<< HEAD

=======
>>>>>>> 4fcbd9c43abcadc60927747b1225710ff25f71d8
def plus_cart(request):
    if request.method == 'POST':
        product_id = request.GET['product_id']
        selected_product = Product.objects.get(id=product_id)
        user_name=Register.objects.get(email_id=request.session['email_id'])
        cart_item = Cart.objects.get(product=selected_product, user=user_name)
    
        cart_item.quantity += 1     
        cart_item.total_price = cart_item.price * cart_item.quantity
        cart_item.save()
        
        return redirect('/cart')
       
    return render(request,'cart.html')

def minus_cart(request):
    if request.method == 'POST':
        product_id = request.GET['product_id']
        selected_product = Product.objects.get(id=product_id)
        user_name=Register.objects.get(email_id=request.session['email_id'])
       
        cart_item = Cart.objects.get(product=selected_product, user=user_name)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1     
            cart_item.total_price = cart_item.price * cart_item.quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return redirect('cart')
       
    return render(request,'cart.html')

def remove_cart(request):
    if request.method == 'POST':
        product_id = request.GET['product_id']
        selected_product = Product.objects.get(id=product_id)
        user_name=Register.objects.get(email_id=request.session['email_id'])
       
        cart_item = Cart.objects.get(product=selected_product, user=user_name)
        cart_item.delete()
        
        return redirect('cart')
       
    return render(request,'cart.html')
<<<<<<< HEAD
=======

def add_wishlist(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        product_id=request.GET.get('product_id')
       
        whishlist_exists = Wishlist.objects.filter(user=user_name, product__id=product_id).exists()
        
        if whishlist_exists:
            selected_product=Product.objects.get(id=product_id)
            wishlist_item = Wishlist.objects.get(user=user_name, product__id=product_id)
            wishlist_item.delete()
            print("removed from wishlist")
        else:
            selected_product=Product.objects.get(id=product_id)
            wishlist_obj=Wishlist.objects.create(
                product=selected_product,
                user=user_name,
            )
            print("added to wishlist")
        wishlist_id=Wishlist.objects.filter(user=user_name)
        print("wishlist items:",wishlist_id)
        contaxt={'whishlist_id':wishlist_id,
                 'user_name':user_name}
        return redirect('shop')
     else:
        return render(request,'login.html')

def remove_wishlist(request):
    if request.method == 'POST':
        product_id = request.GET['product_id']
        selected_product = Product.objects.get(id=product_id)
        user_name=Register.objects.get(email_id=request.session['email_id'])
       
        wishlist_item = Wishlist.objects.get(product=selected_product, user=user_name)
        wishlist_item.delete()
        
        return redirect('wishlist')
       
    return render(request,'wishlist.html')

def add_billing_address(request):
    if request.method == "POST":
        user_name=Register.objects.get(email_id=request.session['email_id'])
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email_id = request.POST.get('email_id', '').strip()
        phone_no = request.POST.get('phone_no', '').strip()
        address_l1 = request.POST.get('address_l1', '').strip()
        address_l2 = request.POST.get('address_l2', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()
        country = request.POST.get('country', '').strip()
        address_obj, created =Billing_address.objects.update_or_create(
            user=user_name,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email_id': email_id,
                'phone_no': phone_no,
                'address_l1': address_l1,
                'address_l2': address_l2,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'country': country
            }
           
        )
        return redirect('checkout')
    return render(request, 'checkout.html')

>>>>>>> 4fcbd9c43abcadc60927747b1225710ff25f71d8
