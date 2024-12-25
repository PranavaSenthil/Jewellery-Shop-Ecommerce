import json
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import *

def home(request):
    category_filter = request.GET.get('category', 'all')
    price_order = request.GET.get('price', None)
    review = request.GET.get('review', None)
    tag = request.GET.get('tag', None)
    search_query = request.GET.get('search-product', None)
    user = request.user
    cart_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)
        for i in cart_items:
            cart_total = (i.product.price)*(i.quantity) + cart_total
        print(cart_total)
        print(cart_items)
        try:
            customer = Customer.objects.get(user=request.user)
            has_profile = bool(customer.gender)
        except Customer.DoesNotExist:
            has_profile = False
    else:
        cart_items = []
        has_profile = False
    if category_filter == 'all':
        products = Product.objects.select_related('category').all()
    else:
        products = Product.objects.select_related('category').filter(category__name=category_filter)
    if price_order == 'low-to-high':
        products = Product.objects.all().order_by('price')
    elif price_order == 'high-to-low':
        products = Product.objects.all().order_by('-price')
    if review == 'Popularity':
        products = products.filter(review__rating__gte=3).distinct()
    elif review == 'Average rating':
        products = products.filter(review__rating__lt=3).distinct()
    products = products.filter(stock__gt=0)
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    if tag == 'latest':
        products = Product.objects.all().order_by('-created_at')[:3]
        print(products)
    elif tag == 'traditional':
        products = Product.objects.all().order_by('created_at')[:3]
    return render(request, 'home-02.html', {'has_profile': has_profile, 'products': products,'category_filter': category_filter,'cart_items': cart_items,'cart_total': cart_total})

def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        phoneno = request.POST['phoneno']

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('user_register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('user_register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                customer = Customer.objects.create(user=user, phoneno=phoneno)
                messages.success(request, 'User created successfully')
                return redirect('user_login')
        else:
            messages.error(request, 'Password not matching')
            return redirect('user_register')
    else:
        return render(request, 'auth/user_register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('user_login')
    return render(request, 'auth/user_login.html')

def user_logout(request):
    auth.logout(request)
    return redirect('home')

def user_profile(request,user_id):
    user = User.objects.get(id=user_id)
    customer, created = Customer.objects.get_or_create(user=user)
    if request.method == 'POST':
        gender = request.POST.get('gender')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        image = request.FILES.get('image')
        customer.gender = gender
        customer.address_line_1 = address_line_1
        customer.address_line_2 = address_line_2
        customer.city = city
        customer.state = state
        customer.postal_code = postal_code
        customer.country = country
        if image:
            customer.image = image 
        customer.save()
        request.session['has_profile'] = True
        return redirect('home')
    has_profile = not created
    return render(request, 'user_details.html', {'customer':customer,'has_profile': has_profile})

def user_edit(request, user_id):
    user = User.objects.get(id=user_id)
    customer = Customer.objects.get(user=user)
    if request.method == 'POST':
        gender = request.POST.get('gender')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        image = request.FILES.get('image')
        if image:
            customer.image = image
        customer.gender = gender
        customer.address_line_1 = address_line_1
        customer.address_line_2 = address_line_2
        customer.city = city
        customer.state = state
        customer.postal_code = postal_code
        customer.country = country
        customer.save()
        return redirect('home')
    return render(request, 'user_edit.html', {'customer': customer})

def user_show(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    try:
        customer = Customer.objects.get(user=user)
        has_profile = True
    except Customer.DoesNotExist:
        customer = None
        has_profile = False
        
    if has_profile:
        return render(request, 'user_show.html', {'customer': customer, 'has_profile': has_profile})
    else:
        return redirect('user_profile', user_id=user_id)
    
def shop(request):
    category_filter = request.GET.get('category', 'all')
    price_order = request.GET.get('price', None)
    review = request.GET.get('review', None)
    tag = request.GET.get('tag', None)
    search_query = request.GET.get('search-product', None)
    user = request.user
    cart_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)
        for i in cart_items:
            cart_total = (i.product.price)*(i.quantity) + cart_total
        print(cart_total)
        print(cart_items)
        try:
            customer = Customer.objects.get(user=request.user)
            has_profile = bool(customer.gender)
        except Customer.DoesNotExist:
            has_profile = False
    else:
        cart_items = []
        has_profile = False
    if category_filter == 'all':
        products = Product.objects.select_related('category').all()
    else:
        products = Product.objects.select_related('category').filter(category__name=category_filter)
    if price_order == 'low-to-high':
        products = Product.objects.all().order_by('price')
    elif price_order == 'high-to-low':
        products = Product.objects.all().order_by('-price')
    if review == 'Popularity':
        products = products.filter(review__rating__gte=3).distinct()
    elif review == 'Average rating':
        products = products.filter(review__rating__lt=3).distinct()
    if tag == 'latest':
        products = Product.objects.all().order_by('-created_at')[:3]
    elif tag == 'traditional':
        products = Product.objects.all().order_by('created_at')[:3]
    products = products.filter(stock__gt=0)
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    return render(request, 'product.html', {'has_profile': has_profile, 'products': products,'category_filter': category_filter,'cart_items': cart_items,'cart_total': cart_total})

def product_detail(request, product_name):
    user = request.user
    cart_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)
        for i in cart_items:
            cart_total = (i.product.price)*(i.quantity) + cart_total
        print(cart_total)
        print(cart_items)
    else:
        cart_items = []
    product = Product.objects.get(name=product_name)
    reviews = Review.objects.filter(product=product)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('review')
        review = Review.objects.create(product=product, user=user, rating=rating, comment=comment)
        review.save()
        messages.success(request, 'Review added successfully')
    if not product:
        messages.error(request, 'Product not found')
        return render(request, 'product-detail.html', {'product': [], 'related_products': []})
    print(product)
    print(user)
    print(reviews)
    for review in reviews:
        print(f'User: {review.user.username}, Comment: {review.comment}, Rating: {review.rating}')
    Category_name = product.category
    related_products = Product.objects.filter(category=Category_name).exclude(name=product_name)
    related_products = related_products.filter(stock__gt=0)
    print(related_products)
    return render(request, 'product-detail.html', {'product': product,'related_products': related_products,'user':user,'reviews': reviews,'cart_items': cart_items,'cart_total': cart_total})

def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('product_name')
        quantity = data.get('quantity', 1)
        
        user = request.user
        product = get_object_or_404(Product, name=product_name)
        cart, created = Cart.objects.get_or_create(user=user, product=product)
        
        if not created:
            cart.quantity += int(quantity)
        else:
            cart.quantity = int(quantity)
        
        cart.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def remove_from_cart(request, product_id):
    cart = Cart.objects.get(product_id=product_id,user=request.user)
    print(cart)
    cart.delete()
    return redirect('home')

def shop_cart(request):
    user = request.user
    cart_total = 0
    cart_items = []
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)

        if request.method == 'POST':
            if 'update_cart' in request.POST:
                quantities = request.POST.getlist('num-product1')

                for i, cart_item in enumerate(cart_items):
                    product_name = cart_item.product.name
                    product_stock = Product.objects.get(name=product_name)
                    if product_stock.stock < int(quantities[i]):
                        messages.error(request,'Product out of stock')
                        return redirect('shop_cart')
                    else:
                        try:
                            quantity = int(quantities[i])
                            if quantity > 0:
                                cart_item.quantity = quantity
                                cart_item.save()
                            else:
                                cart_item.delete()
                        except (ValueError, IndexError):
                            print(f"Error updating cart item {cart_item.product.name}")

            elif 'checkout' in request.POST:
                time = request.POST.get('time')
                state = request.POST.get('state')
                postal_code = request.POST.get('postcode')
                if not time or not state or not postal_code:
                    messages.error(request, 'Enter the shipping address')
                else:
                    address = f"{time}, {state}, {postal_code}"
                    for i in cart_items:
                        order = Order.objects.create(user=user, product=i.product, quantity=i.quantity, price=i.product.price, total_price=i.get_total_price(), status='Pending', shipping_address=address)
                        product_stock = Product.objects.get(name=i.product.name)
                        product_stock.stock-=i.quantity
                        print(product_stock.stock)
                        print(order)
                        product_stock.save()
                        order.save()
                        i.delete()
                    return redirect('home')
        for cart_item in cart_items:
            cart_total += cart_item.get_total_price()

    return render(request, 'shoping-cart.html',{'cart_items': cart_items,'cart_total': cart_total})

def about(request):
    return render(request, 'about.html')

def contact(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('msg')
        query = Queries.objects.create(user=user, email=email, message=message)
        query.save()
        return redirect('home')
    return render(request, 'contact.html')

