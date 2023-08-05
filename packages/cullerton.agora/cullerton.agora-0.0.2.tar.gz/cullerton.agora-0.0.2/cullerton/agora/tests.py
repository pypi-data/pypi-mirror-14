import unittest

from logging import getLogger
logger = getLogger(__name__)


def _populate_test_db(session):
    from cullerton.agora.models import Author, Idea

    # add 2 authors
    [session.add(Author(
        'user_%s' % author,
        'User %s' % author,
        'user_%s@example.com' % author))
        for author in range(1, 3)]

    # add 3 ideas for each of the authors
    [[session.add(Idea(
        'Idea %s' % idea,
        'This is idea number %s' % idea,
        session.query(Author).filter_by(id=author_id).one()))
        for idea in range(1, 4)]
        for author_id in range(1, session.query(Author).count() + 1)]


def _initialize_test_db():

    from cullerton.agora.models import Base

    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    DBSession = scoped_session(sessionmaker())
    DBSession.configure(bind=engine)

    _populate_test_db(DBSession)

    return DBSession


class AgoraBase(unittest.TestCase):

    def setUp(self):
        self.session = _initialize_test_db()

    def tearDown(self):
        self.session.remove()

    def _Forum(self):
        from cullerton.agora import Forum
        return Forum(self.session)


class AgoraAuthorTests(AgoraBase):

    def test_get_author_count(self):
        """should return a scalar
           equal to the number of records added in _initialize_test_db"""
        forum = self._Forum()
        self.assertEqual(forum.get_author_count(), 2)

    def test_get_authors(self):
        """should return a list of length author_count"""
        forum = self._Forum()
        author_count = forum.get_author_count()
        authors = forum.get_authors()

        self.assertIsInstance(authors, list)
        self.assertEqual(len(authors), author_count)

    def test_get_authors_with_limit(self):
        """should return a list of length limit"""
        forum = self._Forum()
        author_count = forum.get_author_count()

        for limit in (0, 1, author_count):

            authors = forum.get_authors(limit=limit)
            self.assertIsInstance(authors, list)
            self.assertEqual(len(authors), limit)

    def test_get_authors_bad_limit(self):
        """should return a list of length author_count"""
        forum = self._Forum()
        author_count = forum.get_author_count()

        for limit in (-1, author_count + 1):
            authors = forum.get_authors(limit=limit)
            self.assertIsInstance(authors, list)
            self.assertEqual(len(authors), author_count)

    def test_get_author(self):
        """should return an author"""
        forum = self._Forum()
        from cullerton.agora.models import Author
        for id in range(1, forum.get_author_count()):
            self.assertIsInstance(forum.get_author(id), Author)

    def test_get_bad_author(self):
        """should return None"""
        forum = self._Forum()
        author_count = forum.get_author_count()
        for i in (-1, 0, author_count + 1):
            self.assertIsNone(forum.get_author(i))

    def test_get_author_repr(self):
        forum = self._Forum()
        for id in range(1, forum.get_author_count()):
            self.assertIn("User %s" % id, forum.get_author(id).__repr__())

    def test_add_author(self):
        forum = self._Forum()

        username = 'test_user'
        fullname = 'Test User'
        email = 'test_user@company.com'
        new_author_id = forum.add_author(username=username,
                                         fullname=fullname,
                                         email=email)

        test_author = forum.get_author(new_author_id)
        self.assertEqual(username, test_author.username)

    def test_edit_author(self):
        forum = self._Forum()
        author_count = forum.get_author_count()

        for id in range(1, author_count):

            username = "edited_user_%s" % id
            fullname = "Edited User %s" % id
            email = "edited_user%s@example.com" % id
            forum.edit_author(id, username=username, fullname=fullname,
                              email=email)
            test_author = forum.get_author(id)
            self.assertEqual(username, test_author.username)
            self.assertEqual(fullname, test_author.fullname)
            self.assertEqual(email, test_author.email)

    def test_edit_bad_author(self):
        forum = self._Forum()
        author_count = forum.get_author_count()
        from sqlalchemy.orm.exc import NoResultFound

        for id in (-1, 0, author_count + 1):
            username = 'bad_user'
            fullname = "Bad User"
            email = 'bad_user@example.com'
            with self.assertRaises(NoResultFound):
                forum.edit_author(
                    id,
                    username=username,
                    fullname=fullname,
                    email=email)

    def test_delete_author(self):
        forum = self._Forum()
        author_count = forum.get_author_count()

        for id in range(1, author_count):
            self.assertEqual(forum.delete_author(id), id)

    def test_delete_bad_author(self):
        forum = self._Forum()
        author_count = forum.get_author_count()
        from cullerton.agora.exceptions import InvalidAuthor

        for id in (-1, 0, author_count + 1):
            with self.assertRaises(InvalidAuthor):
                forum.delete_author(id)


class AgoraIdeaTests(AgoraBase):

    def test_get_idea_count(self):
        """should return a scalar
           equal to the number of records added in _initialize_test_db"""
        forum = self._Forum()
        # we should know how the idea count
        self.assertEqual(forum.get_idea_count(), 6)

    def test_get_ideas(self):
        """should return a list of length idea_count"""
        forum = self._Forum()
        idea_count = forum.get_idea_count()
        ideas = forum.get_ideas()

        # we should get a list and know its length
        self.assertIsInstance(ideas, list)
        self.assertEqual(len(ideas), idea_count)

    def test_get_ideas_with_limit(self):
        """should return a list of length limit"""
        forum = self._Forum()
        idea_count = forum.get_idea_count()

        for limit in (0, 1, idea_count):

            ideas = forum.get_ideas(limit=limit)
            self.assertIsInstance(ideas, list)
            self.assertEqual(len(ideas), limit)

    def test_get_ideas_bad_limit(self):
        """should return a list of length idea_count"""
        forum = self._Forum()
        idea_count = forum.get_idea_count()

        for limit in (-1, idea_count + 1):
            ideas = forum.get_ideas(limit=limit)
            self.assertIsInstance(ideas, list)
            self.assertEqual(len(ideas), idea_count)

    def test_get_idea(self):
        """should return an idea"""
        forum = self._Forum()
        from cullerton.agora.models import Idea
        for id in range(1, forum.get_idea_count()):
            self.assertIsInstance(forum.get_idea(id), Idea)

    def test_get_bad_idea(self):
        """should return None"""
        forum = self._Forum()
        idea_count = forum.get_idea_count()
        for i in (-1, 0, idea_count + 1):
            self.assertIsNone(forum.get_idea(i))

    def test_get_idea_repr(self):
        forum = self._Forum()
        for id in range(1, forum.get_idea_count()):
            self.assertRegexpMatches(
                forum.get_idea(id).__repr__(), 'Idea \d+, User \d+')

    def test_add_idea(self):
        forum = self._Forum()

        title = 'My Test Title'
        idea = 'My test idea'
        author_id = 1
        new_idea_id = forum.add_idea(title=title,
                                     idea=idea,
                                     author_id=author_id)

        test_idea = forum.get_idea(new_idea_id)
        self.assertEqual(title, test_idea.title)
        self.assertEqual(idea, test_idea.idea)

    def test_edit_idea(self):
        forum = self._Forum()
        idea_count = forum.get_idea_count()

        for id in range(1, idea_count):

            forum.edit_idea(id, title='Edited Title',
                            idea='This is the edited idea.')
            test_idea = forum.get_idea(id)
            self.assertEqual('Edited Title', test_idea.title)
            self.assertEqual('This is the edited idea.', test_idea.idea)

    def test_edit_bad_idea(self):
        forum = self._Forum()
        idea_count = forum.get_idea_count()
        from sqlalchemy.orm.exc import NoResultFound

        for id in (-1, 0, idea_count + 1):
            with self.assertRaises(NoResultFound):
                forum.edit_idea(id, title='Bad Edited Title',
                                idea='This is the edited bad idea.')

    def test_delete_idea(self):
        forum = self._Forum()
        idea_count = forum.get_idea_count()

        for id in range(1, idea_count):
            self.assertEqual(forum.delete_idea(id), id)

    def test_delete_bad_idea(self):
        forum = self._Forum()
        idea_count = forum.get_idea_count()
        from cullerton.agora.exceptions import InvalidIdea

        for id in (-1, 0, idea_count + 1):
            with self.assertRaises(InvalidIdea):
                forum.delete_idea(id)
