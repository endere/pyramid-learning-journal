"""Function for adding the views to a route."""


def includeme(config):
    """Assign each view to a route."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('create', '/journal/new-entry')
    config.add_route('edit', '/journal/{id:\d+}/edit-entry')
