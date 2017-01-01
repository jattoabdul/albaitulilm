from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Category Title')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    details = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Category Details')

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def __str__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return 'view_book_category', None, {'slug': self.slug}


class Publisher(models.Model):
    name = models.CharField(max_length=30, verbose_name='Publisher\'s Company Name')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    address = models.CharField(max_length=50, verbose_name='Publisher\'s Address')
    city = models.CharField(max_length=60, verbose_name='Publisher\'s City')
    state_province = models.CharField(max_length=30, verbose_name='Publisher\'s State Province')
    country = models.CharField(max_length=50, verbose_name='Publisher\'s Country')
    website = models.URLField(verbose_name='Publisher\'s Website', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Publishers"

    def __str__(self):
        return '%s' % self.name

    @permalink
    def get_absolute_url(self):
        return 'view_book_publisher', None, {'slug': self.slug}


class Author(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Author\'s First Name')
    last_name = models.CharField(max_length=40, verbose_name='Author\'s Last Name')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    image = models.ImageField(upload_to='authors', verbose_name='Author\'s Avatar', blank=True)
    bio = models.TextField(verbose_name='Author\'s Biography', blank=True)
    email = models.EmailField(verbose_name='Author\'s Email Address', blank=True)
    nationality = models.CharField(max_length=50, verbose_name='Author\'s Nationality', blank=True)
    phone_no = models.CharField(max_length=15, verbose_name='Author\'s Phone Number', blank=True)
    fb_username = models.CharField(max_length=100, verbose_name='Facebook Username', blank=True)
    twitter_handle = models.CharField(max_length=100, verbose_name='Twitter Handle', blank=True)
    linkedin_username = models.CharField(max_length=100, verbose_name='Linkedin Username', blank=True)
    dribble_username = models.CharField(max_length=100, verbose_name='Dribble Username', blank=True)

    class Meta:
        ordering = ['first_name']
        verbose_name_plural = "Authors"

    def __str__(self):
        return '%s' % self.first_name + ' ' + self.last_name

    @permalink
    def get_absolute_url(self):
        return 'view_book_author', None, {'slug': self.slug}


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name='Language Name')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Languages"

    def __str__(self):
        return '%s' % self.name

    @permalink
    def get_absolute_url(self):
        return 'view_book_language', None, {'slug': self.slug}


class Book(models.Model):
    # id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=150, unique=True, verbose_name='Book Title')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Book URL')
    intro = models.CharField(max_length=250, verbose_name='Book Introductory Highlight', blank=True)
    description = models.TextField(verbose_name='Book Detailed Description', blank=True)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    language = models.ForeignKey(Language)
    category = models.ForeignKey(Categories)
    uploaded_by = models.ForeignKey(User, null=True, blank=True)
    pg_number = models.IntegerField(verbose_name='Book Page Numbers', blank=True)
    cover_image = models.ImageField(upload_to='bookcoverimages/%Y/%m/%d/',
                                    verbose_name='Books Cover Image',
                                    blank=True)
    publication_year = models.DateField(verbose_name='Publication Year')
    download_no = models.IntegerField(verbose_name='Number of Book Downloads', default=0)
    isbn = models.CharField(max_length=25, verbose_name='Book ISBN Number', blank=True)
    price = models.DecimalField(verbose_name='Book Price',
                                max_digits=6, decimal_places=2,
                                help_text='book price in dollars e.g $0.00')
    tags = TaggableManager()
    upload = models.FileField(verbose_name='Book File Upload',
                              upload_to='books/%Y/%m/%d/',
                              help_text='Upload the Book Here')
    uploaded_on = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Date of Book Upload',
                                       help_text='Day and time the book was uploaded')

    class Meta:
        ordering = ['title']  # , '-uploaded_on'
        verbose_name_plural = "Books"

    def __str__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return 'view_book_detail', None, {'slug': self.slug}


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews')
    author = models.CharField(max_length=200)
    email = models.EmailField(max_length=75)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_review = models.BooleanField(default=False)

    def approve(self):
        self.approved_review = True
        self.save()

    def __str__(self):
        return self.text
