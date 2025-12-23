from django.db import models

# Create your models here.
class Main_category(models.Model):
    cat_name=models.CharField(max_length=100)
    def __str__(self):
        return self.cat_name
    
class Sub_category(models.Model):
    main_cat=models.ForeignKey(Main_category,on_delete=models.CASCADE,null=True,blank=True)
    sbcat_name=models.CharField(max_length=100)
    def __str__(self):
        return self.sbcat_name
    

    
class Color(models.Model):
    color_name=models.CharField(max_length=100)
    def __str__(self):
        return self.color_name
    
class Size(models.Model):
    size_name=models.CharField(max_length=100)
    def __str__(self):
        return self.size_name
    
class Price_range(models.Model):
    min_price=models.IntegerField()
    max_price=models.IntegerField()
    def __str__(self):
        return self.min_price.__str__() + " Rs. - " + self.max_price.__str__() + " Rs."
   
class Product(models.Model):
    product_name=models.CharField(max_length=200)
    product_price=models.IntegerField()
    product_img=models.ImageField(upload_to='static/image/')
    main_cat=models.ForeignKey(Main_category,on_delete=models.CASCADE,null=True,blank=True)
    sub_cat=models.ForeignKey(Sub_category,on_delete=models.CASCADE,null=True,blank=True)
    color=models.ForeignKey(Color,on_delete=models.CASCADE,null=True,blank=True)
    size=models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
   # sub_sub_cat=models.ForeignKey(Sub_sub_category,on_delete=models.CASCADE,null=True,blank=True,related_name='productdetails')
    def __str__(self):
        return self.product_name
    
class Register(models.Model):
    full_name=models.CharField(max_length=100)
    email_id=models.EmailField()
    phone_no=models.CharField(max_length=10)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    def __str__(self):
        return self.full_name
    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    register_user = models.ForeignKey(Register, on_delete=models.CASCADE, blank=True, null=True)  # Use 'user' instead of 'user_id'
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=False)

    # rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=False)  # rating should not be blank or null
    review = models.TextField(blank=True, null=True)  # Allow comment to be optional
    name = models.CharField(max_length=50, blank=True, null=True)  # If you want it optional
    email = models.EmailField(max_length=50, blank=True, null=True)  # Optional if using user model for authentication
    date = models.DateTimeField(auto_now_add=True)  # auto_now_add to avoid updating it on every save

    def __str__(self):                             
        return f"Rating by {self.name or 'Anonymous'} for {self.product.product_name}"
    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField(default=1)
    image=models.ImageField(upload_to='static/image/',null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    total_price=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.product.product_name + " - " + self.user.full_name

class Wishlist(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    added_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.product_name + " - " + self.user.full_name

class Billing_address(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email_id=models.EmailField()
    phone_no=models.IntegerField(max_length=10)
    address_l1=models.TextField()
    address_l2=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zip_code=models.IntegerField(max_length=10)
    bill_amount=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.first_name + " " + self.last_name

class Discount(models.Model):
    min_amount=models.IntegerField(null=True,blank=True)
    max_amount=models.IntegerField(null=True,blank=True)
    discount_percentage=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.min_amount.__str__() + " Rs. - " + self.max_amount.__str__() + " Rs. : " + self.discount_percentage.__str__() + " %"

class Order(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    billing_address=models.ForeignKey(Billing_address,on_delete=models.CASCADE,null=True,blank=True)
    order_date=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(max_length=100,default='Pending')
    payment_mode=models.CharField(max_length=100,default='COD')
    payment_status=models.CharField(max_length=100,default='Pending')
    def __str__(self):
        return self.user.full_name + " - " + self.order_status 
