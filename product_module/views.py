from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from utils.http_service import get_client_ip

# from django.http import Http404
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductComment
# from django.db.models import Avg
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView
from site_module.models import SiteBanner
from utils.convertors import group_list


# Create your views here.
class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorite")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_detail)
        context['comments'] = ProductComment.objects.filter(product_id=loaded_product.id, parent=None).order_by(
            '-create_date').prefetch_related('productcomment_set')
        context['comments_count'] = ProductComment.objects.filter(product_id=loaded_product.id).count()
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries'] = group_list(galleries, 3)
        related_products = list(
            Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12])
        context['related_products'] = group_list(related_products, 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, )
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)


def add_product_comment(request):
    if request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        product_comment = request.POST.get('product_comment')
        parent_id = request.POST.get('parent_id')
        print(product_id, product_comment, parent_id)
        new_comment = ProductComment(product_id=product_id, parent_id=parent_id, text=product_comment,
                                     user_id=request.user.id)
        new_comment.save()
        context = {
            'comments': ProductComment.objects.filter(product_id=product_id, parent=None).order_by(
                '-create_date').prefetch_related('productcomment_set'),
            'comments_count': ProductComment.objects.filter(product_id=product_id).count()
        }

        return render(request, 'product_module/includes/product_comments_partial.html', context)

    return HttpResponse('response')
