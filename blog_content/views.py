from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Posts, Comentaries
from .forms import CommentForm
from django.db.models import Q, Count, Case, When


class PostIndex(ListView):
    template_name = 'index.html'
    paginate_by = 12
    model = Posts
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(published=True).order_by('-id')
        qs = qs.select_related('user', 'post_category')
        qs = qs.annotate(
            number_of_comments=Count(
                Case(When(comentaries__published=True, then=1)))
        )

        return qs


class PostDetail(DetailView):
    template_name = 'details.html'
    model = Posts
    context_object_name = 'post'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(published=True).order_by('-id')
        qs = qs.select_related('user', 'post_category')
        qs = qs.annotate(
            number_of_comments=Count(
                Case(When(comentaries__published=True, then=1)))
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        comments = Comentaries.objects.filter(
            post=self.get_object(), published=True)
        comments = comments.order_by('-id')
        context['comments'] = comments
        return context

    def post(self, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(self.request.POST or None)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            messages.success(
                self.request,
                'Comment sent for review.'
            )
        else:
            messages.error(
                self.request,
                'Invalid form. Please correct the fields below.'
            )

        return redirect('blog_content:details', pk=post.pk, slug=post.slug)


class PostCategory(PostIndex):
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('slug', None)

        if not category:
            return qs

        qs = qs.filter(post_category__slug=category,
                       published=True).order_by('-id')
        return qs


class PostSearch(PostIndex):
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')

        if not search:
            return qs

        qs = qs.filter(
            Q(title__icontains=search) |
            Q(slug__icontains=search) |
            Q(user__first_name__iexact=search) |
            Q(content__icontains=search) |
            Q(excerpt__icontains=search) |
            Q(keywords__icontains=search) |
            Q(post_category__name__icontains=search) |
            Q(post_category__slug__icontains=search) |
            Q(publication_date__icontains=search) |
            Q(update_date__icontains=search)
        ).order_by('-id')

        return qs
