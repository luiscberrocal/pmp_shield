import string
from random import randint

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakeFactory
from factory import DjangoModelFactory, SubFactory, Sequence, post_generation, LazyAttribute, Iterator

from ...employees.models import OrganizationUnit
from ...employees.tests.factories import EmployeeFactory
from ..models import GradeLevel, Position, PositionDescription

faker = FakeFactory.create()


class GradeLevelFactory(DjangoModelFactory):

    class Meta:
        model = GradeLevel

    grade_type = Iterator(['NM', 'GE'])
    level = LazyAttribute(lambda x: randint(7, 13))


class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    grade = Iterator(GradeLevel.objects.all())
    number = FuzzyText(length=6, chars=string.digits)
    tenure = Iterator(Position.TENURE_TYPES, getter= lambda c: c[0])
    position_description = Iterator(PositionDescription.objects.all())
    current_owner = SubFactory(EmployeeFactory)
    current_office = Iterator(OrganizationUnit.objects.filter(parent__isnull=True))

    @classmethod
    def create_temporary_position(cls, **kwargs):
        return PositionFactory.create(tenure=Position.TEMPORARY_TENURE, current_owner=None, **kwargs)



