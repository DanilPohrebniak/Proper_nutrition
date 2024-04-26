from django.contrib import admin
from django.urls import path, include
from pn.views import home_view,register,login,logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('pn/', include('pn.urls')),
]