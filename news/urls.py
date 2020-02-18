from django.urls import path, include
from .views import gadgetsnow_generate_news, news18_generate_news, news_list, single_news

urlpatterns = [
    path('generate/gadgetsnow/', gadgetsnow_generate_news),
    path('generate/news18/', news18_generate_news),
    path('single/', single_news),
    path('', news_list)
]
