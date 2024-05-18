from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from django.utils.translation import gettext as _


User = get_user_model()

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    fullname = models.CharField(max_length=40, blank=True, verbose_name=_("Pełne imię"))
    slug = models.SlugField(max_length=400, unique=True, blank=True, verbose_name=_("Slug"))
    bio = HTMLField(verbose_name=_("Biografia"))
    points = models.IntegerField(default=0, verbose_name=_("Punkty"))
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default=None, null=True, blank=True, verbose_name=_("Zdjęcie profilowe"))

    def __str__(self):
        return self.fullname

    @property
    def num_posts(self):
        return Post.objects.filter(user=self).count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fullname)
        super(Author, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Autor")
        verbose_name_plural = _("Autorzy")

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Tytuł"))
    slug = models.SlugField(max_length=400, unique=True, blank=True, verbose_name=_("Slug"))
    description = models.TextField(default="description", verbose_name=_("Opis"))

    class Meta:
        verbose_name = _("Kategoria")
        verbose_name_plural = _("Kategorie")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("posts", kwargs={
            "slug": self.slug
        })

    @property
    def num_posts(self):
        return Post.objects.filter(categories=self).count()

    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")

class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Autor"))
    content = models.TextField(verbose_name=_("Treść"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Data"))

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name = _("Odpowiedź")
        verbose_name_plural = _("Odpowiedzi")

class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Autor"))
    content = models.TextField(verbose_name=_("Treść"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Data"))
    replies = models.ManyToManyField(Reply, blank=True, verbose_name=_("Odpowiedzi"))

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name = _("Komentarz")
        verbose_name_plural = _("Komentarze")

class Post(models.Model):
    title = models.CharField(max_length=400, verbose_name=_("Tytuł"))
    slug = models.SlugField(max_length=400, unique=True, blank=True, verbose_name=_("Slug"))
    user = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Autor"))
    content = HTMLField(verbose_name=_("Treść"))
    categories = models.ManyToManyField(Category, verbose_name=_("Kategorie"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Data"))
    approved = models.BooleanField(default=False, verbose_name=_("Zatwierdzony"))
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation', verbose_name=_("Licznik wyświetleń"))
    tags = TaggableManager(verbose_name=_("Tagi"))
    comments = models.ManyToManyField(Comment, blank=True, verbose_name=_("Komentarze"))
    closed = models.BooleanField(default=False, verbose_name=_("Zamknięty"))
    state = models.CharField(max_length=40, default="zero", verbose_name=_("Stan"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("detail", kwargs={
            "slug": self.slug
        })

    @property
    def num_comments(self):
        return self.comments.count()

    @property
    def last_reply(self):
        return self.comments.latest("date")

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posty")

    