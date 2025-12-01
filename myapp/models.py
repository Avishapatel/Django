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
    
# class Sub_sub_category(models.Model):
#     sb_sbcat_name=models.CharField(max_length=100)
#     main_cat=models.ForeignKey(Main_category,on_delete=models.CASCADE,null=True,related_name='sub_subcategories',blank=True)
#     def __str__(self):
#         return self.sb_sbcat_name
    
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
    
