from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from functools import wraps

# Role checkers
def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

def is_seller(user):
    return user.is_authenticated and user.role in ['ADMIN', 'SELLER']

def is_warehouse(user):
    return user.is_authenticated and user.role in ['ADMIN', 'WAREHOUSE']

# Decorators for function-based views
def admin_required(function=None, raise_exception=True):
    """Decorator for views that checks if user is ADMIN."""
    actual_decorator = user_passes_test(
        is_admin,
        login_url='users:login',
        redirect_field_name='next'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def seller_required(function=None, raise_exception=True):
    """Decorator for views that checks if user is ADMIN or SELLER."""
    actual_decorator = user_passes_test(
        is_seller,
        login_url='users:login',
        redirect_field_name='next'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def warehouse_required(function=None, raise_exception=True):
    """Decorator for views that checks if user is ADMIN or WAREHOUSE."""
    actual_decorator = user_passes_test(
        is_warehouse,
        login_url='users:login',
        redirect_field_name='next'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

from django.contrib import messages
from django.shortcuts import redirect

# Mixins for class-based views
class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin for class-based views that requires ADMIN role."""
    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta página.")
        return redirect('dashboard:index')

class SellerRequiredMixin(UserPassesTestMixin):
    """Mixin for class-based views that requires ADMIN or SELLER role."""
    def test_func(self):
        return is_seller(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta página.")
        return redirect('dashboard:index')

class WarehouseRequiredMixin(UserPassesTestMixin):
    """Mixin for class-based views that requires ADMIN or WAREHOUSE role."""
    def test_func(self):
        return is_warehouse(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta página.")
        return redirect('dashboard:index')
