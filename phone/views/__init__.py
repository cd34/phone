from pyramid.view import view_config

from phone.models import (
    DBSession,
    )


@view_config(route_name='index', renderer='index.jinja2')
def index(request):
    return {'one': 'one', 'project': 'phone'}
