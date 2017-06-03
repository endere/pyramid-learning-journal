"""Views for learning journal."""
from pyramid.view import view_config
from pyramid_learning_journal.data.data import Posts
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
    )
from pyramid_learning_journal.models import Entry
import datetime


@view_config(route_name='home', renderer='../templates/home.jinja2')
def list_view(request):
    """Open home page with list of entries."""
    session = request.dbsession
    import pdb; pdb.set_trace()
    all_entries = session.query(Entry).order_by(Entry.id.desc()).all()
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
    if request.method == "POST" and request.POST:
        if not request.POST['title'] or not request.POST['body']:
            return {
                'title': request.POST['title'],
                'body': request.POST['body']
            }
        the_date=datetime.datetime.now()
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body'],
            creation_date=the_date.strftime('%A, %-d %B, %Y, %-I:%M %P')
        )
        print(new_entry)
        request.dbsession.add(new_entry)
        return HTTPFound(
            location=request.route_url('home')
        )
    return {}


@view_config(route_name='edit', renderer='../templates/edit.jinja2')
def edit_view(request):
    """Open edit entry page."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    entry = session.query(Entry).get(the_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        return{'page': 'edit', 'entry': entry}
    if request.method == "POST":
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=entry.id))





