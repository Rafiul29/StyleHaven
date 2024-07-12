from django.shortcuts import render,get_list_or_404
from store.models import Product
from category.models import Category

def home(request):
    
    products=Product.objects.all().filter

    context={
        "products":products,
    }
    
    return render(request,'home.html',context)