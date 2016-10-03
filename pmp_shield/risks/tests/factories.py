from factory import LazyAttribute, SubFactory, Sequence
from factory.django import DjangoModelFactory

from ...projects.tests.factories import ProjectFactory, BasicProjectFactory
from ...projects.models import Project
from ..models import Risk

from faker import Factory as FakeFactory

faker = FakeFactory.create()

class RiskFactory(DjangoModelFactory):

    class Meta:
        model = Risk

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    description = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    display_order = Sequence((lambda n: n))
    project = SubFactory(BasicProjectFactory)
