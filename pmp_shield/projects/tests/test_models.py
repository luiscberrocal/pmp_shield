from datetime import date

from auditlog.models import LogEntry
from django.test import TestCase

from ...risks.models import Risk
from ..models import Project, Assumption, Restriction, Milestone
from .factories import ProjectFactory, RestrictionFactory


class TestProject(TestCase):

    def test_create(self):
        project = ProjectFactory.create()
        self.assertEqual(1, Project.objects.count())
        self.assertEqual(4, project.assumptions.count())
        self.assertEqual(4, project.risks.count())
        self.assertEqual(4, project.restrictions.count())
        self.assertEqual(4, project.milestones.count())

        self.assertTrue(project.history.count() == 1, msg="There is one log entry")

        history = project.history.get()

        self.assertEqual(history.action, LogEntry.Action.CREATE, msg="Action is 'CREATE'")

    def test_update_name(self):
        project = ProjectFactory.create(name='Original name')
        project.name = 'New name'
        project.save()
        self.assertTrue(project.history.count() == 2, msg="There are two log entry")
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
        RestrictionFactory.create()
        self.assertEqual(1, Restriction.objects.count())

