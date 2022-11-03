from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from utils.resize_images import resize_image


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            blank=False, verbose_name='Nome')
    slug = models.SlugField(max_length=128, blank=True,
                            null=True, unique=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.name)
            self.slug = new_slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, verbose_name='User')
    post_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False, verbose_name='Category')
    title = models.CharField(max_length=64, blank=False, verbose_name='Title')
    excerpt = models.CharField(
        max_length=255, blank=False, verbose_name='Excerpt')
    keywords = models.CharField(
        max_length=255, blank=False, verbose_name='Keywords')
    slug = models.SlugField(max_length=128, blank=True, verbose_name='Slug')
    content = models.TextField(blank=False, verbose_name='Content')
    image = models.ImageField(
        blank=True, upload_to='post_img/%Y/%m/%d', verbose_name='Image')
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Publication')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Update')
    published = models.BooleanField(default=False, verbose_name='Published')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title)
            self.slug = new_slug

        if self.image:
            self.image = resize_image(self.image, 800)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comentaries(models.Model):
    post = models.ForeignKey(
        Posts, on_delete=models.CASCADE, blank=False, verbose_name='Post')
    name = models.CharField(max_length=64, blank=False, verbose_name='Name')
    email = models.EmailField(
        max_length=64, blank=False, verbose_name='E-mail')
    title = models.CharField(max_length=255, blank=False, verbose_name='Title')
    message = models.TextField(blank=False, verbose_name='Message')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    published = models.BooleanField(default=False, verbose_name='Published')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comentaries'
