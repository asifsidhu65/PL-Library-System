from django.db import models
from django.utils.text import slugify


def get_unique_slug(model_instance, slugable_field_name, slug_field_name):
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    ModelClass = model_instance.__class__

    while ModelClass._default_manager.filter(
            **{slug_field_name: unique_slug}
    ).exclude(pk=model_instance.pk).exists():
        unique_slug = '{}-{}'.format(slug, extension)
        extension += 1

    return unique_slug


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
        self.slug = get_unique_slug(self, 'name', 'slug')
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
        self.slug = get_unique_slug(self, 'name', 'slug')
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
        self.slug = get_unique_slug(self, 'title', 'slug')
        super(Book, self).save(*args, **kwargs)


