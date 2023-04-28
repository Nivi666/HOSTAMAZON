from django.shortcuts import render
from itertools import zip_longest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from urllib.parse import urlencode
from django.db.models import Q
from django.apps import apps
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import ReviewForm
from django.core import serializers

from django.views.decorators.csrf import csrf_exempt


# this view Store Cart product in Cart Model
@csrf_exempt
def add_cart_product(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
  
    user_id = request.user.id
 
    if (
        request.method == "POST"
        and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    ):
        img1 = request.POST.get("mobile_image")

        head1 = request.POST.get("mobile_head")
        price1 = request.POST.get("mobile_price")
        size1 = request.POST.get("mobile_size")
        total1 = request.POST.get("total")
        int_price1 = price1.replace(",", "")

        if Cart.objects.filter(user_id=user_id, head=head1).exists():
            for cart in Cart.objects.filter(user_id=user_id):
                if cart.head == head1:
                    obj = Cart.objects.get(id=cart.id)
                 
                    if total1:
                        obj.quantity += int(total1)
                        obj.int_price = obj.quantity * int(int_price1)

                    else:
                        obj.quantity += 1
                        obj.int_price = obj.int_price + int(int_price1)
                    obj.save()

                    break
        else:
            int_price1 = int(int_price1) * int(total1)
            str_price = "{:,}".format(int_price1)
            cart = Cart(
                user=user,
                image=img1,
                head=head1,
                int_price=int_price1,
                str_price=str_price,
                quantity=total1,
                size=size1,
            )
            cart.save()
        prices = Cart.objects.filter(user=user).values("int_price")
        items = Cart.objects.filter(user=user).values("quantity")
        total_items = 0
        for item in items:
            total_items = total_items + item["quantity"]
        total_amount = 0
        for i in prices:
            total_amount = total_amount + i["int_price"]
        number = "{:,}".format(total_amount)
        return JsonResponse(
            {
                "status": "Cart added successfully",
                "total_items": total_items,
                "total_price": number,
            }
        )
    else:
        return JsonResponse({"error": "invalid"})


# this view make register user


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if mobile.isdigit():
            if len(mobile) == 10:
                if len(password) > 6:
                    for user in usermodel.objects.all():
                        if user.username == username:
                            msg = "The User is Already Exist with that username"
                            return render(
                                request, "app_1/signout_and_signin/register.html", {"Error": msg}
                            )
                        elif user.email == email:
                            msg = "The User is Already Exist with that Email"
                            return render(
                                request, "app_1/signout_and_signin/register.html", {"Error": msg}
                            )
                        elif user.mobile == mobile:
                            msg = "The User Already Exist with that Mobile Number"
                            return render(
                                request, "app_1/signout_and_signin/register.html", {"Error": msg}
                            )
                    else:
                        user = usermodel.objects.create_user(
                            username=username,
                            email=email,
                            password=password,
                            mobile=mobile,
                        )
                        user.save()
                        user = authenticate(
                            request, username=username, password=password
                        )
                        login(request, user=user)
                        return redirect("home")
                else:
                    msg = "Please Enter Password above 6 Characters"
                    return render(request, "app_1/signout_and_signin/register.html", {"Error": msg})
            else:
                msg = "Please Enter 10 numbers in Mobile Field"
                return render(request, "app_1/signout_and_signin/register.html", {"Error": msg})
        else:
            msg = "Please Enter Number only in Mobile Field"
            return render(request, "app_1/signout_and_signin/register.html", {"Error": msg})

    return render(request, "app_1/signout_and_signin/register.html")


# this view make register user
def loginpage(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            return redirect("home")
        else:
            msg = "Please Enter correct Username and Passoword"
            return render(request, "app_1/signout_and_signin/loginpage.html", {"Error": msg})
    return render(request, "app_1/signout_and_signin/loginpage.html")


# this view make logout
def logoutpage(request):
    
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
  
    if request.user.is_authenticated:
        logout(request)

    return redirect("loginpage")


# This views gets the User search Value and redirect to the search_page
def search_product(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
  
    
    search = request.GET.get("q")
    search = search.lower().strip()

    if search == "mobile" or search == "mobiles":
        return redirect("search", "mobile")
    elif search == "headset" or search == "headsets":
        return redirect("search", value="headset")
    elif search == "shirts" or search == "shirt":
        return redirect("search", value="shirts")
    elif search == "tv" or search == "tvs":
        return redirect("search", value="tv")
    elif (
        search == "womens dress"
        or search == "womenscloth"
        or search == "womensdresses"
        or search == "womensclothes"
    ):
        return redirect("search", value="womens_clothes")
    elif search == "laptop" or search == "laptops":
        return redirect("search", value="laptop")
    elif search == "fashion":
        return redirect("fashion")
    elif search == "electronics":
        return redirect("electronics")
    elif search == "todaydeals" or search == "todaydeal":
        return redirect("today")

    else:
        results = Search.objects.filter(head__icontains=search)
        all_ids = []
        for i in results:
            all_ids.append(i.object_id)
        context = {
            "objects": results,
            "type": "mixed",
            "all_id": all_ids,
            "counts": Cart.objects.filter(user=user).all(),
        }

        return render(request, "app_1/main/filter.html", context)


# this View make Home logic
def home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    

    browsing_object1 = None
    browsing_object2 = None
    browsing_object3 = None
    browsing_object4 = None
    datas = Search.objects.exclude(
        Q(type__in=["womens_clothes", "shirts", "mobile"])
    ).order_by("?")[:15]

    fashion = Search.objects.filter(
        Q(type="shirts") | Q(type="womens_clothes")
    ).order_by("?")[:15]
    womens = Womens_clothes.objects.all()[:15]
    img_groups = (list(zip_longest(*[iter(datas)] * 5, fillvalue=None)),)
    dresses = (list(zip_longest(*[iter(fashion)] * 5, fillvalue=None)),)
    womens_cloth = (list(zip_longest(*[iter(womens)] * 5, fillvalue=None)),)
  
    # today deals
    img1 = img_groups[0][0]
    img2 = img_groups[0][1]
    img3 = img_groups[0][2]

    ###fashion
    images1 = dresses[0][0]
    images2 = dresses[0][1]
    images3 = dresses[0][2]
    # womens clothes
    images4 = womens_cloth[0][0]
    images5 = womens_cloth[0][1]
    images6 = womens_cloth[0][2]
    datas = Browsing.objects.filter(user=user).order_by("-id").all()
    values = (
        Laptop.objects.order_by("?")
        .all()
        .exclude(type__in=["shirts", "womens_clothes"])
    )
  
    user = request.user
    # browsing history
    browsing = Browsing.objects.filter(user=user).order_by("-id")[:12]
    # Ad
    ad1 = Mobile_depth.objects.all().order_by("?")[:1]
    ad = ad1[0]

    # mobile
    counts = Cart.objects.filter(user=user).count()

    # frequently purchased products
    max_mobiles = Mobile_depth.objects.filter(users__gt=5000)[:8]
    max_laptop = Laptop.objects.filter(users__gt=3000)[:5]
    max_tv = Tv.objects.filter(users__gt=5000)[:3]
    try:
        browsing_object1 = datas[0]
        
        browsing_object2 = datas[1]
        browsing_object3 = datas[2]
        browsing_object4 = datas[3]
    except IndexError:
       pass
    
    context = {
        "image_group1": img1,
        "image_group2": img2,
        "image_group3": img3,
        "image_group4": images1,
        "image_group5": images2,
        "image_group6": images3,
        "image_group7": images4,
        "image_group8": images5,
        "image_group9": images6,
        "browsing_object1": browsing_object1,
        "browsing_object2": browsing_object2,
        "browsing_object3": browsing_object3,
        "browsing_object4": browsing_object4,
        "value1": values[0],
        "value2": values[1],
        "value3": values[2],
        "Mobiles": max_mobiles,
        "Laptops": max_laptop,
        "Tv": max_tv,
        "browsing": browsing,
        "ad": ad,
        "counts": counts,
    }
    return render(request, "app_1/home/home.html", context)

# this view store user submited review and rating on the database
def submit_review(request, product_id, type):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    url = request.META.get("HTTP_REFERER")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        try:
            old_review = Rating.objects.get(
                user__id=request.user.id, product_id=product_id
            )
            form = ReviewForm(request.POST, instance=old_review)
            form.save()
            return redirect(url)
        except Rating.DoesNotExist:
            if form.is_valid():
                model = Rating()
                model.rating = form.cleaned_data["rating"]
                model.review = form.cleaned_data["review"]
                model.product_id = product_id
                model.type = type
                model.user = request.user
                model.save()

                return redirect(url)

#this view redirect buynow page through product page
def buy_now_page_through_product(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    obj_type = request.GET.get("type")
    obj_id = request.GET.get("id")
    object = Search.objects.get(type=obj_type, object_id=obj_id)
    context = {"object": object}
    return render(request, "app_1/buynow/buynowpage.html", context)

# this view store user oreder to the database
def store_order(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    url = request.META.get("HTTP_REFERER")

    type = request.GET.get("type")
    id = request.GET.get("id")
   
    if type == "cart":
        all_products = Cart.objects.filter(user=request.user).all()
        new_obj = []
        for i in all_products:
            old_obj = Search.objects.filter(head=i.head)[0]
            new_obj.append(old_obj)
        for i, j in zip(new_obj, all_products):
            product = Buynow.objects.create(
                user=request.user,
                head=j.head,
                image=j.image,
                str_price=j.str_price,
                int_price=j.str_price.replace(",", ""),
                quantity=1,
                content_object=i.content_object,
            )
          
            return render(request, "app_1/buynow/thankyou.html", {"product": product})

    else:
        datas = Search.objects.get(type=type, object_id=id)
        model_class = datas.content_type.model_class()
        obj = model_class.objects.get(id=id)
        product = Buynow.objects.create(
            user=request.user,
            head=obj.head,
            image=obj.image,
            str_price=obj.discount_price,
            int_price=obj.discount_price.replace(",", ""),
            quantity=1,
            content_object=obj,
        )
      
        return render(request, "app_1/buynow/thankyou.html", {"product": product})

#this view check user eligible for rating
def check_user_elgible_rating(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage") 
    url = request.META.get("HTTP_REFERER")
    id = request.GET.get("id")
    product_type = request.GET.get("type")

    all_data = Buynow.objects.all()
    eligible=None
    for i in all_data:
        if i.user.id == request.user.id and i.object_id == int(id) and i.content_object.type == product_type:
            eligible=True
            break
    if eligible:
        msg = "yess"
    else:
        msg="noo"    
    return JsonResponse({"msg": msg})

#this page confirm user order
def order_success(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    return render(request, "app_1/buynow/thankyou.html")

#this view redirect buynow page through cart
def buy_now_cart(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    cart = Cart.objects.filter(user=request.user).all()
    total = 0
    t_quantity = 0
    type = "cart"
    for i in cart:
        total += int(i.int_price)
        t_quantity += int(i.quantity)
    price = "{:,}".format(total)
    context = {"type": type, "cart": cart, "t_price": price, "qty": t_quantity}
    return render(request, "app_1/buynow/buynowpage.html", context)


# This view redirect to the all products page
def search_page(request, value):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    
    user = request.user
    obj = Search.objects.filter(type=value)[0]
    model_class = obj.content_type.model_class()
    all_datas = model_class.objects.all()
    page_datas=all_datas.order_by('head')
    if all_datas[0].type=="mobile":
        page_datas=all_datas.order_by('discount')
    if value == "womens_clothes":
        pages = Paginator(page_datas, 21)
        page = request.GET.get("page")
        objects = pages.get_page(page)
    else:
        pages = Paginator(page_datas, 10)
        page = request.GET.get("page")
        objects = pages.get_page(page)
    request.session["model"] = all_datas[0].type
    context = {
        "objects": objects,
        "type": all_datas[0].type,
        "counts": Cart.objects.filter(user=user).count(),
    }
    return render(request, "app_1/main/productspage.html", context)


# this view

# this view creates all the product page logic


def productpage(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage") 
    user = request.user
    datas = Browsing.objects.all().filter(user=user).order_by("-id")[:12]
    head = request.GET.get("head")
    id = request.GET.get("id")
    print(id,head)
    data =  Search.objects.get(Q(head=head) & Q(object_id=id))
    product_object = data.content_object
    model_class = data.content_type.model_class()
    obj = serializers.serialize("json", [product_object])
    request.session["obj"] = obj
    store_browsing(request)
    if product_object.type == "shirts" or product_object.type == "womens_clothes":
        brands = model_class.objects.exclude(id=product_object.id).filter(
            fashion_model=product_object.fashion_model
        )[:3]
    else:
        brands = model_class.objects.exclude(id=product_object.id).filter(brand=product_object.brand)[:3]
    types = []
    # most users products
    most_users = model_class.objects.order_by("-users")[:5]
    for i in datas:
        type = i.content_object.type
        types.append(type)
    context = {
        "mobile": product_object,
        "brands": brands,
        "browsing": datas,
        "types": type,
        "title":product_object.head,
        "most_bought_products": most_users,
        "counts": Cart.objects.filter(user=user).count(),
    }
    return render(request, "app_1/main/productpage.html", context)


# this view  store browsing data
def store_browsing(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    user = request.user
    browsing = Browsing.objects.all()
    obj = request.session.get("obj")
  
    count = 0
    id = None
    new_data = None
    if obj:
        object = serializers.deserialize("json", obj)
        data = next(object).object
        for i in browsing:
            if i.content_object.image == data.image:
                count += 1
                id = i.id
                new_data = data
        if count == 0:
            if data.type == "mobile":
                Browsing.objects.create(
                    user=user, img=data.url_image, content_object=data, type=data.type
                )
            else:
                Browsing.objects.create(
                    user=user, img=data.image, content_object=data, type=data.type
                )
        else:
            if data.type == "mobile":
                Browsing.objects.get(id=id).delete()
                Browsing.objects.create(
                    user=user,
                    img=new_data.url_image,
                    content_object=new_data,
                    type=new_data.type,
                )
            else:
                Browsing.objects.get(id=id).delete()
                Browsing.objects.create(
                    user=user,
                    img=new_data.image,
                    content_object=new_data,
                    type=new_data.type,
                )

    return HttpResponse()


# this view redirect from cart product to product page


def cart_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage") 
    cart_head = request.GET.get("cart_head")
    user = request.user
    allcard = Search.objects.all()
    data = allcard[1].content_object.head
    for i in allcard:
        obj = i.content_type.model_class()
        if i.content_object.head == cart_head:
            datas = {"head": i.content_object.head, "id": i.object_id}
            url = reverse("productpage") + "?" + urlencode(datas)
            return redirect(url)
    return HttpResponse()


# this view redirect browsing product to product page


def browsing_redirect(request, pk):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    data = Browsing.objects.get(id=pk)

    datas = {"head": data.content_object.head, "id": data.object_id}
    url = reverse("productpage") + "?" + urlencode(datas)
    return redirect(url)


def addtocart(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage")
    user = request.user
    cart = Cart.objects.all().filter(user=user)
    amount = 0
    items = 0
    for i in cart:
        amount = amount + i.int_price
        items = items + i.quantity
    amount = "{:,}".format(amount)
    context = {
        "carts": cart,
        "total_amount": amount,
        "total_items": items,
        "counts": Cart.objects.filter(user=user).count(),
    }
    return render(request, "app_1/cart/addtocart.html", context)


# this view creates today deal page
def today_deals(request):
    user = request.user
     
    if not user.is_authenticated:
        return redirect("loginpage")
    datas = Search.objects.exclude(
        Q(type="womens_clothes") | Q(type="Shirts")
    ).order_by("?")[:24]
    Type = "today_deals"
    context = {
        "objects": datas,
        "Type": Type,
        "counts": Cart.objects.filter(user=user).count(),
    }
    return render(request, "app_1/main/todaydeals.html", context)


# this view creates Browsing History page
def browsing_history(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage") 
    datas = Browsing.objects.filter(user=user).all().order_by("-id")
    Type = "browsing_history"
    context = {
        "counts": Cart.objects.filter(user=user).count(),
        "objects": datas,
        "Type": Type,
    }
    return render(request, "app_1/main/todaydeals.html", context)


# this view creates fashion page
def fashion(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("loginpage") 
    datas = Search.objects.filter(Q(type="shirts") | Q(type="womens_clothes")).order_by('head')
    pages = Paginator(datas, 50)
    page = request.GET.get("page")
    objects = pages.get_page(page)

    Type = "fashion"
    context = {
        "objects": objects,
        "Type": Type,
        "counts": Cart.objects.filter(user=user).count(),
    }
    return render(request, "app_1/main/todaydeals.html", context)


# this view creates electronics page


def electronics(request):
    user = request.user
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage") 
    datas = Search.objects.filter(
        Q(type="laptop") | Q(type="tv") | Q(type="mobile")
    ).order_by("?")
    pages = Paginator(datas, 21)
    page = request.GET.get("page")
    objects = pages.get_page(page)

    Type = "electronics"
    context = {
        "objects": objects,
        "Type": Type,
        "counts": Cart.objects.filter(user=user).count(),
    }
    return render(request, "app_1/main/todaydeals.html", context)


# this view sort the product in products page
def sort_products_high_price(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("loginpage") 
    class_name = request.session.get("model")
    model_class = Search.objects.filter(type=class_name)[0]
    o_class = model_class.content_type.model_class()
    all_datas = o_class.objects.all().order_by("-int_discount_price")
    if model_class.type == "womens_clothes" or model_class.type=="shirts":
       pages = Paginator(all_datas,15)
       page = request.GET.get("page")
       objects = pages.get_page(page)
    else:
        pages = Paginator(all_datas,5)
        page = request.GET.get("page")
        objects = pages.get_page(page)
    
    context = {"objects": objects, "counts": Cart.objects.filter(user=user).count()}

    return render(request, "app_1/main/productspage.html", context)


# this view sort the products low price in products page
def sort_products_low_price(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage") 
    class_name = request.session.get("model")
    model_class = Search.objects.filter(type=class_name)[0]
    o_class = model_class.content_type.model_class()
    all_datas = o_class.objects.all().order_by("int_discount_price")
    if model_class.type == "womens_clothes" or model_class.type=="shirts":
     pages = Paginator(all_datas,15)
     page = request.GET.get("page")
     objects = pages.get_page(page)
    else:
     pages = Paginator(all_datas,5)
     page = request.GET.get("page")
     objects = pages.get_page(page)
    
    return render(
        request,
        "app_1/main/productspage.html",
        {
            "objects": objects,
        },
    )


# this view delete cart product


def cart_delete(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("loginpage") 
    cart_id = request.GET.get("id")
  
    Cart.objects.get(id=cart_id).delete()
    return redirect("cart")
