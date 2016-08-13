from factory import DjangoModelFactory, SubFactory, Sequence, post_generation, LazyAttribute
from faker import Factory as FakeFactory


from ..models import Project, Assumption
from ...employees.tests.factories import EmployeeFactory

faker = FakeFactory.create()

class BasicProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    sponsor = SubFactory(EmployeeFactory)
    project_manager = SubFactory(EmployeeFactory)
    justification = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    scope = LazyAttribute(lambda x: faker.paragraph(nb_sentences=5, variable_nb_sentences=True))


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    sponsor = SubFactory(EmployeeFactory)
    project_manager = SubFactory(EmployeeFactory)
    justification = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    scope = LazyAttribute(lambda x: faker.paragraph(nb_sentences=5, variable_nb_sentences=True))

    @post_generation
    def assumptions(self, create, count, **kwargs):
        if count is None:
            count = 4
        make_assumption = getattr(AssumptionFactory, 'create' if create else 'build')
        assumptions = [make_assumption(project=self) for i in range(count)]

        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'assumptions': assumptions}

    @post_generation
    def risks(self, create, count, **kwargs):
        from ...risks.tests.factories import RiskFactory
        if count is None:
            count = 4
        make_risk = getattr(RiskFactory, 'create' if create else 'build')
        risks = [make_risk(project=self) for i in range(count)]

        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'risks': risks}

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     project = super()._create(model_class, *args, **kwargs)
    #     AssumptionFactory.create_batch(4, project=project)
    #     RiskFactory.create_batch(4, project=project)
    #     return project



class AssumptionFactory(DjangoModelFactory):

    class Meta:
        model = Assumption

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    description = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    display_order = Sequence((lambda n: n))
    project = SubFactory(BasicProjectFactory)
