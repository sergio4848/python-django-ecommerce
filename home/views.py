from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, FAQ
from order.models import ShopCart
from product.models import Category, Product, Images, Comment


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    sliderdata = Product.objects.all()[:6]
    dayproducts = Product.objects.filter(category='2')[:]
    lastproducts = Product.objects.all().order_by('-id')[:3]
    randomproducts = Product.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context={
        'page':'home',
        'category':category,
        'sliderdata': sliderdata,
        'setting': setting,
        'dayproducts': dayproducts,
        'lastproducts': lastproducts,
        'randomproducts': randomproducts,

             }
    return render(request,'index.html',context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={

        'setting':setting,
        'category': category,
             }
    return render(request,'hakkimizda.html',context)

def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={

        'setting':setting,
        'category': category,
             }
    return render(request,'references.html',context)


def contact(request):
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    category = Category.objects.all()
    context={

        'setting':setting,
        'form':form,
        'category': category,
             }
    return render(request,'contact.html',context)


def category_products(request,id,slug):
    products = Product.objects.filter(category_id=id)
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)

    context = {'products':products,
               'category':category,
               'slug':slug,
               'setting': setting,
               'categorydata':categorydata,
               }
    return render(request,'products.html',context)


def product_detail(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    lastproducts = Product.objects.all().order_by('-id')[:4]
    image = Images.objects.filter(product_id=id)

    context = {
                'product':product,

               'category': category,
               'slug': slug,
               'setting': setting,
                'image':image,
        'lastproducts': lastproducts,
               }
    return render(request,'product_detail.html',context)




def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/')


def login_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş başarısız. Tekrar Deneyiniz.")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category,
        'setting': setting,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form':form,
        'setting': setting,
    }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all()
    setting = Setting.objects.get(pk=1)


    context = {
        'faq': faq,
        'category':category,
        'setting':setting,

    }
    return render(request, 'faq.html', context)