from factory import DjangoModelFactory, SubFactory, Sequence, post_generation
from faker import Factory as FakeFactory

from ..models import Project, Assumption
from ...employees.tests.factories import EmployeeFactory

faker = FakeFactory.create()

class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project
    name = faker.text(max_nb_chars=120)
    sponsor = SubFactory(EmployeeFactory)
    project_manager = SubFactory(EmployeeFactory)
    justification = faker.paragraph(nb_sentences=3, variable_nb_sentences=True)
    scope = faker.paragraph(nb_sentences=5, variable_nb_sentences=True)

    

class AssumptionFactory(DjangoModelFactory):
    class Meta:
        model = Assumption

    name = faker.text(max_nb_chars=120)
    description = faker.paragraph(nb_sentences=3, variable_nb_sentences=True)
    display_order = Sequence((lambda n: n))
    project = SubFactory(Project)
