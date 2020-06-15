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
    newCategory = ""

    if category == "Tech news":
        newCategory = "tech"
    elif category == "Jobs news":
        newCategory = "jobs"
    elif category == "IT Services news":
        newCategorynewCategory = "it-services"
    elif category == "Social news":
        newCategory = "social"
    elif category == "Mobiles news":
        newCategory = "mobiles"
    elif category == "PC's news":
        newCategory = "pcs"
    elif category == "Apps news":
        newCategory = "apps"
    elif category == "Gaming news":
        newCategory = "gaming"
    elif category == "Computing news":
        newCategory = "computing"
    elif category == "Who is news":
        newCategory = "who-is"
    elif category == "More Gadgets news":
        newCategory = "more-gadgets"
    elif category == "Politics news":
        newCategory = "politics"
    elif category == "India news":
        newCategory = "india"
    elif category == "Auto news":
        newCategory = "auto"
    elif category == "Buzz news":
        newCategory = "buzz"
    elif category == "Entertainment news":
        newCategory = "entertainment"
    else:
        newCategory = False

    if index == -1:
        if newCategory:
            news = News.objects.filter(Q(publish=True) & Q(
                category=newCategory)).order_by('-time')[0:25]
        else:
            news = News.objects.filter(publish=True).order_by('-time')[0:25]
    else:
        if newCategory:
            news = News.objects.filter(Q(publish=True) & Q(
                pk__lt=index) & Q(category=newCategory)).order_by('-time')[0:25]
        else:
            news = News.objects.filter(Q(publish=True) & Q(
                pk__lt=index)).order_by('-time')[0:25]
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def single_news(request):
    slug = request.data.get("url")
    news = News.objects.get(slug=slug)
    serializer = NewsSerializer(news, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
