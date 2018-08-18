from django.db import models
from django.utils.text import slugify


class DefaultModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BookRack(DefaultModel):
    name = models.CharField(null=False, blank=False, max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    @property
    def total_books(self):
        return self.book_set.count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BookRack, self).save(*args, **kwargs)


class Author(DefaultModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)

    @property
    def total_books(self):
        return self.book_set.count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)


class Book(DefaultModel):
    book_rack = models.ForeignKey(BookRack, on_delete=models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)
    authors = models.ManyToManyField(Author)
    published_year = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)


