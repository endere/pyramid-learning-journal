"""Test for views creation and link to html pages."""
from pyramid import testing
from pyramid_learning_journal.data.data import Posts
import pytest
import os

import transaction
from pyramid_learning_journal.models import (
    Entry,
    get_tm_session,
)
from pyramid_learning_journal.models.meta import Base
from pyramid_learning_journal.views.default import (
    list_view,
    create_view,
    detail_view,
    edit_view
)
from pyramid_learning_journal.models.meta import Base
from pyramid.httpexceptions import HTTPNotFound


@pytest.fixture
def dummy_request(db_session):
    """Make a fake HTTP request."""
    return testing.DummyRequest(dbsession=db_session)


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
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def testapp():
    """Create a test application to use for functional tests."""
    from webtest import TestApp
    from pyramid.config import Configurator
    import os

    def main(global_config, **settings):
        """Function returns a Pyramid WSGI application."""
        settings['sqlalchemy.url'] = os.environ.get('TEST_DATABASE')
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.add_static_view(name='static', path='pyramid_learning_journal:static')
        config.scan()
        return config.make_wsgi_app()

    app = main({})

    return TestApp(app)


@pytest.fixture
def db_session(configuration, request):
    """."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.creat_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """."""
    req = testing.DummyRequest()
    req.dbsession = db_session
    return req


@pytest.fixture
def post_request(dummy_request):
    """."""
    dummy_request.method = "POST"
    return dummy_request


@pytest.fixture
def get_request(dummy_request):
    """."""
    dummy_request.method = "GET"
    return dummy_request


# got to here.


@pytest.fixture
def home_response():
    """Set fixture for home page."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    return response


@pytest.fixture
def new_entry_response():
    """Set fixture for new entry page."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    return response


def test_home_view_page_is_home(home_response):
    """Test if list view is routed to home page."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    assert response['page'] is 'home'


def test_home_route_has_list_of_entries(testapp):
    """Test if there are the right amount of entries on home page."""
    response = testapp.get('/')
    html = response.html
    assert html.find()
    num_list_items = (len(html.find_all('h2')))
    assert num_list_items == len(Posts)


def test_home_view_returns_proper_content(testapp):
    """Home view returns the actual content from the html."""
    response = testapp.get('/')
    html = response.html
    expected_text = '<h1 class="blog-title">The pyramid Blog</h1>'
    assert expected_text in str(html)


def test_new_entry_view_page_is_create(new_entry_response):
    """Test if create_view is routed to create page."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    assert response['page'] is 'create'


def test_new_entry_view_returns_proper_content(testapp):
    """New entry view returns the actual content from the html."""
    response = testapp.get('/journal/new-entry')
    html = response.html
    expected_text = '<h1>New Journal entry</h1>'
    assert expected_text in str(html)


def test_edit_entry_view_returns_proper_content(testapp):
    """Edit entry view returns the actual content from the html."""
    response = testapp.get('/journal/1/edit-entry')
    html = response.html
    assert html.find()
    expected_text = '<h1>Edit Journal entry</h1>'
    assert expected_text in str(html)


def test_detail_entry_has_single_entry(testapp):
    """Check amount of entries on detail entry page."""
    response = testapp.get('/journal/1')
    html = response.html
    assert html.find()
    num_list_items = (len(html.find_all('h2')))
    assert num_list_items == 1


def test_detail_entry_returns_proper_content(testapp):
    """Edit detail view returns the actual content from the html."""
    response = testapp.get('/journal/1')
    html = response.html
    assert html.find()
    expected_text = '<h2 class="blog-post-title">5/27/17 journal</h2>'
    assert expected_text in str(html)


def test_detail_entry_has_404(testapp):
    """Check to see if detail view 404s properly."""
    response = testapp.get('/journal/100', status=404)
    html = response.html
    assert html.find()
    expected_text = '<p class="lead"><span class="font-semi-bold">404</span> Page Not Found</p>'
    assert expected_text in str(html)


def test_edit_entry_has_404(testapp):
    """Check to see if edit view 404s properly."""
    response = testapp.get('/journal/100/edit-entry', status=404)
    html = response.html
    assert html.find()
    expected_text = '<p class="lead"><span class="font-semi-bold">404</span> Page Not Found</p>'
    assert expected_text in str(html)


def test_list_view_returns_dict(dummy_request):
    """Test list view returns a dict when called."""
    assert type(list_view(dummy_request)) == dict


def test_detail_view_with_id_raises_except(dummy_request):
    """Test proper error raising with non matching id on detail view."""
    dummy_request.matchdict['id'] = '9000'
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_view_returns_dict(dummy_request):
    """Test create view returns a dict when called."""
    assert type(create_view(dummy_request)) == dict


def test_edit_view_with_id_raises_except(dummy_request):
    """Test proper error raising with non matching id on edit view."""
    dummy_request.matchdict['id'] = '9000'
    with pytest.raises(HTTPNotFound):
        edit_view(dummy_request)


def test_create_view_returns_200(testapp, db_session):
    """Look for a 200 in create view."""
    response = testapp.get('/journal/new-entry')
    assert response.status_code == 200


def test_home_view_returns_200(testapp, db_session):
    """Look for a 200 in home view."""
    response = testapp.get('/')
    assert response.status_code == 200


def test_edit_view_returns_200(testapp, db_session):
    """Look for a 200 in edit view."""
    response = testapp.get('/journal/0/edit-entry')
    assert response.status_code == 200


def test_detail_view_returns_200(testapp, db_session):
    """Look for a 200 in detail view."""
    response = testapp.get('/journal/0')
    assert response.status_code == 200
