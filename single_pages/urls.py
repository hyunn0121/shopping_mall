from django.urls import path
from . import views

urlpatterns = [   # IP주소/ (IP 주소만 가지고 왔을 때 전달되는 것을 적어주면 됨)
    path('', views.landing),          # IP주소/
    path('about_company/', views.about_company) # IP주소/about_me (IP주소 뒤에 about_me가 왔을 경우에 views 밑에 있는 about_me를 보여줘라)
]
