from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from apis import views

# router = routers.DefaultRouter()
# router.register(r'users', views.hello_world)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apis.urls'))
]
