from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Author, Quote


def user_is_added(view_func):
    def _wrapped_view(request, *args, **kwargs):
        author = kwargs.get('author')
        quote_id = kwargs.get('quote_id')

        if author:
            author = get_object_or_404(Author, fullname=author)
            if author.user != request.user:
                raise PermissionDenied("You don't have permission to access this.")
        elif quote_id:

            quote = get_object_or_404(Quote, id=quote_id)
            if quote.user != request.user:
                raise PermissionDenied("You don't have permission to access this.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
