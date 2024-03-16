from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from customer.views import (
    Menu,
    Index,
    About,
    OrderView,
    MenuSearch,
    OrderConfirmation,
    OrderPayConfirmation
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('order/', OrderView.as_view(), name='order'),
    path('order-conf/<int:pk>', OrderConfirmation.as_view(), name='order-conf'),
    path('payment-conf/<int:pk>', OrderPayConfirmation.as_view(), name='payment-conf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
