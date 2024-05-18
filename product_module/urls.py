from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='products_categories_list'),
    path('brands/<brand>', views.ProductListView.as_view(), name='products_list_by_brands'),
    path('add-product-comment', views.add_product_comment, name='add_product_comment'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
]
