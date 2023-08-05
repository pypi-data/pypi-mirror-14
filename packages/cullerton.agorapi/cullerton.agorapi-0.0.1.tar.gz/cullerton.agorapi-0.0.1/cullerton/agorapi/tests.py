import unittest


class AgoraAPIWebTests(unittest.TestCase):

    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('agorapi.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        from agora import DBSession
        DBSession.remove()

    def test_get_ideas(self):

        resp = self.testapp.get('/ideas')
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')
        self.assertIn(b'Idea', resp.body)

        resp = self.testapp.get('/ideas?limit=1')
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')
        self.assertIn(b'Idea', resp.body)

    # def test_add_idea(self):
    #     request = testing.DummyRequest(post={'title': 'My test title',
    #                                          'idea': 'My test idea'})
    #     api = self._callAgoraAPI(request)
    #     response = api.add_idea()

    #     self.assertEqual('201 Created', response.status)


# class AgoraAPITests(unittest.TestCase):
#     def setUp(self):
#         self.session = _initTestingDB()
#         self.config = testing.setUp()

#     def tearDown(self):
#         testing.tearDown()
#         # from .models import DBSession
#         # DBSession.remove()
#         self.session.remove()

#     def _callAgoraAPI(self, request):
#         from agora.api import AgoraAPI
#         return AgoraAPI(request)

#     def test_get_ideas(self):

#         request = testing.DummyRequest()
#         api = self._callAgoraAPI(request)
#         # idea_count = api.get_idea_count()

#         response = api.get_ideas()

#         self.assertIsInstance(response, list)
#         self.assertEqual(len(response), 5)
#         self.assertIn('First Idea', response[0]['title'])
#         self.assertIn('YA Idea', response[1]['title'])

#     def test_get_idea(self):
#         from pyramid.response import Response

#         request = testing.DummyRequest()
#         request.matchdict['idea'] = 1
#         api = self._callAgoraAPI(request)
#         idea = api.get_idea()

#         self.assertIsInstance(idea, Response)
#         self.assertIn(b'First Idea', idea.body)

#     def test_add_idea(self):
#         request = testing.DummyRequest(post={'title': 'My test title',
#                                              'idea': 'My test idea'})
#         api = self._callAgoraAPI(request)
#         response = api.add_idea()

#         self.assertEqual('201 Created', response.status)

#     # def test_edit_idea(self):
#     #     request = testing.DummyRequest(put={'title': 'My edited title',
#     #                                         'idea': 'My edited idea'})
#     #     api = self._callAgoraAPI(request)
#     #     response = api.edit_idea()

#     #     self.assertEqual('201 Created', response.status)

#     def test_delete_idea(self):
#         pass

# #     def test_view_idea_no_idea(self):
# #         request = testing.DummyRequest()
# #         api = self._callAgoraAPI(request)
# #         response = api.view_idea()

# #         self.assertEqual('400 Bad Request', response.status)
