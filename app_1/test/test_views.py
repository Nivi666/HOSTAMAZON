from django.test import TestCase,Client
from django.urls import reverse,resolve
from app_1.views import *
from app_1.models import *
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class CartDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.cart_item = Cart.objects.create(
            user=self.user,
            image='test_image.jpg',
            head='Test Item',
            size='M',
            quantity=2,
            int_price=100,
            str_price='100.00'
        )
        self.url = reverse('cart_delete')

    def test_cart_item_deletion(self):
        response = self.client.get(self.url, {'id': self.cart_item.id})
        self.assertEqual(response.status_code, 302) # expect redirect
        self.assertFalse(Cart.objects.filter(id=self.cart_item.id).exists()) # expect item to be deleted







#
#
#
#
#from django.test import TestCase, Client
#from django.urls import reverse
#from app_1.models import Search, Cart, Buynow
#from django.test import TestCase, Client
#from django.urls import reverse
#from app_1.models import Search, Cart, Buynow
#
#class TestViews(TestCase):
#    
#    def setUp(self):
#        self.client = Client()
#        self.url = reverse('buynow')
#        # create any necessary objects for the test case
#        
#    def test_buy_now(self):
#        # simulate a GET request with query parameters
#        response = self.client.get(self.url + '?type=mobile&id=27')
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'app_1/buynowpage.html')
#        # assert any other expected behavior
#        
#    def test_store_order(self):
#        # simulate a GET request with query parameters
#        response = self.client.get(self.url + '?type=cart&id=27')
#        self.assertEqual(response.status_code, 302)  # expect a redirect
#        # assert any other expected behavior
#        
#    def test_check_user_elgible_rating(self):
#        # simulate a GET request with query parameters
#        response = self.client.get(reverse('checkrating') + '?id=1&type=mobile')
#        self.assertEqual(response.status_code, 302)  # expect a redirect
#        # assert any other expected behavior
#        
#    def test_order_success(self):
#        response = self.client.get(reverse('thankyou'))
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'app_1/thankyou.html')
#        # assert any other expected behavior
#        
#    def test_buy_now_cart(self):
#        response = self.client.get(reverse('buynow_cart'))
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'app_1/buynowpage.html')
#        # assert any other expected behavior
#        
#    def test_search_page(self):
#        response = self.client.get(reverse('search', args=['mobile']))
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'app_1/mobile.html')
#        # assert any other expected behavior
#        
#    def test_productpage(self):
#        response = self.client.get(reverse('productpage') + '?head=xyz&id=1')
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'app_1/productpage.html')
#        # assert any other expected behavior
#        
#    def test_store_browsing(self):
#        # simulate a session with obj set
#        session = self.client.session
#        session['obj'] = '{"model": "app_1.mobile", "pk": 1, "fields": {"type": "mobile", "brand": "Samsung", "model_name": "Galaxy S21", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "price": "999.99", "discount_price": "899.99", "image": "/media/mobiles/SamsungGalaxyS21.png", "url_image": "/media/mobiles/SamsungGalaxyS21.png", "image_1": "/media/mobiles/SamsungGalaxyS21_1.png", "url_image_1": "/media/mobiles/SamsungGalaxyS21_1.png", "image_2": "/media/mobiles/SamsungGalaxyS21_2.png", "url_image_2": "/media/mobiles/SamsungGalaxyS21_2.png", "users": 10}}'
#        session.save()
#        response = self.client.get(reverse('browsing'))
#        self.assertEqual(response.status_code, 200)
#        # assert any other expected behavior
#



















from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.user_data = {
            'name': 'testuser',
            'mobile': '1234567890',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # redirect to home page
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

    def test_register_existing_user(self):
        user = usermodel.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', mobile='1234567890')
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)  # stay on register page
        self.assertContains(response, 'The User is Already Exist with that username')
        self.assertFalse(get_user_model().objects.filter(email='testuser@example.com', password='testpassword').exists())



from django.test import Client, TestCase
from django.urls import reverse
from app_1.models import Browsing, Search, Cart
from django.contrib.auth.models import User

class ProductPageTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass')
        self.browsing = Browsing.objects.create(user=self.user, type='shirts',object_id=1,content_type_id=1)
        self.search = Search_product.objects.create(user=self.user,head='test', object_id=1,content_type_id=1)
        self.cart = Cart.objects.create(user=self.user)

    def test_productpage_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('productpage')
        response = self.client.get(url, {'head': 'test', 'id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_1/productpage.html')
        self.assertContains(response, 'Test Mobile') #replace with expected mobile name
        self.assertEqual(response.context['counts'], 1)
