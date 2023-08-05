class InvalidSession(Exception):
    pass


class DuplicateIdea(Exception):
    pass


class DuplicateAuthor(Exception):
    pass


class InvalidItem(Exception):
    pass


class InvalidIdea(Exception):
    pass


class InvalidAuthor(Exception):
    pass


class DeleteItem(Exception):
    pass


class DeleteIdea(Exception):
    pass


class DeleteAuthor(Exception):
    pass


class AddItem(Exception):
    pass


class AddIdea(Exception):
    pass


class AddAuthor(Exception):
    pass


class EditItem(Exception):
    pass


class EditIdea(Exception):
    pass


class EditAuthor(Exception):
    pass

__all__ = ['InvalidSession', 'InvalidItem', 'InvalidIdea', 'InvalidAuthor',
           'AddItem', 'EditItem', 'DeleteItem',
           'AddIdea', 'EditIdea', 'DeleteIdea', 'DuplicateIdea',
           'AddAuthor', 'EditAuthor', 'DeleteAuthor', 'DuplicateAuthor',
           ]
