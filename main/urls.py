from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('activate-email/', email_activate, name='activate-email'),
    path('register/', user_register_view, name='register'),
    path('<slug:type_url>/', ProductListView.as_view(), name='type'),
    path('products/detail/<int:pk>',
         ProductDetailView.as_view(), name='product-detail'),
    path('products/create',
         ProductCreateView.as_view(), name='product-create'),
        
]
