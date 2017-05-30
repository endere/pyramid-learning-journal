"""."""
from .default import list_view, detail_view, create_view, edit_view


def includeme(config):
    """."""
    config.add_view(list_view, route_name='home')
    config.add_view(detail_view, route_name='detail')
    config.add_view(create_view, route_name='create')
    config.add_view(edit_view, route_name='update')
