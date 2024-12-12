from django import urls
from django.shortcuts import redirect, render, get_object_or_404
from . models import *
from django.core.paginator import Paginator
from django.db.models import Q
import sqlite3 as sql
import datetime
from django.db.models import Avg

def index(request):
    prs = Product.objects.all().filter(is_available=True)
    count = prs.count()
    context = {
        'products': prs,
        'count': count
    }
    return render(request, "index.html", context)

def store(request, category_slug=None):
    cat = None
    pr = None

    if category_slug != None:
        cate = get_object_or_404(Category,slug = category_slug)
        product = Product.objects.filter(category = cate)
        p = Paginator(product, 3)
        page = request.GET.get('page')
        paged_products = p.get_page(page)
        count = product.count()
    else:
        product = Product.objects.all().filter(is_available=True)
        p = Paginator(product, 3)
        page = request.GET.get('page')
        paged_products = p.get_page(page)
        count = product.count()

    context = {'products':paged_products, 'count': count}

    return render(request, "store/store.html", context)

def product_detail(request, category_slug, product_slug):
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    product_gallery = ImageGallery.objects.filter(product_id=product.id)
    star_range = range(1, 6)
    # Дундаж үнэлгээний тооцоолол
    rate = ReviewRating.objects.filter(product_id=product.id).aggregate(Avg('rating'))['rating__avg']
    average_rating = rate if rate is not None else 0  # Хэрэв үнэлгээ байхгүй бол 0 гэж авна.

    con = sql.connect("db.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f"""SELECT title, review, username, pro_image FROM 
        (auth_user INNER JOIN accounts_account
        ON auth_user.id = accounts_account.user_id) 
        INNER JOIN store_reviewrating
        ON accounts_account.user_id = store_reviewrating.user_id 
        WHERE product_id={product.id}""")

    comments = cur.fetchall()

    context = {
        'single_product': product,
        'product_gallery': product_gallery,
        'rate': average_rating,  # Дундаж үнэлгээ
        'comments': comments,
        'star_range': star_range
    }

    return render(request, "store/product_detail.html", context)

def search(request):
    if 'keyword' in request.GET:
        kw = request.GET['keyword']
        if kw:
            products = Product.objects.filter(Q(product_name__contains=kw) 
            | Q(description__contains=kw))
            count = products.count()

    context = {
        'products': products,
        'count': count,
        'kw': kw,
    }

    return render(request, "store/store.html", context)

def submit_review(request, product_id):
    if request.method == "POST":
        # Create a new review object
        rev = ReviewRating()
        
        # Assign values to the review object
        rev.product_id = product_id
        rev.user_id = request.user.id
        rev.title = request.POST['title']
        rev.review = request.POST['review']
        rev.rating = request.POST['rate']  # This is where the rating is saved
        rev.ip = request.META.get('REMOTE_ADDR')  # To capture the user's IP address

        # Save the review to the database
        rev.save()

        # Redirect to the product page after saving the review
        pr = Product.objects.get(id=product_id)
        return redirect(pr.get_url())
