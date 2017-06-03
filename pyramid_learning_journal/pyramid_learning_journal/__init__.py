"""Instantiate the inclusion."""
from pyramid.config import Configurator
import os
import psycopg2
import urlparse


def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )
    settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL')
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.routes')
    config.include('.models')
    # config.include('.views')
    config.add_static_view(name='static', path='pyramid_learning_journal:static')
    config.scan()
    return config.make_wsgi_app()


