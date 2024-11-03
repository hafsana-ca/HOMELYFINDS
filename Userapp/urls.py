from django.urls import path
from Userapp import views

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),
    path("aboutus/",views.aboutus,name="aboutus"),
    path("contact/",views.contact,name="contact"),
    path("contact_form/",views.contact_form,name="contact_form"),
    path("products/",views.products,name="products"),
    path("single_product/<int:pro_id>/",views.single_product,name="single_product"),
    path('product/<int:product_id>/add-review/', views.add_review, name='your_review_submission_view'),
    path("filtered_product/<str:cat_name>/",views.filtered_product,name="filtered_product"),
    path("",views.user_login_page,name="user_login_page"),
    path("user_register_page/",views.user_register_page,name="user_register_page"),
    path("register_details/",views.register_details,name="register_details"),
    path("UserLogin/",views.UserLogin,name="UserLogin"),
    path("user_logout/",views.user_logout,name="user_logout"),
    path("add_cart/",views.add_cart,name="add_cart"),
    path("cart_page/",views.cart_page,name="cart_page"),
    path("delete_item/<int:dataid>/",views.delete_item,name="delete_item"),
    path("wishlist_page/",views.wishlist_page,name="wishlist_page"),
    path("add_to_wishlist/",views.add_to_wishlist,name="add_to_wishlist"),
    path("delete_wishlist/<int:dataid>/",views.delete_wishlist,name="delete_wishlist"),
    path("checkout_page/",views.checkout_page,name="checkout_page"),
    path("add_order/",views.add_order,name="add_order"),
    path("payment_page/",views.payment_page,name="payment_page"),
    path('search_products/', views.search_products, name='search_products'),


]