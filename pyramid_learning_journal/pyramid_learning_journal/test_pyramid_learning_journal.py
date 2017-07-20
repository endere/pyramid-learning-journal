"""Test for views creation and link to html pages."""
from pyramid import testing
from pyramid_learning_journal.models import (
    Entry,
    get_tm_session,
)
from pyramid_learning_journal.models.meta import Base
from pyramid_learning_journal.views.default import (
    list_view,
    create_view,
    detail_view,
    edit_view,
    login,
    logout
)
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from faker import Faker
import pytest
import datetime
import transaction
import os


FAKE_STUFF = Faker()
FAKE_ENTRIES = [Entry(
    title=FAKE_STUFF.text(20),
    body=FAKE_STUFF.text(250),
    creation_date=datetime.datetime.now()
) for x in range(25)]


@pytest.fixture
def set_creds():
    """Set credentials for user and secret for tests."""
    from passlib.apps import custom_app_context as context
    os.environ['AUTH_USERNAME'] = 'badman'
    os.environ['AUTH_PASSWORD'] = context.hash('thatsnotthejoker')
    os.environ['SESSION_SECRET'] = 'sneekysnackbox'


@pytest.fixture
def dummy_request(db_session):
    """Make a fake HTTP request."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add entries to a dummy request."""
    dummy_request.dbsession.add_all(FAKE_ENTRIES)


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ.get('TEST_DATABASE')
    })
    config.include('pyramid_learning_journal.models')
    config.include('pyramid_learning_journal.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="session")
def testapp(request):
    """Create a test application to use for functional tests."""
    from webtest import TestApp

    def main(global_config, **settings):
        """Function returns a fake Pyramid WSGI application."""
        settings['sqlalchemy.url'] = os.environ.get('TEST_DATABASE')
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('pyramid_learning_journal.models')
        config.include('pyramid_learning_journal.routes')
        config.include('pyramid_learning_journal.security')
        config.add_static_view(name='static',
                               path='pyramid_learning_journal:static')
        config.scan()
        return config.make_wsgi_app()

    app = main({})

    SessionFactory = app.registry['dbsession_factory']
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def teardown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)
    return TestApp(app)


@pytest.fixture
def fill_test_db(testapp):
    """Set fake entries to the db for a session."""
    SessionFactory = testapp.app.registry['dbsession_factory']
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(FAKE_ENTRIES)

    return dbsession


# ----- Unit Tests ----- #

def test_login_returns_dict(dummy_request):
    """Test request to login returns a dict."""
    response = login(dummy_request)
    assert type(response) == dict


def test_login_bad_creds_both(dummy_request):
    """Test login with bad credentials returns error message."""
    dummy_request.method = 'POST'
    dummy_request.POST = {
        'username': 'blergflerg',
        'password': 'asfdsakfmldsa'
    }
    assert login(dummy_request) == {'error': 'Bad username or password'}


def test_login_bad_creds_one(dummy_request, set_creds):
    """Test login with bad password returns error message."""
    dummy_request.method = 'POST'
    dummy_request.POST = {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'asfdsakfmldsa'
    }
    assert login(dummy_request) == {'error': 'Bad username or password'}
    assert type(login(dummy_request)) == dict


def test_login_with_good_creds(dummy_request, set_creds):
    """Test login with good credentials redirects."""
    dummy_request.method = 'POST'
    dummy_request.POST = {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    }
    response = login(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_logout_redirect(dummy_request):
    """Test for redirection upon logout."""
    response = logout(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_list_view_returns_empty_without_db(dummy_request):
    """Test list view returns a dict when called."""
    response = list_view(dummy_request)
    assert len(response['posts']) == 0


def test_filling_fake_db(add_models, db_session):
    """Check for entries added to db."""
    assert len(db_session.query(Entry).all()) == 25


def test_list_view_returns_dict(dummy_request):
    """Test list view returns a dict when called."""
    assert type(list_view(dummy_request)) == dict


def test_detail_view_with_id_raises_except(dummy_request):
    """Test proper error raising with non matching id on detail view."""
    dummy_request.matchdict['id'] = '9000'
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_detail_view_returns_dict_with_db(db_session, dummy_request):
    """Test detail view returns a dict when called."""
    fake = Entry(
        title=u'Stuff',
        body=u'Some thing goes here.',
        creation_date=datetime.datetime.now()
    )
    db_session.add(fake)
    fakeid = str(db_session.query(Entry)[0].id)
    dummy_request.matchdict['id'] = fakeid
    response = detail_view(dummy_request)
    assert type(response) == dict


def test_create_view_returns_dict(dummy_request):
    """Test create view returns a dict when called."""
    assert type(create_view(dummy_request)) == dict


def test_create_view_with_incomplete_post(dummy_request):
    """Test that create view returns the partial input."""
    dummy_request.method = 'POST'
    dummy_request.POST = {'title': 'bobs post', 'body': ''}
    response = create_view(dummy_request)
    assert response['title'] == 'bobs post'


def test_create_view_addes_a_post(dummy_request, db_session):
    """Given a complete post create view adds it to the DB."""
    assert len(db_session.query(Entry).all()) == 0
    dummy_request.method = 'POST'
    dummy_request.POST = {'title': 'bobs post', 'body': 'stuff'}
    create_view(dummy_request)
    assert len(db_session.query(Entry).all()) == 1
    assert db_session.query(Entry).first().title == 'bobs post'


def test_create_view_on_success_redirects(dummy_request):
    """Test that on creation of a new post redirects."""
    dummy_request.method = 'POST'
    dummy_request.POST = {'title': 'morgans post', 'body': 'cake'}
    response = create_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_edit_view_returns_dict_with_db(dummy_request, db_session):
    """Test edit view returns a dict when called with a db."""
    fake = Entry(
        title=u'Stuff',
        body=u'Some thing goes here.',
        creation_date=datetime.datetime.now()
    )
    db_session.add(fake)
    fakeid = str(db_session.query(Entry)[0].id)
    dummy_request.matchdict['id'] = fakeid
    response = edit_view(dummy_request)
    assert type(response) == dict


def test_db_gets_new_entry_with_content(dummy_request, db_session):
    """Test db gets entry with proper content."""
    fake = Entry(
        title=u'Stuff',
        body=u'Some thing goes here.',
        creation_date=datetime.datetime.now()
    )
    db_session.add(fake)
    fakeid = str(db_session.query(Entry)[0].id)
    dummy_request.matchdict['id'] = fakeid
    response = detail_view(dummy_request)
    assert len(db_session.query(Entry).all()) == 1
    assert fake.title in response['entry'].title
    assert fake.body in response['entry'].body


def test_edit_view_with_id_raises_except(dummy_request):
    """Test proper error raising with non matching id on edit view."""
    dummy_request.matchdict['id'] = '9000'
    with pytest.raises(HTTPNotFound):
        edit_view(dummy_request)


def test_edit_view_with_post_changes_an_entry(dummy_request, db_session):
    """Test that a post request changes an entry."""
    fake = Entry(
        title=u'Cake Story',
        body=u'The best cake ever eaten was chocolate!',
        creation_date=datetime.datetime.now()
    )
    db_session.add(fake)
    fakeid = str(db_session.query(Entry)[0].id)
    dummy_request.matchdict['id'] = fakeid
    dummy_request.method = 'POST'
    dummy_request.POST = {'title': 'Pie Story',
                          'body': 'The pie story is better though!'}
    edit_view(dummy_request)
    assert db_session.query(Entry)[0].title == 'Pie Story'
    assert db_session.query(Entry)[0].body == 'The pie story is better though!'


def test_edit_view_on_success_redirects(dummy_request, db_session):
    """Test that on edit of post redirects."""
    fake = Entry(
        title=u'Cake Story',
        body=u'The best cake ever eaten was chocolate!',
        creation_date=datetime.datetime.now()
    )
    db_session.add(fake)
    fakeid = str(db_session.query(Entry)[0].id)
    dummy_request.matchdict['id'] = fakeid
    dummy_request.method = 'POST'
    dummy_request.POST = {'title': 'Pie Story',
                          'body': 'The pie story is better though!'}
    response = edit_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


# # ----- Functional Tests ----- #

def test_user_forbidden_create_page(testapp):
    """Test access blocked for non logged users on create page."""
    testapp.get('/logout')
    response = testapp.get('/journal/new-entry', status=403)
    assert response.status_code == 403


def test_user_forbidden_update_page(testapp):
    """Test access blocked for non logged users on update page."""
    testapp.get('/logout')
    response = testapp.get('/journal/1/edit-entry', status=403)
    assert response.status_code == 403


def test_home_route_has_home_contents(testapp, db_session):
    """Test list view is routed to home page."""
    response = testapp.get('/')
    assert '<h1 class="blog-title">The Pyramid Blog</h1>' in response


def test_home_view_returns_200(testapp, db_session):
    """Test home view with testapp returns 200 OK."""
    response = testapp.get('/')
    assert response.status_code == 200


def test_home_route_has_list_of_entries(fill_test_db, db_session, testapp):
    """Test if there are the right amount of entries on the home page."""
    response = testapp.get('/')
    num_posts = response.html.find_all('h2')
    assert len(num_posts) == 25


def test_new_entry_view_returns_proper_content(testapp, set_creds):
    """New entry view returns the actual content from the html."""
    testapp.post('/login', {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    })
    response = testapp.get('/journal/new-entry')
    assert '<h1 class="blog-title">Create New Entry!</h1>' in response


def test_detail_view_has_single_entry(testapp, db_session):
    """Test that the detail page only brings up one entry."""
    testapp.post('/login', {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    })
    response = testapp.get('/journal/1')
    html = response.html
    assert html.find()
    num_list_items = (len(html.find_all('h2')))
    assert num_list_items == 1


def test_detail_view_returns_proper_content(testapp, db_session):
    """Entry view returns a Response object when given a request."""
    testapp.post('/login', {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    })
    response = testapp.get('/journal/1', status=200)
    html = response.html
    entry = db_session.query(Entry).first()
    assert html.find()
    expected_text = entry.title
    assert expected_text in str(html)


def test_edit_view_has_single_entry(testapp, db_session):
    """Test that the detail page only brings up one entry."""
    testapp.post('/login', {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    })
    response = testapp.get('/journal/1/edit-entry')
    html = response.html
    entry = db_session.query(Entry).first()
    assert html.find()
    assert entry.title in str(html)


def test_edit_view_returns_proper_content(testapp, db_session):
    """Entry view returns a Response object when given a request."""
    testapp.post('/login', {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    })
    response = testapp.get('/journal/1/edit-entry')
    assert '<h1 class="blog-title">Edit Entry</h1>' in response.text


def test_detail_view_with_bad_id(testapp):
    """Test a bad ID to the detail view returns 404 page."""
    response = testapp.get('/journal/9001', status=404)
    assert '404 page not found' in response.text


def test_edit_view_with_bad_id(testapp):
    """Test a bad ID to the edit view returns 404 page."""
    response = testapp.get('/journal/9001/edit-entry', status=404)
    assert '404 page not found' in response.text


def test_detail_entry_has_404(testapp):
    """Check to see if detail view 404s properly."""
    response = testapp.get('/journal/100', status=404)
    html = response.html
    assert html.find()
    expected_text = '404 page not found'
    assert expected_text in str(html)


def test_edit_entry_has_404(testapp):
    """Check to see if edit view 404s properly."""
    response = testapp.get('/journal/100/edit-entry', status=404)
    html = response.html
    assert html.find()
    expected_text = '404 page not found'
    assert expected_text in str(html)


def test_create_view_returns_200(testapp, db_session):
    """Look for a 200 in create view."""
    testapp.post('/login', {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    })
    response = testapp.get('/journal/new-entry')
    assert response.status_code == 200


def test_edit_view_returns_200(testapp, db_session):
    """Look for a 200 in edit view."""
    testapp.post('/login', {
        'username': os.environ.get('AUTH_USERNAME'),
        'password': 'thatsnotthejoker'
    })
    response = testapp.get('/journal/1/edit-entry')
    assert response.status_code == 200


def test_detail_view_returns_200(testapp, db_session):
    """Look for a 200 in detail view."""
    response = testapp.get('/journal/1')
    assert response.status_code == 200


# # ----- Security/CSRF Tests ----- #


def test_login_returns_200(testapp):
    """Test that the response code for the login view is 200."""
    response = testapp.get('/login')
    assert response.status_code == 200


def test_create_view_logged_in_partial_post(testapp):
    """Test that post creation is open when logged and returns partial data."""
    response = testapp.get('/journal/new-entry')
    token = response.html.find('input', {'type': 'hidden'}).attrs['value']
    fake_post = {
        'csrf_token': token,
        'title': '',
        'body': 'sample text'
    }
    response = testapp.post('/journal/new-entry', fake_post)
    assert 'sample text' in response.text


def test_create_view_logged_in_full_post(testapp):
    """Test post creation is open when logged, redirects with a full post."""
    response = testapp.get('/journal/new-entry')
    token = response.html.find('input', {'type': 'hidden'}).attrs['value']
    fake_post = {
        'csrf_token': token,
        'title': 'yes',
        'body': 'sample text'
    }
    response = testapp.post('/journal/new-entry', fake_post)
    assert response.location == 'http://localhost/'
    assert fake_post['title'] in testapp.get('/')
    assert fake_post['body'] in testapp.get('/')


def test_edit_view_logged_in_edit_post(testapp):
    """Test edit is open when logged, redirects, and has the new content."""
    response = testapp.get('/journal/1/edit-entry')
    token = response.html.find('input', {'type': 'hidden'}).attrs['value']
    response_body = response.html.find('textarea',
                                       {'name': 'body'})
    fake_post = {
        'csrf_token': token,
        'title': 'New title for some stuff!',
        'body': response_body
    }
    response = testapp.post('/journal/1/edit-entry', fake_post)
    assert response.location == 'http://localhost/journal/1'
    assert fake_post['title'] in testapp.get('/journal/1')
