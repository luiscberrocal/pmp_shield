from datetime import date, timedelta, datetime

from auditlog.models import LogEntry
from django.test import TestCase

from ....risks.models import Risk
from ....projects.models import Project, Assumption, Restriction, Milestone, ProjectMembership
from ....projects.tests.factories import ProjectFactory, RestrictionFactory, MilestoneFactory


class TestProject(TestCase):

    def test_create(self):
        project = ProjectFactory.create()
        self.assertEqual(1, Project.objects.count())
        self.assertEqual(4, project.assumptions.count())
        self.assertEqual(4, project.risks.count())
        self.assertEqual(4, project.restrictions.count())
        self.assertEqual(4, project.milestones.count())
        self.assertEqual(4, project.members.count())
        self.assertEqual(1, project.members.filter(role=ProjectMembership.LEADER_ROLE).count())

        self.assertEqual(2, project.history.count(), msg="There is one log entry")

        history = project.history.last()
        self.assertEqual(history.action, LogEntry.Action.CREATE, msg="Action is 'CREATE'")

    def test_create_with_start_date(self):
        project = ProjectFactory.create(milestones={'start_date': date(2016,10,1)})
        start, _ =  project.start_end_dates()
        self.assertEqual(start, date(2016,10,1))
        self.assertEqual('AF17', project.fiscal_year)
        self.assertEqual(4, project.milestones.count())

    def test_update_name(self):
        project = ProjectFactory.create(name='Original name')
        project.name = 'New name'
        project.save()
        self.assertEqual(3, project.history.count())
        self.assertEqual('New name', project.history.first().changes_dict['name'][1])
        self.assertJSONEqual('{"name": ["Original name", "New name"]}', project.history.first().changes)

    def test_update_delete_assumption(self):
        project = ProjectFactory.create()
        first_assumption = project.assumptions.first()
        history = first_assumption.history.latest()
        first_assumption.delete()
        self.assertEqual(3, project.assumptions.count())
        self.assertEqual(1, LogEntry.objects.filter(content_type=history.content_type,
                                                    object_pk=history.object_pk,
                                                    action=LogEntry.Action.DELETE).count())


    def test_start_end_dates(self):
        project = ProjectFactory.create()
        start, end = project.start_end_dates()
        self.assertTrue(end > start)

    def test_start_end_dates_no_end_milestone(self):
        project = ProjectFactory.create(milestones=1)
        start, end = project.start_end_dates()
        self.assertIsNone(end)
        self.assertIsInstance(start, date)

    def test_create_batch(self):
        ProjectFactory.create_batch(5)
        self.assertEqual(5, Project.objects.count())
        self.assertEqual(20, Assumption.objects.count())
        self.assertEqual(20, Risk.objects.count())
        self.assertEqual(20, Restriction.objects.count())
        self.assertEqual(20, Milestone.objects.count())


class TestRestriction(TestCase):

    def test_create_with_project_factory(self):
        ProjectFactory.create(restrictions=1)
        self.assertEqual(1, Restriction.objects.count())

    def test_create(self):
        restriction = RestrictionFactory.create()
        self.assertEqual(1, Restriction.objects.count())
        self.assertTrue(restriction.history.count() == 1, msg="There is one log entry")

        history = restriction.history.get()
        self.assertEqual(history.action, LogEntry.Action.CREATE, msg="Action is 'CREATE'")

    def test_update_name(self):
        restriction = RestrictionFactory.create(name='Restriction 1')
        restriction.name = 'Important restriction'
        restriction.save()
        self.assertEqual(2, restriction.history.count())

    def test_update_display_order(self):
        """
        Display order is no included in history
        """
        restriction = RestrictionFactory.create(display_order=1)
        restriction.display_order = 2
        restriction.save()
        self.assertEqual(1, restriction.history.count())


class TestMilestone(TestCase):

    def test_create_with_project_factory(self):
        ProjectFactory.create(milestones=1)
        self.assertEqual(1, Milestone.objects.count())

    def test_create(self):
        milestone = MilestoneFactory.create()
        self.assertEqual(1, Milestone.objects.count())
        self.assertTrue(milestone.history.count() == 1, msg="There is one log entry")

    def test_update_expected_date(self):
        start_date = date(2016, 1, 2)
        start_ms, end_ms = MilestoneFactory.create_start_end_milestones(start_date)
        self.assertTrue(start_ms.date < end_ms.date)
        self.assertEqual(start_ms.project.pk, end_ms.project.pk)
        end_ms.date = end_ms.date + timedelta(weeks=2)
        end_ms.save()
        self.assertEqual(2, end_ms.history.count())
        self.assertEqual(1, start_ms.history.count())



