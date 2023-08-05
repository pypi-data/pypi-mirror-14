import json

from cullerton.agora import Forum
from cullerton.agora.session import DBSession
from cullerton.agora.exceptions import *

from pyramid.view import view_config
from pyramid.response import Response

from logging import getLogger
logger = getLogger(__name__)


def process_request_items(items):
    """takes a list of 2-tuples
       returns dict of list items
           uses first value of tuple as key, and
           uses second value of tuple as value
       """
    request_dict = {}
    for item in items:
        request_dict[item[0]] = item[1]
    return request_dict


class AgoraAPI(object):

    def __init__(self, request):
        self.request = request
        self.agora = Forum(DBSession)

    @view_config(route_name='home')
    def home(self):
        author_url = "%s/authors" % self.request.application_url
        idea_url = "%s/ideas" % self.request.application_url
        home_url = "%s/" % self.request.application_url
        home = {'title': 'Agora',
                '_links': {
                    'self': {'href': home_url},
                    'authors': {'href': author_url},
                    'ideas': {'href': idea_url}}
                }
        return Response(
            body=json.dumps(home),
            status='200',
            content_type='application/json'
        )

    @view_config(route_name='list_authors', request_method='GET')
    def get_authors(self):

        """retrieve list of authors"""

        request_dict = process_request_items(self.request.GET.items())
        if 'limit' in request_dict:
            get_authors = self.agora.get_authors(limit=request_dict['limit'])
        else:
            get_authors = self.agora.get_authors()

        authors = []
        for author in get_authors:
            authors.append(author.to_dict())
        # TODO: add custom HTTP header for total count (X-Total-Count)
        return authors

    @view_config(route_name='list_ideas', request_method='GET')
    def get_ideas(self):

        """retrieve list of ideas"""

        request_dict = process_request_items(self.request.GET.items())
        if 'limit' in request_dict:
            get_ideas = self.agora.get_ideas(limit=request_dict['limit'])
        else:
            get_ideas = self.agora.get_ideas()

        ideas = []
        for idea in get_ideas:
            ideas.append(idea.to_dict())
        # TODO: add custom HTTP header for total count (X-Total-Count)
        return ideas

    @view_config(route_name='view_author', request_method='GET')
    def get_author(self):

        """retrieve an author"""

        if 'author' in self.request.matchdict:
            id = int(self.request.matchdict['author'])
            author = self.agora.get_author(id)
            if author:
                logger.info("get_author: author: %s" % str(author))
                return Response(
                    body=json.dumps({'username': author.username,
                                     'fullname': author.fullname,
                                     'email': author.email,
                                     'active': author.active,
                                     'created': str(author.created),
                                     'ideas': str(author.ideas)
                                     }),
                    status='200',
                    content_type='application/json'
                )

            else:
                return Response(
                    body=json.dumps({'message': 'Author not found'}),
                    status='404 Not Found',
                    content_type='application/json')
        else:
            return Response(
                body=json.dumps({'message': 'No author provided.'}),
                status='400 Bad Request',
                content_type='application/json')

    @view_config(route_name='view_idea', request_method='GET')
    def get_idea(self):

        """retrieve an idea"""

        if 'idea' in self.request.matchdict:
            id = int(self.request.matchdict['idea'])
            idea = self.agora.get_idea(id)
            if idea:
                return Response(
                    body=json.dumps({'title': idea.title,
                                     'idea': idea.idea,
                                     'author': idea.author}),
                    status='200',
                    content_type='application/json'
                )

            else:
                return Response(
                    body=json.dumps({'message': 'Idea not found'}),
                    status='404 Not Found',
                    content_type='application/json')
        else:
            return Response(
                body=json.dumps({'message': 'No idea provided.'}),
                status='400 Bad Request',
                content_type='application/json')

    @view_config(route_name='add_author', request_method='POST')
    def add_author(self):

        """create a new author"""

        post_items = self.request.POST.items()
        request_dict = process_request_items(post_items)
        username = request_dict['username'] if 'username' in request_dict else None
        fullname = request_dict['fullname'] if 'fullname' in request_dict else None
        email = str(request_dict['email']) if 'email' in request_dict else None

        try:
            new_author_id = self.agora.add_author(username, fullname, email)
        except DuplicateAuthor:
            return Response(
                body=json.dumps({'message':
                                 'That author already exists.'}),
                status='400 Bad Request',
                content_type='application/json')
        except AddAuthor:
            return Response(
                body=json.dumps({'message':
                                 'There was a problem adding your author.'}),
                status='400 Bad Request',
                content_type='application/json')
        else:
            logger.info("new_author_id: %s" % new_author_id)
            logger.info("new_author_id: %s" % new_author_id.__str__)
            return Response(
                body=json.dumps({'new_author_id': new_author_id}),
                status='201 Created',
                content_type='application/json')

    @view_config(route_name='add_idea', request_method='POST')
    def add_idea(self):

        """create a new idea"""

        post_items = self.request.POST.items()
        request_dict = process_request_items(post_items)
        title = request_dict['title'] if 'title' in request_dict else None
        idea = request_dict['idea'] if 'idea' in request_dict else None
        author_id = str(request_dict['author_id']) if 'author_id' in request_dict else None

        logger.info("title: %s" % title)

        try:
            new_idea_id = self.agora.add_idea(title, idea, author_id)
        except InvalidAuthor:
            return Response(
                body=json.dumps({'message':
                                 'That author does not exist.'}),
                status='400 Bad Request',
                content_type='application/json')
        except DuplicateIdea:
            return Response(
                body=json.dumps({'message':
                                 'That idea already exists.'}),
                status='400 Bad Request',
                content_type='application/json')
        except AddIdea or InvalidIdea:
            return Response(
                body=json.dumps({'message':
                                 'There was a problem adding your idea.'}),
                status='400 Bad Request',
                content_type='application/json')
        else:
            logger.info("new_idea_id: %s" % new_idea_id)
            logger.info("new_idea_id: %s" % new_idea_id.__str__)
            return Response(
                body=json.dumps({'new_idea_id': new_idea_id}),
                status='201 Created',
                content_type='application/json')

    @view_config(route_name='edit_idea', request_method='PUT')
    def edit_idea(self):

        """edit an idea"""

        if 'idea' in self.request.matchdict:
            idea = int(self.request.matchdict['idea'])
        params = self.request.params

        self.agora.edit_idea(idea, **params)

    @view_config(route_name='delete_idea', request_method='DELETE')
    def delete_idea(self):

        """delete an idea"""

        idea = self.request.matchdict['idea']
        self.agora.delete_idea(idea)

        return Response(status='202 Accepted',
                        content_type='application/json; charset=UTF-8')

    @view_config(route_name='author_ideas', request_method='GET')
    def author_ideas(self):

        """get ideas for an author"""

        author_id = self.request.matchdict['author']
        author = self.agora.get_author(author_id)
        ideas = author.ideas

        author_ideas = []
        for idea in ideas:
            author_ideas.append(idea.to_dict())
        return author_ideas
