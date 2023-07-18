from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, NewsCategoryView, CategoryDetailView, UnsubscribeCategory, SubscribeCategory, СategoryCreateView
from django.views.decorators.cache import cache_page  # cache


urlpatterns = [
    path('', cache_page(60*2)(PostsList.as_view())),
    path('<int:pk>/', PostDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('add/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('categories/', NewsCategoryView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView, name='category'),
    path('categories/unsubscribe/<int:pk>/', UnsubscribeCategory, name='category_unsubscribe'),
    path('categories/subscribe/<int:pk>/', SubscribeCategory, name='category_subscribe'),
    path('category/create/', СategoryCreateView.as_view(), name='create_category'),
]
