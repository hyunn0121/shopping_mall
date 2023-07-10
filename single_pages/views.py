from django.shortcuts import render
from product.models import Item


# Create your views here.
def landing(request):
    recent_post = Item.objects.order_by('-pk')[:3]

    return render(request, 'single_pages/landing.html', {
        'recent_posts': recent_post,
    })


def about_company(request):
    return render(request, 'single_pages/about_company.html')
