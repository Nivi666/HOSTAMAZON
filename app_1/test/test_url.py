from django.test import SimpleTestCase
from django.urls import reverse,resolve
from app_1.views import *
class Testingurl(SimpleTestCase):
    def test_url_register_page_resolves(self):
        register_url=reverse('register')
        self.assertAlmostEqual(resolve(register_url).func,register)
    def test_url_login_page_resolves(self):
        login_url=reverse('loginpage')
        self.assertAlmostEqual(resolve(login_url).func,loginpage)
    def test_url_logot_page_resolves(self):
        logout_url=reverse('logout')
        self.assertAlmostEqual(resolve(logout_url).func,logoutpage) 
    def test_url_home_page_resolves(self):
        home_url=reverse('home')
        self.assertAlmostEqual(resolve(home_url).func,home) 
    def test_url_product_page_resolves(self):
        productpage_url=reverse('productpage')
        self.assertAlmostEqual(resolve(productpage_url).func,productpage) 
    def test_url_store_cart_data_to_the_cart_model_resolves(self):
        addcart_url=reverse('add_cart')
        self.assertAlmostEqual(resolve(addcart_url).func,add_cart_product) 
    def test_url_display_cart_data_resolves(self):
        addtocart_url=reverse('cart')
        self.assertAlmostEqual(resolve(addtocart_url).func,addtocart) 
    def test_url_store_browsingh_data_to_the_browsing_model_resolves(self):
        store_browsing_url=reverse('browsing')
        self.assertAlmostEqual(resolve(store_browsing_url).func,store_browsing) 
    def test_url_redirect_browsing_data_to_the_product_page_resolves(self):
        browsing_redirect_url=reverse('browsing_redirect',args=[1])
        self.assertAlmostEqual(resolve(browsing_redirect_url).func,browsing_redirect) 
        
    def test_url_shows_today_deals_page_resolves(self):
        today_deals_url=reverse('today')
        self.assertAlmostEqual(resolve(today_deals_url).func,today_deals)

    def test_url_shows_fashion_page_resolves(self):
        fashion_url=reverse('fashion')
        self.assertAlmostEqual(resolve(fashion_url).func,fashion)
    
    def test_url_shows_browsing_page_resolves(self):
        browsing_history_url=reverse('browsing_history')
        self.assertAlmostEqual(resolve(browsing_history_url).func,browsing_history)
    
    def test_url_shows_electronics_page_resolves(self):
        electronics_url=reverse('electronics')
        self.assertAlmostEqual(resolve(electronics_url).func,electronics)
        
    def test_url_submit_product_review_resolves(self):
        submit_review_url=reverse('submit_review',args=[1,"mobile"])
        self.assertAlmostEqual(resolve(submit_review_url).func,submit_review)
    
    def test_url_redirect_buynow_page_from_productpage_resolves(self):
        buynow_url=reverse('buynow')
        self.assertAlmostEqual(resolve(buynow_url).func,buy_now)
    
    
    def test_url_redirect_buynow_page_from_Cart_page_resolves(self):
        buynow_cart_url=reverse('buynow_cart')
        self.assertAlmostEqual(resolve(buynow_cart_url).func,buy_now_cart)

    def test_url_store_order_from_order_page_resolves(self):
        store_order_url=reverse('store_order')
        self.assertAlmostEqual(resolve(store_order_url).func,store_order)
    
    def test_url_check_user_elgible_rating_resolves(self):
        check_rating_url=reverse('checkrating')
        self.assertAlmostEqual(resolve(check_rating_url).func,check_user_elgible_rating)

    def test_url_shows_order_success_page_resolves(self):
        order_success_url=reverse('thankyou')
        self.assertAlmostEqual(resolve(order_success_url).func,order_success)

    def test_delete_the_product_in_the_cart_resolves(self):
        cart_delete_url=reverse('cart_delete')
        self.assertAlmostEqual(resolve(cart_delete_url).func,cart_delete)

    def test_redirect_productpage_from_cart_page_resolves(self):
        cart_redirect_url=reverse('cart_redirect')
        self.assertAlmostEqual(resolve(cart_redirect_url).func,cart_redirect)
       
    def test_redirect_all_products_pages_resolves(self):
        search_page_url=reverse('search',args=["mobile"])
        self.assertAlmostEqual(resolve(search_page_url).func,search_page)

       
    def test_redirect_user_searchable_product_in_search_bar_resolves(self):
        search_product_page_url=reverse('search_product')
        self.assertAlmostEqual(resolve(search_product_page_url).func,search_product)

    def test_sort_price_high_all_products_pages_resolves(self):
        sort_products_high_price_url=reverse('sort_high')
        self.assertAlmostEqual(resolve(sort_products_high_price_url).func,sort_products_high_price)
    
    def test_sort_price_low_all_products_pages_resolves(self):
        sort_products_low_price_url=reverse('sort_low')
        self.assertAlmostEqual(resolve(sort_products_low_price_url).func,sort_products_low_price)
    