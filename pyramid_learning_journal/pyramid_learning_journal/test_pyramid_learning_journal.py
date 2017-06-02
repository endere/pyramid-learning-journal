"""Test for views creation and link to html pages."""
from pyramid_learning_journal.data.data import Posts
from pyramid import testing
import pytest


@pytest.fixture
def testapp():
    """Create a test application to use for functional tests."""
    from pyramid_learning_journal import main
    from webtest import TestApp
    app = main({})
    return TestApp(app)


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
