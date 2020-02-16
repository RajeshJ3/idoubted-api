from django.urls import path, include
from rest_framework import routers
from .views import NewsViewSet, gadgetsnow_generate_news, news18_generate_news

router = routers.DefaultRouter()
router.register(r"", NewsViewSet)

urlpatterns = [
    path('generate/gadgetsnow/', gadgetsnow_generate_news),
    path('generate/news18/', news18_generate_news),
    path('', include(router.urls)),
]
