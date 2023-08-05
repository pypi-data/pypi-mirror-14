=====
Agora
=====

Agora is a forum for ideas. It is a simple, blog-like application, with support for multiple authors.

It is developed for a class curriculum, and is not intended for real deployment, although it could serve some purpose.

There are two classes--Author and Idea. A forum can have zero or more authors. Each author can have zero or more ideas.

Agora uses SQLAlchemy for a persistence layer. You need a valid SQLAlchemy session to initialize agora.

-----
Usage
-----

Set up SQLAlchemy session
-------------------------

::

    >>> from agora.models import Base

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.orm import scoped_session, sessionmaker

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)

    >>> DBSession = scoped_session(sessionmaker())
    >>> DBSession.configure(bind=engine)

Forum Basics
------------

::

    >>> from agora import Forum
    >>> forum = Forum(DBSession)

A new forum has no authors or ideas.

::

    >>> forum.get_authors()
    []
    >>> forum.get_ideas()
    []

To add an idea, you first need an author.

To add a new author, pass a username, fullname, and email to the `add_author` method.

::

    >>> forum.add_author(username='schmoe', fullname='Joe Schmoe', email='schmoe@example.com')
    1
    >>> forum.add_author(username='misinformation', fullname='Miss Information', email='misinformation@example.com')
    2

Notice that the method returns the author's id.


We now have authors.

::

    >>> forum.get_authors()
    [Joe Schmoe, March 02, 2016, Miss Information, March 02, 2016]

You can access authors by id.

::

    >>> forum.get_author(1)
    Joe Schmoe, March 02, 2016

To add a new idea, pass a title, idea, and author_id to the `add_idea` method.

::

    >>> forum.add_idea(title='First Idea!', idea='This is my idea.', author_id=1)
    1

    >>> forum.add_idea(title='My First Idea!', idea='This is my idea.', author_id=2)
    2

    >>> forum.add_idea(title='Another Idea!', idea='This is my idea.', author_id=1)
    3

    >>> forum.add_idea(title='Another Idea!', idea='This is my idea.', author_id=2)
    4

We now have ideas.

::

    >>> forum.get_ideas()
    [First Idea!, Joe Schmoe, March 02, 2016, My First Idea!, Miss Information, March 02, 2016, Another Idea!, Joe Schmoe, March 02, 2016, Another Idea!, Miss Information, March 02, 2016]

You can access ideas by id.

::

    >>> forum.get_idea(1)
    First Idea!, Joe Schmoe, March 02, 2016

You can also access ideas with filters.

::

    >>> forum.get_ideas(filters={'author': forum.get_author(1)})
    [First Idea!, Joe Schmoe, March 02, 2016, Another Idea!, Joe Schmoe, March 02, 2016]

    >>> forum.get_ideas(filters={'title': 'First Idea!'})
    [First Idea!, Joe Schmoe, March 02, 2016]

    >>> forum.get_ideas(filters={'title': 'Another Idea!'})
    [Another Idea!, Joe Schmoe, March 02, 2016, Another Idea!, Miss Information, March 02, 2016]

    >>> forum.get_ideas(filters={'author': forum.get_author(2), 'title': 'Another Idea!'})
    [Another Idea!, Miss Information, March 02, 2016]

You can delete ideas by id.

::

    >>> forum.delete_idea(1)
    1

    >>> forum.get_ideas()
    [My First Idea!, Miss Information, March 02, 2016, Another Idea!, Joe Schmoe, March 02, 2016, Another Idea!, Miss Information, March 02, 2016]

-------------------
Initialize Database
-------------------

There is a script provided to initialize the database. It is installed into the bin directory of your virtualenv. You must pass it a valid SQLAlchemy database URI.

::

    $ initialize_agora_db <database_uri>

    $ initialize_agora_db sqlite:///agora.sqlite


You can also use the script to seed the database with a sample author and two ideas, if you append the word `seed` to the command.

::

    $ initialize_agora_db sqlite:///agora.sqlite seed
