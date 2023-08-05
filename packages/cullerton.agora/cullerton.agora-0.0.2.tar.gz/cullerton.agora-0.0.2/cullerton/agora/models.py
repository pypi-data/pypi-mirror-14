#
# sqlalchemy models for agora
#

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Text,
    Sequence,
    Boolean,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()


class Mixin(object):

    id = Column(Integer, Sequence('idea_id_seq'), primary_key=True)
    created = Column(DateTime, default=datetime.now())


class Idea(Mixin, Base):
    """"""
    __tablename__ = 'ideas'
    title = Column(Text, nullable=False)
    idea = Column(Text, nullable=False)
    visible = Column(Boolean, default=False)
    modified = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    UniqueConstraint('title', 'author_id', name='unique_title')

    author = relationship("Author", back_populates="ideas")

    def __init__(self, title, idea, author):
        self.title = title
        self.idea = idea
        self.author = author

    def __repr__(self):
        return "%s, %s" % (self.title, self.author)

    def to_dict(self):
        return {'title': self.title,
                'idea': self.idea,
                'author': str(self.author)}


class Author(Mixin, Base):
    """"""
    __tablename__ = 'authors'
    username = Column(Text, unique=True)
    fullname = Column(Text, default='Anonymous')
    email = Column(Text)
    active = Column(Boolean, default=False)

    ideas = relationship("Idea", order_by=Idea.id, back_populates="author")

    def __init__(self, username, fullname, email):
        self.username = username
        self.fullname = fullname
        self.email = email

    def __repr__(self):
        return "%s, %s" % (self.fullname, self.created.strftime("%B %d, %Y")
                           if self.created else self.created)

    def to_dict(self):
        return {'username': self.username,
                'fullname': self.fullname,
                'email': self.email,
                'active': str(self.active),
                'created': str(self.created)}

__all__ = ['Author', 'Idea', 'Base']
