from random import randint

from factory.django import DjangoModelFactory
from faker import Factory as FakeFactory
from factory import DjangoModelFactory, SubFactory, Sequence, post_generation, LazyAttribute, Iterator
from ..models import GradeLevel

faker = FakeFactory.create()


class GradeLevelFactory(DjangoModelFactory):

    class Meta:
        model = GradeLevel

    grade_type = Iterator(['NM', 'GE'])
    level = LazyAttribute(lambda x: randint(7, 13))


