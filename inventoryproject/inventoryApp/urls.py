from django.urls import path
from . import views



urlpatterns = [
    path('products/', views.products_view, name="home"),
    path('product/<pk>', views.product_detail_view, name="product_detail_view"),
    path('categories/',views.categories_view, name= "categories_view"),
    path('category/<pk>', views.category_detail_view, name="category_detail_view"),
    path('sellers/', views.seller_view, name="seller_view"),
    path('seller/<pk>', views.seller_detail_view, name="seller_detail_view"),
    path('transactions/', views.transactions_view, name="transactions_view"),
    path('transaction/<pk>', views.transaction_detail_view, name="transaction_detail_view"),
    path('dashboard/', views.dashboard_view)

   
]
