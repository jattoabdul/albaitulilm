from django.conf.urls import url, include
from bookstore import views as bookstore_views
from django.conf import settings

urlpatterns = [
    url(r'^$', bookstore_views.view_book_list, name='view_book_list'),
    url(r'^book/(?P<slug>[^\.]+)', bookstore_views.view_book_detail, name='view_book_detail'),
    url(r'^category/(?P<slug>[^\.]+)', bookstore_views.view_book_category, name='view_book_category'),
    url(r'^publisher/(?P<slug>[^\.]+)', bookstore_views.view_book_publisher, name='view_book_publisher'),
    url(r'^author/(?P<slug>[^\.]+)', bookstore_views.view_book_author, name='view_book_author'),
    url(r'^download/(?P<path>.*)$', bookstore_views.download_book, name='view_download_book'),
    url(r'^language/(?P<slug>[^\.]+)', bookstore_views.view_book_language, name='view_book_language'),
    url(r'^search/', bookstore_views.search, name='searchresult'),
    url(r'^ratings', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]
