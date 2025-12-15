from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.inventory.models import Product, Category
from apps.sales.models import Client as ClientModel

User = get_user_model()

class CRUDEvidenceTests(TestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_user(username='admin', password='password', role='ADMIN')
        self.seller = User.objects.create_user(username='seller', password='password', role='SELLER')
        self.warehouse = User.objects.create_user(username='warehouse', password='password', role='WAREHOUSE')
        
        self.client = Client()
        
        # Setup Data
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product", price=100, cost=50, stock=10, category=self.category)
        self.client_obj = ClientModel.objects.create(name="Test Client", phone="12345678")

    def log_result(self, role, action, resource, success, expected):
        status = "✅ ALLOWED" if success else "⛔ DENIED"
        match = "MATCH" if success == expected else "MISMATCH ❌"
        print(f"[{role:<10}] {action:<10} {resource:<10} -> {status:<10} ({match})")

    def perform_crud(self, user, role_name):
        self.client.force_login(user)
        print(f"\n--- Testing CRUD for Role: {role_name} ---")

        # Create fresh resources for this role's test
        product = Product.objects.create(name=f"Prod {role_name}", code=f"INIT_{role_name}", price=100, cost=50, stock=10, min_stock=5, category=self.category)
        client_obj = ClientModel.objects.create(name=f"Client {role_name}", phone="12345678")

        # --- INVENTORY (Products) ---
        # READ
        resp = self.client.get(reverse('inventory:product_list'))
        self.log_result(role_name, "READ", "Product", resp.status_code == 200, True)

        # CREATE
        resp = self.client.post(reverse('inventory:product_add'), {
            'name': f'New Prod {role_name} 2', 'code': f'C{role_name}', 
            'price': 100, 'cost': 50, 'stock': 10, 'min_stock': 5, 'category': self.category.id
        })
        
        success = False
        if resp.status_code == 302:
            if resp.url == reverse('inventory:product_list'):
                success = True
        elif resp.status_code == 200 and 'form' in resp.context:
             print(f"    [DEBUG] Product CREATE Form Errors: {resp.context['form'].errors}")
        else:
             print(f"    [DEBUG] Product CREATE Unexpected Status: {resp.status_code}")
        
        expected_inv = role_name in ['ADMIN', 'WAREHOUSE']
        self.log_result(role_name, "CREATE", "Product", success, expected_inv)

        # UPDATE
        resp = self.client.post(reverse('inventory:product_edit', args=[product.id]), {
            'name': f'Updated {role_name}', 'code': f'C{role_name}_UPD', 
            'price': 100, 'cost': 50, 'stock': 10, 'min_stock': 5, 'category': self.category.id
        })
        success = False
        if resp.status_code == 302:
            if resp.url == reverse('inventory:product_list'):
                success = True
            else:
                print(f"    [DEBUG] Product UPDATE Redirected to: {resp.url}")
        elif resp.status_code == 200 and 'form' in resp.context:
             print(f"    [DEBUG] Product UPDATE Form Errors: {resp.context['form'].errors}")
        else:
             print(f"    [DEBUG] Product UPDATE Unexpected Status: {resp.status_code}")

        self.log_result(role_name, "UPDATE", "Product", success, expected_inv)

        # DELETE
        resp = self.client.post(reverse('inventory:product_delete', args=[product.id]))
        success = False
        if resp.status_code == 302:
            if resp.url == reverse('inventory:product_list'):
                success = True
            else:
                print(f"    [DEBUG] Product DELETE Redirected to: {resp.url}")
        else:
             print(f"    [DEBUG] Product DELETE Unexpected Status: {resp.status_code}")
        self.log_result(role_name, "DELETE", "Product", success, expected_inv)


        # --- SALES (Clients) ---
        # READ
        resp = self.client.get(reverse('sales:client_list'))
        # Warehouse should be denied (redirect)
        success = resp.status_code == 200
        expected_sales = role_name in ['ADMIN', 'SELLER']
        self.log_result(role_name, "READ", "Client", success, expected_sales)

        # CREATE
        resp = self.client.post(reverse('sales:client_add'), {
            'name': f'Client {role_name} New', 'phone': '123'
        })
        success = False
        if resp.status_code == 302:
            if resp.url == reverse('sales:client_list'):
                success = True
            else:
                print(f"    [DEBUG] Client CREATE Redirected to: {resp.url}")
        elif resp.status_code == 200 and 'form' in resp.context:
             print(f"    [DEBUG] Client CREATE Form Errors: {resp.context['form'].errors}")
        else:
             print(f"    [DEBUG] Client CREATE Unexpected Status: {resp.status_code}")

        self.log_result(role_name, "CREATE", "Client", success, expected_sales)

        # UPDATE
        resp = self.client.post(reverse('sales:client_edit', args=[client_obj.id]), {
            'name': f'Client Upd {role_name}', 'phone': '123'
        })
        success = False
        if resp.status_code == 302:
            if resp.url == reverse('sales:client_list'):
                success = True
            else:
                print(f"    [DEBUG] Client UPDATE Redirected to: {resp.url}")
        elif resp.status_code == 200 and 'form' in resp.context:
             print(f"    [DEBUG] Client UPDATE Form Errors: {resp.context['form'].errors}")
        else:
             print(f"    [DEBUG] Client UPDATE Unexpected Status: {resp.status_code}")
        
        self.log_result(role_name, "UPDATE", "Client", success, expected_sales)

        # DELETE
        resp = self.client.post(reverse('sales:client_delete', args=[client_obj.id]))
        success = False
        if resp.status_code == 302:
            if resp.url == reverse('sales:client_list'):
                success = True
            else:
                print(f"    [DEBUG] Client DELETE Redirected to: {resp.url}")
        else:
             print(f"    [DEBUG] Client DELETE Unexpected Status: {resp.status_code}")
        self.log_result(role_name, "DELETE", "Client", success, expected_sales)

    def test_evidence(self):
        print("\n=======================================================")
        print("       EVIDENCIA DE PRUEBAS CRUD POR ROL")
        print("=======================================================")
        self.perform_crud(self.admin, 'ADMIN')
        self.perform_crud(self.seller, 'SELLER')
        self.perform_crud(self.warehouse, 'WAREHOUSE')
        print("\n=======================================================")
