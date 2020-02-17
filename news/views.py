from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from django.db.models import Q
from .serializers import NewsSerializer
from .models import News
from .news.gadgetsnow import gadgetsnow_generate
from .news.news18 import news18_generate


def gadgetsnow_generate_news(request):
    gadgetsnow_generate()


def news18_generate_news(request):
    news18_generate()


@api_view(['POST'])
@permission_classes([AllowAny])
def news_list(request):
    index = request.data.get("index")
    category = request.data.get("category")

    if category == "Tech news":
        category = "tech"
    else:
        category = False

    if index == -1:
        if category:
            news = News.objects.filter(Q(publish=True) & Q(
                category=category)).order_by('-time')[0:5]
        else:
            news = News.objects.filter(publish=True).order_by('-time')[0:5]
        serializer = NewsSerializer(news, many=True)
    else:
        if category:
            news = News.objects.filter(Q(publish=True) & Q(
                pk__lt=index) & Q(category=category)).order_by('-time')[0:5]
        else:
            news = News.objects.filter(Q(publish=True) & Q(
                pk__lt=index)).order_by('-time')[0:5]

    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
