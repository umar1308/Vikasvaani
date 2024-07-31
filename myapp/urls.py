from django.contrib import admin
from django.urls import path
from myapp import views
# from .views import save_session

urlpatterns = [
    path('', views.index,name="index"),
    path('register.html', views.register,name="register"),
    path('login.html', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('about.html', views.about,name="about"),
    path('testform.html', views.testform,name="testform"),
    path('quiz/questions/<str:field_of_study>/', views.get_questions, name='get_questions'),
    path('allcourse.html', views.allcourse, name='allcourse'),
    path('api/my-view/', views.my_view, name='my_view'),
    path('report/', views.reportfunc, name='reportfunc'),
    path('reportnotfound.html', views.reportnotfound, name='reportnotfound'),
    path('ngoenroll.html', views.ngoenroll, name='ngoenroll'),
    path('explore.html', views.explore, name='explore'),
    path('tc.html', views.tc, name='tc'),
    path('pp.html', views.profile, name='profile'),
]