from django.db import models
from django.utils.text import slugify


CATEGORY_CHOICES = (
    ('jobs', 'jobs'),
    ('it-services', 'it-services'),
    ('social', 'social'),
    ('mobiles', 'mobiles'),
    ('pcs', 'pcs'),
    ('apps', 'apps'),
    ('gaming', 'gaming'),
    ('computing', 'computing'),
    ('who-is', 'who-is'),
    ('more-gadgets', 'more-gadgets'),
    ('tech', 'tech'),
    ('politics', 'politics'),
    ('india', 'india'),
    ('auto', 'auto'),
    ('buzz', 'buzz'),
    ('entertainment', 'entertainment'),
)


class News(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    description = models.CharField(max_length=500)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    image = models.CharField(max_length=300)
    views = models.IntegerField(default=0)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while News.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        slug = unique_slug
        return slug
