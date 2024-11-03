from django.shortcuts import render, redirect
from Userapp.models import ContactDB, RegisterDB, CartDB, WishlistDB, OrderDB, Review
from Adminapp.models import ProductDB, CategoryDB, HotDealDB
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404
import razorpay
from django.http import HttpResponseRedirect
from django.db.models import Avg
from django.core.paginator import Paginator
from django.db.models import F


# Create your views here.

def homepage(request):
    cat = CategoryDB.objects.all()

    # Fetch the latest available products, ordered by creation date (up to 8)
    latest_products = ProductDB.objects.filter(status='available').order_by('-created_at')[:8]

    # Fetch "Coming Soon" products from the database
    coming_products = ProductDB.objects.filter(status='coming_soon').order_by('-created_at')[:8]

    deals_of_the_week = ProductDB.objects.filter(is_deal_of_the_week=True)

    hotdeal = HotDealDB.objects.last()  # Fetch the latest hot deal

    # If the hot deal has ended, don't show it
    if hotdeal and hotdeal.has_ended():
        hotdeal = None  # Clear the hot deal if it's expired

    context = {
        'latest_products': latest_products,
        'coming_products': coming_products,
        'deals_of_the_week': deals_of_the_week,
        'hotdeal': hotdeal,
        'cat': cat
    }

    return render(request, "HomePage.html", context)


def aboutus(request):
    cat = CategoryDB.objects.all()
    return render(request, "About_us.html", {'cat':cat})

def contact(request):
    cat = CategoryDB.objects.all()
    return render(request, "Contact.html", {'cat':cat})

def contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        sub = request.POST.get('subject')
        msg = request.POST.get('message')

        obj = ContactDB(Name=name, Email=email, Subject=sub, Message=msg)
        obj.save()
        messages.success(request, "Send successfully..!")
        return redirect(contact)


# In views.py
def products(request):
    cat = CategoryDB.objects.all()  # Fetch all categories
    product_list = ProductDB.objects.all()
    deals_of_the_week = ProductDB.objects.filter(is_deal_of_the_week=True)


    # Set up pagination
    paginator = Paginator(product_list, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "All_Products.html", {
        'products': page_obj,
        'cat': cat,
        'deals_of_the_week': deals_of_the_week,

    })

def single_product(request, pro_id):
    cat = CategoryDB.objects.all()
    product = get_object_or_404(ProductDB, id=pro_id)  # Use get_object_or_404 for better error handling
    deals_of_the_week = ProductDB.objects.filter(is_deal_of_the_week=True)
    reviews = Review.objects.filter(product=product)

    avg_rating = reviews.aggregate(average_rating=Avg('rating'))['average_rating'] or 0
    rating_counts = {star: reviews.filter(rating=star).count() for star in range(1, 6)}

    # Check if the product is already in the user's wishlist
    username = request.session.get('username')
    is_in_wishlist = WishlistDB.objects.filter(User_Name=username, Product_Name=product.Product_Name).exists()

    context = {
        'product': product,
        'cat': cat,
        'rating_counts': rating_counts,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_in_wishlist': is_in_wishlist,
        'deals_of_the_week': deals_of_the_week
    }

    return render(request, "Single_Product.html", context)


def add_review(request, product_id):
    if request.method == "POST":
        user_name = request.POST.get('name')
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')  # Handle rating selection appropriately
        product = get_object_or_404(ProductDB, id=product_id)

        # Create and save the review
        Review.objects.create(product=product, user_name=user_name, comment=comment, rating=rating)

        # Redirect to the correct single product view after adding the review
        return HttpResponseRedirect(reverse('single_product', args=[product_id]))

def filtered_product(request, cat_name):
    cat = CategoryDB.objects.all()
    data = ProductDB.objects.filter(Category_Name=cat_name)
    return render(request, "Filtered_Product.html", {'cat': cat,'data':data,'cat_name':cat_name})


def user_register_page(request):
    return render(request, "User_Registration.html")

def register_details(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        img = request.FILES['image']

        obj = RegisterDB(Username=username, Email=email, Password1=password1, Password2=password2, Image=img)
        obj.save()
        messages.success(request, "Registered successfully..!")
        return redirect(user_register_page)

def user_login_page(request):
    # Check if user is already logged in, redirect to homepage
    if 'username' in request.session:
        return redirect('homepage')  # Redirect to homepage if already logged in
    return render(request, "User_Login.html")


def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch user from the database by username
            user = RegisterDB.objects.get(Username=username)

            # Check if the password matches
            if user.Password1 == password:
                # Store the username in session
                request.session['username'] = username
                messages.success(request, "Login successful!")
                return redirect('homepage')  # Redirect to homepage
            else:
                messages.warning(request, "Invalid username or password")
        except RegisterDB.DoesNotExist:
            messages.warning(request, "User not found")

    return render(request, 'User_Login.html')


def user_logout(request):
    request.session.flush()  # Clears all session data
    logout(request)
    return redirect(user_login_page)


def add_cart(request):
    if request.method == "POST":
        username = request.POST.get('username')
        product_name = request.POST.get('productname')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        total_price = request.POST.get('total')
        pro_id = request.POST.get('pro_id')

        try:
            # Fetch the product based on the name
            product = ProductDB.objects.get(Product_Name=product_name)
            image = product.Image1.url if product.Image1 else ''
        except ProductDB.DoesNotExist:
            # Handle case when product is not found
            image = ''
            messages.error(request, "Product does not exist!")
            return redirect('single_product', pro_id=pro_id)

        # Remove commas from the price and total price before saving to the database
        price = price.replace(",", "") if price else "0"
        total_price = total_price.replace(",", "") if total_price else "0"

        # Convert price and total_price to numeric types (float or Decimal)
        try:
            price = float(price)
            total_price = float(total_price)
        except ValueError:
            messages.error(request, "Invalid price format!")
            return redirect('single_product', pro_id=pro_id)

        # Create a new cart entry
        obj = CartDB(
            User_Name=username,
            Product_Name=product_name,
            Quantity=quantity,
            Price=price,  # Numeric value without commas
            Total_Price=total_price,  # Numeric value without commas
            Image=image
        )
        obj.save()

        # Success message and redirect
        messages.success(request, "Product added to cart successfully!")
        return redirect('single_product', pro_id=pro_id)

    return render(request, "Single_Product.html")




def cart_page(request):
    data = CartDB.objects.filter(User_Name=request.session['username'])
    cat = CategoryDB.objects.all()

    sub_total = 0
    total = 0
    shipping = 0
    for i in data:
        sub_total += i.Total_Price

        if sub_total > 10000:
            shipping = 0  # Free shipping for orders above 10,000
        elif sub_total > 7000:
            shipping = 100  # Shipping charge of 100 for orders above 7,000
        elif sub_total > 5000:
            shipping = 150  # Shipping charge of 150 for orders above 5,000
        elif sub_total > 3000:
            shipping = 200  # Shipping charge of 200 for orders above 3,000
        elif sub_total > 1000:
            shipping = 250  # Shipping charge of 250 for orders above 1,000
        else:
            shipping = 300

        total = sub_total + shipping

    return render(request, "Cart.html", {'data': data, 'cat': cat, 'sub_total': sub_total,
                                         'shipping': shipping, 'total': total})

def delete_item(request, dataid):
    x = CartDB.objects.filter(id=dataid)
    x.delete()
    messages.success(request,"Item Deleted..!")
    return redirect(cart_page)


def wishlist_page(request):
    data = WishlistDB.objects.filter(User_Name=request.session['username'])
    cat = CategoryDB.objects.all()
    return render(request, "Wishlist.html", {'cat':cat, 'data':data})

def add_to_wishlist(request):
    if request.method == "POST":
        username = request.POST.get('username')
        product_name = request.POST.get('productname')
        price = request.POST.get('price')
        image_url = request.POST.get('image')
        pro_id = request.POST.get('pro_id')  # Get the pro_id from the form

        # Validate pro_id
        if not pro_id:
            messages.error(request, "Product ID is missing.")
            return redirect('homepage')

        # Remove commas from the price and convert to float
        price = price.replace(',', '')
        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Invalid price format.")
            return redirect(reverse('single_product', args=[pro_id]))

        # Try to retrieve the product by pro_id
        product = get_object_or_404(ProductDB, id=pro_id)

        # Check if the image URL matches Image1
        if image_url == product.Image1.url:
            img = product.Image1
        else:
            img = None

        if img is None:
            messages.error(request, "Image not found or not available.")
            return redirect(reverse('single_product', args=[pro_id]))

        # Create a new WishlistDB entry
        obj = WishlistDB(User_Name=username, Image=img, Product_Name=product.Product_Name, Price=price)
        obj.save()

        messages.success(request, "Successfully Added to Wishlist!")
        return redirect(reverse('single_product', args=[pro_id]))

    messages.error(request, "Invalid request.")
    return redirect('homepage')


def delete_wishlist(request, dataid):
    x = WishlistDB.objects.filter(id=dataid)
    x.delete()
    messages.success(request,"Item removed from wishlist..!")
    return redirect(wishlist_page)

def checkout_page(request):
    data = CartDB.objects.filter(User_Name=request.session['username'])
    cat = CategoryDB.objects.all()

    sub_total = 0
    total = 0
    shipping = 0
    for i in data:
        sub_total += i.Total_Price

        if sub_total > 10000:
            shipping = 0  # Free shipping for orders above 10,000
        elif sub_total > 7000:
            shipping = 100  # Shipping charge of 100 for orders above 7,000
        elif sub_total > 5000:
            shipping = 150  # Shipping charge of 150 for orders above 5,000
        elif sub_total > 3000:
            shipping = 200  # Shipping charge of 200 for orders above 3,000
        elif sub_total > 1000:
            shipping = 250  # Shipping charge of 250 for orders above 1,000
        else:
            shipping = 300

        total = sub_total + shipping

    return render(request, "Checkout.html", {'data': data, 'cat': cat, 'sub_total': sub_total,
                                             'shipping': shipping, 'total': total})

def add_order(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        country = request.POST.get('country')
        state = request.POST.get('state')
        pin = request.POST.get('zip')
        address = request.POST.get('address')
        total_price = request.POST.get('total')

        # Create the order object
        obj = OrderDB(
            Name=name,
            Email=email,
            Phone=mobile,
            Country=country,
            State=state,
            Pin=pin,
            Address=address,
            Total_Price=total_price
        )
        obj.save()

        messages.success(request, "Billing details submitted! Proceed to payment..!")
        return redirect(payment_page)  # Adjust this to your actual payment page

    return render(request, "Checkout.html")

def payment_page(request):
        cat = CategoryDB.objects.all()
        customer = OrderDB.objects.order_by('-id').first()

        payy = customer.Total_Price
        amount = int(payy * 100)
        payy_str = str(amount)

        for i in payy_str:
            print(i)

        if request.method == "POST":
            order_currency = 'INR'
            client = razorpay.Client(auth=('rzp_test_GgqJ5qD6i2W5HL ', 'a6zCHkUkHBHKgMCMnhvzK8Wi'))
            payment = client.order.create({'amount': amount, 'currency': order_currency})

        return render(request, "Payment.html", {'cat': cat, 'customer': customer, 'payy_str': payy_str})


def paginate_products(request, products_list):
    paginator = Paginator(products_list, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def search_products(request):
    query = request.GET.get('q')
    products_list = ProductDB.objects.filter(Product_Name__icontains=query)
    page_obj = paginate_products(request, products_list)
    deals_of_the_week = ProductDB.objects.filter(is_deal_of_the_week=True)

    return render(request, 'search_results.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'deals_of_the_week':deals_of_the_week
    })


