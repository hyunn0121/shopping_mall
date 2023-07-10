from django.shortcuts import render, redirect
from .models import Item, Category, Tag, Comment, Manufacturer
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets

# Create your views here.

class PostCreate(LoginRequiredMixin, CreateView) :
    model = Item
    fields = ['title', 'content', 'price', 'head_image', 'category', 'manufacturer']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str :
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';')
                tag_list = tags_str.split(';')
                for t in tag_list :
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created :
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response

        else :
            return redirect('/product/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Item.objects.filter(category=None).count
        return context

class PostUpdate(LoginRequiredMixin, UpdateView) :
    model = Item
    fields = ['title', 'content', 'price', 'head_image', 'category', 'manufacturer']
    template_name = 'product/item_update_form.html'


    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()  # 모든 tag를 지우고 새롭게 추가하겠다?

        tags_str = self.request.POST.get(
            'tags_str')  # 'tags_str'의 값을 모두 가져오기? / 앞의 tags_str은 변수 / 뒤의 'tags_str'은 post_form.html에서 지정한 입력받은 tags_str를 의미

        if tags_str:
            tags_str = tags_str.strip()  # strip() : 앞 뒤에 공백이 있다면 제거해주는 것
            tags_str = tags_str.replace(',',
                                        ';')  # ,로 되어있는 구분자를 다 ;으로 변경(대체)하겠다는 것 + 다른 구분자를 쓰고 싶다면 ',' 자리에 원하는 구분자를 넣어주면 됨
            tag_list = tags_str.split(';')  # 하나의 문자열로 되어있는 (전달받은) tags_str을 단어별로 분리해서 tag_list라는 배열에 저장해주기

            for t in tag_list:
                t = t.strip()  # 앞뒤 공백 제거
                tag, is_tag_created = Tag.objects.get_or_create(
                    name=t)  # get_or_create : 주어진 tag를 name으로 하는데 있으면 get하고 없으면 create

                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()

                self.object.tags.add(tag)

        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Item.objects.filter(category=None).count
        return context


class PostList(ListView):
    model = Item
    ordering = 'pk'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Item.objects.filter(category=None).count
        return context

def category_page(request, slug):

    if slug == 'no_category' :
        category = '미분류'
        item_list = Item.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        item_list = Item.objects.filter(category=category)

    return render(request, 'product/item_list.html', {
        'category' : category,  #'' 안의 category는 template 쪽에서 사용하는 변수인 category
        'item_list': item_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Item.objects.filter(category=None).count()
    })

# def manufacturer_page(request, slug) :
#     manufacturer = Manufacturer.obejcts.get(slug=slug)
#     item_list = manufacturer.item_set.all()
#
#     return render(request, 'product/manufacturer_list.html', {
#         'manufacturer' : manufacturer,
#         'item_list ' : item_list,
#         'categories' : Category.objects.all(),
#         'no_category_post_count' : Item.objects.filter(category=None).count
#
#     })

def tag_page(request, slug) :
    tag = Tag.objects.get(slug=slug)
    item_list = tag.item_set.all()

    return render(request, 'product/item_list.html', {
        'tag' : tag,
        'item_list' : item_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Item.objects.filter(category=None).count
    })

class PostDetail(DetailView):
    model = Item

def get_context_data(self, *, object_list=None, **kwargs):
    context = super(PostDetail, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Item.objects.filter(category=None).count()
    context['comment_form'] = CommentForm
    return context

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Item, pk=pk)

        if request.method == 'Item' :
            comment_form = CommentForm(request.Item)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())

        else : # GET
            return redirect(post.get_absolute_url())

    else : # 로그인 안한 사용자
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    # 템플릿 : 이름이 comment_form인 템플릿이 자동으로 불러짐

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)

        else : # expection 발생
            raise PermissionDenied

def delete_comment(request, pk) :
    comment = get_object_or_404(Comment, pk = pk)
    post = comment.post

    if request.user.is_authenticated and request.user == comment.author :
        comment.delete()
        return redirect(post.get_absolute_url())

    else :
        PermissionDenied

# serach 클래스 정의 !!
class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']

        post_list = Item.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()
        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'

        return context

