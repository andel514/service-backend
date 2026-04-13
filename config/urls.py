from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('', health_check, name='health'),
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/chat/', include('apps.chat.urls')),
]
