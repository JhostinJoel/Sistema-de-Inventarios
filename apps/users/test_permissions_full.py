from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class RolePermissionTests(TestCase):
    def setUp(self):
        # Create users with different roles
        self.admin = User.objects.create_user(
            username='admin_test', email='admin@test.com', password='password', role='ADMIN'
        )
        self.seller = User.objects.create_user(
            username='seller_test', email='seller@test.com', password='password', role='SELLER'
        )
        self.warehouse = User.objects.create_user(
            username='warehouse_test', email='warehouse@test.com', password='password', role='WAREHOUSE'
        )
        self.client = Client()

    def check_access(self, user, url_name, expected_status=200, should_redirect=False):
        self.client.force_login(user)
        url = reverse(url_name)
        response = self.client.get(url)
        
        if should_redirect:
            # Expect redirect (usually to dashboard or login) implies access denied
            if response.status_code == 200:
                return False, f"Expected redirect/denial but got 200 OK for {url_name}"
            return True, "OK"
        else:
            # Expect access granted
            if response.status_code != expected_status:
                return False, f"Expected {expected_status} but got {response.status_code} for {url_name}"
            return True, "OK"

    def test_admin_permissions(self):
        print("\nTesting ADMIN Permissions...")
        users_access, msg1 = self.check_access(self.admin, 'users:user_list')
        inventory_access, msg2 = self.check_access(self.admin, 'inventory:product_add')
        sales_access, msg3 = self.check_access(self.admin, 'sales:pos')
        
        self.assertTrue(users_access, f"Admin should access users: {msg1}")
        self.assertTrue(inventory_access, f"Admin should access inventory: {msg2}")
        self.assertTrue(sales_access, f"Admin should access sales: {msg3}")

    def test_seller_permissions(self):
        print("\nTesting SELLER Permissions...")
        # Should access Sales
        sales_access, msg1 = self.check_access(self.seller, 'sales:pos')
        self.assertTrue(sales_access, f"Seller should access POS: {msg1}")

        # Should NOT access User Management
        users_access, msg2 = self.check_access(self.seller, 'users:user_list', should_redirect=True)
        self.assertTrue(users_access, f"Seller should NOT access users: {msg2}")

        # Should NOT access Inventory Create (Based on README)
        # Note: This test might fail if views are not protected
        inv_add_access, msg3 = self.check_access(self.seller, 'inventory:product_add', should_redirect=True)
        if not inv_add_access:
            print(f"⚠️  SECURITY WARNING: Seller was able to access 'inventory:product_add'")
        
        # We assert it to fail if we want to confirm the bug, or assert True if we expect it to be fixed.
        # For now, let's assert True to see the failure in the report.
        self.assertTrue(inv_add_access, f"Seller should NOT access product add: {msg3}")

    def test_warehouse_permissions(self):
        print("\nTesting WAREHOUSE Permissions...")
        # Should access Inventory
        inv_access, msg1 = self.check_access(self.warehouse, 'inventory:product_add')
        self.assertTrue(inv_access, f"Warehouse should access inventory: {msg1}")

        # Should NOT access User Management
        users_access, msg2 = self.check_access(self.warehouse, 'users:user_list', should_redirect=True)
        self.assertTrue(users_access, f"Warehouse should NOT access users: {msg2}")

        # Should NOT access Sales (Based on README)
        # Note: This test might fail if views are not protected
        sales_access, msg3 = self.check_access(self.warehouse, 'sales:pos', should_redirect=True)
        if not sales_access:
            print(f"⚠️  SECURITY WARNING: Warehouse was able to access 'sales:pos'")
            
        self.assertTrue(sales_access, f"Warehouse should NOT access POS: {msg3}")
