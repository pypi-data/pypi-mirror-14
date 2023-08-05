from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///agora.sqlite')
DBSession = scoped_session(sessionmaker())
DBSession.configure(bind=engine)

__all__ = ['DBSession']
