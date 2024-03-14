from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import Order

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        orders = Order.objects.filter(
            created_at__year=today.year, created_at__month=today.month, created_at__day=today.day)

        total_revenue = 0
        for order in orders:
            total_revenue += order.price

        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }
        return render(request, 'restaurant/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
