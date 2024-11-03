from django.shortcuts import render, redirect,get_object_or_404
from Adminapp.models import CategoryDB, ProductDB, HotDealDB
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone

def index_page(request):
    return render(request, "index.html")

def category_page(request):
    return render(request, "Categories.html")


def add_category(request):
    if request.method == "POST":
       name = request.POST.get('name')
       desc = request.POST.get('description')
       img = request.FILES['image']

       obj = CategoryDB(Name=name, Description=desc, Image=img)
       obj.save()
       messages.success(request, "Category saved successfully..!")
       return redirect(add_category)

    else:
     return render(request, "Categories.html")

def view_category(request):
    data = CategoryDB.objects.all()
    return render(request, "Display_Category.html", {'data':data})

def edit_category(request,dr_id):
    data = CategoryDB.objects.get(id=dr_id)
    return render(request,"Update_Category.html", {'data':data})

def delete_category(request,dr_id):
    x = CategoryDB.objects.filter(id=dr_id)
    x.delete()
    messages.error(request, "Category deleted successfully..!")
    return redirect(view_category)

def update_category(request,data_id):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('description')
        try:
            img = request.FILES['Image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = CategoryDB.objects.get(id=data_id).Image

        CategoryDB.objects.filter(id=data_id).update(Name=name, Description=desc, Image=file)
        return redirect(view_category)

def product_page(request):
    category = CategoryDB.objects.all()
    return render(request, "Products.html", {'category':category})


def add_products(request):
    if request.method == "POST":
        c_name = request.POST.get('name')
        p_name = request.POST.get('productname')
        b_name = request.POST.get('brandname')
        price = request.POST.get('price')
        weight = request.POST.get('weight')
        desc = request.POST.get('description')
        img1 = request.FILES['image1']
        img2 = request.FILES['image2']
        img3 = request.FILES['image3']
        status = request.POST.get('status')
        is_deal_of_the_week = request.POST.get('is_deal_of_the_week') == 'on'

        obj = ProductDB(Category_Name=c_name, Product_Name=p_name, Brand_Name=b_name, Price=price, Weight=weight,
                        Description=desc, Image1=img1, Image2=img2, Image3=img3,
                        status=status,  is_deal_of_the_week=is_deal_of_the_week)
        obj.save()
        messages.success(request, "Product added successfully..!")
        return redirect(product_page)

    else:
        return render(request, "Products.html")


def view_product(request):
    data = ProductDB.objects.all()
    return render(request, "Display_Products.html", {'data':data})

def edit_product(request, dr_id):
    data = ProductDB.objects.get(id=dr_id)
    categories = CategoryDB.objects.all()  # Assuming you want to list categories
    return render(request, "Update_Products.html", {'data': data, 'categories': categories})

def delete_product(request,dr_id):
    x = ProductDB.objects.filter(id=dr_id)
    x.delete()
    messages.error(request, "Product deleted successfully..!")
    return redirect(view_product)


def update_product(request,data_id):
    if request.method == "POST":
        c_name = request.POST.get('name')
        p_name = request.POST.get('productname')
        b_name = request.POST.get('brandname')
        price = request.POST.get('price')
        weight = request.POST.get('weight')
        desc = request.POST.get('description')
        try:
            img = request.FILES['Image1']
            fs = FileSystemStorage()
            file1 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file1 = ProductDB.objects.get(id=data_id).Image1

        try:
            img = request.FILES['Image2']
            fs = FileSystemStorage()
            file2 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file2 = ProductDB.objects.get(id=data_id).Image2

        try:
            img = request.FILES['Image3']
            fs = FileSystemStorage()
            file3 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file3 = ProductDB.objects.get(id=data_id).Image3

        ProductDB.objects.filter(id=data_id).update(Category_Name=c_name, Product_Name=p_name, Brand_Name=b_name, Price=price, Weight=weight, Description=desc, Image1=file1, Image2=file2, Image3=file3)
        return redirect(view_product)


def admin_login_page(request):
    return render(request, "Admin_Login.html")


def admin_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(request, username=un, password=pwd)

        if user is not None and user.is_staff:  # Check if the user is a staff/admin
            login(request, user)  # Django's built-in login function
            request.session['username'] = user.username  # Store username in session
            messages.success(request, "Login Successful!")
            return redirect('index_page')  # Redirect after successful login
        else:
            messages.warning(request, "Invalid username or password")
            return redirect('admin_login_page')  # Redirect back to login on failure

    return render(request, 'Admin_Login.html')

def admin_logout(request):
    request.session.flush()  # Clears all session data
    logout(request)
    return redirect('admin_login_page')


def add_hot_deal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        product_ids = request.POST.getlist('products')  # Get selected product IDs

        if len(product_ids) != 3:
            messages.error(request, "Please select exactly 3 products.")
            return redirect('add_hot_deal')

        # Convert string dates into datetime objects
        try:
            start_date = timezone.datetime.fromisoformat(start_date)
            end_date = timezone.datetime.fromisoformat(end_date)
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('add_hot_deal')

        # Create HotDeal object
        hot_deal = HotDealDB.objects.create(
            title=title,
            start_date=start_date,
            end_date=end_date
        )

        # Add selected products to the hot deal
        products = ProductDB.objects.filter(id__in=product_ids)
        hot_deal.products.set(products)  # Set many-to-many relation

        messages.success(request, "Hot deal added successfully!")
        return redirect('add_hot_deal')

    else:
        products = ProductDB.objects.all()  # Fetch all products for the form
        return render(request, 'Hot_Deals.html', {'products': products})


def view_hot_deals(request):
    hot_deals = HotDealDB.objects.all()

    return render(request, 'View_Hot_Deals.html', {'hot_deals':hot_deals})


def edit_hotdeal(request, deal_id):
    hotdeal = get_object_or_404(HotDealDB, id=deal_id)
    products = ProductDB.objects.all()  # Fetch all available products for the form
    return render(request, "Update_Hotdeals.html", {'hotdeal': hotdeal, 'products': products})


# Function to update the hot deal
def update_hotdeal(request, deal_id):
    if request.method == "POST":
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_products = request.POST.getlist('products')  # Get the selected products from the form

        hotdeal = HotDealDB.objects.get(id=deal_id)

        # Update the fields
        hotdeal.title = title
        hotdeal.start_date = start_date
        hotdeal.end_date = end_date
        hotdeal.save()

        # Update many-to-many relationship
        hotdeal.products.set(selected_products)
        hotdeal.save()

        messages.success(request, "Hot deal updated successfully!")
        return redirect('view_hot_deals')


# View to delete the hot deal
def delete_hotdeal(request, deal_id):
    hotdeal = get_object_or_404(HotDealDB, id=deal_id)
    hotdeal.delete()
    messages.error(request, "Hot deal deleted successfully!")
    return redirect('view_hot_deals')