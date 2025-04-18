from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import register, home, item_detail, my_items, edit_item, create_item, create_proposal, exchange_proposals,delete_item, delete_proposal

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('register/', register, name='register'),
    path('item/<int:pk>/', item_detail, name='item_detail'),
    path('my-items/', my_items, name='my_items'),
    path('item/create/', create_item, name='create_item'),
    path('item/delete/<int:pk>/', delete_item, name='delete_item'),
    path('item/delete_proposal/<int:pk>/', delete_proposal, name='delete_proposal'),
    path('item/<int:pk>/edit/', edit_item, name='edit_item'),
    path('create_proposal/<int:pk_other>/', create_proposal, name='create_proposal'),
    path('create_proposal/<int:pk_other>/<int:pk_my>/', create_proposal, name='create_proposal_with_my_item'),
    path('exchange-proposals/', exchange_proposals, name='exchange_proposals'),

    

       
]