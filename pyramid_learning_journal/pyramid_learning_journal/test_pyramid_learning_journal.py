"""Test for views creation and link to html pages."""
from pyramid import testing
from pyramid.response import Response
import pytest


@pytest.fixture
def home_response():
    """Set fixture for home page."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    return response


@pytest.fixture
def entry_response():
    """Set fixture for individual entry page."""
    from pyramid_learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    response = detail_view(request)
    return response


@pytest.fixture
def edit_entry_response():
    """Set fixture for edit entry page."""
    from pyramid_learning_journal.views.default import edit_view
    request = testing.DummyRequest()
    response = edit_view(request)
    return response


@pytest.fixture
def new_entry_response():
    """Set fixture for new entry page."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    return response


def test_home_view_returns_response_given_request(home_response):
    """Home view returns a Response object when given a request."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    assert isinstance(response, Response)


def test_home_view_is_good(home_response):
    """Home view hass a 200 ok."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    assert response.status_code == 200


def test_home_view_returns_proper_content(home_response):
    """Home view returns the actual content from the html."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    expected_text = '<h1 class="blog-title">The pyramid Blog</h1>'
    assert expected_text in response.text


def test_new_entry_view_returns_response_given_request(new_entry_response):
    """New entry view returns a Response object when given a request."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    assert isinstance(response, Response)


def test_new_entry_view_is_good(new_entry_response):
    """New entry view hass a 200 ok."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    assert response.status_code == 200


def test_new_entry_view_returns_proper_content(new_entry_response):
    """New entry view returns the actual content from the html."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    expected_text = '<h1>New Journal entry</h1>'
    assert expected_text in response.text


def test_edit_entry_view_returns_response_given_request(edit_entry_response):
    """Edit entry view returns a Response object when given a request."""
    from pyramid_learning_journal.views.default import edit_view
    request = testing.DummyRequest()
    response = edit_view(request)
    assert isinstance(response, Response)


def test_edit_entry_view_is_good(edit_entry_response):
    """Edit entry view hass a 200 ok."""
    from pyramid_learning_journal.views.default import edit_view
    request = testing.DummyRequest()
    response = edit_view(request)
    assert response.status_code == 200


def test_edit_entry_view_returns_proper_content(edit_entry_response):
    """Edit entry view returns the actual content from the html."""
    from pyramid_learning_journal.views.default import edit_view
    request = testing.DummyRequest()
    response = edit_view(request)
    expected_text = '<h1>Edit Journal entry</h1>'
    assert expected_text in response.text


def test_entry_view_returns_response_given_request(entry_response):
    """Entry view returns a Response object when given a request."""
    from pyramid_learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    response = detail_view(request)
    assert isinstance(response, Response)


def test_entry_view_is_good(entry_response):
    """Entry view hass a 200 ok."""
    from pyramid_learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    response = detail_view(request)
    assert response.status_code == 200


def test_entry_view_returns_proper_content(entry_response):
    """Entry view returns the actual content from the html."""
    from pyramid_learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    response = detail_view(request)
    expected_text = '<h2 class="blog-post-title">Sample journal post</h2>'
    assert expected_text in response.text



#_____-----------------------------___________________________
@pytest.fixture
def testapp():
    from python_learning_journal import main
    from webtest import TestApp
    app = main({})
    return TestApp(app)


def test_list_route_has_list_of_entries(testapp):
    response = testapp.get('/')
    html = response.html
    assert html.find()
    num_list_items = (len(html.find_all('li')))
    assert num_list_items == len(Posts)