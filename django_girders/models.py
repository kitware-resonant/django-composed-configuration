from typing import List

from django.db.models import Manager, QuerySet


class SelectRelatedManager(Manager):
    """
    A Manager which always follows specified foreign-key relationships.

    For Models which very frequently need to follow forign-key relationships
    (e.g. to generate their own __str__), it may be best to make this the
    "_default_manager", so many automatically generated queries are more
    efficient. To do so, define a custom "objects" as the first
    Manager in the Model:
        objects = SelectRelatedManager('foreign_thing')

    Passing no arguments makes this follow all the Model's non-null
    foreign-key relationships.
    """

    def __init__(self, *related_fields: str) -> None:
        self.related_fields: List[str] = list(related_fields)
        super().__init__()

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(*self.related_fields)
