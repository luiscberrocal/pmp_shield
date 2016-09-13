from factory import SubFactory, Iterator, LazyAttribute
from factory.django import DjangoModelFactory
from faker import Factory as FakeFactory

from ...employees.tests.factories import EmployeeFactory
from ..models import Achievement

faker = FakeFactory.create()

class AchievementFactory(DjangoModelFactory):

    class Meta:
        model = Achievement

    employee = SubFactory(EmployeeFactory)
    fiscal_year = 2016
    type = Iterator(Achievement.ACHIEVEMENT_TYPES, getter=lambda x: x[0])
    description = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
