"""Views for learning journal."""
from pyramid.response import Response
import os
import io

HERE = os.path.dirname(__file__)


def list_view(request):
    """."""
    with io.open(os.path.join(HERE, '../templates/home.html')) as the_file:
        imported_page = the_file.read()
    print(imported_page)
    return Response(imported_page)


def detail_view(request):
    """."""
    with io.open(os.path.join(HERE, '../templates/detail.html')) as the_file:
        imported_page = the_file.read()
    print(imported_page)
    return Response(imported_page)


def create_view(request):
    """."""
    with io.open(os.path.join(HERE, '../templates/create.html')) as the_file:
        imported_page = the_file.read()
    print(imported_page)
    return Response(imported_page)


def edit_view(request):
    """."""
    with io.open(os.path.join(HERE, '../templates/edit.html')) as the_file:
        imported_page = the_file.read()
    print(imported_page)
    return Response(imported_page)
