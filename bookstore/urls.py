from django.conf.urls import url, include
from bookstore import views as bookstore_views

urlpatterns = [
    url(r'^$', bookstore_views.view_book_list, name='booklist'),
    url(r'^book/', bookstore_views.view_book_detail, name='bookdetail'),
    url(r'^category/', bookstore_views.view_book_category, name='bookcategories'),
    url(r'^publisher/', bookstore_views.view_book_publisher, name='bookpublishers'),
    url(r'^authors/', bookstore_views.view_book_author, name='bookauthors'),
    url(r'^languages/', bookstore_views.view_book_language, name='booklanguages'),
    url(r'^ratings', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]
