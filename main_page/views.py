from django.shortcuts import render, redirect
from .models import Category, Product, Backet
from . import models
from . forms import SearchForm
from telebot import TeleBot
# Create your views here.
bot = TeleBot('6044834919:AAG3L_ILVQpl1xRpUbsf0FPNhzKHH_4vK_s', parse_mode='HTML')
def index(request):
    all_categories = Category.objects.all()
    all_product = Product.objects.all()
    search_bar =SearchForm()

    context ={'all_categories': all_categories,
              'all_product': all_product,
              'form': search_bar}

    if request.method == 'POST':
        product_find = request.POST.get('search_product')
        try:
            search_result = Product.objects.get(product_name=product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')
    return render(request, 'index.html', context)

# def current_category(request, pk):
#     category = Product.objects.get(id=pk)
#
#     context = {'category': category}
#
#     return render(request, 'current_category.html', context)

def get_exact_categeory(request, pk):
    exact_category = Category.objects.get(id=pk)
    categories = models.Category.objects.all()
    category_products = Product.objects.filter(product_category=exact_category)
    return render(request, 'categrory_products.html', {'category_products': category_products,
                                                       'categories': categories})

def exact_product(request, pk):

    product = models.Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == 'POST':
        models.Backet.objects.create(user_id=request.user.id,
                                     user_product=product,
                                     user_product_quantity=request.POST.get('user_product_quantity'),
                                     total_for_product= product.product_price*int(request.POST.get('user_product_quantity')))
        return redirect('/cart')
    return render(request, 'about_product.html', context)

def get_user_cart(request):
    user_cart = models.Backet.objects.filter(user_id=request.user.id)
    context = {'backet': user_cart}
    return render(request, 'user_cart.html', context)

def complete_order(request):
    user_cart = models.Backet.objects.filter(user_id=request.user.id)
    result_message = 'Новый заказ(Сайт)\n\n'
    total_for_all_cart = 0
    for cart in user_cart:
        result_message+=f'<b>{cart.user_product}</b> x {cart.user_product_quantity} = {cart.total_for_product} \n'

        total_for_all_cart += cart.total_for_product
    result_message += f'\n----------\n{total_for_all_cart}'
    bot.send_message(71944170, result_message )
    return redirect('/')