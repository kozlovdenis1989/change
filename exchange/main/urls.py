from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import register, home, item_detail, my_items

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('register/', register, name='register'),
    path('item/<int:pk>/', item_detail, name='item_detail'),
    path('my-items/', my_items, name='my_items'),

       
]