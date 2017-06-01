"""Views for learning journal."""
from pyramid.response import Response
from pyramid.view import view_config
from pyramid_learning_journal.data.data import Posts
from pyramid.httpexceptions import HTTPNotFound
import os
import io

HERE = os.path.dirname(__file__)


@view_config(route_name='home', renderer='../templates/home.jinja2')
def list_view(request):
    """Open home page with list of entries."""
    return {'page': 'home', "posts": Posts}


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """Open individual entry page."""
    # import pdb; pdb.set_trace()
    the_id = int(request.matchdict['id'])
    entry = None
    for item in Posts:
        if item['id'] == the_id:
            entry = item
            break
    if entry is None:
        raise HTTPNotFound
    return{'page': 'detail', 'entry': entry}


@view_config(route_name='create', renderer='../templates/create.jinja2')
def create_view(request):
    """Open new entry page."""
    return {'page': 'create'}


@view_config(route_name='edit', renderer='../templates/edit.jinja2')
def edit_view(request):
    """Open edit entry page."""
    the_id = int(request.matchdict['id'])
    entry = None
    for item in Posts:
        if item['id'] == the_id:
            entry = item
            break
    if entry is None:
        raise HTTPNotFound
    return{'page': 'edit', 'entry': entry}

#entry = list(filter(lambda itemL item['id'] == the_id, JOURNAL ENTRIES))