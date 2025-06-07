from django.urls import path
from . import views

urlpatterns =[
    path('search/',views.search, name="search"),
    path('update_info/',views.update_info, name="update_info"),
    path('update_password/',views.update_password, name="update_password"),
    path('update_user/',views.update_user, name="update_user"),
    path('category_summary/', views.category_summary, name="category_summary"),
    path('category/<str:foo>', views.category, name="category"),
    path('product/<int:pk>', views.product, name='product'),
    path('register/',views.register_user,name='register'),
    path('login/', views.login_user, name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about")
]