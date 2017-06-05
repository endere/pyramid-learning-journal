"""Views for learning journal."""
from pyramid.view import view_config
from pyramid_learning_journal.data.data import Posts
from pyramid.httpexceptions import HTTPNotFound
from pyramid_learning_journal.models import Entry


@view_config(route_name='home', renderer='../templates/home.jinja2')
def list_view(request):
    """Open home page with list of entries."""
    session = request.dbsession
    all_entries = session.query(Entry).all()
    return {'page': 'home', "posts": all_entries}


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """Open individual entry page."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    entry = session.query(Entry).get(the_id)
    if not entry:
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
    session = request.dbsession
    entry = session.query(Entry).get(the_id)
    if not entry:
        raise HTTPNotFound
    return{'page': 'edit', 'entry': entry}

#entry = list(filter(lambda itemL item['id'] == the_id, JOURNAL ENTRIES))