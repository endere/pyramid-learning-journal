# """Test for views creation and link to html pages."""
# from pyramid import testing
# from pyramid_learning_journal.models import (
#     Entry,
#     get_tm_session,
# )
# from pyramid_learning_journal.models.meta import Base
# from pyramid_learning_journal.views.notfound import notfound_view
# from pyramid_learning_journal.views.default import (
#     list_view,
#     create_view,
#     detail_view,
#     edit_view
# )
# from pyramid.config import Configurator
# from pyramid.httpexceptions import HTTPNotFound, HTTPFound
# from faker import Faker
# import pytest
# import datetime
# import transaction
# import os


# FAKE_STUFF = Faker()
# FAKE_ENTRIES = [Entry(
#     title=FAKE_STUFF.text(20),
#     body=FAKE_STUFF.text(250),
#     creation_date=datetime.datetime.now(),
# ) for x in range(25)]


# @pytest.fixture
# def dummy_request(db_session):
#     """Make a fake HTTP request."""
#     return testing.DummyRequest(dbsession=db_session)


# @pytest.fixture
# def add_models(dummy_request):
#     """Add entries to a dummy request."""
#     dummy_request.dbsession.add_all(FAKE_ENTRIES)


# @pytest.fixture(scope="session")
# def configuration(request):
#     """Set up a Configurator instance."""
#     config = testing.setUp(settings={
#         'sqlalchemy.url': os.environ.get('TEST_DATABASE')
#     })
#     config.include('pyramid_learning_journal.models')
#     config.include('pyramid_learning_journal.routes')

#     def teardown():
#         testing.tearDown()

#     request.addfinalizer(teardown)
#     return config


# @pytest.fixture
# def db_session(configuration, request):
#     """Create a session for interacting with the test database."""
#     SessionFactory = configuration.registry['dbsession_factory']
#     session = SessionFactory()
#     engine = session.bind
#     Base.metadata.create_all(engine)

#     def teardown():
#         session.transaction.rollback()
#         Base.metadata.drop_all(engine)

#     request.addfinalizer(teardown)
#     return session


# @pytest.fixture(scope="session")
# def testapp(request):
#     """Create a test application to use for functional tests."""
#     from webtest import TestApp

#     def main(global_config, **settings):
#         """Function returns a fake Pyramid WSGI application."""
#         settings['sqlalchemy.url'] = os.environ.get('TEST_DATABASE')
#         config = Configurator(settings=settings)
#         config.include('pyramid_jinja2')
#         config.include('pyramid_learning_journal.models')
#         config.include('pyramid_learning_journal.routes')
#         config.add_static_view(name='static',
#                                path='pyramid_learning_journal:static')
#         config.scan()
#         return config.make_wsgi_app()

#     app = main({})
#     testapp = TestApp(app)

#     SessionFactory = app.registry['dbsession_factory']
#     engine = SessionFactory().bind
#     Base.metadata.create_all(bind=engine)

#     def teardown():
#         Base.metadata.drop_all(bind=engine)

#     request.addfinalizer(teardown)
#     return testapp


# @pytest.fixture
# def fill_test_db(testapp):
#     """Set fake entries to the db for a session."""
#     SessionFactory = testapp.app.registry['dbsession_factory']
#     with transaction.manager:
#         dbsession = get_tm_session(SessionFactory, transaction.manager)
#         dbsession.add_all(FAKE_ENTRIES)
#     # import pdb; pdb.set_trace()
#     return dbsession


# @pytest.fixture
# def reset_db(testapp):
#     """Clear and start a new DB."""
#     SessionFactory = testapp.app.registry['dbsession_factory']
#     engine = SessionFactory().bind
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)


# @pytest.fixture
# def post_request(dummy_request):
#     """Make a fake HTTP POST request."""
#     dummy_request.method = "POST"
#     return dummy_request


# # # ----- Unit Tests ----- #

# def test_filling_fake_db(fill_test_db, db_session):
#     """Check for entries added to db."""
#     assert len(db_session.query(Entry).all()) == 25


# # def test_list_view_returns_dict(dummy_request):
# #     """Test list view returns a dict when called."""
# #     assert type(list_view(dummy_request)) == dict

# # def test_detail_view_with_id_raises_except(dummy_request):
# #     """Test proper error raising with non matching id on detail view."""
# #     dummy_request.matchdict['id'] = '9000'
# #     with pytest.raises(HTTPNotFound):
# #         detail_view(dummy_request)


# # def test_detail_view_returns_dict_with_db(db_session, dummy_request):
# #     """Test detail view returns a dict when called."""
# #     fake = Entry(
# #         title=u'Stuff',
# #         body=u'Some thing goes here.',
# #         creation_date=datetime.datetime.now(),
# #     )
# #     db_session.add(fake)
# #     fakeid = str(db_session.query(Entry)[0].id)
# #     dummy_request.matchdict['id'] = fakeid
# #     response = detail_view(dummy_request)
# #     assert type(response) == dict


# # def test_create_view_returns_dict(dummy_request):
# #     """Test create view returns a dict when called."""
# #     assert type(create_view(dummy_request)) == dict


# # def test_edit_view_returns_dict_with_db(testapp, db_session):
# #     """Test edit view returns a dict when called with a db."""
# #     fake = Entry(
# #         title=u'Stuff',
# #         body=u'Some thing goes here.',
# #         creation_date=datetime.datetime.now(),
# #     )
# #     db_session.add(fake)
# #     fakeid = str(db_session.query(Entry)[0].id)
# #     dummy_request.matchdict['id'] = fakeid
# #     response = testapp.get('/journal/1/edit-entry')
# # ---------------------------
# #     response = edit_view(dummy_request)
# #     assert type(response) == dict


# # def test_db_gets_new_entry_with_content(dummy_request, db_session):
# #     """Test db gets entry with proper content."""
# #     fake = Entry(
# #         title=u'Stuff',
# #         body=u'Some thing goes here.',
# #         creation_date=datetime.datetime.now(),
# #     )
# #     db_session.add(fake)
# #     fakeid = str(db_session.query(Entry)[0].id)
# #     dummy_request.matchdict['id'] = fakeid
# #     response = detail_view(dummy_request)
# #     assert len(db_session.query(Entry).all()) == 1
# #     assert fake.title in response['entry'].title
# #     assert fake.body in response['entry'].body


# # def test_edit_view_with_id_raises_except(dummy_request):
# #     """Test proper error raising with non matching id on edit view."""
# #     dummy_request.matchdict['id'] = '9000'
# #     with pytest.raises(HTTPNotFound):
# #         edit_view(dummy_request)


# # def test_list_view_returns_empty_without_db(dummy_request):
# #     """Test list view returns a dict when called."""
# #     response = list_view(dummy_request)
# #     assert len(response['posts']) == 0


# # #----- Functional Tests ----- #

# # def test_home_route_has_home_contents(testapp, db_session):
# #     """Test list view is routed to home page."""
# #     response = testapp.get('/')
# #     assert '<h1 class="blog-title">The Pyramid Blog</h1>' in response


# # def test_home_view_returns_200(testapp, db_session):
# #     """."""
# #     response = testapp.get('/')
# #     assert response.status_code == 200


# # # def test_home_route_has_list_of_entries(testapp, db_session):
# # #     """Test if there are the right amount of entries on the home page."""
# # #     response = testapp.get('/')
# # #     num_posts = len(response.html.find_all('h2'))
# # #     print(response)
# # #     assert num_posts == 25


# # # def test_new_entry_view_returns_proper_content(testapp, db_session):
# # #     """New entry view returns the actual content from the html."""
# # #     response = testapp.get('/journal/new-entry')
# # #     # html = response.html
# # #     # expected_text = '<h1 class="blog-title">Create New Entry!</h1>'
# # #     print(response)
# # #     # assert expected_text in str(html)
# # #     # response = testapp.get('/')
# # #     # assert '<h1 class="blog-title">The Pyramid Blog</h1>' in response

# # #<h1 class="blog-title">Entry View</h1>

# # # def test_detail_view_has_single_entry(testapp, db_session, fill_test_db):
# # #     """Test that the detail page only brings up one entry."""
# # #     response = testapp.get('/journal/1')
# # #     html = response.html
# # #     assert html.find()
# # #     num_list_items = (len(html.find_all('h3')))
# # #     assert num_list_items == 1


# # # def test_detail_view_returns_proper_content(testapp, db_session, fill_test_db):
# # #     """Entry view returns a Response object when given a request."""
# # #     # import pdb; pdb.set_trace()
# # #     response = testapp.get('/journal/1')
# # #     html = response.html
# # #     assert html.find()
# # #     expected_text = '<div class="entries">'
# # #     assert expected_text in str(html)


# # # def test_edit_view_has_single_entry(testapp, db_session, fill_test_db):
# # #     """Test that the detail page only brings up one entry."""
# # #     response = testapp.get('/journal/1/edit-entry')
# # #     html = response.html
# # #     assert html.find()
# # #     num_list_items = (len(html.find_all('h3')))
# # #     assert num_list_items == 1


# # # def test_edit_view_returns_proper_content(testapp, db_session, fill_test_db):
# # #     """Entry view returns a Response object when given a request."""
# # #     response = testapp.get('/journal/1/edit-entry')
# # #     assert '<div class="titlearea">' in response.html.text


# # # def test_detail_view_with_bad_id(testapp, db_session, fill_test_db):
# # #     """."""
# # #     response = testapp.get('/journal/9001', status=404)
# # #     assert "These are not the pages you're looking for!" in response.text


# # # def test_edit_view_with_bad_id(testapp, db_session, fill_test_db):
# # #     """."""
# # #     response = testapp.get('/journal/9001/edit-entry', status=404)
# # #     assert "These are not the pages you're looking for!" in response.text