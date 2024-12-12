from . models import Category

def menus(request):
    cat = Category.objects.all() 
    return dict(links = cat)
