import os
import sys
# import transaction

from sqlalchemy import create_engine

from .models import Idea, Author, Base
from .session import DBSession


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <database_uri>\n'
          '(example: "%s sqlite:///agora.sqlite")\n'
          'to seed the database: "%s <database_uri> seed\n'
          '(example: "%s sqlite:///agora.sqlite seed")\n'
          % (cmd, cmd, cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if not 2 <= len(argv) <= 3:
        usage(argv)
    database_uri = argv[1]
    seed = argv[2] if len(argv) > 2 else False

    engine = create_engine(database_uri)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    if seed == 'seed':
        author = Author(username='misinformation',
                        fullname='Miss Information',
                        email='misinformation@example.com')
        DBSession.add(author)

        author = DBSession.query(Author).filter_by(
            username='misinformation').one()
        idea = Idea(title='First Idea!',
                    idea='This is my idea.',
                    author=author)
        DBSession.add(idea)
        idea = Idea(title='Another Idea!',
                    idea='This is another idea.',
                    author=author)
        DBSession.add(idea)
