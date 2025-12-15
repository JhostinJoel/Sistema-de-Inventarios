from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.inventory.models import Category, Product, Warehouse

User = get_user_model()

class InventoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='password123', role='ADMIN')
        self.client = Client()
        self.client.force_login(self.user)
        
        self.category = Category.objects.create(name='Electronics', description='Gadgets')
        self.warehouse = Warehouse.objects.create(name='Main Warehouse', location='City Center')
        self.product = Product.objects.create(
            code='TEST001',
            name='Test Product',
            description='Description',
            price=100.00,
            cost=50.00,
            stock=10,
            category=self.category,
            min_stock=5
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('inventory:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_create(self):
        url = reverse('inventory:product_add')
        data = {
            'code': 'NEW001',
            'name': 'New Product',
            'description': 'New Description',
            'price': 200.00,
            'cost': 100.00,
            'stock': 20,
            'category': self.category.id,
            'min_stock': 5
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('inventory:product_list'))
        self.assertTrue(Product.objects.filter(code='NEW001').exists())

    def test_category_create(self):
        url = reverse('inventory:category_add')
        data = {'name': 'New Category', 'description': 'Desc'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('inventory:category_list'))
        self.assertTrue(Category.objects.filter(name='New Category').exists())

    def test_warehouse_create(self):
        url = reverse('inventory:warehouse_add')
        data = {'name': 'New Warehouse', 'location': 'Location'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('inventory:warehouse_list'))
        self.assertTrue(Warehouse.objects.filter(name='New Warehouse').exists())
