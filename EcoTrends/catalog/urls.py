from django.urls import path
from . import views
from .views import product_list, product_list_by_category, product_list_by_subcategory, rate, ProductDetailView, rate_index, staff_dashboard_view, delete_product, delete_comment, product_search,save_product,unsave_product,delete_commentProfile


app_name = 'catalog'    

urlpatterns = [
    path('', product_list, name='product_list'),
    path('products/category/<int:category_id>/', product_list_by_category, name='product_list_by_category'),
    path('products/subcategory/<int:subcategory_id>/', product_list_by_subcategory, name='product_list_by_subcategory'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('rate/<int:product_id>/<int:rating>/', rate, name='rate'),        
    path('rate_index', rate_index),
    path('staff_dashboard/', staff_dashboard_view, name='staff_dashboard'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('delete_comment/<int:comment_id>/', delete_comment.as_view(), name='delete_comment'),
    path('product_search/', product_search, name='product_search'),
    path('save_product/<int:product_id>/', save_product, name='save_product'),
    path('unsave_product/<int:product_id>/', unsave_product, name='unsave_product'),
    path('delete_commentProfile/<int:comment_id>/', delete_commentProfile.as_view(), name='delete_commentProfile')

]