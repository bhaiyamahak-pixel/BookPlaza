from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('register/', views.register_view, name='register'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/place/', views.place_order, name='place_order'),
    path('book/<int:pk>/',views.book_detail, name='book_detail'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:category>/',views.category_books,name='category_books'),
    path("your-orders/",views.your_orders,name="your_orders"),
    path("login/", views.user_login, name="login"),
    path('about-us/', views.about_us, name='about_us'),
    path('search/', views.search_books, name='search_books'),
    path('place-order/<int:pk>/',views.direct_place_order,name='direct_place_order'),
    path('cart/place-order/',views.cart_place_order,name='cart_place_order'),
    path('logout/', views.user_logout, name='logout'),
]    
