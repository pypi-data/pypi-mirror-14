from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    json_renderer = JSON()

    config = Configurator(settings=settings)
    config.add_renderer(None, json_renderer)
    config.add_route('home', '/', request_method='GET')
    config.add_route('view_idea', '/ideas/{idea}', request_method='GET')
    config.add_route('edit_idea', '/ideas/{idea}', request_method='PUT')
    config.add_route('delete_idea', '/ideas/{idea}', request_method='DELETE')
    config.add_route('list_ideas', '/ideas', request_method='GET')
    config.add_route('add_idea', '/ideas', request_method='POST')
    config.add_route('view_author', '/authors/{author}', request_method='GET')
    config.add_route('edit_author', '/authors/{author}', request_method='PUT')
    config.add_route('delete_author', '/authors/{author}', request_method='DELETE')
    config.add_route('list_authors', '/authors', request_method='GET')
    config.add_route('add_author', '/authors', request_method='POST')
    config.add_route('author_ideas', '/authors/{author}/ideas', request_method='GET')
    config.scan()
    return config.make_wsgi_app()
