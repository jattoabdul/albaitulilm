from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.http import Http404
from bookstore.forms import ContactForm
from django.utils.encoding import smart_str
from django.shortcuts import render, get_object_or_404, redirect, render_to_response, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from bookstore.models import *
from django.utils.translation import ugettext as _, ugettext_noop as _noop
from bookstore.search import *
from bookstore.forms import *
from django.http import HttpResponse


# Create your views here.
# view_book_list also index view - home view
def index(request):
    new_book_releases = Book.objects.all().filter(is_public=True)[:4]  # order_by('-publication_year')
    top_writers = Author.objects.all()[:4]  # change query to author with highest no of books (order_by('book'))
    context_dict = {'new_book_releases': new_book_releases, 'top_writers': top_writers}
    return render(request, "bookstore/index.html", context_dict)


# view book list function
def view_book_list(request):
    categories = Categories.objects.all()
    most_recent_books = Book.objects.all().filter(is_public=True)[:3]  # order_by(-'uploaded_on')
    most_recent_books_2 = Book.objects.all().filter(is_public=True)[3:6]  # order_by(-'uploaded_on')
    most_downloaded_books = Book.objects.all().order_by('-download_no').filter(is_public=True)[:3]
    books = Book.objects.all().filter(is_public=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(books, 12)  # Show 12 books per page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    context_dict = {'categories': categories, 'books': books, 'most_recent_books': most_recent_books,
                    'most_recent_books_2': most_recent_books_2, 'most_downloaded_books': most_downloaded_books}
    return render(request, "bookstore/book_list.html", context_dict)


# view book detail function
def view_book_detail(request, slug):
    categories = Categories.objects.all()
    book = get_object_or_404(Book, slug=slug)
    related_books = Book.objects.all().filter(is_public=True)[:3]  # authors__in='book.authors'
    most_recent_books = Book.objects.all().filter(is_public=True)[:3]  # order_by(-'uploaded_on')
    most_recent_books_2 = Book.objects.all().filter(is_public=True)[3:6]  # order_by(-'uploaded_on')
    most_downloaded_books = Book.objects.all().order_by('-download_no').filter(is_public=True)[:3]
    tags = book.tags.all()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return redirect('view_book_detail', slug=book.slug)
    else:
        form = ReviewForm()

    context_dict = {'categories': categories, 'related_books': related_books, 'book': book,
                    'most_recent_books': most_recent_books, 'most_recent_books_2': most_recent_books_2,
                    'most_downloaded_books': most_downloaded_books, 'tags': tags, 'form': form}
    return render(request, "bookstore/book_detail.html", context_dict)


# def download_book(request, slug):
#     book = Book.objects.get(slug=slug)
#     path_to_file = book.upload.path
#
#     response = HttpResponse(content_type='application/force-download')
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(book.title)
#     response['X-Sendfile'] = smart_str(path_to_file)
#     return response


def download_book(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            response['X-Sendfile'] = smart_str(file_path)
            return response
    else:
        raise Http404


# List of views to create
def view_book_category(request):
    context_dict = locals()
    return render(request, "bookstore/book_category.html", context_dict)


def view_book_publisher(request):
    context_dict = locals()
    return render(request, "bookstore/book_publisher.html", context_dict)


def view_book_author(request):
    context_dict = locals()
    return render(request, "bookstore/book_author.html", context_dict)


def view_book_language(request):
    context_dict = locals()
    return render(request, "bookstore/book_language.html", context_dict)


# Search View function
def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'description', 'intro', ])  # 'publisher__name',
        found_entries = Book.objects.filter(entry_query).order_by('-uploaded_on')
    context_dict = {'query_string': query_string, 'found_entries': found_entries}
    return render(request, "common/searchresult.html", context_dict)


# Contact view
def contact(request):
    form_class = ContactForm
    # if request is not post, initialize an empty form
    form = form_class(request.POST or None)
    confirm_message = None
    # contact form logic!
    # if request.method == 'POST':
    if form.is_valid():
        contact_name = form.cleaned_data.get('contact_name', None)
        contact_email = form.cleaned_data.get('contact_email', None)
        comment = form.cleaned_data.get('content', None)
        subject = 'New Message from users on www.baitulilm.com'
        message = '%s %s' %(comment, contact_name)
        email_to = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, contact_email, email_to, fail_silently=True)
        confirm_message = "Thank you for the message. We will get right back to you ASAP."
        form = None

    context_dict = {'form': form, 'confirm_message': confirm_message, }
    template = 'bookstore/contact.html'
    return render(request, template, context_dict)