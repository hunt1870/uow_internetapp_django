from django.urls import path
from myapp import views
app_name = 'myapp'
urlpatterns = [path(r'', views.index, name='index'),
               path(r'about/', views.about, name='about'),
               path(r'<int:cat_no>', views.detail, name='detail'),
               path(r'products/', views.products, name='products'),
               path(r'product/<int:prod_id>', views.product_detail, name='product_detail'),
               path(r'placeorder/', views.place_order, name='place_order'),
               path(r'login/', views.user_login, name='login'),
               path(r'logout/', views.user_logout, name='logout'),
               path(r'orders/', views.myorders, name='orders'),
               path(r'register/', views.user_register, name='register'),
               ]
