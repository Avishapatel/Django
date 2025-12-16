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
     
        for category in c_id:
            random_product = Product.objects.filter(main_cat=category).order_by('?').first()
            category.random_product = random_product
    
        contaxt = {'c_id': c_id,'user_name':user_name}
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
            contaxt={'c_id':c_id,
                     'user_name':user_name,
                     'cart_id':cart_id
                     }
            return render(request,'cart.html',contaxt)
        else:
            selected_product=Product.objects.get(id=product_id) 
            cart_id=Cart.objects.filter(user=user_name)
            contaxt={'c_id':c_id,
                    'user_name':user_name,
                    'selected_product':selected_product,
                    'cart_id':cart_id
                    }
            return render(request,'cart.html',contaxt)
    else:
        return render(request,'login.html')

    

def checkout(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        c_id=Main_category.objects.all()
        contaxt={'c_id':c_id}
        return render(request,'checkout.html',contaxt)
     else:
        return render(request,'login.html')

def contact(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        c_id=Main_category.objects.all()
        contaxt={'c_id':c_id}
        return render(request,'contact.html',contaxt)
     else:
        return render(request,'login.html')

def detail(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        user_email=request.session.get('email_id')
        product_id=request.GET.get('product_id')
        c_id=Main_category.objects.all()

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
        price_id,total_price_product,price_range=find_price_range(request)
   

        sub=request.GET.get('s_id')
        if sub:
            p_id=Product.objects.filter(sub_cat__id=sub)
            
        else:   
            p_id=Product.objects.order_by('-id')
        
         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

       
        contaxt= {
        "p_id":p_id,
        "page_obj": page_obj,
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
     else:
        return render(request,'login.html')

def color_filter(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        # Support POST (form) and fallback to GET, accept multiple values
        selected_color = request.POST.getlist('color') or request.GET.getlist('color') or []
   
        if selected_color:
            p_id = Product.objects.filter(color__id__in=selected_color).distinct()
        else:
            p_id = Product.objects.order_by('-id')

        price_id,total_price_product,price_range=find_price_range(request)

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

       
        contaxt = {
        "p_id": p_id,
        "page_obj": page_obj,
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
     else:
        return render(request,'login.html')

def size_filter(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        selected_size=request.GET.getlist('size') or request.POST.getlist('size') or []
        if selected_size:
            p_id=Product.objects.filter(size__id__in=selected_size).distinct()
        else:
            p_id=Product.objects.order_by('-id')

        price_id,total_price_product,price_range=find_price_range(request)

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        
        contaxt={
        "p_id":p_id,
        "page_obj": page_obj,
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
     else:
        return render(request,'login.html')

def price_filter(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
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
            p_id=Product.objects.order_by('-id')

        price_id,total_price_product,price_range=find_price_range(request)

         # Pagination: 9 items per page (change page_size as needed)
        paginator = Paginator(p_id, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

       
        contaxt={
        "p_id":p_id,
        "page_obj": page_obj,
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
     else:
        return render(request,'login.html')

def view_details(request):
     if 'email_id' in request.session or 'user_name' in request.session:
        user_name=Register.objects.get(email_id=request.session['email_id'])
        user_email=request.session.get('email_id')
        product = request.GET.get('product_id')
        selected_product = Product.objects.get(id=product)
        c_id = Main_category.objects.all()
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
                'size_id': Size.objects.all(),
                'color_id': Color.objects.all(),
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

# def cart_view(request):
#     if 'email_id' in request.session or 'user_name' in request.session:
#         user_name=Register.objects.get(email_id=request.session['email_id'])
#         c_id=Main_category.objects.all()
#         product_id=request.GET.get('product_id')
#         selected_product=Product.objects.get(id=product_id) 
#         cart_id=Cart.objects.filter(user=user_name)
#         contaxt={'c_id':c_id,
#                  'user_name':user_name,
#                  'selected_product':selected_product,
#                  'cart_id':cart_id
#                  }
#         return render(request,'cart.html',contaxt)
#     else:
#         return render(request,'login.html')

def add_to_cart(request):
    product_id = request.GET.get('product_id')
    quantity=request.POST.get('quantity',1)
    if not product_id:
        return HttpResponse("Product ID missing")   
    try:
        selected_product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product matching query does not exist")
    
    user_name=Register.objects.get(email_id=request.session['email_id'])
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
   
