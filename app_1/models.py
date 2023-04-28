from django.db import models
from random import shuffle
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# Create your models here.
class usermodel(User,models.Model):
    mobile=models.CharField(max_length=10,null=True,blank=True)


class User_Register(models.Model):
    name=models.CharField(max_length=20)
    mobile=models.CharField(max_length=10)
    email=models.EmailField()
    password=models.CharField(max_length=20)


    def __str__(self) -> str:
        return self.user.username



class Search(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    type=models.CharField(max_length=20,default="product")
    head=models.CharField(max_length=1000,default="main head")
class Browsing(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    img=models.CharField(max_length=1000,default="image")
    type=models.CharField(max_length=100,default="product")
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
class Search_product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    type=models.CharField(max_length=20,default="product")
    head=models.CharField(max_length=1000,default="main head")
         
class Today_deals(models.Model):
    image=models.CharField(max_length=1000)
    discount=models.CharField(max_length=100)
    head=models.CharField(max_length=500)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
  
class Cart(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    image=models.CharField(max_length=800)
    head=models.CharField(max_length=400)
    size=models.CharField(max_length=100)
    quantity=models.IntegerField()
    size=models.CharField(max_length=100)
    int_price=models.IntegerField()
    str_price=models.CharField(max_length=200)

class Buynow(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.CharField(max_length=1000,blank=True)
    head=models.CharField(max_length=500)
    quantity=models.PositiveIntegerField()
    str_price=models.CharField(max_length=40)
    int_price=models.CharField(max_length=40)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    


class Mobile_depth(models.Model):
    brand=models.CharField(max_length=20)
    head=models.TextField(max_length=500,default="head")
    discount=models.CharField(max_length=20)
    orginal_price=models.CharField(max_length=10,default="1",null=False)
    discount_price=models.CharField(max_length=10,default="1")
    rating_img=models.ImageField(upload_to='pics',default="pics")
    day=models.CharField(max_length=10,default="10")
    date=models.IntegerField(default=1)
    users=models.CharField(max_length=40,default=1)
    int_discount_price=models.IntegerField(default="10")
    int_orginal_price=models.IntegerField(blank=True,null=True,default="10")
    advertise=models.BooleanField(default="False")    
    image=models.ImageField(upload_to='pics',default="image")
    url_image=models.CharField(max_length=900,default="image")
    model_name=models.CharField(max_length=20)
    retailer=models.CharField(max_length=100)
    size=models.CharField(max_length=10)
    screen_size=models.CharField(max_length=50,default="mobile")
    Camera_description=models.CharField(max_length=50,default="mobile")
    screen_type=models.CharField(max_length=50,default="mob")
    Battery=models.CharField(max_length=50,default="5000mah")
    Ram=models.CharField(max_length=400,default="4Gb")
    storage=models.CharField(max_length=50,default="2Gb")
    os=models.CharField(max_length=50,default="12")    
    browsing=GenericRelation(Browsing)
    search=GenericRelation(Search)
    deals=GenericRelation(Today_deals)
    search_product=GenericRelation(Search_product)
    buynow=GenericRelation(Buynow)
     
    type=models.CharField(max_length=20,default="mobile")
    @classmethod
    def all_datas(cls):
         return cls.objects.all()

class Laptop(models.Model):
     image=models.CharField(max_length=1000)
     head=models.CharField(max_length=200)
     discount_price=models.CharField(max_length=10)
     orginal_price=models.CharField(max_length=10)
     discount=models.CharField(max_length=10)
     int_discount_price=models.IntegerField()
     int_orginal_price=models.IntegerField()
     advertise=models.BooleanField(default="False")
     users=models.CharField(max_length=30)
     color=models.CharField(max_length=100)
     rating_img=models.ImageField(upload_to='pics',default="pics")
     
     screen_type=models.CharField(max_length=50,default="mob")
     processor=models.CharField(max_length=1000,default="5000mah")
     Ram=models.CharField(max_length=400,default="4Gb")
     storage=models.CharField(max_length=450,default="2Gb")
     os=models.CharField(max_length=150,default="12")    
     warranty=models.CharField(max_length=1000,default="warranty")
     brand=models.CharField(max_length=30,default="brand")
     browsing=GenericRelation(Browsing)
     search=GenericRelation(Search)
     deals=GenericRelation(Today_deals)
     search_product=GenericRelation(Search_product)    
     buynow=GenericRelation(Buynow)
     type=models.CharField(max_length=20,default="laptop")
     @classmethod
     def all_datas(cls):
         return cls.objects.all()

class headset(models.Model):
     image=models.CharField(max_length=1000)
     type=models.CharField(max_length=10,default="headset")
     head=models.CharField(max_length=200)
     discount_price=models.CharField(max_length=10)
     orginal_price=models.CharField(max_length=10)
     advertise=models.BooleanField(default="False")
     discount=models.CharField(max_length=10)
     rating_img=models.ImageField(upload_to='pics',default="pics")
     day=models.CharField(max_length=10,default="10")
     date=models.IntegerField(default=1)
    
     int_discount_price=models.IntegerField()
     int_orginal_price=models.IntegerField()
     users=models.CharField(max_length=30)
     color=models.CharField(max_length=100)
     brand=models.CharField(max_length=30,default="brand")
     deals=GenericRelation(Today_deals)
     browsing=GenericRelation(Browsing)
     search=GenericRelation(Search)
     buynow=GenericRelation(Buynow)
     search_product=GenericRelation(Search_product)    
    
     @ classmethod
     def all_datas(cls):
         return cls.objects.all()
              
class Tv(models.Model):
      image=models.CharField(max_length=400)
      head=models.CharField(max_length=200)
      discount_price=models.CharField(max_length=10)
      orginal_price=models.CharField(max_length=10)
      discount=models.CharField(max_length=10)
      advertise=models.BooleanField(default="False")
      rating_img=models.ImageField(upload_to='pics',default="pics")
      day=models.CharField(max_length=10,default="10")
      date=models.IntegerField(default=1)
      int_discount_price=models.IntegerField()
      int_orginal_price=models.IntegerField()
      users=models.CharField(max_length=30)
      warranty=models.CharField(max_length=500)
      screen=models.CharField(max_length=100) 
      os=models.CharField(max_length=100,null=True)
      brand=models.CharField(max_length=20,default="brand")
      browsing=GenericRelation(Browsing)
      search=GenericRelation(Search)
      deals=GenericRelation(Today_deals)
      type=models.CharField(max_length=20,default="tv")
      search_product=GenericRelation(Search_product)
      buynow=GenericRelation(Buynow)
          
      @classmethod
      def all_datas(cls):
         return cls.objects.all()
 
class Shirts(models.Model):
    image=models.CharField(max_length=200)
    head=models.CharField(max_length=200)
    discount_price=models.CharField(max_length=10)
    orginal_price=models.CharField(max_length=10)
    discount=models.CharField(max_length=10)
    advertise=models.BooleanField(default="False")
    rating_img=models.ImageField(upload_to='pics',default="pics")
    day=models.CharField(max_length=10,default="10")
    date=models.IntegerField(default=1)
    users=models.CharField(max_length=30,default="10")
    
    int_discount_price=models.IntegerField()
    int_orginal_price=models.IntegerField() 
    fashion_model=models.CharField(max_length=100) 
    browsing=GenericRelation(Browsing)
    deals=GenericRelation(Today_deals)
    search=GenericRelation(Search)
    type=models.CharField(max_length=20,default="shirts")
    search_product=GenericRelation(Search_product) 
    buynow=GenericRelation(Buynow)
         
    @classmethod
    def all_datas(cls):
         return cls.objects.all()
  
class Womens_clothes(models.Model):   
    image=models.CharField(max_length=200)
    head=models.CharField(max_length=200)
    discount_price=models.CharField(max_length=10)
    orginal_price=models.CharField(max_length=10)
    advertise=models.BooleanField(default="False")
    discount=models.CharField(max_length=10)
    day=models.CharField(max_length=10,default="10")
    date=models.IntegerField(default=1)
    rating_img=models.ImageField(upload_to='pics',default="pics")
    users=models.CharField(max_length=30,default="10")
        
    int_discount_price=models.IntegerField()
    int_orginal_price=models.IntegerField() 
    fashion_model=models.CharField(max_length=100) 
    browsing=GenericRelation(Browsing)
    search=GenericRelation(Search)
    deals=GenericRelation(Today_deals)
    type=models.CharField(max_length=20,default="womens_clothes")
    search_product=GenericRelation(Search_product)
    buynow=GenericRelation(Buynow)
          
class Rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.FloatField(default=0)
    review=models.TextField(max_length=500,blank=True)
    type=models.CharField(max_length=100)
    product_id=models.PositiveIntegerField()
