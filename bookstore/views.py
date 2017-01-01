from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bookstore.forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from bookstore.models import *
from django.utils.translation import ugettext as _, ugettext_noop as _noop


# Create your views here.
# view_book_list also index view - home view
def index(request):
    books = Book.objects.all()[:5]
    context_dict = {'books': books}
    return render(request, "bookstore/index.html", context_dict)


def view_book_list(request):
    context_dict = locals()
    return render(request, "bookstore/book_list.html", context_dict)


# List of views to create
def view_book_detail(request):
    context_dict = locals()
    return render(request, "bookstore/book_detail.html", context_dict)


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