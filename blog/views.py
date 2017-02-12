from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from blog.models import Posts, Categories
from blog.forms import CommentForm
from django.shortcuts import redirect


# Create your views here.
def blog(request):
    categories = Categories.objects.all()
    posts = Posts.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)  # Show 25 contacts per page
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post = paginator.page(paginator.num_pages)

    context_dict = {'categories': categories, 'posts': post}
    return render(request, 'blog/blog-list.html', context=context_dict)


def view_blog_post(request, slug):
    categories = Categories.objects.all()
    posts = Posts.objects.all()[:5]
    post = get_object_or_404(Posts, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('view_blog_post', slug=post.slug)
    else:
        form = CommentForm()

    context_dict = {'categories': categories, 'posts':posts, 'post': post, 'form': form}
    return render(request, 'blog/blog-detail.html', context=context_dict)


def view_blog_category(request, slug):
    categories = Categories.objects.all()
    category = get_object_or_404(Categories, slug=slug)
    posts = Posts.objects.filter(category=category)[:5]

    context_dict = {'categories': categories, 'category': category, 'posts': posts}
    return render(request, 'blog/blog-category.html', context=context_dict)
