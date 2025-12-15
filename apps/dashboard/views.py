from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.inventory.models import Product, InventoryMovement
from apps.sales.models import Sale, Purchase
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        User = get_user_model()
        
        # General Stats
        context['total_products'] = Product.objects.count()
        context['low_stock_products'] = Product.objects.filter(stock__lte=5).count()
        context['total_sales_today'] = Sale.objects.filter(date__date=timezone.now().date()).count()
        context['total_users'] = User.objects.count()
        
        # Recent Activity
        context['recent_sales'] = Sale.objects.order_by('-date')[:5]
        context['recent_movements'] = InventoryMovement.objects.order_by('-created_at')[:5]
        
        return context
