from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('register/', signUp, name='register'),
    path('login/', logIn, name='login'),
    path('logout/', logout_user, name='logout'),
    path('activity/<int:activity_id>', activity, name='activity'),
    path('podcasts/', PodCasts, name='podcasts'),
    path('podcast/<int:pod_id>', PodCast, name='podcast'),
    path('System/', SyStEm, name='sstm'),
    path('delete/', DeLeTe, name='delete'),
    path('update/', UpDaTe, name='update'),
    path('create_article/', create_article, name='create_article'),
    path('articles/', Articles, name='articles'),
    path('article/<int:art_id>', Article, name='article'),
    path('create_quiz/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add_questions/', add_questions, name='add_questions'),
    path('quiz/<int:quiz_id>/add_answers/', add_answers, name='add_answers'),
    path('quiz/<str:article_title>/', take_quiz, name='take_quiz'),
    path('search_users/', search_Users, name='search-users'),
    path('delete_user/<str:user_code>', delete_Users, name='delete-user'),
    path('delete_article/<str:article_title>', delete_Articles, name='delete-article'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
