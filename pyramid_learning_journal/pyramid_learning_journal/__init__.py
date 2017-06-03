"""Instantiate the inclusion."""
from pyramid.config import Configurator
import os
import psycopg2


def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
    settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL')
    conn_string = "host='localhost' dbname='learning_journal' user='erik' password='1234'"
    conn = psycopg2.connect(conn_string)
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.routes')
    config.include('.models')
    # config.include('.views')
    config.add_static_view(name='static', path='pyramid_learning_journal:static')
    config.scan()
    return config.make_wsgi_app()


