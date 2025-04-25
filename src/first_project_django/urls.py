from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rooms_app.urls')), # <--- включаем urls нашего приложения

]
