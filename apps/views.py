from django.shortcuts import render, redirect
from .models import User, Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def get_product(product_id):
    return get_object_or_404(Product, id=product_id)

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            # Foydalanuvchi mavjudligini tekshirish
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Bu foydalanuvchi allaqachon mavjud.'})

            User.objects.create(username=username, password=password)
            return redirect('/login/')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username, password=password).first()
        if user:
            return render(request, 'profile.html', {'username': username})
        else:
            return render(request, 'login.html', {'error': 'Login yoki parol noto‘g‘ri.'})

    return render(request, 'login.html')

def logout_view(request):
    return redirect('/login/')

def home_view(request):
    category = request.GET.get('category', None)
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_list(request, category=None):
    if category == 'all' or category is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)

    return render(request, 'home.html', {'products': products})

def succes_view(request):
    return render(request, 'succes.html')

@csrf_exempt
def purchase(request, product_id):
    product = get_product(product_id)
    if request.method == "POST":
        return render(request, 'succes.html', {'product': product, 'Karta raqami': 'Yashiringan (xafsizlik uchun)'})
    return render(request, 'purchase.html', {'product': product})

def profile_view(request):
    username = request.user.username
    return render(request, 'profile.html', {'username': username})