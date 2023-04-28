from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.register,name="register"),
    path('register/', views.register, name='register'),
    path('loginpage/',views.loginpage,name="loginpage"),
    path('logout/',views.logoutpage,name="logout"),
    path('home/',views.home,name="home"),
    
    path('productpage/',views.productpage,name="productpage"),
    
    path('add_cart_product/',views.add_cart_product,name="add_cart"),
    path('addtocart/',views.addtocart,name="cart"),
    path('browsing/',views.store_browsing,name="browsing"),
    path('browsing_redirect<int:pk>/',views.browsing_redirect,name="browsing_redirect"),
    path('today_deals/',views.today_deals,name="today"),
    path('Browsing_History/',views.browsing_history,name="browsing_history"),
    path('submit_review/<int:product_id>/<str:type>',views.submit_review,name="submit_review"),
    path('fashion/',views.fashion,name="fashion"),
    path('buynow/',views.buy_now_page_through_product,name="buynow"),
    path('buynow_cart/',views.buy_now_cart,name="buynow_cart"),
    path('checkrating/',views.check_user_elgible_rating,name="checkrating"),
   
    path('store_order/',views.store_order,name="store_order"),
    path('order_success/',views.order_success,name="thankyou"),
    
    path('electronics/',views.electronics,name="electronics"),
    path('cart_delete/',views.cart_delete,name="cart_delete"),
    path('cart_redirect/',views.cart_redirect,name="cart_redirect"),
    path('search_page<str:value>/',views.search_page,name="search"),
    path('search_product/',views.search_product,name="search_product"),
    
    path('sort_product_high/',views.sort_products_high_price,name="sort_high"),
    path('sort_product_low/',views.sort_products_low_price,name="sort_low"),
    ]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
