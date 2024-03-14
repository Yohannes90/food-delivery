from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from customer.views import (
    Index,
    About,
    OrderView,
    OrderConfirmation,
    OrderPayConfirmation
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('order/', OrderView.as_view(), name='order'),
    path('order-conf/<int:pk>', OrderConfirmation.as_view(), name='order-conf'),
    path('payment-conf/<int:pk>', OrderPayConfirmation.as_view(), name='payment-conf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
