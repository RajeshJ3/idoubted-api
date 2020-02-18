from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%I:%M %p (%d %b)")

    class Meta:
        model = News
        fields = '__all__'
