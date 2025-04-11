from unicodedata import category

from django.db import models
from django.db.models import ManyToManyField
from django.utils.text import slugify



# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(max_length=100,  blank=True)
    description = models.TextField(blank=True, null=True)
    programming_language = models.CharField(max_length=20)
    technologies = models.CharField(max_length=100, blank=True)
    category = ManyToManyField('Category', blank=True)
    github_link = models.URLField(blank=True, null=True)
    live_demo_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects', blank=True, null=True)
    image2 = models.ImageField(upload_to='projects', blank=True, null=True)
    image3 = models.ImageField(upload_to='projects', blank=True, null=True)
    video = models.FileField(upload_to='projects', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Categories'