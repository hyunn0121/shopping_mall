# <product의 models.py>
from django.db import models
from django.contrib.auth.models import User
from category.models import Category # Category model import?
from manufacturer.models import Manufacturer
from tag.models import Tag
import os

# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=30)  # 상품명
    content = models.TextField()  # 간단한 설명

    price = models.IntegerField() # 상품 가격

    # 이미지 필드 추가
    head_image = models.ImageField(upload_to='product/images/%Y/%m/%d/', blank=True)

    # 카테고리 다대일 관계 연결
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # 제조사 다대일 관계 연결
    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL)

    # 태그 다대다 관계 연결
    tags = models.ManyToManyField(Tag, blank=True)

    # 그 외의 필드 1개 추가
    volume = models.CharField(max_length=10, null=True)


    def __str__(self):
        return f'[{self.pk}] {self.title} - {self.manufacturer} [{self.category}]'

    def get_absolute_url(self):
        return f'/product/{self.pk}'

    # def get_avatar_url(self):
    #     if self.author.socialaccount_set.exists() :
    #         return self.author.socialaccount_set.first().get_avatar_url() # first() = 결국 google쪽에서 로그인 한 것에서 이 함수를 호출하겠다는 것
    #
    #     else : # socialaccount로 가입한 사용자가 아니고 그냥 이메일로 가입해서 로그인한 사용자인 경우에는 일반 dummy 이미지를 출력
    #         return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

class Comment(models.Model) :  # post 밑에 붙는 모델이기 때문에 post가 먼저 선언되어야 함 -> post 밑에 class를 선언해주기
    post = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}' # id를 나타내주는 url 주소는 '#'으로 표현

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists() :
            return self.author.socialaccount_set.first().get_avatar_url() # first() = 결국 google쪽에서 로그인 한 것에서 이 함수를 호출하겠다는 것

        else : # socialaccount로 가입한 사용자가 아니고 그냥 이메일로 가입해서 로그인한 사용자인 경우에는 일반 dummy 이미지를 출력
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'
