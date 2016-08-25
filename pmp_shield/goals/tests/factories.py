
from factory import DjangoModelFactory, SubFactory, Sequence, post_generation, LazyAttribute, Iterator
from faker import Factory as FakeFactory

from ...employees.tests.factories import EmployeeFactory
from ...projects.tests.factories import BasicProjectFactory
from ..models import Goal, EmployeeGoal, ExpectationsList

faker = FakeFactory.create()


class GoalFactory(DjangoModelFactory):

    class Meta:
        model = Goal

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    description = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    project = SubFactory(BasicProjectFactory)
    expected_advancement = 0.9


class ExpectationsListFactory(DjangoModelFactory):
    class Meta:
        model = ExpectationsList

    version = 1


class EmployeeGoalFactory(DjangoModelFactory):

    class Meta:
        model = EmployeeGoal

    employee = SubFactory(EmployeeFactory)
    goal = SubFactory(GoalFactory)
    expectations = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    weight = 0.1
    fiscal_year = 'AF16'
    expectations_list = SubFactory(ExpectationsListFactory)



