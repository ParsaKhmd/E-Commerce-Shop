from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from article_module.models import Article, ArticleCategory, ArticleComment
from django.utils.encoding import force_str


# Create your views here.

class ArticleListView(ListView):
    template_name = 'article_module/article_page.html'
    model = Article
    paginate_by = 5

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


def article_categories_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,
                                                                                                     parent_id=None)
    context = {
        'main_categories': article_main_categories
    }
    return render(request, 'article_module/components/article_categories_component.html', context)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by(
            '-create_date').prefetch_related(
            'articlecomment_set')
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()

        return context


def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        request.encoding = 'utf-8'
        article_id = request.POST.get('article_id')
        article_comment = request.POST.get('article_comment')
        parent_id = request.POST.get('parent_id')

        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id,
                                     parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by(
                '-create_date').prefetch_related('articlecomment_set'),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
        }

        return render(request, 'article_module/includes/article_comments_partial.html', context)

    return HttpResponse('response')