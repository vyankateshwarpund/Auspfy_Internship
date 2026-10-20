import json
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from products.models import Category, Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics', description='Audio and Tech')
        self.product1 = Product.objects.create(
            category=self.category,
            name='Wireless Headphone',
            sku='ELEC-001',
            price=Decimal('100.00'),
            stock=10,
            is_active=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='USB-C Cable',
            sku='ELEC-002',
            price=Decimal('15.00'),
            stock=50,
            is_active=True
        )

    def test_get_product_list(self):
        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['count'], 2)

    def test_search_product(self):
        res = self.client.get('/api/products/?search=Headphone')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['sku'], 'ELEC-001')

    def test_price_filter(self):
        res = self.client.get('/api/products/?min_price=50')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['sku'], 'ELEC-001')

    def test_product_detail(self):
        res = self.client.get(f'/api/products/{self.product1.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], 'Wireless Headphone')


class UserAuthAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration_and_duplicate_check(self):
        payload = {
            'username': 'internship_user',
            'email': 'intern@auspify.com',
            'password': 'Password@123',
            'password_confirm': 'Password@123',
            'first_name': 'Auspify',
            'last_name': 'Intern'
        }
        res = self.client.post('/api/auth/register/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(User.objects.filter(username='internship_user').exists())

        # Attempt duplicate registration with same username
        res2 = self.client.post('/api/auth/register/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res2.status_code, 400)

    def test_user_login_and_logout(self):
        user = User.objects.create_user(username='testlog', email='log@test.com', password='Password@123')
        # Login
        res = self.client.post('/api/auth/login/', data=json.dumps({'username': 'testlog', 'password': 'Password@123'}), content_type='application/json')
        self.assertEqual(res.status_code, 200)

        # Profile check
        res_prof = self.client.get('/api/auth/profile/')
        self.assertEqual(res_prof.status_code, 200)

        # Logout
        res_logout = self.client.post('/api/auth/logout/')
        self.assertEqual(res_logout.status_code, 200)


class CartAndOrderFlowTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='shopper', email='shopper@auspify.com', password='Password@123')
        self.other_user = User.objects.create_user(username='other', email='other@auspify.com', password='Password@123')

        self.category = Category.objects.create(name='Gadgets')
        self.product = Product.objects.create(
            category=self.category,
            name='Smartwatch',
            sku='WATCH-01',
            price=Decimal('150.00'),
            stock=5,
            is_active=True
        )

    def test_cart_operations_and_stock_validation(self):
        self.client.force_login(self.user)

        # Add to cart within stock
        res = self.client.post('/api/cart/items/', data=json.dumps({'product_id': self.product.id, 'quantity': 3}), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        # Add exceeding remaining stock (5 - 3 = 2 left, trying to add 3 more)
        res_fail = self.client.post('/api/cart/items/', data=json.dumps({'product_id': self.product.id, 'quantity': 3}), content_type='application/json')
        self.assertEqual(res_fail.status_code, 400)

        # Get cart
        res_cart = self.client.get('/api/cart/')
        self.assertEqual(res_cart.status_code, 200)
        cart_data = res_cart.json()
        self.assertEqual(cart_data['total_items'], 3)
        self.assertEqual(float(cart_data['total_price']), 450.00)

        # Update quantity
        item_id = cart_data['items'][0]['id']
        res_update = self.client.patch(f'/api/cart/items/{item_id}/', data=json.dumps({'quantity': 2}), content_type='application/json')
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(res_update.json()['cart_item']['quantity'], 2)

    def test_order_creation_stock_deduction_and_isolation(self):
        self.client.force_login(self.user)

        # Put 2 watches into cart
        self.client.post('/api/cart/items/', data=json.dumps({'product_id': self.product.id, 'quantity': 2}), content_type='application/json')

        checkout_payload = {
            'full_name': 'Shopper Auspify',
            'email': 'shopper@auspify.com',
            'phone_number': '+91 9999988888',
            'shipping_address': 'Building 7, Tech Boulevard',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'postal_code': '560001',
            'payment_method': 'Cash on Delivery'
        }

        # Place Order
        res_order = self.client.post('/api/orders/', data=json.dumps(checkout_payload), content_type='application/json')
        self.assertEqual(res_order.status_code, 201)
        order_data = res_order.json()['order']
        order_id = order_data['id']

        # 1. Verify calculated total
        self.assertEqual(float(order_data['total_amount']), 300.00)

        # 2. Verify stock deduction: 5 - 2 = 3
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # 3. Verify cart is cleared
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

        # 4. Verify user isolation: another user cannot access this order
        other_client = Client()
        other_client.force_login(self.other_user)
        res_forbidden = other_client.get(f'/api/orders/{order_id}/')
        self.assertEqual(res_forbidden.status_code, 404)

        # 5. Verify the order owner can access it
        res_owner = self.client.get(f'/api/orders/{order_id}/')
        self.assertEqual(res_owner.status_code, 200)
