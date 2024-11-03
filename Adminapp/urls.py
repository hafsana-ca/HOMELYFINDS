from django.urls import path
from Adminapp import views

urlpatterns = [
    path("index_page/",views.index_page,name="index_page"),

    path("category_page/",views.category_page,name="category_page"),
    path("add_category/",views.add_category,name="add_category"),
    path("view_category/",views.view_category,name="view_category"),
    path("edit_category/<int:dr_id>/",views.edit_category,name="edit_category"),
    path("delete_category/<int:dr_id>/",views.delete_category,name="delete_category"),
    path("update_category/<int:data_id>/",views.update_category,name="update_category"),

    path("product_page/",views.product_page,name="product_page"),
    path("add_products/",views.add_products,name="add_products"),
    path("view_product/",views.view_product,name="view_product"),
    path("edit_product/<int:dr_id>/",views.edit_product,name="edit_product"),
    path("delete_product/<int:dr_id>/",views.delete_product,name="delete_product"),
    path("update_product/<int:data_id>/",views.update_product,name="update_product"),

    path("admin_login_page/",views.admin_login_page,name="admin_login_page"),
    path("admin_login/",views.admin_login,name="admin_login"),
    path("admin_logout/",views.admin_logout,name="admin_logout"),

    path("add_hot_deal/",views.add_hot_deal,name="add_hot_deal"),
    path("view_hot_deals/",views.view_hot_deals,name="view_hot_deals"),
    path('edit_hotdeal/<int:deal_id>/', views.edit_hotdeal, name='edit_hotdeal'),
    path('update_hotdeal/<int:deal_id>/', views.update_hotdeal, name='update_hotdeal'),
    path('delete_hotdeal/<int:deal_id>/', views.delete_hotdeal, name='delete_hotdeal'),






]