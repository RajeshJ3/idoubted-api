from django.shortcuts import render
from rest_framework import viewsets
from .serializers import NewsSerializer
from .models import News
from .news.gadgetsnow import gadgetsnow_generate
from .news.news18 import news18_generate


def gadgetsnow_generate_news(request):
    gadgetsnow_generate()


def news18_generate_news(request):
    news18_generate()


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(publish=True).order_by('-time')
    serializer_class = NewsSerializer
    lookup_field = 'slug'
