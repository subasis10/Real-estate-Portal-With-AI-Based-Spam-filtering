from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.choices import price_choices, bedroom_choices

from listings.models import Listing
from realtors.models import Realtor
from spam.views import detect_spam


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    # detect_spam()

    context = {
        'listings': paged_listings

    }

    return render(request, 'listings/listings.html', context)

def listing(request,listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    #keywords
    if 'keywords' in request.GET:
      keywords =request.GET['keywords']
      if keywords:
          queryset_list = queryset_list.filter(description__icontains=keywords)
    
    # City
    if 'city' in request.GET:
      city =request.GET['city']
      if city:
          queryset_list = queryset_list.filter(city__iexact=city)

    
    # Bedrooms
    if 'price' in request.GET:
      price =request.GET['price']
      if price:
          queryset_list = queryset_list.filter(price__lte=price)

     # Price
    if 'bedrooms' in request.GET:
      bedrooms =request.GET['bedrooms']
      if bedrooms:
          queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    context = {
          'bedroom_choices':bedroom_choices,
          'price_choices':price_choices,
          'listings': queryset_list,
          'values': request.GET
    }

    return render(request, 'listings/search.html', context)

def about(request):
    mvp_realtor = Realtor.objects.all().filter(is_mvp=True)
    realtors = Realtor.objects.all()
    context = {
        'mvp_realtors':mvp_realtor,
        'realtors':realtors,
    }
    return render(request, 'pages/about.html',context=context)