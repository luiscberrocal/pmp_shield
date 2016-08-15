from datetime import timedelta
from random import randint

from factory import DjangoModelFactory, SubFactory, Sequence, post_generation, LazyAttribute
from faker import Factory as FakeFactory

from django.conf import settings
from pytz import timezone

from ..models import Project, Assumption, Restriction, Milestone
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


class ProjectFactory(BasicProjectFactory):

    # class Meta:
    #     model = Project
    #
    # name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    # sponsor = SubFactory(EmployeeFactory)
    # project_manager = SubFactory(EmployeeFactory)
    # justification = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    # scope = LazyAttribute(lambda x: faker.paragraph(nb_sentences=5, variable_nb_sentences=True))

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

    @post_generation
    def restrictions(self, create, count, **kwargs):
        if count is None:
            count = 4
        make_restriction = getattr(RestrictionFactory, 'create' if create else 'build')
        restrictions = [make_restriction(project=self) for i in range(count)]

        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'restrictions': restrictions}

    @post_generation
    def milestones(self, create, count, **kwargs):
        if count is None:
            count = 4
        make_milestones = getattr(MilestoneFactory, 'create' if create else 'build')
        milestones = list() #[make_milestones(project=self) for i in range(count)]
        start_date = faker.date_time_between(start_date="now", end_date="1y",
                                            tzinfo=timezone(settings.TIME_ZONE))
        for i in range(count):
            if i == 0:
                milestone = make_milestones(project=self, milestone_type=Milestone.MILESTONE_START,
                                            date=start_date)
                start_date = start_date + timedelta(weeks=randint(2, 8))
            elif i == count - 1:
                milestone = make_milestones(project=self, milestone_type=Milestone.MILESTONE_END,
                                            date=start_date)
                start_date = start_date + timedelta(weeks=randint(2, 8))
            else:
                milestone = make_milestones(project=self, date=start_date)
                start_date = start_date + timedelta(weeks=randint(2, 8))
            milestones.append(milestone)

        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'milestones': milestones}

class AssumptionFactory(DjangoModelFactory):

    class Meta:
        model = Assumption

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    description = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    display_order = Sequence((lambda n: n))
    project = SubFactory(BasicProjectFactory)


class RestrictionFactory(DjangoModelFactory):

    class Meta:
        model = Restriction

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    description = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    display_order = Sequence((lambda n: n))
    project = SubFactory(BasicProjectFactory)


class MilestoneFactory(DjangoModelFactory):

    class Meta:
        model = Milestone

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=120))
    description = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    date = LazyAttribute(lambda x: faker.date_time_between(start_date="now", end_date="1y",
                                                           tzinfo=timezone(settings.TIME_ZONE)))
    milestone_type = Milestone.MILESTONE_OTHER
    project = SubFactory(BasicProjectFactory)